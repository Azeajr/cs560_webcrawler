"""This module contains the spider that crawls zillow's houses for sale page."""
import hashlib

import scrapy
import structlog
from scrapy.http import Response
from scrapy.loader import ItemLoader
from sqlalchemy.orm import sessionmaker

from zillow_crawler.items import HouseItem
from zillow_crawler.models import ZillowPage, engine

log = structlog.get_logger()


class ZillowHousesSpider(scrapy.Spider):
    """Spider that crawls zillow's houses for sale page."""

    name = "zillow_houses"
    allowed_domains = ["zillow.com"]
    # According to zillow's robots.txt, this path was not disallowed
    starting_url = "https://www.zillow.com/homes/for_sale/"
    start_urls = [starting_url]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """Initialize the crawler."""
        spider = super(ZillowHousesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(
            spider.spider_closed, signal=scrapy.signals.spider_closed
        )
        return spider

    def spider_closed(self, spider):
        """Log the stats when the spider is closed."""
        log.info("Spider closed", stats=spider.crawler.stats.get_stats())

    def parse(self, response: Response, **kwargs):
        item_loader = ItemLoader(item=HouseItem(), response=response)
        item_loader.add_css("address", "article address::text")
        item_loader.add_css(
            "price", "article span[data-test='property-card-price']::text"
        )
        item_loader.add_css("sqft", "article ul li:nth-of-type(3) b::text")
        item_loader.add_css("bedrooms", "article ul li:nth-of-type(1) b::text")
        item_loader.add_css("bathrooms", "article ul li:nth-of-type(2) b::text")
        scraped_data = item_loader.load_item()
        for address, price, sqft, bedrooms, bathrooms in zip(
            scraped_data["address"],
            scraped_data["price"],
            scraped_data["sqft"],
            scraped_data["bedrooms"],
            scraped_data["bathrooms"],
        ):
            # Perhaps sha256 is faster than md5 on newer machines
            house_hash = hashlib.md5(
                f"{address}{price}{sqft}{bedrooms}{bathrooms}".encode()
            ).hexdigest()

            log.info(
                "House found",
                address=address,
                price=price,
                sqft=sqft,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                house_hash=house_hash,
            )

            yield {
                "type": "house",
                "address": address,
                "price": price,
                "sqft": sqft,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "house_hash": house_hash,
            }

        current_page = response.url
        current_page_hash = hashlib.md5(response.body).hexdigest()
        log.info(
            "Current Page",
            current_page=current_page,
            current_page_hash=current_page_hash,
        )

        yield {
            "type": "page",
            "url": current_page,
            "crawled": True,
            "page_hash": current_page_hash,
        }

        pages = response.css("div.search-pagination ul li a::attr(href)").getall()
        if pages:
            session = sessionmaker(bind=engine)()

            for page in pages:
                full_url = response.urljoin(page)
                log.info("Full URL", full_url=full_url)
                page_exists = (
                    session.query(ZillowPage)
                    .filter_by(url=response.urljoin(page))
                    .first()
                )
                if not page_exists:
                    yield response.follow(page, callback=self.parse)

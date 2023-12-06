"""This module contains the spider that crawls zillow's houses for sale page."""
import hashlib

import scrapy
import structlog
from scrapy.http import Response
from scrapy.loader import ItemLoader

from webcrawler.zillow_crawler.items import HouseItem

log = structlog.get_logger()


class ZillowHousesSpider(scrapy.Spider):
    """
    Spider that crawls Zillow's houses for sale page.

    Attributes:
        name (str): The name of the spider.
        allowed_domains (list): List of allowed domains for crawling.
        starting_url (str): The starting URL for crawling.
        start_urls (list): List of starting URLs for crawling.
        duplicate_page_count (int): Counter for duplicate pages encountered.
        duplicate_page_count_limit (int): Limit for duplicate page count.

    Methods:
        __init__: Initialize the spider.
        from_crawler: Initialize the spider from the crawler.
        spider_closed: Log the stats when the spider is closed.
        get_stats: Get the stats of the spider.
        parse: Parse the response and extract data.
    """

    name = "zillow_houses"
    allowed_domains = ["zillow.com"]
    # According to Zillow's robots.txt, this path was not disallowed
    starting_url = "https://www.zillow.com/homes/for_sale/"
    start_urls = [starting_url]

    def __init__(self, *args, **kwargs):
        """
        Initialize the spider.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        # Call the parent constructor
        super().__init__(*args, **kwargs)
        # This is a counter for duplicate pages encountered
        self.duplicate_page_count = 0
        # This is the limit for duplicate page count
        self.duplicate_page_count_limit = 10

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """
        Initialize the spider from the crawler. Override this method to
        instantiate the spider with custom arguments.  Specifically, to add a
        signal that will be used to log the stats when the spider is closed.

        Args:
            crawler (scrapy.crawler.Crawler): The crawler object.

        Returns:
            ZillowHousesSpider: The initialized spider.
        """
        spider = super(ZillowHousesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(
            spider.spider_closed, signal=scrapy.signals.spider_closed
        )
        return spider

    def spider_closed(self, spider):
        """
        Log the stats when the spider is closed.

        Args:
            spider (ZillowHousesSpider): The spider object.
        """
        log.info("Spider closed", stats=spider.crawler.stats.get_stats())

    def get_stats(self):
        """
        Get the stats of the spider.

        Returns:
            dict: The statistics of the spider.
        """
        return self.crawler.stats.get_stats()

    def parse(self, response: Response, **kwargs):
        """
        Parse the response and extract data.

        Args:
            response (scrapy.http.Response): The response object.

        Yields:
            dict: The extracted data from the response.
        """
        # Use an ItemLoader to extract data from the response
        item_loader = ItemLoader(item=HouseItem(), response=response)
        # Add CSS selectors to extract data from the response
        item_loader.add_css("address", "article address::text")
        item_loader.add_css(
            "price", "article span[data-test='property-card-price']::text"
        )
        item_loader.add_css("sqft", "article ul li:nth-of-type(3) b::text")
        item_loader.add_css("bedrooms", "article ul li:nth-of-type(1) b::text")
        item_loader.add_css("bathrooms", "article ul li:nth-of-type(2) b::text")
        # Load the item
        scraped_data = item_loader.load_item()
        for address, price, sqft, bedrooms, bathrooms in zip(
            scraped_data["address"],
            scraped_data["price"],
            scraped_data["sqft"],
            scraped_data["bedrooms"],
            scraped_data["bathrooms"],
        ):
            # Calculate a hash for the house. This will be used to determine if
            # the house has already been scraped.
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

        # Calculate a hash for the current page. This will be used to determine
        # if the page has already been scraped.
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

        # Get a list of links to other pages
        pages = response.css("div.search-pagination ul li a::attr(href)").getall()
        if pages:
            for page in pages:
                # Send the crawler to each page
                yield response.follow(page, callback=self.parse)

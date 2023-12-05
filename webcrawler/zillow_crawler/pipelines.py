# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import structlog
from scrapy import Spider
from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker

from zillow_crawler.models import ZillowListing, ZillowPage, engine
from zillow_crawler.validation import ZillowListingModel

log = structlog.get_logger()


class ZillowListingPipeline:
    def __init__(self) -> None:
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, _):
        session = self.Session()
        if item.get("type") == "house":
            validated_item = ZillowListingModel(**item)

            house = ZillowListing(
                street=validated_item.street,
                city=validated_item.city,
                state=validated_item.state,
                zipcode=validated_item.zipcode,
                address=validated_item.address,
                price=validated_item.price,
                sqft=validated_item.sqft,
                bedrooms=validated_item.bedrooms,
                bathrooms=validated_item.bathrooms,
                house_hash=validated_item.house_hash,
            )
            session.add(house)
            session.commit()
            session.close()
        return item


class ZillowPagePipeline:
    def __init__(self) -> None:
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider: Spider):
        session = self.Session()
        if item.get("type") == "page":
            if (
                session.query(ZillowPage)
                .filter(
                    or_(
                        ZillowPage.url == item["url"],
                        ZillowPage.page_hash == item["page_hash"],
                    )
                )
                .first()
            ):
                log.info("Page already exists. Skipping...")
                spider.duplicate_page_count += 1
                if spider.duplicate_page_count >= spider.duplicate_page_count_limit:
                    log.info("Duplicate page count limit reached. Stopping spider...")
                    spider.crawler.engine.close_spider(
                        spider, "Duplicate page count limit reached"
                    )
                return item

            page = ZillowPage(
                url=item["url"],
                crawled=item["crawled"],
                page_hash=item["page_hash"],
            )

            session.add(page)
            session.commit()
            session.close()
        return item

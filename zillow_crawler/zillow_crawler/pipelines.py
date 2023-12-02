# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import structlog
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

    def process_item(self, item, _):
        session = self.Session()
        if item.get("type") == "page":
            page = ZillowPage(
                url=item["url"],
                crawled=item["crawled"],
                page_hash=item["page_hash"],
            )
            session.add(page)
            session.commit()
            session.close()
        return item

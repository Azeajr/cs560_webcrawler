"""
Pipelines for the Zillow crawler.

Attributes:
    log (Logger): The logger for this module.
    structlog (Logger): The structured logger for this module.
    Spider (type): The Spider class from scrapy.
    sessionmaker (session): The SQLAlchemy session for the database.
"""

import structlog
from scrapy import Spider
from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker

from webcrawler.zillow_crawler.models import ZillowListing, ZillowPage, engine
from webcrawler.zillow_crawler.validation import ZillowListingModel

# Create the logger for this module
log = structlog.get_logger()


class ZillowListingPipeline:
    """
    Pipeline for storing house data in the database.

    Attributes:
        session (session): The SQLAlchemy session for the database.
    """

    def __init__(self) -> None:
        # Create the SQLAlchemy session
        self.session = sessionmaker(bind=engine)

    def process_item(self, item, _):
        """
        Process the item.

        Args:
            item (Item): The item to process.
            _: The spider that generated the item.

        Returns:
            Item: The item that was processed.
        """
        # Create the SQLAlchemy session
        session = self.session()
        # If the item is a house, validate it and store it in the database
        # Otherwise, return the item which will continue to be processed by
        # other pipelines
        if item.get("type") == "house":
            # Check that the item contains all of the required fields and that
            # the inputs are valid
            validated_item = ZillowListingModel(**item)

            # Check if the house already exists in the database
            if (
                session.query(ZillowListing)
                .filter(ZillowListing.house_hash == validated_item.house_hash)
                .first()
            ):
                log.info("House already exists. Skipping...")
                return item

            # Create the SQLAlchemy model and add it to the database
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
    """
    Pipeline for storing page data in the database.

    Attributes:
        session (session): The SQLAlchemy session for the database.
    """

    def __init__(self) -> None:
        # Create the SQLAlchemy session
        self.session = sessionmaker(bind=engine)

    def process_item(self, item, spider: Spider):
        session = self.session()
        if item.get("type") == "page":
            # Check if the page already exists in the database.  Either the
            # URL or the page hash can be used to check for duplicates.
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
                # If the page already exists, log it and increment the
                # duplicate page count.  If the duplicate page count limit is
                # reached, gracefully stop the spider.
                log.info("Page already exists. Skipping...")
                spider.duplicate_page_count += 1
                if spider.duplicate_page_count >= spider.duplicate_page_count_limit:
                    log.info("Duplicate page count limit reached. Stopping spider...")
                    spider.crawler.engine.close_spider(
                        spider, "Duplicate page count limit reached"
                    )
                return item

            # Create the SQLAlchemy model and add it to the database
            page = ZillowPage(
                url=item["url"],
                crawled=item["crawled"],
                page_hash=item["page_hash"],
            )

            session.add(page)
            session.commit()
            session.close()
        return item

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import structlog
from sqlalchemy.orm import sessionmaker

from zillow_crawler.models import Book, engine

log = structlog.get_logger()


class ZillowCrawlerPipeline:
    def process_item(self, item, spider):
        return item


class BooksToscrapePipeline:
    def __init__(self) -> None:
        self.Session = sessionmaker(bind=engine)

    def process_item(self, books, spider):
        session = self.Session()
        if spider.name == "books_toscrape":
            for book_name, product_price in zip(
                books["book_name"], books["product_price"]
            ):
                book = Book(book_name=book_name, product_price=product_price)
                session.add(book)
            session.commit()
            session.close()
            return books

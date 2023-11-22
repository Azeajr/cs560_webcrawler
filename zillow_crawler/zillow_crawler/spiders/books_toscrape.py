import scrapy
import structlog
from scrapy.http import TextResponse
from scrapy.loader import ItemLoader

from zillow_crawler.items import BooksToscrapeItem

log = structlog.get_logger()


class BooksToscrapeSpider(scrapy.Spider):
    name = "books_toscrape"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response: TextResponse):
        # log.info("\n".join(f"Attr {attr}: Value {value}" for attr, value in vars(response).items() if not attr.startswith("_")))
        # log.info("text", text=response.text)  # response.text is a str object
        # log.info("cached_selector", cached_selector=response._cached_selector)
        # log.info("meta", meta=response.meta)
        # log.info("selector", selector=response.selector)
        # log.info("xpath", xpath=response.xpath)
        # log.info("attributes", attributes=response.attributes)
        # log.info("url", url=response.url)
        # log.info("status", status=response.status)
        # log.info("headers", headers=response.headers)
        # log.info("body", body=response.body) # response.body is a bytes object
        # log.info("flags", flags=response.flags)
        # log.info("request", request=response.request)
        # log.info("certificate", certificate=response.certificate)
        # log.info("ip_address", ip_address=response.ip_address)
        # log.info("protocol", protocol=response.protocol)
        # log.info("encoding", encoding=response.encoding)
        item_loader = ItemLoader(item=BooksToscrapeItem(), response=response)

        item_loader.add_css("book_name", "article.product_pod h3 a::attr(title)")
        item_loader.add_css("product_price", "article.product_pod p.price_color::text")
        yield item_loader.load_item()

        # book_containers = response.css("article.product_pod")

        # for book in book_containers:
        #     book_name = book.css("h3 a::attr(title)").get()
        #     product_price = book.css("p.price_color::text").get()
        #     yield {"book_name": book_name, "product_price": product_price}

import scrapy
import structlog

from zillow_crawler.items import BooksToscrapeItem

log = structlog.get_logger()


class ZillowHousesSpider(scrapy.Spider):
    name = "zillow_houses"
    allowed_domains = ["zillow.com"]
    # According to zillow's robots.txt, this path was not disallowed
    start_urls = ["https://www.zillow.com/homes/"]

    def parse(self, response):
        log.info("Parsing response", response=response)

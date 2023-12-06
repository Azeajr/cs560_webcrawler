"""Test configuration for the webcrawler package."""
import pytest
# from scrapy.http import HtmlResponse
from webcrawler.zillow_crawler.spiders.zillow_houses import ZillowHousesSpider


@pytest.fixture
def spider():
    """Return the spider class."""
    return ZillowHousesSpider()

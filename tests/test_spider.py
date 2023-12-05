# from unittest.mock import Mock, patch

import pytest
# from scrapy.http import HtmlResponse
from webcrawler.zillow_crawler.spiders.zillow_houses import ZillowHousesSpider


@pytest.fixture
def spider():
    return ZillowHousesSpider()


def test_init(spider):
    assert spider.duplicate_page_count == 0
    assert spider.duplicate_page_count_limit == 10


# @patch.object(ZillowHousesSpider, "spider_closed")
# def test_from_crawler(mock_spider_closed):
#     crawler = Mock()
#     spider = ZillowHousesSpider.from_crawler(crawler)
#     assert crawler.signals.connect.called
#     assert mock_spider_closed.called


# @patch.object(ZillowHousesSpider, "get_stats")
# def test_spider_closed(mock_get_stats, spider):
#     spider = Mock()
#     spider.spider_closed(spider)
#     assert mock_get_stats.called


# def test_get_stats(spider):
#     stats = spider.get_stats()
#     assert isinstance(stats, dict)


# def test_parse(spider):
#     response = HtmlResponse(
#         url="http://www.example.com",
#         body="""
#         <html>
#         <body>
#         <article>
#             <address>123 Main St</address>
#             <span data-test='property-card-price'>$200,000</span>
#             <ul>
#                 <li><b>3</b> bd</li>
#                 <li><b>2</b> ba</li>
#                 <li><b>1500</b> sqft</li>
#             </ul>
#         </article>
#         </body>
#         </html>
#     """,
#     )
#     results = list(spider.parse(response))
#     assert len(results) == 2
#     assert results[0]["type"] == "house"
#     assert results[0]["address"] == "123 Main St"
#     assert results[0]["price"] == "$200,000"
#     assert results[0]["sqft"] == "1500"
#     assert results[0]["bedrooms"] == "3"
#     assert results[0]["bathrooms"] == "2"
#     assert results[1]["type"] == "page"
#     assert results[1]["url"] == "http://www.example.com"
#     assert results[1]["crawled"]


@pytest.mark.asyncio(asyncio_mode="strict")
class TestSpider:
    """Test the spider."""

    def test_init(self, spider):
        assert spider.duplicate_page_count == 0
        assert spider.duplicate_page_count_limit == 10

    # async def test_parse(self, spider):
    #     """Test the parse method."""
    #     response = HtmlResponse(
    #         url="http://www.example.com",
    #         body="""
    #         <html>
    #         <body>
    #         <article>
    #             <address>123 Main St</address>
    #             <span data-test='property-card-price'>$200,000</span>
    #             <ul>
    #                 <li><b>3</b> bd</li>
    #                 <li><b>2</b> ba</li>
    #                 <li><b>1500</b> sqft</li>
    #             </ul>
    #         </article>
    #         </body>
    #         </html>
    #     """,
    #     )
    #     results = list(spider.parse(response))
    #     assert len(results) == 2
    #     assert results[0]["type"] == "house"
    #     assert results[0]["address"] == "123 Main St"
    #     assert results[0]["price"] == "$200,000"
    #     assert results[0]["sqft"] == "1500"
    #     assert results[0]["bedrooms"] == "3"
    #     assert results[0]["bathrooms"] == "2"
    #     assert results[1]["type"] == "page"
    #     assert results[1]["url"] == "http://www.example.com"
    #     assert results[1]["crawled"]

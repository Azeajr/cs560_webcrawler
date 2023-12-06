"""Test the spider."""
from scrapy.http import HtmlResponse



# @pytest.mark.asyncio(asyncio_mode="strict")
class TestSpider:
    """Test the spider."""

    def test_init(self, spider):
        """Test spider initialization."""
        assert spider.duplicate_page_count == 0
        assert spider.duplicate_page_count_limit == 10

    def test_parse(self, spider):
        """Test the parse method."""
        response = HtmlResponse(
            url="http://www.example.com",
            body="""
            <html>
            <body>
            <article>
                <address>123 Main St</address>
                <span data-test='property-card-price'>$200,000</span>
                <ul>
                    <li><b>3</b> bd</li>
                    <li><b>2</b> ba</li>
                    <li><b>1500</b> sqft</li>
                </ul>
            </article>
            </body>
            </html>""".encode(
                "utf-8"
            ),
            encoding="utf-8",
        )
        listing, page = list(spider.parse(response))

        assert listing["type"] == "house"
        assert listing["address"] == "123 Main St"
        assert listing["price"] == "$200,000"
        assert listing["sqft"] == "1500"
        assert listing["bedrooms"] == "3"
        assert listing["bathrooms"] == "2"
        assert listing["house_hash"] == "a944b8c57499cb3c80c82e625be1ca3b"

        assert page["type"] == "page"
        assert page["url"] == "http://www.example.com"
        assert page["crawled"]
        assert page["page_hash"] == "58ea65a68ae25c138c4b9de30031de29"

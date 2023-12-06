"""
This module contains the scrapy items for the zillow_crawler.  These items
are used to store data from the response in a standardized format.  This
allows for easier processing and storage of the data.
"""
import scrapy


class HouseItem(scrapy.Item):
    """
    Item for storing house data.
    """

    address = scrapy.Field()
    price = scrapy.Field()
    sqft = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    house_hash = scrapy.Field()


class PageItem(scrapy.Item):
    """
    Item for storing page data.
    """

    page_url = scrapy.Field()
    page_title = scrapy.Field()
    page_content = scrapy.Field()
    page_hash = scrapy.Field()

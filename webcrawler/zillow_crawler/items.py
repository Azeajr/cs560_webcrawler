# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    sqft = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    house_hash = scrapy.Field()


class PageItem(scrapy.Item):
    page_url = scrapy.Field()
    page_title = scrapy.Field()
    page_content = scrapy.Field()
    page_hash = scrapy.Field()

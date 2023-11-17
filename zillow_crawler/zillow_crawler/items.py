# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZillowCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()


class BooksToscrapeItem(scrapy.Item):
    # define the fields for your item here like:
    book_name = scrapy.Field()
    product_price = scrapy.Field()

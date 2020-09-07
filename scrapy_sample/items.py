# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapySampleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PostItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
    comments = scrapy.Field()
    score = scrapy.Field()
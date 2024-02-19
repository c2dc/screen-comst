# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FirmwareItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    vendor = scrapy.Field()
    model = scrapy.Field()
    version = scrapy.Field()
    file_urls = scrapy.Field()

    #Used by pipeline
    file_urls = scrapy.Field()
    #stores the result 
    files = scrapy.Field()

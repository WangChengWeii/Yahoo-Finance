# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FinalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Code = scrapy.Field()
    Name = scrapy.Field()
    Price = scrapy.Field()
    Change = scrapy.Field()
    Percentage = scrapy.Field()
    Volume = scrapy.Field()
    Avg_Vol = scrapy.Field()
    Market_Cap = scrapy.Field()
    PE = scrapy.Field()
    _id = scrapy.Field()

    pass

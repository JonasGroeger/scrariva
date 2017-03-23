# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrarivaItem(scrapy.Item):
    isin = scrapy.Field()
    min_time = scrapy.Field()
    max_time = scrapy.Field()
    secu = scrapy.Field()
    csv = scrapy.Field()

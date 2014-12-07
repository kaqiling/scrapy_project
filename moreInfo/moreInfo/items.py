# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MoreinfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    release_time = scrapy.Field()
    popularity = scrapy.Field()
    comfort = scrapy.Field()
    transport = scrapy.Field()
    business = scrapy.Field()
    education = scrapy.Field()
    hospital = scrapy.Field()

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SecondHandItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    district = scrapy.Field()
    street = scrapy.Field()
    address = scrapy.Field()
    avg_price = scrapy.Field()
    area = scrapy.Field()
    price_num = scrapy.Field()
    price_unit = scrapy.Field()
    house_type = scrapy.Field()
    floor = scrapy.Field()
    construct_year =scrapy.Field()



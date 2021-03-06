# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewhouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    district = scrapy.Field()
    street = scrapy.Field()
    address = scrapy.Field()
    avg_price = scrapy.Field()
    status = scrapy.Field()
    open_time = scrapy.Field()
    delivery_time = scrapy.Field()
    transport = scrapy.Field()
    business = scrapy.Field()
    education = scrapy.Field()
    hospital = scrapy.Field()

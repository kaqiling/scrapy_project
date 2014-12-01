# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RentalHouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    district = scrapy.Field()
    street = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    rental_type = scrapy.Field()
    house_type = scrapy.Field()
    floor = scrapy.Field()
    decoration =scrapy.Field()

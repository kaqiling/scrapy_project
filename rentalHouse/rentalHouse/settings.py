# -*- coding: utf-8 -*-

# Scrapy settings for rentalHouse project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'rentalHouse'

SPIDER_MODULES = ['rentalHouse.spiders']
NEWSPIDER_MODULE = 'rentalHouse.spiders'
ITEM_PIPELINES = {'rentalHouse.pipelines.SQLStorePipeline':1}
AUTOTHROTTLE_ENABLED = True
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'rentalHouse (+http://www.yourdomain.com)'

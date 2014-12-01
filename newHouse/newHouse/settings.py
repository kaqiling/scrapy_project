# -*- coding: utf-8 -*-

# Scrapy settings for newHouse project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'newHouse'

SPIDER_MODULES = ['newHouse.spiders']
NEWSPIDER_MODULE = 'newHouse.spiders'
ITEM_PIPELINES = {'newHouse.pipelines.SQLStorePipeline':300}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'newHouse (+http://www.yourdomain.com)'

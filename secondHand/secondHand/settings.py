# -*- coding: utf-8 -*-

# Scrapy settings for secondHand project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'secondHand'

SPIDER_MODULES = ['secondHand.spiders']
NEWSPIDER_MODULE = 'secondHand.spiders'
ITEM_PIPELINES = {'secondHand.pipelines.SQLStorePipeline':300}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'secondHand (+http://www.yourdomain.com)'

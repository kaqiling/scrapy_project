# -*- coding: utf-8 -*-

# Scrapy settings for moreInfo project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'moreInfo'

SPIDER_MODULES = ['moreInfo.spiders']
NEWSPIDER_MODULE = 'moreInfo.spiders'
AUTOTHROTTLE_ENABLED = True
CONCURRENT_REQUESTS = '600'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'moreInfo (+http://www.yourdomain.com)'

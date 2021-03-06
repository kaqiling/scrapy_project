# -*- coding: utf-8 -*-
import scrapy
from newHouse.items import NewhouseItem

class NewhouseSpider(scrapy.Spider):
	name = 'newSpider'
	allowed_domains = ['hz.fang.anjuke.com']
	start_urls = ['http://hz.fang.anjuke.com/loupan/']

	def parse(self,response):
		url = 'http://hz.fang.anjuke.com/loupan/s?p=';
		for pageNum in range(1,42):
			yield scrapy.Request(url + str(pageNum),callback=self.parse2)

	def parse2(self,response):
		for sel in response.xpath("//div[contains(@class,'item-mod') and descendant::span[contains(@class,'price')]]"):
			item = NewhouseItem()
			item['url'] = sel.xpath('./@data-link').extract()[0].split('?')[0].encode('utf-8')
			item['name'] = sel.xpath('.//h3/text()').extract()[0].encode('utf-8').rstrip()
			item['district'] = sel.css('.plate').xpath('./text()').extract()[0].split(' ')[1].encode('utf-8')
			item['street'] = sel.css('.plate').xpath('./text()').extract()[0].split(' ')[2].encode('utf-8')
			item['address'] = sel.xpath('.//p[1]/text()').extract()[0].encode('utf-8')
			item['avg_price'] = sel.css('.price').xpath('./text()').extract()[0].encode('utf-8')
 			request = scrapy.Request(item['url'],callback=self.parse3)
			request.meta['item'] = item
			yield request

	def parse3(self,response):
		item = NewhouseItem()
		item = response.meta['item']
		item['status'] = response.css('.lp-tag-status').xpath('./text()').extract()[0].encode('utf-8')
		item['open_time'] = response.css('.spe-dd').xpath('./text()').extract()[0].encode('utf-8')
		item['delivery_time'] = response.css('.spe-dd').xpath('./text()').extract()[1].encode('utf-8')
		item['transport'] = response.css('.life-block')[0].css('.star-num').xpath('./@style').re('\d+')[0].encode('utf-8')
		item['business'] = response.css('.life-block')[1].css('.star-num').xpath('./@style').re('\d+')[0].encode('utf-8')
		item['education'] = response.css('.life-block')[2].css('.star-num').xpath('./@style').re('\d+')[0].encode('utf-8')
		item['hospital'] = response.css('.life-block')[3].css('.star-num').xpath('./@style').re('\d+')[0].encode('utf-8')
		yield item
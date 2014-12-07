# -*- coding: utf-8 -*-  
import scrapy
import pymysql
from moreInfo.items import MoreinfoItem
from scrapy.selector import Selector
from selenium import webdriver
import sys

class moreInfoSpider(scrapy.Spider):

	reload(sys)
	sys.setdefaultencoding('utf-8')

	name = 'getMoreSpider'
	allowed_domains = ['hangzhou.anjuke.com']
	start_urls = ['http://hangzhou.anjuke.com/']
	service_args = ['--load-images=false']
	db = pymysql.Connect(host="localhost",unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock",port=3306,user="root",passwd="root",db="estate_appraisal_db",charset="utf8")
	cursor = db.cursor()
	cursor.execute("SET NAMES utf8")

	def parse(self,response):
		sql = "SELECT url FROM second_house_table WHERE release_time = ''"
		self.cursor.execute(sql)
		results = self.cursor.fetchall()
		for row in results:
			url = row[0]
			request = scrapy.Request(url,callback=self.parse2)
			request.meta['url'] = url
			yield request

	def parse2(self,response):		
		url = response.meta['url']
		driver = webdriver.PhantomJS(executable_path = '/Users/hantianyan/phantomjs-1.9.8-macosx/bin/phantomjs', service_args = self.service_args)
		driver.get(response.url)
		sel = Selector(text = driver.page_source)
		item = MoreinfoItem()
		release_list = sel.css('.extra-info').xpath('./text()').extract()
		if len(release_list) > 0:
			item['release_time'] = release_list[0].encode('utf-8').split('：')[2]
			item['popularity'] = sel.css('#star_greet').xpath('./@style').re('\d+')[0].encode('utf-8')
			item['comfort'] = sel.css('#star_comfort').xpath('./@style').re('\d+')[0].encode('utf-8')
			nearsel = sel.css('.nearbox')
			item['transport'] = 0
			transport_list = nearsel.xpath(".//div[@data-attr='traffic']").css('.p_star_s').xpath('./@style').re('\d+')
			if len(transport_list) > 0:
				item['transport'] = transport_list[0].encode('utf-8')
			item['hospital'] = 0
			hospital_list = nearsel.xpath(".//div[@data-attr='hospital']").css('.p_star_s').xpath('./@style').re('\d+')
			if len(hospital_list) > 0:
				item['hospital'] = hospital_list[0].encode('utf-8')
			item['education'] = 0
			education_list = nearsel.xpath(".//div[@data-attr='school']").css('.p_star_s').xpath('./@style').re('\d+')
			if len(education_list) > 0:
				item['education'] = education_list[0].encode('utf-8')
			item['business'] = 0
			business_list = nearsel.xpath(".//div[@data-attr='commerce']").css('.p_star_s').xpath('./@style').re('\d+')
			if len(business_list) > 0:
				item['business'] = business_list[0].encode('utf-8')
			sql = "update second_house_table set release_time = '%s',popularity = '%s',comfort = '%s',transport = '%s',hospital = '%s',education = '%s',business = '%s' WHERE url = '%s' " % \
			(item['release_time'],item['popularity'],item['comfort'],item['transport'],item['hospital'],item['education'],item['business'],url)
			self.cursor.execute(sql)
			self.db.commit()
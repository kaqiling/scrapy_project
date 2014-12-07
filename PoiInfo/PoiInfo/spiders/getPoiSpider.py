# -*- coding: utf-8 -*-  
import scrapy
from PoiInfo.items import PoiinfoItem
from scrapy.selector import Selector
import pymysql
import json
import sys

class PoiInfoSpider(scrapy.Spider):

	reload(sys)
	sys.setdefaultencoding('utf-8')

	name = 'getPoiSpider'
	allowed_domains = ['api.map.baidu.com']
	start_urls = ['http://api.map.baidu.com/place/v2/search?&q=%E9%A5%AD%E5%BA%97&region=%E5%8C%97%E4%BA%AC&output=json&ak=E4805d16520de693a3fe707cdc962045']

	query_key = '银行$医院$学校$酒店$餐饮$公交站$地铁$超市$购物$景点'
	uid_dis_dict = {}
	db = pymysql.Connect(host="localhost",unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock",port=3306,user="root",passwd="root",db="estate_appraisal_db",charset="utf8")
	cursor = db.cursor()
	cursor.execute("SET NAMES utf8")

	def parse(self,response):
		sql = "SELECT url,latitude,longitude FROM new_house_table WHERE uid_dis_dict = ''"
		self.cursor.execute(sql)
		results = self.cursor.fetchall()
		for row in results:
			url = row[0]
			latitude = row[1]
			longitude = row[2]
			request_url = "http://api.map.baidu.com/place/v2/search?&query=" + self.query_key.decode('utf-8') + "&location=" + str(latitude).decode('utf-8') + "," + str(longitude).decode('utf-8') + "&radius=1000&ak=0LnNaEYoprF736QdhXNmAnX2&scope=2&page_size=20&page_num=0"
			request = scrapy.Request(request_url,callback=self.parse2)
			request.meta['url'] = url
			request.meta['latitude'] = latitude
			request.meta['longitude'] = longitude
			yield request

	def parse2(self,response):		
		url = response.meta['url']
		self.uid_dis_dict[url] = {}
		latitude = response.meta['latitude']
		longitude = response.meta['longitude']
		total = int(response.xpath("//total/text()").extract()[0])
		page_source = response.body_as_unicode()
		sel = Selector(text = page_source)
		results = sel.xpath("//result")
		for i in range(len(results)):
			uid = results[i].xpath("./uid/text()").extract()[0]
			dis_list = results[i].xpath("./detail_info/distance/text()").extract()
			if len(dis_list) > 0:
				distance = int(dis_list[0])
				if distance <= 1000:
					self.uid_dis_dict[url][uid] = distance
					item = PoiinfoItem()
					item['uid'] = uid
					item['latitude'] = float(results[i].xpath("./location/lat/text()").extract()[0])
					item['longitude'] = float(results[i].xpath("./location/lng/text()").extract()[0])
					item['address'] = results[i].xpath("./address/text()").extract()[0]
					item['name'] = results[i].xpath("./name/text()").extract()[0]
					item['category'] = "unknown"
					item['rating'] = "0"
					item['comment_num'] = "0"
					cate_list = results[i].xpath("./detail_info/type/text()").extract()
					if len(cate_list) > 0: 
						item['category'] = cate_list[0]
					rating_list = results[i].xpath("./detail_info/overall_rating/text()").extract()
					if len(rating_list) > 0:
						item['rating'] = rating_list[0]
					comment_list = results[i].xpath("./detail_info/comment_num/text()").extract()
					if len(comment_list) > 0:
						item['comment_num'] = comment_list [0]
					yield item			
		if(total > 20):						
			for page_num in range(1,total / 20 + 1):
				request_url = "http://api.map.baidu.com/place/v2/search?&query=" + self.query_key.decode('utf-8') + "&location=" + str(latitude).decode('utf-8') + "," + str(longitude).decode('utf-8') + "&radius=1000&ak=0LnNaEYoprF736QdhXNmAnX2&scope=2&page_size=20&page_num=" + str(page_num).decode('utf-8')
				request = scrapy.Request(request_url,callback=self.parse3)
				request.meta['uid_dis_dict'] = self.uid_dis_dict[url]
				request.meta['url'] = url
				yield request
		else:
			insert_sql = "update new_house_table set uid_dis_dict = '%s' WHERE url = '%s' " % \
			(str(self.uid_dis_dict[url]).replace("u'",'"').replace("'",'"'),url)
			self.cursor.execute(insert_sql)
			self.db.commit()

	def parse3(self,response):
		url = response.meta['url']
		self.uid_dis_dict[url] = response.meta['uid_dis_dict']
		page_source = response.body_as_unicode()
		sel = Selector(text = page_source)
		results = sel.xpath("//result")
		for i in range(len(results)):
			uid = results[i].xpath("./uid/text()").extract()[0]
			dis_list = results[i].xpath("./detail_info/distance/text()").extract()
			if len(dis_list) > 0:
				distance = int(dis_list[0])
				if distance <= 1000:
					self.uid_dis_dict[url][uid] = distance
					item = PoiinfoItem()
					item['uid'] = uid
					item['latitude'] = float(results[i].xpath("./location/lat/text()").extract()[0])
					item['longitude'] = float(results[i].xpath("./location/lng/text()").extract()[0])
					item['address'] = results[i].xpath("./address/text()").extract()[0]
					item['name'] = results[i].xpath("./name/text()").extract()[0]
					item['category'] = "unknown"
					item['rating'] = "0"
					item['comment_num'] = "0"
					cate_list = results[i].xpath("./detail_info/type/text()").extract()
					if len(cate_list) > 0: 
						item['category'] = cate_list[0]
					rating_list = results[i].xpath("./detail_info/overall_rating/text()").extract()
					if len(rating_list) > 0:
						item['rating'] = rating_list[0]
					comment_list = results[i].xpath("./detail_info/comment_num/text()").extract()
					if len(comment_list) > 0:
						item['comment_num'] = comment_list [0]
					yield item
		insert_sql = "update new_house_table set uid_dis_dict = '%s' WHERE url = '%s' " % \
		(str(self.uid_dis_dict[url]).replace("u'",'"').replace("'",'"'),url)
		self.cursor.execute(insert_sql)
		self.db.commit()
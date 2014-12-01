# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class SQLStorePipeline(object):

	def __init__(self):
		self.db = MySQLdb.connect(host="localhost",user="root",passwd="",db="estate_appraisal_db")
		self.cursor = self.db.cursor()
		self.cursor.execute("SET NAMES utf8")
		self.db.commit()

	def process_item(self, item, spider):
		sql = "INSERT INTO RENTAL_HOUSE_TABLE(URL,NAME,DISTRICT,STREET,ADDRESS,PRICE,\
			HOUSE_TYPE,FLOOR,RENTAL_TYPE,DECORATION) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
			(item['url'],item['name'],item['district'],item['street'],item['address'],item['price'],item['house_type'],\
				item['floor'],item['rental_type'],item['decoration'])
		self.cursor.execute(sql)
		self.db.commit()
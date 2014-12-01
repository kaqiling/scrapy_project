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
		sql = "INSERT INTO SECOND_HOUSE_TABLE(URL,NAME,DISTRICT,STREET,ADDRESS,AVG_PRICE,\
			AREA,PRICE_NUM,PRICE_UNIT,HOUSE_TYPE,FLOOR,CONSTRUCT_YEAR) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
			(item['url'],item['name'],item['district'],item['street'],item['address'],item['avg_price'],item['area'],item['price_num'],item['price_unit'],item['house_type'],item['floor'],item['construct_year'])
		self.cursor.execute(sql)
		self.db.commit()
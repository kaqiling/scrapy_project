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
		self.db = MySQLdb.connect(host="localhost",user="root",passwd="",db="estate_appraisal_db",charset="utf8")
		self.cursor = self.db.cursor()
		self.cursor.execute("SET NAMES utf8")
		self.cursor.execute("SET CHARACTER_SET_CLIENT=utf8")
		self.cursor.execute("SET CHARACTER_SET_RESULTS=utf8")
		self.db.commit()

	def process_item(self, item, spider):
		sql = "INSERT INTO NEW_HOUSE_TABLE(URL,NAME,DISTRICT,STREET,\
				ADDRESS,AVG_PRICE) VALUES ('%s','%s','%s','%s','%s','%s')" % \
				(item['url'],item['name'],item['district'],item['street'],item['address'],item['avg_price'])
		self.cursor.execute(sql.encode('utf8'))
		self.db.commit()
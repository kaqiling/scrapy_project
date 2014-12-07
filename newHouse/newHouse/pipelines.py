# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class SQLStorePipeline(object):

	def __init__(self):
		self.db = pymysql.Connect(host="localhost",unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock",port=3306,user="root",passwd="root",db="estate_appraisal_db",charset="utf8")
		self.cursor = self.db.cursor()
		self.cursor.execute("SET NAMES utf8")
		self.cursor.execute("SET CHARACTER_SET_CLIENT=utf8")
		self.cursor.execute("SET CHARACTER_SET_RESULTS=utf8")
		self.db.commit()

	def process_item(self, item, spider):
		sql = "INSERT INTO NEW_HOUSE_TABLE(URL,NAME,DISTRICT,STREET,\
				ADDRESS,AVG_PRICE,STATUS,OPEN_TIME,DELIVERY_TIME,TRANSPORT,BUSINESS,EDUCATION,HOSPITAL) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
				(item['url'],item['name'],item['district'],item['street'],item['address'],item['avg_price'],item['status'],item['open_time'],item['delivery_time'],item['transport'],item['business'],item['education'],item['hospital'])
		self.cursor.execute(sql.encode('utf8'))
		self.db.commit()
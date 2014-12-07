# -*- coding: utf-8 -*-  
import pymysql
import urllib2
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def geocoding_api_request( address ):
	try:
		request_url = "http://api.map.baidu.com/geocoder/v2/?address=" + address + "&output=json&ak=0LnNaEYoprF736QdhXNmAnX2"
		response = urllib2.urlopen(request_url).read()
		result = json.loads(response)
		if result['status'] == 0:
			return result['result']['location']
		else:
			print address
			return None
	except BaseException:
		print address
		return None

def geocoding_process_table(sql,table_name):
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		url = row[0]
		name = row[1]
		district = row[2]
		street = row[3]
		address = row[4]
		location = geocoding_api_request((pro_city.decode('utf-8') + district + street + address + name).replace(' ','').replace('...',''))
		if(location != None):
			longitude = location['lng']
			latitude = location['lat']
			if table_name == 'new_house_table':
				insert_sql = "update new_house_table set longitude = '%f', latitude = '%f' WHERE url = '%s' " % (longitude,latitude,url)
			elif table_name == 'second_house_table':
				insert_sql = "update second_house_table set longitude = '%f', latitude = '%f' WHERE url = '%s' " % (longitude,latitude,url)
			elif table_name == 'rental_house_table':
				insert_sql = "update rental_house_table set longitude = '%f', latitude = '%f' WHERE url = '%s' " % (longitude,latitude,url)
			cursor.execute(insert_sql)
			db.commit()
pro_city = "浙江省杭州市"
db = pymysql.Connect(host="localhost",unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock",port=3306,user="root",passwd="root",db="estate_appraisal_db",charset="utf8")
cursor = db.cursor()
cursor.execute("SET NAMES utf8")

geocoding_process_table("SELECT url,name,district,street,address FROM new_house_table","new_house_table")
#geocoding_process_table("SELECT url,name,district,street,address FROM second_house_table","second_house_table")
#geocoding_process_table("SELECT url,name,district,street,address FROM rental_house_table","rental_house_table")




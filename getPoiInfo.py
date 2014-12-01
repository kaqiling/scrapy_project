# -*- coding: utf-8 -*-  
import MySQLdb
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

def insert_poiInfo(poi):
	uid = poi['uid']
	latitude = poi['location']['lat']
	longitude = poi['location']['lng']
	address = poi['address']
	name = poi['name']
	rating = "0"
	comment_num = "0"
	category = "unknown"
	if 'overall_rating' in poi['detail_info']:
		rating = poi['detail_info']['overall_rating']
	if 'comment_num' in poi['detail_info']:
		comment_num = poi['detail_info']['comment_num']
	if 'type' in poi['detail_info']:
		category = poi['detail_info']['type']
	sql = "INSERT INTO POI_INFO_TABLE(uid,latitude,longitude,address,name,category,rating,comment_num) VALUES \
			('%s','%f','%f','%s','%s','%s','%s','%s')" % \
			(uid,latitude,longitude,address,name,category,rating,comment_num)
	try: 
		cursor.execute(sql)
		db.commit()
	except BaseException:
		return

def uid_dis_dict_push(poi):		
	if 'distance' in poi['detail_info'] and poi['detail_info']['distance'] <= 1000:
		distance = poi['detail_info']['distance']
		insert_poiInfo(poi)
		uid_dis_dict[poi['uid']] = distance


def place_api_request(latitude,longitude,page_num):
	try:
		request_url = "http://api.map.baidu.com/place/v2/search?&query=" + query_key.decode('utf-8') + "&location=" + str(latitude).decode('utf-8') + "," + str(longitude).decode('utf-8') + "&radius=1000&output=json&ak=0LnNaEYoprF736QdhXNmAnX2&scope=2&page_size=20&page_num=" + str(page_num).decode('utf-8')
		response = urllib2.urlopen(request_url).read()
		result = json.loads(response)
		if result['status'] == 0 and len(result['results']) > 0:
			return result
		else:
			print result['message'],len(result['results'])
			return None
	except BaseException:
		print "exception"
		return None

def place_api_request_loop(latitude,longitude):
	result = place_api_request(latitude,longitude,0)
	if result != None:
		total = result['total']
		for i in range(len(result['results'])):
			uid_dis_dict_push(result['results'][i])
		if(total > 20):			
			for i in range(1,total / 20 + 1):
				result = place_api_request(latitude,longitude,i)
				if result != None:
					for j in range(len(result['results'])):
						uid_dis_dict_push(result['results'][j])

def dict_to_string(dict):
	return str(dict).replace("u'",'"').replace("'",'"')

def place_process_table(sql,table_name):
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		uid_dis_dict.clear()
		url = row[0]
		latitude = row[1]
		longitude = row[2]
		place_api_request_loop(latitude,longitude)
		if table_name == 'new_house_table':
			insert_sql = "update new_house_table set uid_dis_dict = '%s' WHERE url = '%s' " % \
			(dict_to_string(uid_dis_dict),url)
		elif table_name == 'second_house_table':
			insert_sql = "update second_house_table set uid_dis_dict = '%s' WHERE url = '%s' " % \
			(dict_to_string(uid_dis_dict),url)
		elif table_name == 'rental_house_table':
			insert_sql = "update rental_house_table set uid_dis_dict = '%s' WHERE url = '%s' " % \
			(dict_to_string(uid_dis_dict),url)
		cursor.execute(insert_sql)
		db.commit()



pro_city = '浙江省杭州市'
db = MySQLdb.connect(host="localhost",user="root",passwd="",db="estate_appraisal_db",charset="utf8")
cursor = db.cursor()
cursor.execute("SET NAMES utf8")

#geocoding_process_table("SELECT url,name,district,street,address FROM new_house_table","new_house_table")
#geocoding_process_table("SELECT url,name,district,street,address FROM second_house_table","second_house_table")
#geocoding_process_table("SELECT url,name,district,street,address FROM rental_house_table","rental_house_table")


uid_dis_dict = {}
query_key = '银行$医院$学校$酒店$餐饮$公交站$地铁$超市$购物$景点'
#place_process_table("SELECT url,latitude,longitude FROM new_house_table","new_house_table")
place_process_table("SELECT url,latitude,longitude FROM second_house_table","second_house_table")
#place_process_table("SELECT url,latitude,longitude FROM rental_house_table","rental_house_table")



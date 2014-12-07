import scrapy
from rentalHouse.items import RentalHouseItem

class RentalHouseSpider(scrapy.Spider):
	name = 'rentalSpider'
	allowed_domains = ['hz.zu.anjuke.com']
	start_urls = ['http://hz.zu.anjuke.com/fangyuan/']

	def parse(self,response):
		url = 'http://hz.zu.anjuke.com/fangyuan/p';
		for pageNum in range(1,2198):
			yield scrapy.Request(url + str(pageNum) + '/',callback=self.parse2)

	def parse2(self,response):
		for sel in response.xpath("//div[@id='apf_id_13_list']/dl"):
			item = RentalHouseItem()
			item['url'] = sel.xpath("./@link").extract()[0].split('?')[0].encode('utf-8')

			selInfo = sel.xpath("./dd[@class='dd_info']/p[@class='p_tag']/text()")
			item['house_type'] = selInfo.extract()[0].strip().encode('utf-8')
			item['rental_type'] = selInfo.extract()[1].strip().encode('utf-8')
			item['decoration'] = selInfo.extract()[2].strip().encode('utf-8')
			item['floor'] = selInfo.extract()[3].strip().encode('utf-8')

			address = sel.xpath("./dd[@class='dd_info']/address/text()").extract()[0].replace(u'\xa0',u' ')
			item['name'] = address.split('[')[0].strip().encode('utf-8')
			item['district'] = address.split('[')[1].split('  ')[0].split('-')[0].strip().encode('utf-8')
			item['street'] = address.split('[')[1].split('  ')[0].split('-')[1].strip().encode('utf-8')
			item['address'] = address.split('[')[1].split('  ')[1].replace(']','').encode('utf-8')
			item['price'] = sel.xpath("./dd[@class='dd_price']/strong/text()").extract()[0].encode('utf-8')
			yield item
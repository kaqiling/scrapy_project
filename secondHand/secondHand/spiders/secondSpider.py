import scrapy
from secondHand.items import SecondHandItem

class SecondHandSpider(scrapy.Spider):
	name = 'secondSpider'
	allowed_domains = ['hangzhou.anjuke.com']
	start_urls = ['http://hangzhou.anjuke.com/sale/']

	def parse(self,response):
		url = 'http://hangzhou.anjuke.com/sale/p';
		for pageNum in range(1,101):
			yield scrapy.Request(url + str(pageNum) + '/',callback=self.parse2)

	def parse2(self,response):
		for sel in response.xpath("//ul[@id='apf_id_13_list']/li"):
			item = SecondHandItem()
			item['url'] = sel.xpath("./a/@href").extract()[0].split('?')[0].encode('utf-8')
			selDetail = sel.xpath("./div[@class='details']")
			item['area'] = selDetail.xpath("./div[2]/span[1]/text()").re('\d+')[0].encode('utf-8')
			item['house_type'] = selDetail.xpath("./div[2]/span[3]/text()").extract()[0].encode('utf-8')
			item['avg_price'] = selDetail.xpath("./div[2]/span[5]/text()").re('\d+')[0].encode('utf-8')
			item['floor'] = selDetail.xpath("./div[2]/span[7]/text()").extract()[0].encode('utf-8')
			item['construct_year'] = selDetail.xpath("./div[2]/span[9]/text()").re('\d+')[0].encode('utf-8')
			communityName = selDetail.xpath(".//span[@class='community_name']/text()").extract()[0].replace(u'\xa0',u' ')
			item['name'] = communityName.split('[')[0].rstrip().encode('utf-8')
			item['district'] = communityName.split('[')[1].split(' ')[0].split('-')[0].encode('utf-8')
			item['street'] = communityName.split('[')[1].split(' ')[0].split('-')[1].encode('utf-8')
			item['address'] = communityName.split('[')[1].split(' ')[1].replace(']','').encode('utf-8')
			item['price_num'] = sel.xpath(".//span[@class='price-num']/text()").extract()[0].encode('utf-8')
			item['price_unit'] = sel.xpath(".//span[@class='price-unit']/text()").extract()[0].encode('utf-8')
			yield item
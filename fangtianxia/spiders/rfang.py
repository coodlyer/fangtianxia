# coding=utf-8
import scrapy
import re
import sys 
from fangtianxia.items import Rent_houseItem

reload(sys)  
sys.setdefaultencoding('utf8')  

class RfangSpider(scrapy.Spider):
    name = "rfang"
    allowed_domains = ["fang.com"]

    def start_requests(self):
        total_page = 100
        baseURL = "http://zu.cd.fang.com/house/"
        for i in xrange(1, total_page+1):
            url = baseURL +"i3" + str(i) + "/"
            yield scrapy.Request(url, callback=self.parse_rent_house_list)

    def parse_rent_house_list(self, response):
        item = Rent_houseItem()
        URL = "http://zu.cd.fang.com"

        sels = response.xpath('//dl[@class="list hiddenMap rel"]')
        for sel in sels:
            renting_type = sel.xpath('.//dd[@class="info rel"]/p[2]/text()[1]').extract()[0]
            house_link = sel.xpath('.//dt/a/@href').extract()
            house_link = URL + str(sel.xpath('.//dt/a/@href').extract()[0])
            yield scrapy.Request(house_link,meta={"renting_type":renting_type},callback=self.parse_zufang_page)

    def parse_zufang_page(self, response):
        item = Rent_houseItem()        
        item["renting_type"] = response.meta['renting_type']
        basic_infor = response.xpath("//ul[@class='house-info']")

        name = basic_infor.xpath(".//li[3]/a[1]/text()").extract()[0]
        price = basic_infor.xpath(".//li[1]/strong[1]/text()").extract()[0]
        house_gaikuo = basic_infor.xpath(".//li[2]/text()[1]").extract()[0]
        house_type = basic_infor.xpath(".//li[2]/text()[2]").extract()[0]
        mianji = basic_infor.xpath(".//li[2]/span[4]/text()").extract()[0]
        cenggao = basic_infor.xpath(".//li[2]/text()[4]").extract()[0]
        chaoxiang = basic_infor.xpath(".//li[2]/text()[5]").extract()[0]
        zhuangxiuzhuangkuang = basic_infor.xpath(".//li[2]/text()[6]").extract()[0]
        
        payment = basic_infor.xpath(".//li[1]/text()").extract()[0]
        fangyuanbianhao = response.xpath("//span[@class='mr10']/text()").extract()[0]
        update_time = response.xpath("//p[@class='gray9']/span[2]/text()").extract()[0]

        payment=re.findall("\[.*\]",payment)[0]
        fangyuanbianhao = re.findall("\d+",fangyuanbianhao)
        update_time = re.findall("[\u4e00-\u9fa5]+",update_time)
        
        item["mianji"] = mianji
        item['name'] = name
        item['price'] = price
        item["house_gaikuo"] = house_gaikuo
        item["house_type"] = house_type
        item["cenggao"] = cenggao
        item["chaoxiang"] = chaoxiang
        item['zhuangxiuzhuangkuang'] = zhuangxiuzhuangkuang
        item["payment"] = payment
        item["fangyuanbianhao"] = fangyuanbianhao
        item["update_time"] = update_time

        yield item
        
# coding=utf-8
import scrapy

class Shand_houseItem(scrapy.Item):

	house_id = scrapy.Field()
	name = scrapy.Field()
	wuye_gongsi = scrapy.Field()
	loudong_shu = scrapy.Field()

	xiaoqu_address = scrapy.Field()	
	location = scrapy.Field()
	huanxianweizhi = scrapy.Field()
	wuye_type = scrapy.Field()
	kaifashang = scrapy.Field()
	jianzhu_type = scrapy.Field()
	zhandi_mianji = scrapy.Field()
	zonghu_shu = scrapy.Field()	
	rongji_lv = scrapy.Field()
	wuye_fee = scrapy.Field()
	wuye_address = scrapy.Field()
	xiangmutese = scrapy.Field()
	youbian = scrapy.Field()
	chanquan = scrapy.Field()
	built_time = scrapy.Field()
	jianzhu_jiegou = scrapy.Field()
	jianzhu_mianji = scrapy.Field()
	dangqihu_shu = scrapy.Field()
	lvhua_lv = scrapy.Field()
	wuye_phone = scrapy.Field()

	## gps
	gps_x = scrapy.Field()
	gps_y = scrapy.Field()

class Rent_houseItem(scrapy.Item):
	
	mianji = scrapy.Field()
	name = scrapy.Field()
	price = scrapy.Field()
	payment = scrapy.Field()
	house_gaikuo = scrapy.Field()
	house_type = scrapy.Field()
	cenggao = scrapy.Field()
	chaoxiang = scrapy.Field()
	zhuangxiuzhuangkuang = scrapy.Field()
	renting_type = scrapy.Field()

	fangyuanbianhao = scrapy.Field()
	update_time = scrapy.Field()

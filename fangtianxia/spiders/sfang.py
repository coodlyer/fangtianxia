# coding=utf-8
import scrapy
import re
import sys
from fangtianxia.items import Shand_houseItem

reload(sys)
sys.setdefaultencoding('utf8')

class SfangSpider(scrapy.Spider):
    name = "sfang"
    allowed_domains = ["fang.com"]

    def start_requests(self):
        total_page = 100
        baseURL = "http://esf.cd.fang.com/housing/"
        for i in xrange(1, total_page+1):
            url = baseURL +"__0_0_0_0_" + str(i) + "_0_0/"
            yield scrapy.Request(url, callback=self.parse_s_hand_house_list)

    def parse_s_hand_house_list(self, response):
        links = response.xpath('//dl[@class="plotListwrap clearfix"]/dt/a/@href').extract()
        for house_link in links:
            yield scrapy.Request(house_link,callback=self.parse_xiaoqu_page)

    def parse_xiaoqu_page(self, response):
        detail_link = response.xpath('//ul[@class="nav clearfix"]/li[2]/a/@href').extract()[0]

        newcode = response.xpath('/html/body/script[1]/text()').re('newcode=*(.*)')[0]
        newcode = re.findall("([0-9]+)",newcode)[0]
        map_link = "http://esf.cd.fang.com/newsecond/Map/?newcode="+ str(newcode)

        house_id = re.findall('http://(.+).fang.com', response.url)[0]
        wuye_gongsi = response.xpath("//div[@class='plptinfo_list clearfix']/ul/li[9]/text()").extract()[0]
        loudong_shu = response.xpath("//div[@class='plptinfo_list clearfix']/ul/li[2]/text()").extract()[0]

        if map_link is not None:
        # go to map page
            if detail_link is not None:
                yield scrapy.Request(map_link, meta={"detail_link": detail_link,"house_id": house_id,
                                     "wuye_gongsi":wuye_gongsi,"loudong_shu":loudong_shu},callback=self.parse_gps)
        else:
        # go to detail page
            if detail_link is not None:
                yield scrapy.Request(detail_link, meta={"house_id": house_id,"gps_x": "","gps_y": "",
                                     "wuye_gongsi":wuye_gongsi,"loudong_shu":loudong_shu}, callback=self.parse_detail_page)

    def parse_gps(self, response):
        #print response
        script_str = response.xpath("//script").extract()[4]

        gps_x = re.findall("([0-9]+\.[0-9]+)", script_str)[1]
        if len(gps_x) == 0:  gps_x = ""
        gps_y = re.findall("([0-9]+\.[0-9]+)", script_str)[2]
        if len(gps_y) == 0:  gps_y = ""

        # go to detail page
        yield scrapy.Request(response.meta["detail_link"],
                             meta={"house_id": response.meta["house_id"],"gps_x": gps_x,"gps_y": gps_y,
                                   "wuye_gongsi":response.meta['wuye_gongsi'],"loudong_shu":response.meta['loudong_shu']},
                                   callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        item = Shand_houseItem()
        item['house_id'] = response.meta['house_id']
        item['wuye_gongsi'] = response.meta['wuye_gongsi']
        item['loudong_shu'] = response.meta['loudong_shu']
        item['gps_x'] = response.meta['gps_x']
        item['gps_y'] = response.meta['gps_y']

        house_name = response.xpath("//a[@class='tt']/text()").extract()
        if len(house_name)!=0:
            house_name = house_name[0]
        else:
            house_name = ""
        item["name"] =  house_name

        basic_infor = response.xpath("//div[2]/div[2]/dl")
        basic_title={"xiaoqu_address":u"小区地址：","xiangmutese":u"项目特色：","location":u"所属区域：",
                     "youbian":u"邮    编：","huanxianweizhi":u"环线位置","chanquan":u"产权描述：",
                     "wuye_type":u"物业类别：","kaifashang":u"开 发 商：","jianzhu_type":u"建筑类别：",
                     "jianzhu_mianji":u"建筑面积：","zhandi_mianji":u"占地面积：","dangqihu_shu":u"当期户数：",
                     "zonghu_shu":u"总 户 数：","lvhua_lv":u"绿 化 率：","rongji_lv":u"容 积 率：","wuye_fee":u"物 业 费：",
                     "wuye_phone":u"物业办公电话：","wuye_address":u"物业办公地点：","built_time":u"竣工时间："}

        
        for i in xrange(1,25):
            infor_title = basic_infor.xpath("./dd["+str(i)+"]/strong/text()").extract()
            jianzhu_jiegou = basic_infor.xpath("./dd["+str(i)+"]/span/text()").extract()
            if(len(jianzhu_jiegou)!=0):
                item["jianzhu_jiegou"] = jianzhu_jiegou[0]
            if(len(infor_title)!=0):
                infor_title = infor_title[0]

            infor = basic_infor.xpath("./dd["+str(i)+"]/text()").extract()
            if(len(infor)!=0):
                infor = infor[0]
            # print type(str(infor_title).encode("utf-8"))
            for title in basic_title:   
                if basic_title[title]==str(infor_title).encode("utf-8"): 
                    item[title] = str(infor).encode("utf-8")
        yield item
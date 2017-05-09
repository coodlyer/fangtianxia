
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.contrib.exporter import CsvItemExporter
from scrapy.contrib.exporter import JsonLinesItemExporter
from scrapy import signals
import re

SHAND_HOUSE_EXPORT_FIELDS = ["name","house_id","location","xiaoqu_address", "huanxianweizhi","xiangmutese", "youbian", 
                             "chanquan", "kaifashang", "jianzhu_type", "jianzhu_mianji","jianzhu_jiegou",
                             "zhandi_mianji", "dangqihu_shu", "loudong_shu","zonghu_shu", "lvhua_lv", "rongji_lv",
                             "wuye_gongsi","wuye_fee", "wuye_phone", "wuye_type","wuye_address", 
                             "gps_x", "gps_y", "built_time" ]

RENT_HOUSE_EXPORT_FIELDS = ["name","mianji","price","payment","house_gaikuo",
                            "house_type","cenggao","chaoxiang","zhuangxiuzhuangkuang",
                            "renting_type","fangyuanbianhao","update_time"]


def strip(text):
    if text is not None:
        return re.sub(' +', ' ', text.strip().replace('\n', '').replace('\t', ''))
    else:
        return None


class SomePipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        if spider.name == 'sfang':
            file = open('shand_house.csv', 'w+b')
            self.files[spider] = file
            self.exporter = CsvItemExporter(file)
            self.exporter.fields_to_export = SHAND_HOUSE_EXPORT_FIELDS

        if spider.name == 'rfang':
            file = open('rent_house.csv', 'w+b')
            self.files[spider] = file
            self.exporter = CsvItemExporter(file)
            self.exporter.fields_to_export = RENT_HOUSE_EXPORT_FIELDS

        self.exporter.start_exporting()

    def process_item(self, item, spider):
        # if spider.name == 'sfang':
        #     for key in SHAND_HOUSE_EXPORT_FIELDS:
        #         item[key] = strip(item[key])
        self.exporter.export_item(item)

        return item


    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
class JsonLinesExportPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls,crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        out_file = open('%s_detail.json' % spider.name, 'a')
        self.files[spider] = out_file
        self.exporter = JsonLinesItemExporter(out_file, ensure_ascii=False)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        out_file = self.files.pop(spider)
        out_file.close()


    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
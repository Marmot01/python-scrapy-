# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class TtfundPipeline:

    def open_spider(self, spider):
        if spider.name =="ttfund":
            #存入mongodb数据库
            self.client = MongoClient('127.0.0.1',27017)
            self.db = self.client['TTFund']
            self.col = self.db['ttfund']

    def process_item(self, item, spider):
        if spider.name == "ttfund":
            data  = dict(item)
            self.col.insert(data)
        return item

    def close_spider(self,spider):
        if spider.name == "ttfund":
            self.client.close()

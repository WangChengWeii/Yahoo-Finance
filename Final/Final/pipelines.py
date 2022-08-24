# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import datetime
import re


class FinalPipeline:

    def open_spider(self, spider):
        client = MongoClient()
        Date = "Date" + "_" + re.sub(r"-", "_", str(datetime.date.today()))
        self.collection = client["Stock"][Date]

    def process_item(self, item, spider):

        # delete the existing data
        self.collection.delete_one({'Name': item['Name']})
        # update the data
        self.collection.insert_one(item)
        print(item)
        return item

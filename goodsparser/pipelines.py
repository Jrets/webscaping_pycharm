# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import scrapy
# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class GoodsparserPipeline:
    def __init__(self):
        client = MongoClient("localhost", 27017)
        self.mongobase = client.goods

    def process_item(self, item, spider):
        item["params"] = dict(zip(item["specs_name"], item["specs_value"]))
        del item["specs_name"]
        del item["specs_value"]
        collection = self.mongobase[spider.name]
        collection.update_one({"_id": item["_id"]},
                              {"$set": item}, upsert=True)
        print()
        return item


class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item["photos"]:
            for img in item["photos"]:
                try:
                    yield scrapy.Request(img)
                except TypeError as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item["photos"] = [itm[1] for itm in results if itm[0]]
        return item
        print()

    def file_path(self, request, response=None, info=None, *, item=None):
        directory = item["_id"]
        split_url = request.url.split("/")
        file_name = split_url[len(split_url) - 1]
        return f"full/{directory}/{file_name}"

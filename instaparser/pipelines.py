from pymongo import MongoClient


class InstaparserPipeline:
    def __init__(self):
        client = MongoClient("localhost", 27017)
        self.mongobase = client.instagram

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        collection.update_one(
            {"user_id": item.get("user_id")}, {"$set": item}, upsert=True
        )
        print(f"В коллекции {spider.name} документов: {collection.count_documents({})}")
        return item

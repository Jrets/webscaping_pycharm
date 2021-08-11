from pymongo import MongoClient
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instaparser import settings
from instaparser.spiders.instagram import InstagramSpider

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstagramSpider)
    process.start()


# Написать функцию, которая будет делать запрос к базе, который вернет список
# подписчиков только указанного пользователя
client = MongoClient("localhost", 27017)
db = client["instagram"]
collection = db.instagram
user_name = "nemnogo.knig"


def get_followers(user):
    followers_list = []
    for doc in collection.find({"parent_name": user_name, "type": "followers"}):
        followers_list.append(doc)
    return followers_list


# Написать функцию, которая будет делать запрос к базе, который вернет список
# профилей, на кого подписан указанный пользователь
def get_following(user):
    following_list = []
    for doc in collection.find({"parent_name": user_name, "type": "following"}):
        following_list.append(doc)
    return following_list


# followers = pprint(get_followers('mis_knitting'))
# following = pprint(get_following('mis_knitting'))

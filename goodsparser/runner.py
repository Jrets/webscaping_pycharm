from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from goodsparser import settings
from goodsparser.spiders.leroymerlinru import LeroymerlinruSpider

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinruSpider, search_name="Сплит-система")

    process.start()

import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from goodsparser.items import GoodsparserItem


class LeroymerlinruSpider(scrapy.Spider):
    name = "leroymerlinru"
    allowed_domains = ["leroymerlin.ru"]

    def __init__(self, search_name):
        super(LeroymerlinruSpider, self).__init__()
        self.start_urls = [f"https://leroymerlin.ru/search/?q={search_name}"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']"
                                   "/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        goods_links = response.xpath("//a[@data-qa='product-name']")
        for link in goods_links:
            yield response.follow(link, callback=self.goods_parse)

    def goods_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=GoodsparserItem(), response=response)
        loader.add_xpath("_id", "//span[@slot='article']/text()")
        loader.add_xpath("name", "//h1[@slot='title']/text()")
        loader.add_xpath("specs_name", "//dt/text()")
        loader.add_xpath("specs_value", "//dd/text()")
        loader.add_value("params", None)
        loader.add_xpath("price", "//span[@slot='price']/text()")
        loader.add_xpath("photos", "//img[@slot='thumbs']/@src")
        loader.add_value("link", response.url)
        yield loader.load_item()

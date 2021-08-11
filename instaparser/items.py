import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    parent_name = scrapy.Field()
    parent_id = scrapy.Field()
    user_id = scrapy.Field()
    type = scrapy.Field()
    name = scrapy.Field()
    photo = scrapy.Field()

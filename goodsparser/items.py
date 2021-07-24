# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def change_url(value):
    try:
        result = value.replace("_82", "_1200")
        return result
    except Exception:
        return value


def clear(value):
    try:
        result = value.replace("Арт. ", "").replace("\n", "").strip()
        return result
    except Exception:
        return value


def dead_space(value):
    try:
        result = value.strip()
        return result
    except Exception:
        return value


def get_int(value):
    try:
        result = int(value.replace(" ", ""))
        return result
    except Exception:
        return value


class GoodsparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor=MapCompose(clear),
                        output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(change_url))
    specs_name = scrapy.Field(input_processor=MapCompose(clear))
    specs_value = scrapy.Field(input_processor=MapCompose(clear))
    params = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field(
        input_processor=MapCompose(get_int),
        output_processor=TakeFirst()
    )
    _id = scrapy.Field(input_processor=MapCompose(clear), output_processor=TakeFirst())

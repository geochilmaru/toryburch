# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ToryburchItem(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    category_url = scrapy.Field()
    name = scrapy.Field()
    full_name = scrapy.Field()
    desc = scrapy.Field()
    url = scrapy.Field()
    img_url = scrapy.Field()
    alt_img_url = scrapy.Field()
    alt_img_desc = scrapy.Field()
    standard_price = scrapy.Field()
    sales_price = scrapy.Field()
    details = scrapy.Field()
    color = scrapy.Field()
    created = scrapy.Field()
    last_upd = scrapy.Field()

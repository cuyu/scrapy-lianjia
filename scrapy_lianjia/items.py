# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    price = scrapy.Field()
    room = scrapy.Field()
    area = scrapy.Field()
    url = scrapy.Field()

    price_per_area = scrapy.Field()
    floor_number = scrapy.Field()
    year = scrapy.Field()
    decoration = scrapy.Field()
    direction = scrapy.Field()
    first_pay = scrapy.Field()
    month_pay = scrapy.Field()
    community = scrapy.Field()
    district = scrapy.Field()
    address = scrapy.Field()

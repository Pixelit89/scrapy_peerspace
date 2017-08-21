# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PeerspaceItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    name = scrapy.Field()
    location = scrapy.Field()
    price = scrapy.Field()
    saves = scrapy.Field()
    about_the_space = scrapy.Field()
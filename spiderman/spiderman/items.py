# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpidermanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Movie(scrapy.Item):
    """电影信息"""
    name = scrapy.Field()
    desc = scrapy.Field()
    image = scrapy.Field()
    link = scrapy.Field()
    ctime = scrapy.Field()
    utime = scrapy.Field()
    albumid = scrapy.Field()

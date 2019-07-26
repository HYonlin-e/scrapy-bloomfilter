# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyBloomfilterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class NewsItem(scrapy.Item):

    source_url = scrapy.Field()
    thumb = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    release_time = scrapy.Field()
    content = scrapy.Field()
    inner_imgs = scrapy.Field()



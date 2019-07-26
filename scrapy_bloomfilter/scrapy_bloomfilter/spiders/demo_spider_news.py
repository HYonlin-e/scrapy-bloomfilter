
from scrapy_bloomfilter.scrapy_bloomfilter.spiders.base_spider_news import baseSpider


class demoSpider(baseSpider):

    name = "demoSpider"
    allowed_domains = []
    start_urls = []


    def get_item_urls(self, response):
        return ''

    def get_thumbs(self, response):
        return ''

    def get_title(self, response):
        return ''

    def get_author(self, response):
        return ''

    def get_release_time(self, response):
        return ''

    def get_content(self, response):
        return ''

    def get_inner_lst(self, response, content=''):
        return ''
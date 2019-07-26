
from scrapy_bloomfilter.scrapy_bloomfilter.spiders.base_spider_news import baseSpider


class demoSpider(baseSpider):

    name = "demoSpider"
    allowed_domains = ['demo.com']
    start_urls = ['www.demo.com']


    def get_item_urls(self, response):
        imem_urls = []
        return imem_urls

    def get_thumbs(self, response):
        thumbs = []
        return thumbs

    def get_title(self, response):
        title = ''
        return title

    def get_author(self, response):
        author = ''
        return author

    def get_release_time(self, response):
        release_time = ''
        return release_time

    def get_content(self, response):
        content = ''
        return content

    def get_inner_lst(self, response, content=''):
        inner_lst = []
        return inner_lst
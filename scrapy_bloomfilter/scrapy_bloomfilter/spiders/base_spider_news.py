# coding=utf-8

from scrapy import Request, Spider
from scrapy.utils.project import get_project_settings
from dateutil import parser
from redis import Redis
import logging
import re

from scrapy_bloomfilter.scrapy_bloomfilter.items import NewsItem
from scrapy_redis_bloomfilter.bloomfilter import BloomFilter

logging.basicConfig(level=logging.NOTSET)


class baseSpider(Spider):

    settings = get_project_settings()
    name = None
    allowed_domains = None
    custom_settings = {}
    server = Redis.from_url(settings.get("REDIS_URL"))
    start_urls = None
    headers = {}

    def start_requests(self):
        '''
        一般爬虫入口是类似文章列表的页面
        配合start_urls使用，如果start_urls结构变动，这个函数也要重写，例如可以带上默认属性，然后通过meta传到parse处理。
        :return:
        '''
        for url in self.start_urls:
            yield Request(url, headers=self.headers, dont_filter=True, callback=self.parse)

    def parse(self, response):
        '''
        解析文章列表页面，拿出所有文章url，缩略图看情况而定。
        如果在文章列表页面中获取缩略图则重写get_thumbs()并处理。
        :param response:
        :return:
        '''
        item_urls = self.get_item_urls(response)
        thumbs = self.get_thumbs(response)

        for index, item_url in enumerate(item_urls):
            meta = {
                "thumb": thumbs[index],
            }
            # 在这里就调用bloomfilter做去重
            if not self.dul_url_bf(item_url):
                yield Request(item_url, meta=meta, callback=self.parse_art)

    def parse_art(self, response):
        '''
        解析文章页面，取出有用的信息，这里最终获得信息有：url、缩略图、标题、作者、发布时间、正文、正文图片列表
        :param response:
        :return:
        '''
        source_url = response.url

        # 缩略图
        if 'thumb' in response.meta.keys():
            thumb = response.meta["thumb"]
        else:
            thumb = self.get_thumb(response)
        title = self.get_title(response)
        author = self.get_author(response)
        release_time = self.date_format(self.get_release_time(response))
        content = self.remove_ads_iframe(self.get_content(response))
        # 文章图
        inner_lst = self.get_inner_lst(response, content)

        art_item = NewsItem()
        art_item["source_url"] = source_url
        art_item["thumb"] = thumb
        art_item["title"] = self.un_escape(title)
        art_item["author"] = self.un_escape(author)
        art_item["release_time"] = release_time
        art_item["content"] = self.un_escape(content)
        art_item["inner_imgs"] = inner_lst

        self.itemPrint(art_item)
        yield art_item

    def get_item_urls(self, response):
        return []

    def get_thumbs(self, response):
        '''
        get thumbs urls. 在parse跑, 取的是整个文章列表的所有缩略图组成一个List，配合itemurls使用。
        :param response:
        :return: [thumb_url]
        '''
        return []

    def get_thumb(self, response):
        '''
        在parse_art使用，如果传来的meta没有thumb这在这里进行获取缩略图。
        :param response:
        :return: thumb_url
        '''
        return ''

    def get_inner_lst(self, response, content=''):
        return []

    def get_title(self, response):
        return ''

    def get_author(self, response):
        return ''

    def get_release_time(self, response):
        return ''

    def get_content(self, response):
        return ''

    def date_format(self, date_string):
        '''
        格式化时间
        :param date_string:
        :return:
        '''
        deltatime = parser.parse(date_string)
        return deltatime.strftime("%Y-%m-%d %H:%M:%S")

    def remove_ads_iframe(self, html):
        """去广告和iframe和注释和img/@srcset"""
        return html

    def dul_url_bf(self, url):
        '''
        url去重，如果url已经存在返回True,反之把url写入bloomfilter,并返回False(bf组件的exist()存在的时候返回1, 不存在返回false)
        :param url:
        :return: 如果存在返回True,不存在返回False
        '''
        bf = BloomFilter(server=self.server, key=self.settings.get("REDIS_DUL_URL_KEY"), hash_number=self.settings.get("BLOOMFILTER_HASH_NUMBER_URL"),
                         bit=self.settings.get("BLOOMFILTER_BIT_URL"))
        if bf.exists(url):
            logging.debug(f'dupeurl:{url}')
            return True
        else:
            bf.insert(url)
            return False

    def itemPrint(item):
        '''
        打印item，用作日志，应该在传入pipeline前调用。打印除content以外的信息。
        :param item:spider解析网页生成的item对象
        :return:
        '''
        if isinstance(item, NewsItem):
            pdict = {}
            for key in item.keys():
                if key != "content":
                    pdict[key] = item[key]
            logging.info("打印NewsItem:")
            mstr = ''
            for i in pdict.items():
                mstr = mstr + str(i) + '\n'
            logging.info(mstr)
        return 0

    def un_escape(text):
        html = text.replace('&#8203;', '').replace('&nbsp;', ' ').replace('&gt;', '>'). \
            replace('&lt;', '<').replace('&quot;', '"'). \
            replace('&#x3D;', '=').replace('\xa0', ' ').replace("xa0", ""). \
            replace("\u200b", "").replace("u200b", ""). \
            replace("\u3000", " ").replace("&amp;", "&"). \
            replace("&#x27;", "'")
        # 去注释
        html = re.sub("<!--.*?-->", "", html)
        return html
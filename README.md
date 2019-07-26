# scrapy-bloomfilter

​       scrapy-bloomfilter是一个用bloomfilter（布隆过滤器）作为去重工具的轻量级scrapy项目，并提供了模板化的基类爬虫。



## 特点

- 使用bloomfilter（布隆过滤器）作为去重工具。
- 提供了模板化的基类爬虫，让爬虫开发只需专注页面解析，实现爬虫快速开发（目前可供选择的有新闻资讯类）。
- 轻量级，适用于每天少量更新的数据源。



## requirement.txt

```
scrapy=1.3.3
scrapy-redis-bloomfilter=0.7.0
redis=3.2.1
dateutil=2.4.1
```



## 说明

- 如何快速开发：

  ```
  # 以新闻资讯类爬虫为例，只需继承baseSpider并重写解析方法
  # demo_spider_news.py
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
  
  ```

  

- 为什么不直接用scrapy-redis-bloomfilter
  
- scrapy-redis-bloomfilter默认使用的是scrapy-redis的调度器，更注重的是分布式爬取，而且为了达到某些常见需求（如新闻资讯类爬虫，文章列表页面url不去重，文章页面url去重）必须以master-slave形式开发爬虫使得开发更繁杂。
  
- 为什么需要scrapy-redis-bloomfilter
  
  - 主要是用到其中的bloomfiler实现，避免重复造轮子。
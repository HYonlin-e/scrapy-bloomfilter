# scrapy-bloomfilter

​       scrapy-bloomfilter是一个用bloomfilter（布隆过滤器）作为去重工具的scrapy项目，并提供了模板化的基类爬虫。



## 特点

- 使用bloomfilter（布隆过滤器）作为去重工具。
- 提供了模板化的基类爬虫，让爬虫开发只需专注数据解析，实现爬虫快速开发（目前可供选择的有新闻资讯类）。



## requirement.txt

```
scrapy
scrapy-redis-bloomfilter
redis
dateutil
```



## 说明

- 为什么不直接用scrapy-redis-bloomfilter
  - scrapy-redis-bloomfilter默认使用的是scrapy-redis的调度器，更注重的是分布式爬取，而且为了达到某些常见需求（如新闻资讯类爬虫，文章列表页面url不去重，文章页面url去重）必须以master-slave形式开发爬虫使得开发更繁杂。

- 为什么需要scrapy-redis-bloomfilter
  - 主要是用到其中的bloomfiler实现，避免重复造轮子。
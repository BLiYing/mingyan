#!/usr/bin/python

from scrapy import cmdline
#定时执行任务
# cmdline.execute('scrapy crawlall'.split())
from scrapy import cmdline
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

import mingyan
'''
以下是多个爬虫顺序执行的命令
'''
configure_logging()
# 加入setting配置文件，否则配置无法生效
# get_project_settings()获取的是setting.py的配置
runner = CrawlerRunner(get_project_settings())

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(mingyan.spiders.spider_1.WeatherSpider)
    yield runner.crawl(mingyan.spiders.spider_2.WeatherSpider)
    yield runner.crawl(mingyan.spiders.spider_3.WeatherSpider)
    yield runner.crawl(mingyan.spiders.spider_4.WeatherSpider)
    yield runner.crawl(mingyan.spiders.spider_5.WeatherSpider)
    yield runner.crawl(mingyan.spiders.spider_6.WeatherSpider)
    yield runner.crawl(mingyan.spiders.spider_7.WeatherSpider)
    yield runner.crawl(mingyan.spiders.spider_8.WeatherSpider)
    yield runner.crawl(mingyan.spiders.spider_9.WeatherSpider)
    yield runner.crawl(mingyan.spiders.spider_10.WeatherSpider)
    yield runner.crawl(mingyan.spiders.spider_11.WeatherSpider)
    yield runner.crawl(mingyan.spiders.spider_12.WeatherSpider)
    yield runner.crawl(mingyan.spiders.spider_13.WeatherSpider)
    yield runner.crawl(mingyan.spiders.spider_14.WeatherSpider)
    yield runner.crawl(mingyan.spiders.spider_15.WeatherSpider)
    reactor.stop()


crawl()
reactor.run()  # the script will block here until the last crawl call is finished
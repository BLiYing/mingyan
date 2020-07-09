#!/usr/bin/python

from scrapy import cmdline
#定时执行任务
cmdline.execute('scrapy crawl beike_1'.split())
cmdline.execute('scrapy crawl beike_2'.split())
cmdline.execute('scrapy crawl beike_3'.split())
cmdline.execute('scrapy crawl beike_4'.split())
cmdline.execute('scrapy crawl beike_5'.split())
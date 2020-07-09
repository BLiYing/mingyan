#!/usr/bin/python

from scrapy import cmdline
#定时执行任务
cmdline.execute('scrapy crawlall'.split())

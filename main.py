#!/usr/bin/python

from scrapy import cmdline

cmdline.execute('scrapy crawl beike'.split())
# cmdline.execute('scrapy crawl beike_b'.split())
# cmdline.execute('scrapy crawl beike_c'.split())

# cmdline.execute('scrapy crawl getip_spider'.split())
# cmdline.execute('scrapy crawl beike -o ./beike.json'.split())
# cmdline.execute('scrapy crawlall'.split())

#
# scrapy crawl beike -o ./beike.json -s JOBDIR=crawls/001 dont_filter=True
# cmdline.execute('scrapy crawl beike -s JOBDIR=crawls/001'.split())
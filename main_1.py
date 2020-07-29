#!/usr/bin/python

from scrapy import cmdline

# cmdline.execute('scrapy crawl beike_1 -o ./beike.json'.split())
# cmdline.execute('scrapy crawl beike_b'.split())
# cmdline.execute('scrapy crawl beike_all_area_of_wuhan'.split())




cmdline.execute('scrapy crawl beike_all_area_of_chengjiao_by_city'.split())
# cmdline.execute('scrapy crawl beike_all_area_of_chengjiao_by_city_2'.split())

# cmdline.execute('scrapy crawl getip_spider'.split())
# cmdline.execute('scrapy crawl beike -o ./beike.json'.split())
# cmdline.execute('scrapy crawlall'.split())

#
# scrapy crawl beike -o ./beike.json -s JOBDIR=crawls/001 dont_filter=True
# cmdline.execute('scrapy crawl beike -s JOBDIR=crawls/001'.split())
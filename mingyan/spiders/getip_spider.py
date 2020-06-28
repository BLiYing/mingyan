import time

import scrapy


class WeatherSpider(scrapy.Spider):
    # https://sz.ke.com/chengjiao/nanshanqu/pg2/
    # name = "getip_spider"

    # 允许访问的域名
    allowed_domains = ['icanhazip.com']
    # 起始爬取的url
    start_urls = ['http://icanhazip.com/']

    def start_requests(self):

        for i in range(1, 1):
            url = self.start_urls[0]
            time.sleep(2)
            yield scrapy.Request(url=url)


    def parse(self, response):
        if response is None:
            return
        print('--------------------------------')
        print('--------------------------------')
        print('--------------------------------')
        print('--------------------------------')
        print('--------------------------------代理后的ip: ', response.text)

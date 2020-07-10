import scrapy

# 打开数据库连接
# from test import time_mk
from mingyan.util.minyanitem import getMinyanItem

city_name = '上海'
start_page = 1
end_page = 8


class WeatherSpider(scrapy.Spider):
    name = "beike_2"
    allowed_domains = ["sh.ke.com"]
    start_urls = ['https://sh.ke.com']

    def start_requests(self):
        # 武汉二手房：https://wh.ke.com/chengjiao/pg2/
        url = self.start_urls[0] + "/chengjiao/"
        yield scrapy.Request(url=url, callback=self.parse_a)

    def parse_a(self, response):
        select_area_href_list_first = response.xpath(
            '//*[@data-role="ershoufang"]/div[1]/a[@class=" CLICKDATA"]/@href').extract()

        for area_i in select_area_href_list_first:
            url = self.start_urls[0] + area_i + "pg1"
            yield scrapy.Request(url=url, callback=self.parse_b, dont_filter=True)

    def parse_b(self, response):
        select_area_list = response.xpath(
            '//*[@data-role="ershoufang"]/div[1]/a[@class="selected CLICKDATA"]/@href').extract()
        if isinstance(select_area_list, list) and len(select_area_list) == 1:
            areaname = select_area_list[0]
            for i in range(start_page, end_page):
                url = self.start_urls[0] + areaname + "pg" + str(i) + '/'
                print("请求url:" + url)
                yield scrapy.Request(url=url, callback=self.parse_first, dont_filter=True)

    def parse_first(self, response):
        select_area_list = response.xpath(
            '//*[@data-role="ershoufang"]/div[1]/a[@class="selected CLICKDATA"]/text()').extract()
        if isinstance(select_area_list, list) and len(select_area_list) == 1:
            area = select_area_list[0]
            # area = area.replace(' ', '').replace('\n', '')

            common_str = '//*[@data-component="list"]/ul/li/div[@class="info"]'
            ListTitle = response.xpath(
                common_str + '/div[@class="title"]/a/text()').extract()
            ListMaidian = response.xpath(
                common_str + '/div[@class="title"]/a/@href').extract()
            ListdealDate = response.xpath(
                common_str + '/div[@class="address"]/div[@class="dealDate"]/text()').extract()
            ListtotalPrice = response.xpath(
                common_str + '/div[@class="address"]/div[@class="totalPrice"]/span/text()').extract()
            ListUnitPrice = response.xpath(
                common_str + '/div[@class="flood"]/div[@class="unitPrice"]/span/text()').extract()

            ListHouseAge = response.xpath(
                common_str + '/div[@class="flood"]/div[1]/text()').extract()

            ListGuapai_price = response.xpath(
                common_str + '/div[@class="dealCycleeInfo"]/span[@class="dealCycleTxt"][1]/span[1]/text()').extract()

            Listdealcycle_date = response.xpath(
                common_str + '/div[@class="dealCycleeInfo"]/span[@class="dealCycleTxt"][1]/span[2]/text()').extract()

            size = len(ListTitle)
            size_house_age = len(ListHouseAge)
            flag = size_house_age == size * 2

            for i in range(size):
                item = getMinyanItem(i, ListMaidian, ListTitle, ListdealDate, ListtotalPrice, ListUnitPrice,
                                     ListGuapai_price,
                                     Listdealcycle_date, ListHouseAge, flag, area, city_name)

                yield item

import time
import traceback
from decimal import Decimal

import scrapy

from mingyan.items import MingyanItem

# 打开数据库连接
# from test import time_mk
from mingyan.util.minyanitem import getMinyanItem

city_name = '上海'
# tiaojian = ''
p_list = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7']
a_list = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7']
y_list = ['y4', 'y5']


class WeatherSpider(scrapy.Spider):
    # https://sz.ke.com/chengjiao/nanshanqu/pg2/
    name = "beike_all_area_of_chengjiao_by_city"
    allowed_domains = ["sh.ke.com"]
    start_urls = ['https://sh.ke.com']

    def start_requests(self):
        # 武汉二手房：https://wh.ke.com/chengjiao/pg2/
        url = self.start_urls[0] + "/chengjiao/"
        yield scrapy.Request(url=url, callback=self.parse_a)

    def parse_a(self, response):
        select_area_href_list_first = response.xpath(
            '//*[@data-role="ershoufang"]/div[1]/a[@class=" CLICKDATA"]/@href').extract()

        for j in range(len(select_area_href_list_first) - 1, -1, -1):
            area_i = select_area_href_list_first[j]
            if str(area_i).__contains__('pudong'):
                for p_index in range(0, len(p_list)):
                    for a_index in range(0, len(a_list)):
                        for y_index in range(0, len(y_list)):
                            tiaojian = p_list[p_index] + a_list[a_index] + y_list[y_index]
                            url = self.start_urls[0] + area_i + "pg1" + tiaojian
                            # print(url)
                            yield scrapy.Request(url=url, callback=self.parse_b, meta={'tiaojian': tiaojian})

    def parse_b(self, response):
        # tiaojian = response.meta['tiaojian']
        total_num = response.xpath(
            '//*[@data-component="listOverview"]/div[@class="resultDes clear"]/div[@class="total fl"]/span/text()').extract()
        if len(total_num) > 0:
            total_num = total_num[0].replace(' ', '').replace('\n', '')
            select_area_list = response.xpath(
                '//*[@data-role="ershoufang"]/div[1]/a[@class="selected CLICKDATA"]/@href').extract()
            areaname = select_area_list[0]
            # areaname = areaname.replace(' ', '').replace('\n', '')
            if int(total_num) > 0:
                num_avg = int(int(total_num)/30)
                total_page = num_avg + 2
                if total_page > 101:
                    total_page = 101
                for i in range(total_page - 1, -1, -1):
                    url = self.start_urls[0] + areaname + "pg" + str(i)
                    print("请求url:" + url)
                    # time.sleep(0.5)
                    yield scrapy.Request(url=url, callback=self.parse_first)


    def parse_first(self, response):

        select_area_list = response.xpath(
            '//*[@data-role="ershoufang"]/div[1]/a[@class="selected CLICKDATA"]/text()').extract()
        if  isinstance(select_area_list, list) and len(select_area_list) == 1:
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




def getId(a):
    if a:
        end_index = a.find('.html')
        start_index = a.find('chengjiao') + len('chengjiao/')
        if end_index > start_index:
            b = str(a)[start_index: end_index]
            return b
        else:
            return a
    else:
        return a


def getXiaquName(community_name):
    if community_name:
        end_index = community_name.find(' ')
        xiaoqu_name = community_name[0:end_index]
        return xiaoqu_name
    else:
        return ''


def getAge(a):
    # a = ' 高楼层(共9层) 1998年建板楼 '
    a = a.replace(' ', '').replace('\n', '')
    start_index = a.find(')')
    if start_index > 0:
        end_index = start_index + 5
        b = str(a)[start_index + 1:end_index]
        return b
    else:
        return ''


def time_mk(time):
    if str(time).__contains__('.'):
        a = str(time).replace('.', '-')
        return a

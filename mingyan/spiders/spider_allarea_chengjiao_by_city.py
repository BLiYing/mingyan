import time
from decimal import Decimal

import scrapy

from mingyan.items import MingyanItem

# 打开数据库连接
# from test import time_mk

city_name = '北京'
tiaojian = '/'
end_page = 50


class WeatherSpider(scrapy.Spider):
    # https://sz.ke.com/chengjiao/nanshanqu/pg2/
    name = "beike_all_area_of_chengjiao_by_city"
    allowed_domains = ["bj.ke.com"]
    start_urls = ['https://bj.ke.com']

    def start_requests(self):
        # 武汉二手房：https://wh.ke.com/chengjiao/pg2/
        url = self.start_urls[0] + "/chengjiao/"
        yield scrapy.Request(url=url, callback=self.parse_a)

    def parse_a(self, response):
        select_area_href_list_first = response.xpath(
            '//*[@data-role="ershoufang"]/div[1]/a[@class=" CLICKDATA"]/@href').extract()
        for j in range(len(select_area_href_list_first)):
            # 武汉二手房：https://wh.ke.com/chengjiao/pg2/
            for i in range(1, end_page):
                url = self.start_urls[0] + select_area_href_list_first[j] + "pg" + str(i) + tiaojian
                print("请求url:" + url)
                yield scrapy.Request(url=url, callback=self.parse_first)

    def parse_first(self, response):

        select_area_list = response.xpath(
            '//*[@data-role="ershoufang"]/div[1]/a[@class="selected CLICKDATA"]/text()').extract()
        if  isinstance(select_area_list, list) and len(select_area_list) == 1:
            area = select_area_list[0]
            area = area.replace(' ', '').replace('\n', '')

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
                item = MingyanItem()
                href_str = ListMaidian[i]
                new_str = getId(href_str)
                item['maidian_id'] = new_str
                community_name = ListTitle[i]
                item['community_name'] = community_name
                chengjiao_dealDate_str = str(ListdealDate[i]).replace(' ', '').replace('\n', '').replace('\r', '')
                item['chengjiao_dealDate'] = time_mk(chengjiao_dealDate_str)
                item['chengjiao_totalPrice'] = ListtotalPrice[i]
                item['chengjiao_unitPrice'] = ListUnitPrice[i]
                item['xiaoqu_name'] = getXiaquName(community_name)

                guapai_price_str = ListGuapai_price[i]
                item['guapai_price'] = str(guapai_price_str).replace('挂牌', '').replace('万', '').replace(' ', '')
                dealcycle_date_str = Listdealcycle_date[i]
                item['dealcycle_date'] = str(dealcycle_date_str).replace('成交周期', '').replace('天', '').replace(' ', '')
                item['kanjia_price'] = Decimal(item['guapai_price']) - Decimal(item['chengjiao_totalPrice'])
                item['area'] = area
                if flag:
                    house_age = getAge(ListHouseAge[2 * i + 1])
                else:
                    house_age = ''

                item['house_age'] = house_age
                item['city_name'] = city_name

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

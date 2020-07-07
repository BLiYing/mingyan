import traceback
from decimal import Decimal

import scrapy

from mingyan.items import MingyanItem
# 打开数据库连接
#from test import time_mk
from mingyan.util.minyanitem import getMinyanItem

city_name = '武汉'
# area = 'wuchang'
#根据面积查找 hanyang/a3a4a5a6a7/ https://wh.ke.com/chengjiao/qingshan/
tiaojian = ''
start_page = 1
end_page = 16



class WeatherSpider(scrapy.Spider):
    # https://sz.ke.com/chengjiao/nanshanqu/pg2/
    # name = "beike"
    allowed_domains = ["wh.ke.com"]
    start_urls = ['https://wh.ke.com/']

    def start_requests(self):
        arealist = ['jiangan', 'jianghan', 'qiaokou', 'dongxihu', 'wuchang', 'qingshan', 'hongshan', 'donghugaoxin',
                    'jiangxia', 'caidian', 'huangbei', 'xinzhou', 'zhuankoukaifaqu', 'hannan']
        arealist = ['dongxihu', 'jiangxia', 'caidian', 'huangbei', 'xinzhou', 'zhuankoukaifaqu', 'hannan']
        for area in arealist:
            for i in range(start_page, end_page):
                #
                # 江岸区：成交100-200万，5年以内
                # url = self.start_urls[0] + "chengjiao/jiangan" + "/" + "pg" + str(i) + "y1p3p4/"

                # 江岸区：上海公馆：https://wh.ke.com/chengjiao/pg2c3711063250928/?sug=光明上海公馆
                # url = self.start_urls[0] + "chengjiao/jiangan" + "/" + "pg" + str(i) + "c3711063250928/?sug=光明上海公馆"

                # 江岸区：福星华府成交：https://wh.ke.com/chengjiao/pg2c3711064071099/?sug=福星华府
                # url = self.start_urls[0] + "chengjiao/jianghan" + "/" + "pg" + str(i) + "c3711064071099/?sug=福星华府"

                # 江岸区：长投海德公园：https://wh.ke.com/chengjiao/c3711063612721/?sug=长投海德公园
                # url = self.start_urls[0] + "chengjiao" + "/" + "pg" + str(i) + "c3711063612721/?sug=长投海德公园"

                # https://wh.ke.com/chengjiao/c3711057322313/?sug=星悦城一期
                # url = self.start_urls[0] + "chengjiao" + "/" + "pg" + str(i) + "c3711057322313/?sug=星悦城一期"

                # https://wh.ke.com/chengjiao/c3714076423997585/?sug=星悦城二期
                # url = self.start_urls[0] + "chengjiao" + "/" + "pg" + str(i) + "c3714076423997585/?sug=星悦城二期"

                # https://wh.ke.com/chengjiao/c3711063789400/?sug=星悦城三期
                # url = self.start_urls[0] + "chengjiao" + "/" + "pg" + str(i) + "c3711063789400/?sug=星悦城三期"

                # https://wh.ke.com/chengjiao/c378689980026048/?sug=星悦城华廷
                # url = self.start_urls[0] + "chengjiao" + "/" + "pg" + str(i) + "c378689980026048/?sug=星悦城华廷"

                # https://wh.ke.com/chengjiao/c3711062885724/?sug=越秀星汇君泊
                # url = self.start_urls[0] + "chengjiao" + "/" + "pg" + str(i) + "c3711062885724/?sug=越秀星汇君泊"

                # https://wh.ke.com/chengjiao/c3711767884819691/?sug=越秀星汇君泊越天地
                # url = self.start_urls[0] + "chengjiao" + "/" + "pg" + str(i) + "c3711767884819691/?sug=越秀星汇君泊越天地"

                # https://wh.ke.com/chengjiao/c3711099434403/?sug=绿地汉口中心
                # url = self.start_urls[0] + "chengjiao" + "/" + "pg" + str(i) + "c3711099434403/?sug=绿地汉口中心"

                # https://wh.ke.com/ershoufang/jiangan/su1y1dp1a2a3p3p4/
                # url = self.start_urls[0] + "ershoufang/jiangan" + "/" + "pg" + str(i) + "y1p3p4/"

                # https://wh.ke.com/chengjiao/sq6512/?sug=武汉天地
                # url = self.start_urls[0] + "chengjiao" + "/" + "pg" + str(i) + "sq6512/?sug=武汉天地"

                # https://wh.ke.com/chengjiao/c3711056417888/?sug=保利中央公馆
                # url = self.start_urls[0] + "chengjiao" + "/" + "pg" + str(i) + "c3711056417888/?sug=保利中央公馆"

                # https://wh.ke.com/chengjiao/rs大华南湖公园世家三期/
                # url = self.start_urls[0] + "chengjiao" + "/" + "pg" + str(i) + "rs大华南湖公园世家三期"

                # https://wh.ke.com/chengjiao/c3711057035959/?sug=统建同安家园
                # url = self.start_urls[0] + "chengjiao" + "/" + "pg" + str(i) + "c3711057035959/?sug=统建同安家园"

                # https://wh.ke.com/chengjiao/c3711062828435/?sug=金地自在城
                # url = self.start_urls[0] + "chengjiao" + "/" + "pg" + str(i) + "c3711062828435/?sug=金地自在城"


                # 武汉二手房：https://wh.ke.com/chengjiao/pg2/

                url = self.start_urls[0] + "chengjiao/" + area + "/" + "pg" + str(i) + tiaojian
                print("请求url:" + url)
                yield scrapy.Request(url=url, dont_filter=True)

    def parse(self, response):
        if response is None:
            return
        select_area_list = response.xpath('//*[@data-role="ershoufang"]/div[1]/a[@class="selected CLICKDATA"]/text()').extract()
        if select_area_list is not None and isinstance(select_area_list, list) and len(select_area_list) == 1:
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

            # SQL 插入语句
            # sql = ' INSERT IGNORE INTO beike_inner_5years_100_200 (id,community_name,chengjiao_dealDate,chengjiao_totalPrice,chengjiao_unitPrice) VALUES '
            # sql = ' INSERT IGNORE INTO beike_ja_shgg (id,community_name,chengjiao_dealDate,chengjiao_totalPrice,chengjiao_unitPrice, xiaoqu_name, guapai_price, dealcycle_date, kanjia_price) VALUES '
            # sql = ' INSERT IGNORE INTO beike_sz_nanshanqu (id, community_name, chengjiao_dealDate, chengjiao_totalPrice, chengjiao_unitPrice) VALUES '
            size = len(ListTitle)
            size_house_age = len(ListHouseAge)
            flag = size_house_age == size * 2

            for i in range(size):
                item = getMinyanItem(i, ListMaidian, ListTitle, ListdealDate, ListtotalPrice, ListUnitPrice, ListGuapai_price,
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

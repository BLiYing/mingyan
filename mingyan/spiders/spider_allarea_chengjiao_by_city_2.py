import scrapy

# 打开数据库连接
# from test import time_mk
from mingyan.util.minyanitem import getMinyanItem

city_name = '苏州'
p_list = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8']
a_list = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7']
y_list = ['y4', 'y5']
# lc_list = ['lc1', 'lc2', 'lc3', 'lc4', 'lc5']
proxy_ip = ''


class WeatherSpider(scrapy.Spider):
    # https://sz.ke.com/chengjiao/nanshanqu/pg2/
    name = "beike_all_area_of_chengjiao_by_city_2"
    allowed_domains = ["su.ke.com"]
    start_urls = ['https://su.ke.com']

    def start_requests(self):
        # 武汉二手房：https://wh.ke.com/chengjiao/pg2/
        url = self.start_urls[0] + "/chengjiao/"
        yield scrapy.Request(url=url, callback=self.parse_a, meta={'proxy': proxy_ip})

    def parse_a(self, response):
        select_area_href_list_first = response.xpath(
            '//*[@data-role="ershoufang"]/div[1]/a[@class=" CLICKDATA"]/@href').extract()

        for j in range(len(select_area_href_list_first) - 1, -1, -1):
            area_i = select_area_href_list_first[j]
            # if str(area_i).__contains__('chaoyang'):

            for p_index in range(0, len(p_list)):
                for a_index in range(0, len(a_list)):
                    for y_index in range(0, len(y_list)):
                        # for lc_index in range(0, len(lc_list)):
                            tiaojian = p_list[p_index] + a_list[a_index] + y_list[y_index] #+ lc_list[lc_index]
                            url = self.start_urls[0] + area_i + "pg1" + tiaojian + '/'
                            # print(url)
                            yield scrapy.Request(url=url, callback=self.parse_b,
                                                 meta={'tiaojian': tiaojian, 'proxy': proxy_ip}, dont_filter=True)

    def parse_b(self, response):
        total_num = response.xpath(
            '//*[@data-component="listOverview"]/div[@class="resultDes clear"]/div[@class="total fl"]/span/text()').extract()
        if len(total_num) > 0:
            total_num = total_num[0].replace(' ', '').replace('\n', '')
            select_area_list = response.xpath(
                '//*[@data-role="ershoufang"]/div[1]/a[@class="selected CLICKDATA"]/@href').extract()
            areaname = select_area_list[0]
            # areaname = areaname.replace(' ', '').replace('\n', '')
            if int(total_num) > 0:
                num_avg = int(int(total_num) / 30)
                total_page = num_avg + 2
                if total_page > 101:
                    total_page = 101
                for i in range(total_page - 1, -1, -1):
                    url = self.start_urls[0] + areaname + "pg" + str(i) + '/'
                    print("请求url:" + url)
                    # time.sleep(0.5)
                    yield scrapy.Request(url=url, callback=self.parse_first, meta={'proxy': proxy_ip}, dont_filter=True)


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

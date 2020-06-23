# coding=utf-8
import time

import requests
from scrapy.selector import Selector
import pymysql
import json
import urllib
from urllib import request
from urllib import parse

conn = pymysql.connect(host="127.0.0.1", user="root", passwd="root", db="beike", charset="utf8")
cursor = conn.cursor()


def crawl_ips():
    # headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
    # for i in range(1568):
    #     re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)
    #
    #     selector = Selector(text=re.text)
    #     all_trs = selector.css("#ip_list tr")
    #
    #
    #     ip_list = []
    #     for tr in all_trs[1:]:
    #         speed_str = tr.css(".bar::attr(title)").extract()[0]
    #         if speed_str:
    #             speed = float(speed_str.split("秒")[0])
    #         all_texts = tr.css("td::text").extract()
    #
    #         ip = all_texts[0]
    #         port = all_texts[1]
    #         proxy_type = all_texts[5]
    #
    #         ip_list.append((ip, port, proxy_type, speed))
    #
    #     for ip_info in ip_list:
    #         cursor.execute(
    #             "insert proxy(ip, port, speed, proxy_type) VALUES('{0}', '{1}', {2}, 'HTTP')".format(
    #                 ip_info[0], ip_info[1], ip_info[3]
    #             )
    #         )
    #
    #         conn.commit()
    get_ip()


def get_ip():
    # coding:utf-8
    url = "https://ip.jiangxianli.com/api/proxy_ips"
    for i in range(1, 10):
        data = {"page": i, "country": "中国"}  #
        # 使用urlencode这个方法将字典序列化成字符串，最后和基础网址进行拼接
        data_string = parse.urlencode(data)
        # req = request.Request(url, headers=headers, data=data)  # POST方法
        # req = request.Request(url+params) # GET方法
        print('--------------------------------------------------------------------------------')
        print('data_string:' + data_string)
        new_url = url + "?" + data_string
        print('new_url:' + new_url)

        page = request.urlopen(new_url).read()
        page = page.decode('utf-8')
        if page is not None:

            ip_bean = json.loads(page)
            # print(page)
            # print('------------')
            # print(type(ip_bean))
            # print(ip_bean)

            # print(len(ip_bean['data']['data']))
            # print(ip_bean['data']['data'][0])
            # print(ip_bean['data']['data'][0]['unique_id'])

            size = len(ip_bean['data']['data'])
            ip_list = []
            for i in range(size):

                ip = ip_bean['data']['data'][i]['ip']
                print(ip)
                port = ip_bean['data']['data'][i]['port']
                print(port)

                proxy_type = ip_bean['data']['data'][i]['protocol']
                print(proxy_type)
                speed = ip_bean['data']['data'][i]['speed']
                print(speed)
                unique_id = ip_bean['data']['data'][i]['unique_id']
                print(unique_id)

                ip_list.append((ip, port, proxy_type, speed,unique_id))

                for ip_info in ip_list:
                    cursor.execute("insert ignore proxy(ip, port, proxy_type, speed,unique_id) VALUES('{0}', {1}, '{2}', '{3}','{4}')".format(
                        ip_info[0], ip_info[1], ip_info[2], ip_info[3], ip_info[4])
                    )
                    conn.commit()
        time.sleep(2)


class GetIP(object):
    def delete_ip(self, ip):
        # 从数据库中删除无效的ip
        delete_sql = """
            delete from proxy where ip='{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        # 判断ip是否可用
        http_url = "https://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http": proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict)

        except Exception as e:
            print("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            # select_area_list_index = response.text.find('class=" CLICKDATA"')
            if code >= 200 and code < 300:
                print("effective ip")
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # 从数据库中随机获取一个可用的ip
        random_sql = """ SELECT ip, port FROM proxy WHERE speed < 1000 ORDER BY RAND() LIMIT 1 """
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()


if __name__ == "__main__":
    crawl_ips()
    get_ip = GetIP()
    print(get_ip.get_random_ip())

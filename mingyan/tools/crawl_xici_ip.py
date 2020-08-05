# coding=utf-8
import hashlib
import json
import sys
import time
from urllib import parse
from urllib import request

import pymysql
import requests
import urllib3
from scrapy.utils.project import get_project_settings

from mingyan.tools import mytoken

# 登录后在个人中心获取
spiderId = "2cabc4793e3a4cccab931bcadea3f865"
secret = "fabcdc93e54d411da3579ddd84281819"
time_unit = 10 * 60

# 获取setting文件中的配置
settings = get_project_settings()
conn = pymysql.connect(host=settings.get('MYSQL_HOST'), port=settings.get('MYSQL_PORT'),
                       user=settings.get('MYSQL_USER'), passwd=settings.get('MYSQL_PASSWORD'),
                       db=settings.get('MYSQL_DATABASE'), charset=settings.get('MYSQL_CHARSET'))
cursor = conn.cursor()


def crawl_ips():
    # get_ip()
    # apply_channels()
    get_ip_one()


# 申请拨号服务器
def apply_channels():
    params = {"count": 20}

    timestamp = mytoken.getTime()
    token = mytoken.gen_token(spiderId, secret, params, timestamp)
    apply_headers = mytoken.genHeaders(token, spiderId, timestamp)

    try:
        r = requests.get("http://api.xdaili.cn/xdaili-api/spider/applyChannels", headers=apply_headers, json=params,
                         timeout=120)
    except Exception as err_info:
        r = None
        print(err_info)

    if r is not None:
        print(r.status_code)
        if r.status_code == 200:
            # print(r.content)
            print(r.json())
            result = r.json()
            if result["ERRORCODE"] == "0" and result["RESULT"]:
                for one in result["RESULT"]:
                    # print(one)
                    # print(one["proxyId"])
                    # print(one["orderno"])
                    time_every = 0
                    while (time_every < time_unit):
                        getDynamicIP(one["orderno"], one["proxyId"])
                        time_every += 15
                        time.sleep(15)
            else:
                if result["ERRORCODE"] == "10076":
                    try:
                        timestamp = mytoken.getTime()
                        token = mytoken.gen_token(spiderId, secret, "", timestamp)
                        logoutall_headers = mytoken.genHeaders(token, spiderId, timestamp)
                        r = requests.get("http://api.xdaili.cn/xdaili-api/spider/logOutAll",
                                         headers=logoutall_headers, timeout=120)
                    except Exception as err_info:
                        r = None
                        print(err_info)

                    if r is not None:
                        # print(r.status_code)
                        if r.status_code == 200:
                            # print(r.content)
                            print(r.json())
                            apply_channels()


# """
# 动态拨号
# """
def getDynamicIP(orderno, proxyId):
    url = "http://api.xdaili.cn/xdaili-api/privateProxy/getDynamicIP" + "/" + orderno + "/" + proxyId + "?returnType=2"
    try:
        r = requests.get(url, timeout=120)
    except Exception as err_info:
        r = None
        print(err_info)

    if r is not None:
        print(r.status_code)
        if r.status_code == 200:
            print(r.content)
            print(r.json())
            result = r.json()
            if result["ERRORCODE"] == "0" and result["RESULT"]:
                ip = result["RESULT"]["wanIp"]
                port = result["RESULT"]["proxyport"]
                print("----ip" + ip)
                print("----port" + port)
                cursor.execute(
                    "insert ignore proxy(ip, port, proxy_type, speed,unique_id) VALUES('{0}', '{1}', '{2}', '{3}','{4}')".format(
                        ip, port, 'http', '0', proxyId)
                )
                conn.commit()


def get_ip():
    # coding:utf-8
    url = "https://ip.jiangxianli.com/api/proxy_ips"
    #https://ip.jiangxianli.com/?page=1&country=中国
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
                data_ = ip_bean['data']['data'][i]
                ip = data_['ip']
                print(ip)
                port = data_['port']
                print(port)

                proxy_type = data_['protocol']
                print(proxy_type)
                speed = data_['speed']
                print(speed)
                unique_id = data_['unique_id']
                print(unique_id)

                ip_list.append((ip, port, proxy_type, speed, unique_id))

                for ip_info in ip_list:

                    cursor.execute(
                        "insert ignore proxy(ip, port, proxy_type, speed,unique_id) VALUES('{0}', {1}, '{2}', '{3}','{4}')".format(
                            ip_info[0], ip_info[1], ip_info[2], ip_info[3], ip_info[4])
                    )
                    conn.commit()
        time.sleep(2)

def get_ip_one():
    while(True):
        new_url = "https://ip.jiangxianli.com/api/proxy_ip"
        page = request.urlopen(new_url).read()
        page = page.decode('utf-8')
        if page is not None:

            ip_bean = json.loads(page)

            ip_list = []
            data_ = ip_bean['data']
            ip = data_['ip']
            print(ip)
            port = data_['port']
            print(port)

            proxy_type = data_['protocol']
            print(proxy_type)
            speed = data_['speed']
            print(speed)
            unique_id = data_['unique_id']
            print(unique_id)

            ip_list.append((ip, port, proxy_type, speed, unique_id))

            for ip_info in ip_list:
                cursor.execute(
                    "insert ignore proxy(ip, port, proxy_type, speed,unique_id) VALUES('{0}', {1}, '{2}', '{3}','{4}')".format(
                        ip_info[0], ip_info[1], ip_info[2], ip_info[3], ip_info[4])
                )
                conn.commit()
        time.sleep(10)


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
        # http_url = "https://www.baidu.com"
        # http_url = "https://bj.ke.com/chengjiao"
        http_url = "http://icanhazip.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http": proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict, timeout=15)

        except Exception as e:
            print("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code

            if code >= 200 and code < 300:
                if len(response.content) < 100:
                    print(response.content)
                    print("============  " + str(response.text))
                print("effective ip,code=" + str(code))
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False

    def judge_ip_from_redis(self, http_str):
        # 判断ip是否可用
        # http_url = "https://www.baidu.com"
        # http_url = "https://bj.ke.com/"
        http_url = "http://icanhazip.com"
        proxy_url = http_str
        try:
            proxy_dict = {
                "http": proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict)

        except Exception as e:
            print("invalid ip and port")
            # self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print("effective ip,code=" + str(code))
                return True
            else:
                print("invalid ip and port")
                # self.delete_ip(ip)
                return False

    def get_random_ip_from_mysql(self):
        # 从数据库中随机获取一个可用的ip
        random_sql = """ SELECT ip, port FROM proxy where speed < 1000 ORDER BY RAND() LIMIT 1 """
        result = cursor.execute(random_sql)

        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip_from_mysql()

    def get_ip_from_xun(self):

        ip = "forward.xdaili.cn"
        port = "80"

        ip_port = ip + ":" + port

        # print(auth)
        proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
        return "http://" + ip_port

        # headers = {"Proxy-Authorization": self.get_auth(),
        #            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"}
        # r = requests.get("http://icanhazip.com/", headers=headers, proxies=proxy, verify=False,
        #                  allow_redirects=False)
        # r.encoding = 'utf8'
        # print(r.status_code)
        # if r.status_code == 200:
        #     print('-----------------------------代理ip:' + r.text)
        #     return "http://" + ip_port


        # if r.status_code == 302 or r.status_code == 301:
        #     loc = r.headers['Location']
        #     print(loc)
        #     r = requests.get(loc, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
        #     r.encoding = 'utf8'
        #     print(r.status_code)
        #     print(r.text)
        #     return r.text


    def get_auth(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        _version = sys.version_info

        is_python3 = (_version[0] == 3)

        orderno = "xxxx"

        timestamp = str(int(time.time()))
        string = ""
        string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp

        if is_python3:
            string = string.encode()

        md5_string = hashlib.md5(string).hexdigest()
        sign = md5_string.upper()
        # print(sign)
        auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
        return auth


if __name__ == "__main__":
    # crawl_ips()
    while(True):
        get_ip = GetIP()
        print(get_ip.get_random_ip_from_mysql())
        time.sleep(5)

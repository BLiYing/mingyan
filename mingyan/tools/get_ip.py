import json
import urllib
from urllib import request
from urllib import parse

def get_ip():
    # coding:utf-8

    url = "https://ip.jiangxianli.com/api/proxy_ips"
    data = {"page": "1", "country": "中国", "isp": "电信"}  # "order_by": "", "":"",
    # 使用urlencode这个方法将字典序列化成字符串，最后和基础网址进行拼接
    data_string = parse.urlencode(data)
    # req = request.Request(url, headers=headers, data=data)  # POST方法
    # req = request.Request(url+params) # GET方法

    print('data_string:' + data_string)
    new_url = url + "?" + data_string
    page = request.urlopen(new_url).read()
    page = page.decode('utf-8')
    ip_bean = json.loads(page)
    print(page)
    print('------------')
    print(type(ip_bean))
    print(ip_bean)

    print(len(ip_bean['data']['data']))
    print(ip_bean['data']['data'][0])
    print(ip_bean['data']['data'][0]['unique_id'])


if __name__ == "__main__":
    get_ip()

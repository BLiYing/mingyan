## mingyan
scrapy爬虫抓取数据，grafana分析数据

#### 结合Grafana分析数据
##### 均价走势图，可以看到房价高点在2018年，然后2019开始回落。（意味着什么？）
![image1](https://github.com/BLiYing/mingyan/blob/master/images/WX20200620-135303%402x.png)
##### 从曲线密集度可以看到成交还是比较频繁的。贝壳网武汉二手房成交数据共有56543条（截止2020-6-21），爬虫获取了共计56153条数据（缺少部分为前期部分维度筛选不全导致以及新成交的部分房源没有及时计入）。及时爬取的话需要发布到服务器，定时爬取指定页数。
![image2](https://github.com/BLiYing/mingyan/blob/master/images/WX20200620-135457@2x.png)
##### 此种图叫HeatMap图，可以分析一个区间内多层次的信息。从颜色可以看出成交频次，白色方块是最热，可以得知成交频次最高的时间段。（意味着什么？）
![image3](https://github.com/BLiYing/mingyan/blob/master/images/WX20200620-135536@2x.png)
![image3](https://github.com/BLiYing/mingyan/blob/master/images/WX20200620-141508@2x.png)

## 项目涉及scrapy的知识点：
#### 1.爬虫模拟浏览器行为
#### 2.多任务同时进行
#### 3.ip动态获取，入库及使用
#### 4.基本的xpath使用及setting.py中各参数含义（参考scrapy官网）
#### 5.Mysql数据库批量增删读写

![IMAGE](https://tva1.sinaimg.cn/large/007S8ZIlgy1ghgd1hhxa6j30u016fe53.jpg)

##### 互联网是信息的海洋。每次开始一个新的知识框架的学习时，你会发现百度上到处都有这个关键字的信息，怎么办？在多年自学的经验积累上谈谈自己的经验，也是一次回顾总结。

##### 任何IT方面的技术点都会有官方文档，它最详尽最权威，比如Android，Python，涛思时序数据库，高德地图，基于Python的scrapy框架等等。以[scrapy官方文档](https://docs.scrapy.org/en/latest/index.html)和[Android官方文档](https://developer.android.com/docs)为例：
![Scrapy文档](https://tva1.sinaimg.cn/large/007S8ZIlgy1ghgd1h1iz8j310o0u0am2.jpg)

![Android文档](https://tva1.sinaimg.cn/large/007S8ZIlgy1ghgd1gnnsoj31m80u047m.jpg)

##### 目录清晰，知识点也基本都能搜索，但同样，官方文档也是汪洋大海，如何快速上手呢？如果有官方demo，当然是跟着官方demo(示例代码)学习一遍。如果没有，此时百度相关demo就是最好的方法了。

##### 问题来了，百度来的都是碎片化怎么办。那就得从知名的IT社区和博客找，然后博文中说的不清楚的地方（比如原理，参数设置）就借助官方文档来查看释义。毕竟官方文档最权威，一般而言也最详尽。

#### 下面看下是如何”拼凑“我的爬虫demo。

##### 基本的Demo有了之后就需要开始深入解决问题了，首当其冲的就是由于爬取太快导致的ip暂时性无法访问（还好贝壳网的反爬虫机制没有一上来就给你上黑名单），如何和反爬虫斗智斗勇。我罗列一下自己循序渐进解决这个问题的过程。

#### 1.爬虫模拟浏览器行为
##### middlewares.py中获取setting.py中的USER_AGENT_LIST
```
    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        user_agent = random.choice(USER_AGENT_LIST)
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)
            # logging.info(f"User-Agent:{user_agent}")
        return None
```
#### 2.多任务同时进行
##### 模拟浏览器访问，可以一定程度解决IP封锁问题，但是我需要同时爬取多个城市的数据，一个爬虫进程已经不够了，自然想到如何实现多任务爬取。参考代码commands/crawlall.py：
```
from scrapy.commands import ScrapyCommand

class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def run(self, args, opts):
        spider_list = self.crawler_process.spiders.list()
        for name in spider_list:
            self.crawler_process.crawl(name, **opts.__dict__)
        self.crawler_process.start()
```
同时在setting.py中设置
```
# many task run on the same time
COMMANDS_MODULE = 'mingyan.commands'
```
#### 3.ip动态获取，入库及使用
##### 然而解决ip封锁的根本方式是使用动态ip,一开始是通过爬取网上免费的ip池，结果发现有效的ip少之又少，要么时效太短，要么根本无法使用。在mingyan/tools/crawl_xici_ip.py中的get_random_ip_from_mysql()方法是读取存入数据库中的免费共享ip，get_ip_from_xun()方法是自费购买的讯代理ip。花钱的肯定比免费的好用，使用哪家代理知乎上有推介。

##### 使用动态代理ip的话，必须开启中间件MingyanSpiderMiddleware，和MingyanDownloaderMiddleware中间件一样都在middlewares.py文件中，后面的数字是优先级。

```
# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'mingyan.middlewares.MingyanDownloaderMiddleware': 543,
    'mingyan.middlewares.MingyanSpiderMiddleware': 543,
}
```
在process_request中拦截ip:

```
class MingyanSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened,      signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # ip = random.choice(self.ip)
        get_ip = GetIP()
        # ip = get_ip.get_random_ip_from_mysql()
        ip = get_ip.get_ip_from_xun()

        logging.info("this is request ip:" + str(ip))
        auth = get_ip.get_auth()
        # encoded_user_pass = base64.encodestring(auth)
        request.headers['Proxy-Authorization'] = auth
        request.meta['proxy'] = ip
```

关于”中间件Middleware“概念，是理解Scrapy原理的重要一环，详情去[官网Spider Middleware](https://docs.scrapy.org/en/latest/topics/spider-middleware.html)了解吧。

#### 4.基本的xpath使用及setting.py中各参数含义（参考scrapy官网）
##### 待续
#### 5.Mysql数据库批量增删读写
##### 待续
##### -----------------------------------------------------
## 项目部署阿里云服务器，定时执行爬虫如何，分析并展示数据相关
#### 1.grafana；
#### 2.Linux相关：dnf和yum区分，进程查看，任务执行时间查看，端口占用等等
#### 3.如何部署centos
#### 4.如何定时执行爬虫（crontab）
#### 5.如何后台执行python爬虫（nohup）

#### 以上五点又相当于新知识点了，此时继续重复上面学习方式。（遇到问题如何利用百度和Google？）（举例）
##### 待续
#### 哪些知识点、难点、踩坑罗列下。

* 如何查看shell执行情况；
* 后台nohup命令执行中dev/null重定向是什么意思；
* ##### 待续

# mingyan
scrapy爬虫抓取数据，grafana分析数据

### 结合Grafana分析数据
#### 均价走势图，可以看到房价高点在2018年，然后2019开始回落。（意味着什么？）
![image1](https://github.com/BLiYing/mingyan/blob/master/images/WX20200620-135303%402x.png)
#### 从曲线密集度可以看到成交还是比较频繁的。贝壳网数据共有5万多二手成交房记录，爬虫数据获取了共计51228万条数据（部分非主城区的没有爬取）。
![image2](https://github.com/BLiYing/mingyan/blob/master/images/WX20200620-135457@2x.png)
#### 此种图叫HeatMap图，可以分析一个区间内多层次的信息。从颜色可以看出成交频次，白色方块是最热，可以得知成交频次最高的时间段。（意味着什么？）
![image3](https://github.com/BLiYing/mingyan/blob/master/images/WX20200620-135536@2x.png)


### 项目涉及scrapy的知识点：
#### 1.爬虫模拟浏览器行为
#### 2.多任务同时进行
#### 3.ip动态获取，入库及使用
#### 4.基本的xpath使用及setting.py中各参数含义（参考scrapy官网）
#### 5.Mysql数据库批量增删读写

详细教程创作中.....



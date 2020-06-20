# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MingyanItem(scrapy.Item):
    # define the fields for your item here like:

    community_name = scrapy.Field() # 小区名字
    xiaoqu_name = scrapy.Field() # 小区名字
    chengjiao_dealDate = scrapy.Field() # 成交日期
    chengjiao_unitPrice = scrapy.Field() # 成交单价
    chengjiao_totalPrice = scrapy.Field() # 成交总价
    maidian_id = scrapy.Field() # 埋点id,主键
    #guapai_price dealcycle_date kanjia_price
    guapai_price = scrapy.Field()
    dealcycle_date = scrapy.Field()
    kanjia_price = scrapy.Field()
    area = scrapy.Field() # 区域
    house_age = scrapy.Field() # 区域
    pass



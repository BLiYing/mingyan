import traceback
from decimal import Decimal

from mingyan.items import MingyanItem


def getMinyanItem(i, ListMaidian, ListTitle, ListdealDate, ListtotalPrice, ListUnitPrice, ListGuapai_price,
                  Listdealcycle_date, ListHouseAge, flag, area, city_name):
    item = MingyanItem()
    href_str = ListMaidian[i]
    new_str = getId(href_str)
    item['maidian_id'] = new_str
    community_name = ListTitle[i]
    item['community_name'] = community_name
    chengjiao_dealDate_str = str(ListdealDate[i]).replace(' ', '').replace('\n', '').replace('\r', '')
    item['chengjiao_dealDate'] = time_mk(chengjiao_dealDate_str)
    item['chengjiao_totalPrice'] = ListtotalPrice[i]
    item['xiaoqu_name'] = getXiaquName(community_name)
    item['area'] = area
    if flag:
        house_age = getAge(ListHouseAge[2 * i + 1])
    else:
        house_age = ''

    item['house_age'] = house_age
    item['city_name'] = city_name

    if is_number(str(item['chengjiao_totalPrice'])) :

        item['chengjiao_unitPrice'] = ListUnitPrice[i]

        guapai_price_str = ListGuapai_price[i]
        item['guapai_price'] = str(guapai_price_str).replace('挂牌', '').replace('万', '').replace(' ', '')
        if i < len(Listdealcycle_date):
            dealcycle_date_str = Listdealcycle_date[i]
        else:
            dealcycle_date_str = '成交周期0天'
        item['dealcycle_date'] = str(dealcycle_date_str).replace('成交周期', '').replace('天', '').replace(' ', '')
        if is_number(str(item['guapai_price'])):
            item['kanjia_price'] = Decimal(item['guapai_price']) - Decimal(item['chengjiao_totalPrice'])
        else:
            item['kanjia_price'] = 0

    else:
        item['chengjiao_unitPrice'] = 0
        item['guapai_price'] = 0
        item['dealcycle_date'] = 0
        item['kanjia_price'] = 0
    return item


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
        if str(time).count('.') == 1:
            a = a + "-01"
        return a

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


if __name__ == "__main__":
    a = time_mk('2020.01.05')
    print(a)
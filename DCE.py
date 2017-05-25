#!/usr/local/bin/python
#-*-coding:utf-8-*-
from bs4 import BeautifulSoup
#玉米   http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?jys=dce&pz=C&hy=C0&breed=C0&type=inner&start=2016-08-22&end=2017-05-22

import urllib
import re
from bs4 import BeautifulSoup
from database import database


hold_price = 0
hold_direct = 0
hold_number = 0
all_assets = 100000
days = 0
max_lost = 0
max_get = 0
lost_time = 0
get_time = 0
total_lost = 0
total_get = 0
charge_period = 19
database = database()

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def buy(price):
    global hold_direct
    global hold_number
    global hold_price
    global days
    days+=1
    if hold_direct == 1:
        return

    cover(price)
    hold_price = price
    hold_number = all_assets/hold_price
    hold_direct = 1
    # print 'buy', hold_number


def sell(price):
    global hold_direct
    global hold_number
    global hold_price
    global days
    days+=1
    if hold_direct == -1 or hold_direct==0:
        return
    global hold_price
    cover(price)
    hold_price = price
    hold_number = all_assets / hold_price
    hold_direct = -1
    # print 'sell',hold_number

def cover(price):
    global all_assets
    global days
    global max_lost
    global max_get
    global lost_time
    global get_time
    global total_lost
    global total_get
    dis = (price - hold_price)*hold_direct*hold_number
    precent = dis*100/all_assets
    if precent>max_get:
        max_get = precent
    if precent<max_lost:
        max_lost = precent

    all_assets += dis
    # print "get = " + str(dis),"current = "+str(price),"hold = " +str(hold_price),hold_direct,hold_number,"all = "+str(all_assets),"day ="+str(days)
    days = 1
    if dis>0:
        get_time+=1
        total_get+=dis
    else:
        lost_time+=1
        total_lost+=dis

def ma(x,list):
    return sum(list)/x

def charge(list1,i):
    for index,price in enumerate(list1):
        if(index>(i+3)):
            price = list1[index]
            lma = ma(i,list1[(index-i+1):(index+1)])
            refLma = ma(20,list1[(index-20):(index)])
            if price>lma:
                buy(price)
            elif price<lma :
                sell(price)
        else:
            pass


def getPage(html):
    soup = BeautifulSoup(html, 'html.parser')
    string = soup.find('td',class_='tdr',attrs={'height':'30'})
    result = re.findall(".*共(\d+)页.*",string.encode('utf-8'))
    return int(result[0])

def getPriceList(html):
    soup = BeautifulSoup(html, 'html.parser')
    priceList = []
    for dayPrice in soup.find_all('tr'):
        priceModel = [priceModel.string for priceModel in dayPrice.find_all('div')]
        if(len(priceModel) != 0):
            priceList.append(priceModel)
    return priceList

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

def getClose(database,db_name):
    database.connect()
    list = []
    for data in database.select("close",db_name):
        if type(data[0]) is tuple:
            print 'list'
        if int(data[0])==0:
            pass
        else:
            list.append(int(data[0]))
    return list

def coverResult():
    print  all_assets
    print "max_get =" + str(max_get)+"%"
    print "max_lost = " + str(max_lost)+"%"
    print "get_time =" + str(get_time)
    print "lost_time = " + str(lost_time)
    print "total_get =" + str(total_get)
    print "total_lost = " + str(total_lost)

def coverClear():
    global all_assets
    global days
    global max_lost
    global max_get
    global lost_time
    global get_time
    global total_lost
    global total_get
    global hold_direct
    global hold_number
    global hold_price
    global days
    all_assets = 100000
    days = 0
    max_lost = 0
    max_get = 0
    lost_time = 0
    get_time = 0
    total_lost = 0
    total_get = 0
    hold_price = 0
    hold_direct = 0
    days = 0

# shfe 上期所   dce 大商所   czce  郑商所    cffex 中金所
def getUrl(name,index=0):
    urlname = ''
    if name == '玉米':
        urlname = 'C'
    elif name == '棕榈':
        urlname = 'P'
    return "http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?page=" + str(index) + "&start=1990-08-22&end=2017-05-23&jys=dce&pz=" + urlname + "&type=inner"

def startCharge(db_name,i):
    database.connect()
    c_list = getClose(database,db_name)
    charge(c_list,i)
    coverResult()

def write(c_list):
    database.connect()
    for dayPrice in c_list:
        if (is_number(dayPrice[1])):
            print 'write'
            print dayPrice[0], dayPrice[1], dayPrice[2], dayPrice[3], dayPrice[4], dayPrice[5]
            database.write(dayPrice[0], dayPrice[1], dayPrice[2], dayPrice[3], dayPrice[4], dayPrice[5])
    database.conn.commit()

def spider():
    c_list = []
    count = getPage(getHtml(getUrl('棕榈')))
    for i in range(1, count + 1):
        C_url = getUrl('棕榈',i)
        priceList = getPriceList(getHtml(C_url))
        for priceDay in priceList:
            c_list.append(priceDay)
    return c_list

if __name__ == '__main__':
    database.connect()
    for i in range(3,50):
        print i
        startCharge('c_table',i)
        coverClear()
        print '---------------------------'



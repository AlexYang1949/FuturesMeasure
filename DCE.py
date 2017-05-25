#!/usr/local/bin/python
#-*-coding:utf-8-*-
from bs4 import BeautifulSoup
#玉米   http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?jys=dce&pz=C&hy=C0&breed=C0&type=inner&start=2016-08-22&end=2017-05-22

import urllib
import re
from bs4 import BeautifulSoup
from database import database
import matplotlib.pyplot as plt

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
asset_array = []

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def buy(price,date):
    global hold_direct
    global hold_number
    global hold_price
    global days
    days+=1
    if hold_direct == 1:
        return

    cover(price,date)
    hold_price = price
    hold_number = all_assets/hold_price
    hold_direct = 1
    # print 'buy', hold_number


def sell(price,date):
    global hold_direct
    global hold_number
    global hold_price
    global days
    days+=1
    if hold_direct == -1 or hold_direct==0:
        return
    global hold_price
    cover(price,date)
    hold_price = price
    hold_number = all_assets / hold_price
    hold_direct = -1
    # print 'sell',hold_number

def cover(price,date):
    global all_assets
    global days
    global max_lost
    global max_get
    global lost_time
    global get_time
    global total_lost
    global total_get
    global asset_array
    dis = (price - hold_price)*hold_direct*hold_number
    precent = dis*100/all_assets
    if precent>max_get:
        max_get = precent
    if precent<max_lost:
        max_lost = precent

    all_assets += dis
    asset_array.append((date,all_assets))
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

def charge(list,i):
    list1 =[data[1] for data in list]
    for index,price in enumerate(list1):
        if(index>100):
            price = list1[index]
            lma = ma(i,list1[(index-i+1):(index+1)])
            refLma = ma(i,list1[(index-i):(index)])
            date = list[index][0]
            if price>lma :#and refLma>lma:
                buy(price,date)
            elif price<lma :#and refLma<lma:
                sell(price,date)
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
    for data in database.select("date,close",db_name):
        if int(data[1])==0:
            pass
        else:
            list.append((str(data[0]),int(data[1])))
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
# 大商所  豆一 A   豆二 B     胶合板 BB    玉米 C    纤维板 FB
# 铁矿石 I     焦炭 J      鸡蛋 JD    焦煤 JM   塑料 L   豆粕 M
# PP PP     PVC V      豆油   Y   棕榈  P
def getUrl(name,index=1):
    urlname = ''
    if name == '玉米':
        urlname = 'C'
    elif name == '棕榈':
        urlname = 'P'
    elif name == '豆一':
        urlname = 'A'
    elif name == '豆二':
        urlname = 'B'
    elif name == '胶合板':
        urlname = 'BB'
    elif name == '纤维板':
        urlname = 'FB'
    elif name == '铁矿石':
        urlname = 'I'
    elif name == '焦炭':
        urlname = 'J'
    elif name == '鸡蛋':
        urlname = 'JD'
    elif name == '焦煤':
        urlname = 'JM'
    elif name == '塑料':
        urlname = 'L'
    elif name == '豆粕':
        urlname = 'M'
    elif name == 'PP':
        urlname = 'PP'
    elif name == 'PVC':
        urlname = 'V'
    elif name == '豆油':
        urlname = 'Y'
    return "http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?page=" + str(index) + "&breed="+urlname+"0&start=1990-08-22&end=2017-05-23&jys=dce&pz=" + urlname + "&hy="+urlname+"0&type=inner"

def startCharge(db_name,i):
    database.connect()
    c_list = getClose(database,db_name)
    charge(c_list,i)
    coverResult()

def write(c_list,tablename):
    database.connect()
    for dayPrice in c_list:
        if (is_number(dayPrice[1])):
            print 'write'
            print dayPrice[0], dayPrice[1], dayPrice[2], dayPrice[3], dayPrice[4], dayPrice[5]
            database.write(tablename,dayPrice[0], dayPrice[1], dayPrice[2], dayPrice[3], dayPrice[4], dayPrice[5])
    database.conn.commit()

def spider(name):
    c_list = []
    count = getPage(getHtml(getUrl(name)))
    for i in range(1, count + 1):
        print i
        C_url = getUrl(name,i)
        print C_url
        priceList = getPriceList(getHtml(C_url))
        for priceDay in priceList:
            c_list.append(priceDay)
    return c_list

if __name__ == '__main__':
    # c_list = spider('玉米')
    # write(c_list,'c_table')

    # for i in range(3,30):
    #     print i
    #     startCharge('c_table',i)
    #     coverClear()
    #     print '---------------------------'

    startCharge('p_table',25)
    print asset_array
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(range(len(asset_array)),[price[1] for price in asset_array])
    ax.set_xticklabels([3,123,1,23,123,1,23,1,23,1,231,23],rotation=-30)

    plt.show()


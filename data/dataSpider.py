#!/usr/local/bin/python
#-*-coding:utf-8-*-

from bs4 import BeautifulSoup
import re
import urllib
from data.dataProvider import DataProvider
from utils.utils import utils

class dataSpider():
    def __init__(self,name):
        self.name = name
        self.tablename = utils.getShort(self.name)+'_table'
        self.dataProvider = DataProvider(name)

    def start(self):
        c_list = self.spiderList()
        for dayPrice in c_list:
            if (utils.is_number(dayPrice[1])):
                self.dataProvider.writeData(dataDict=dayPrice)

    #获取整个页面的价格数据
    def spiderList(self):
        c_list = []
        count = self.getPage(self.getUrl(self.name))
        for i in range(1, count + 1):
            print i
            C_url = self.getUrl(self.name,i)
            print C_url
            priceList = self.getPriceList(C_url)
            for priceDay in priceList:
                c_list.append(priceDay)
        return c_list

    def getHtml(self,url):
        page = urllib.urlopen(url)
        html = page.read()
        return html

    def getPageNum(self,url):
        html = self.getHtml(url)
        soup = BeautifulSoup(html, 'html.parser')
        string = soup.find('td',class_='tdr',attrs={'height':'30'})
        result = re.findall(".*共(\d+)页.*",string.encode('utf-8'))
        return int(result[0])

    def getPriceList(self,url):
        html = self.getHtml(url)
        soup = BeautifulSoup(html, 'html.parser')
        priceList = []
        for dayPrice in soup.find_all('tr'):
            priceModel = [priceModel.string for priceModel in dayPrice.find_all('div')]
            if(len(priceModel) != 0):
                priceList.append(priceModel)
        return priceList

    # shfe 上期所   dce 大商所   czce  郑商所    cffex 中金所
    # 大商所  豆一 A   豆二 B     胶合板 BB    玉米 C    纤维板 FB
    # 铁矿石 I     焦炭 J      鸡蛋 JD    焦煤 JM   塑料 L   豆粕 M
    # PP PP     PVC V      豆油   Y   棕榈  P

    # 上期所
    def getUrl(self,name,index=1,exhouse_name='dce'):
        urlname = utils.getShort(name).upper()
        return "http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?page=" + str(index) + "&breed="+urlname+"0&start=1990-08-22&end=2017-05-23&jys="+exhouse_name+"&pz=" + urlname + "&hy="+urlname+"0&type=inner"

if __name__ == '__main__':
    dp = DataProvider('棕榈')
    print dp.getData(name_array=['date','close'])
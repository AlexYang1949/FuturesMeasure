#!/usr/local/bin/python
#-*-coding:utf-8-*-

from bs4 import BeautifulSoup
import re
import urllib
from data.dataProvider import DataProvider
from utils.utils import utils
from database import database

class DataSpider():
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
        count = self.getPageNum(self.getUrl(self.name))
        for i in range(1, count + 1):
            C_url = self.getUrl(self.name,i)
            print '爬取%s,第%d页\nurl=%s'%(self.name,i,C_url)
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

    # 郑商所  棉花 CF   玻璃  FG   郑醇  MA    菜油  OI    早稻  RI      菜粕  RM      菜籽  RS      硅铁  SF      锰硅  SM
    # 白糖  SR      PTA   TA      强麦  WH      动力煤  ZC

    # 上期所   白银  AG     沪铝  AL      黄金   AU      沥青  BU      沪铜   CU     燃油  FU      热扎卷板    HC      沪镍  NI
    #  沪铅   PB      螺纹钢   RB        橡胶  RU      沪锡   SN     线材    WR        沪锌  ZN

    # 中金所   中证500  IC       沪深300   IF      上证50   IH         10年国债     T       5年国债       TF

    shortDict = {'dce':['a','b','bb','c','fb','i','j','jd','jm','l','m','pp','v','y','p'],
                 'shfe':['ag','al','au','bu','cu','fu','hc','ni','pb','rb','ru','sn','wr','zn'],
                 'czce':['cf','fg','ma','oi','ri','rm','rs','sf','sm','sr','ta','wh','zc'],
                 'cffex':['ic','if','ih','t','tf']}

    def getUrl(self,name,index=1):
        shortname = utils.getShort(name)
        exhouse_name = utils.getExhouseName(name)
        return "http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?page=" + str(index) + "&breed="+shortname+"0&start=1990-08-22&end=2017-05-23&jys="+exhouse_name+"&pz=" + shortname + "&hy="+shortname+"0&type=inner"

if __name__ == '__main__':
    # dceNameArray = ['豆一','豆二','胶合板','玉米','纤维板','铁矿石','焦炭','鸡蛋','焦煤','塑料','豆粕','PP','PVC','豆油','棕榈']
    # czceNameArray = ['棉花','玻璃','郑醇','菜油','早稻','菜粕','菜籽','硅铁','锰硅','白糖','PTA','强麦','动力煤']
    # shfeNameArray = ['白银','沪铝','黄金','沥青','沪铜','燃油','热扎卷板','沪镍','沪铅','螺纹钢','橡胶','沪锡','线材','沪锌']
    cffexNameArray = ['中证500','沪深300','上证50','10年国债','5年国债']
    for name in cffexNameArray:
        spider = DataSpider(name)
        spider.start()

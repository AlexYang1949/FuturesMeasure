#!/usr/local/bin/python
#-*-coding:utf-8-*-
#玉米   http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?jys=dce&pz=C&hy=C0&breed=C0&type=inner&start=2016-08-22&end=2017-05-22

import matplotlib.pyplot as plt

from charge.chargeManager import ChargeManager
from data.dataProvider import DataProvider

charge_period = 22

if __name__ == '__main__':
    spiderNameArray = ['棉花', '玻璃', '郑醇', '菜油', '早稻', '菜粕', '菜籽', '硅铁', '锰硅', '白糖', 'PTA', '强麦', '动力煤']
    for name in spiderNameArray:
        for p in range(3,30):
            print '----------------%s--%d周期-------------------'%(name,p)
            dp = DataProvider(name=name)
            p_list = dp.getData(['date','close'])
            cm = ChargeManager(p_list,p)
            cm.startCharge()
            cm.printChargeResult()
            print '------------------------------------'



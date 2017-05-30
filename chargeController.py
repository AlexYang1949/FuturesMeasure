#!/usr/local/bin/python
#-*-coding:utf-8-*-
#玉米   http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?jys=dce&pz=C&hy=C0&breed=C0&type=inner&start=2016-08-22&end=2017-05-22

import matplotlib.pyplot as plt

from charge.chargeManager import ChargeManager
from data.dataProvider import DataProvider

charge_period = 22

if __name__ == '__main__':
    c_list = []
    dp = DataProvider(name='棕榈')
    p_list = dp.getData(['date','close'])
    cm = ChargeManager(p_list,charge_period)
    cm.startCharge()
    cm.printChargeResult()



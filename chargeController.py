#!/usr/local/bin/python
#-*-coding:utf-8-*-
#玉米   http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?jys=dce&pz=C&hy=C0&breed=C0&type=inner&start=2016-08-22&end=2017-05-22

from charge.chargeManager import ChargeManager
from data.dataProvider import DataProvider
from plot.plot import Plot
charge_period = 20
def testMa(nameArray,period):
    for name in nameArray:
        print("Ma----------------{}--{}周期-------------------".format(name, period))
        dp = DataProvider(name=name)
        p_list = dp.getData(['date', 'close'])
        cm = ChargeManager(p_list, period, nodeStat=False)
        cm.startCharge('ma')
        cm.printChargeResult()
        # cm.printStrategyResult()
        # cm.plotResult()


def testPreMa(nameArray,period):
    for name in nameArray:
        print('preMa----------------{}--{}周期-------------------'.format(name, period))
        dp = DataProvider(name=name)
        p_list = dp.getData(['date', 'close'])
        cm = ChargeManager(p_list, period, nodeStat=False)
        cm.startCharge('preMa')
        # cm.printStrategyResult()
        cm.printChargeResult()
        # cm.plotResult()


if __name__ == '__main__':

    dceNameArray = ['豆一', '豆二', '胶合板', '玉米', '纤维板', '铁矿石', '焦炭', '鸡蛋', '焦煤', '塑料', '豆粕', 'PP', 'PVC', '豆油', '棕榈']
    czceNameArray = ['棉花', '玻璃', '郑醇', '菜油', '早稻', '菜粕', '菜籽', '硅铁', '锰硅', '白糖', 'PTA', '强麦', '动力煤']
    shfeNameArray = ['白银', '沪铝', '黄金', '沥青', '沪铜', '燃油', '热扎卷板', '沪镍', '沪铅', '螺纹钢', '橡胶', '沪锡', '线材', '沪锌']
    cffexNameArray = ['中证500', '沪深300', '上证50', '10年国债', '5年国债']
    betterNameArray = ['棉花','硅铁','锰硅','白糖','PTA','动力煤','铁矿石', '焦炭','塑料','PP', '豆粕','豆油', '热扎卷板','螺纹钢','棕榈','橡胶']
    allNameArray = czceNameArray + dceNameArray + shfeNameArray

    for name in betterNameArray:
        testMa([name],period=charge_period)
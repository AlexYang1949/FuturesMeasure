#-*-coding:utf-8-*-

from strategy.chargeStrategy import ChargeStrategy
from chargeModel import ChargeModel
from chargeResult import ChargeResult
from utils.utils import utils

class ChargeManager():
    def __init__(self,data,chargePeriod ,nodeStat=True):
        self.data = data
        self.chargeResult = ChargeResult(len(data))
        self.chargeModel = ChargeModel()
        self.chargeStrategy = ChargeStrategy()
        self.chargePeriod = chargePeriod
        self.nodeStat = nodeStat

    def startCharge(self):
        priceArray = []
        for priceData in self.data:
            priceArray.append(priceData[1])
        for index, price in enumerate(self.data):
            if utils().is_number(priceArray[index]) and priceArray[index]!=0:
                self.exchange(priceArray[index],self.chargeStrategy.maStrategy(priceArray,index,self.chargePeriod),self.data[index][0])

    def exchange(self,price, direction, date):
        if direction!=0:
            self.chargeModel.hold_days += 1
        if self.chargeModel.hold_direct == direction:
            return
        self.cover(price, date)
        self.chargeModel.hold_price = price
        self.chargeModel.hold_number = self.chargeResult.all_assets / price
        # print self.chargeModel.hold_number
        self.chargeModel.hold_direct = direction

    def cover(self,price, date):
        # print price, self.chargeModel.hold_price, self.chargeModel.hold_direct,self.chargeModel.hold_number
        dis = (price - self.chargeModel.hold_price) * self.chargeModel.hold_direct * self.chargeModel.hold_number

        precent = dis * 100 / self.chargeResult.all_assets

        # print date,precent
        if precent > self.chargeResult.max_get:
            self.chargeResult.max_get = precent
        if precent < self.chargeResult.max_lost:
            self.chargeResult.max_lost = precent

        self.chargeResult.all_assets += dis
        self.chargeResult.asset_array.append((date, self.chargeResult.all_assets))
        charge_string  = '日期 : %s  幅度 : %.2f  价格 ：%.2f' %(str(date),precent,price)
        if dis > 0:
            self.chargeResult.get_time += 1
            self.chargeResult.total_get += precent
            if precent > 5:
                self.chargeResult.big_get_time += 1
                self.chargeResult.gap += self.chargeModel.ref_hold_days
                self.chargeResult.gapArray.append(self.chargeModel.ref_hold_days)
                self.chargeResult.gap_lost_array.append(self.chargeResult.gap_lost_time)
                self.chargeModel.ref_hold_days = 0
                self.chargeResult.distant_bigGet = 0
                self.chargeResult.gap_lost_time = 0
                self.chargeResult.big_array.append(charge_string)
                self.chargeResult.con_lost = 0
                self.chargeResult.big_get += precent
            else:
                self.chargeModel.ref_hold_days += self.chargeModel.hold_days
                self.chargeResult.distant_bigGet = self.chargeModel.ref_hold_days
        else:
            self.chargeResult.con_lost += 1
            self.chargeResult.lost_time += 1
            self.chargeResult.total_lost += precent
            self.chargeModel.ref_hold_days += self.chargeModel.hold_days
            self.chargeResult.distant_bigGet = self.chargeModel.ref_hold_days
            self.chargeResult.gap_lost_time += 1
            if precent<-2:
                self.chargeResult.big_array.append(charge_string)

        if self.nodeStat:
            direction = '涨' if self.chargeModel.hold_direct==1 else '跌'
            print  '震荡 %d 时间 %s 价格：%.f 幅度:%.2f 持有时间 %d 方向:%s' % (self.chargeResult.gap_lost_time,str(date), price,precent,self.chargeModel.hold_days,direction)
        self.chargeModel.hold_days = 0

    def printChargeResult(self):
        self.chargeResult.printResult()
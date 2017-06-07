#-*-coding:utf-8-*-

from strategy.chargeStrategy import ChargeStrategy
from chargeModel import ChargeModel
from chargeResult import ChargeResult
from utils.utils import utils
bool
class ChargeManager():
    def __init__(self,data,chargePeriod ,nodeStat=True):
        self.data = data
        self.chargeResult = ChargeResult()
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

        if dis > 0:
            self.chargeResult.get_time += 1
            self.chargeResult.total_get += precent
            if precent > 5:
                self.chargeResult.bigGet += 1
                self.chargeResult.gap += self.chargeModel.ref_hold_days
                self.chargeResult.gapArray.append(self.chargeModel.ref_hold_days)
                self.chargeModel.ref_hold_days = 0
                self.chargeResult.distant_bigGet = 0
            else:
                self.chargeModel.ref_hold_days += self.chargeModel.hold_days
                self.chargeResult.distant_bigGet = self.chargeModel.ref_hold_days
        else:
            self.chargeResult.lost_time += 1
            self.chargeResult.total_lost += precent
            self.chargeModel.ref_hold_days += self.chargeModel.hold_days
            self.chargeResult.distant_bigGet = self.chargeModel.ref_hold_days

        if self.nodeStat:
            print  '%s 收益：%.2f 成交价:%s 账户余额:%.2f ' % (str(date), precent, price,self.chargeResult.all_assets)
        self.chargeModel.hold_days = 1

    def printChargeResult(self):
        self.chargeResult.printResult()
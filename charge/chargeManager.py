from strategy.chargeStrategy import ChargeStrategy
from chargeModel import ChargeModel
from chargeResult import ChargeResult
from utils.utils import utils
class ChargeManager():
    def __init__(self,data,chargePeriod):
        self.data = data
        self.chargeResult = ChargeResult()
        self.chargeModel = ChargeModel()
        self.chargeStrategy = ChargeStrategy()
        self.chargePeriod = chargePeriod

    def startCharge(self):
        for index, price in enumerate(self.data):
            if utils().is_number(price):
                self.exchange(price,self.chargeStrategy.maStrategy(self.data,index,self.chargePeriod),self.data)

    def exchange(self,price, direction, date):
        self.chargeModel.hold_days += 1
        if self.chargeModel.hold_direct == direction:
            return
        self.cover(price, date)
        self.chargeModel.hoeld_price = price
        self.chargeModel.hold_number = self.chargeResult.all_assets / price
        self.chargeModel.hold_direct = direction

    def cover(self,price, date):
        dis = (price - self.chargeModel.hold_price) * self.chargeModel.hold_direct * self.chargeModel.hold_number
        precent = dis * 100 / self.chargeResult.all_assets
        if precent > self.chargeResult.max_get:
            self.chargeResult.max_get = precent
        if precent < self.chargeResult.max_lost:
            self.chargeModel.max_lost = precent

        self.chargeResult.all_assets += dis
        self.chargeResult.asset_array.append((date, self.chargeResult.all_assets))
        # print "get = " + str(dis),"current = "+str(price),"hold = " +str(hold_price),hold_direct,hold_number,"all = "+str(all_assets),"day ="+str(days)
        days = 1
        if dis > 0:
            self.chargeResult.get_time += 1
            self.chargeResult.total_get += dis
        else:
            self.chargeResult.lost_time += 1
            self.chargeResult.total_lost += dis

    def printChargeResult(self):
        self.chargeResult.printResult()
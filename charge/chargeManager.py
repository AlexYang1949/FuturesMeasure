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
                strategyResult = self.chargeStrategy.maStrategy(priceArray,index,self.chargePeriod)
                strategyResult1 = self.chargeStrategy.maAvdStrategy(self.chargeModel.hold_direct,priceArray, index, self.chargePeriod)
                self.exchange(priceArray[index],strategyResult1,self.data[index][0])

    def exchange(self,price, direction, date):
        if direction!=0:
            self.chargeModel.hold_days += 1
            if price >= self.chargeModel.max_price:
                self.chargeModel.max_hold_day = self.chargeModel.hold_days
                self.chargeModel.max_price = price
            if price <= self.chargeModel.min_price:
                self.chargeModel.min_hold_day = self.chargeModel.hold_days
                self.chargeModel.min_price = price

        if self.chargeModel.hold_direct == direction:
            return
        self.cover(price, date)
        self.chargeModel.hold_price = price
        self.chargeModel.hold_number = self.chargeResult.all_assets / price
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
        precentx = ((
                    self.chargeModel.max_price if self.chargeModel.hold_direct == 1 else self.chargeModel.min_price) - self.chargeModel.hold_price) * self.chargeModel.hold_direct * self.chargeModel.hold_number * 100 / self.chargeResult.all_assets
        direction = '涨' if self.chargeModel.hold_direct == 1 else '跌'
        charge_string = '日期 : %s  幅度 : %.2f  价格 ：%.2f 持有时间 %d 方向:%s 最大获利 = %.2f 最大获利时间 = %d' % \
                        (str(date), precent, price, self.chargeModel.hold_days, direction,precentx,(self.chargeModel.max_hold_day if self.chargeModel.hold_direct==1 else self.chargeModel.min_hold_day))
        if dis > 0:
            # 总获利次数
            self.chargeResult.get_time += 1
            # 总获利比例
            self.chargeResult.total_get += precent
            if precent > 5:
                # 大涨次数
                self.chargeResult.big_get_time += 1
                # 大涨之间间隔
                self.chargeResult.gap += self.chargeModel.ref_hold_days
                # 大涨之间间隔
                self.chargeResult.gapArray.append(self.chargeModel.ref_hold_days)
                self.chargeResult.gap_lost_array.append(self.chargeModel.gap_lost_time)
                # 大涨
                self.chargeResult.big_array.append(charge_string)
                # 重置上次上涨之间间隔
                self.chargeModel.ref_hold_days = 0
                # 距离上次大涨天数
                self.chargeResult.distant_bigGet = 0
                # 震荡次数
                self.chargeModel.gap_lost_time = 0
                self.chargeResult.con_lost = 0
                # 大涨比例
                self.chargeResult.big_get += precent
            else:
                self.chargeModel.ref_hold_days += self.chargeModel.hold_days
                self.chargeResult.distant_bigGet = self.chargeModel.ref_hold_days
        else:
            self.chargeResult.con_lost += 1
            if dis<0:
                self.chargeResult.lost_time += 1
            self.chargeResult.total_lost += precent
            self.chargeModel.ref_hold_days += self.chargeModel.hold_days
            self.chargeResult.distant_bigGet = self.chargeModel.ref_hold_days
            # 震荡次数
            self.chargeModel.gap_lost_time += 1
            if precent<-2:
                self.chargeResult.big_array.append(charge_string)

        if self.nodeStat:

            print  '震荡 %d 时间 %s 价格：%.f 幅度:%.2f 持有时间 %d 方向:%s 最大获利 = %.2f 最大获利时间 = %d' % \
                   (self.chargeModel.gap_lost_time,str(date), price,precent,self.chargeModel.hold_days,direction,precentx,(self.chargeModel.max_hold_day if self.chargeModel.hold_direct==1 else self.chargeModel.min_hold_day))
        self.chargeModel.hold_days = 0
        self.chargeModel.max_price = price
        self.chargeModel.min_price = price
        self.chargeModel.min_hold_day = 0
        self.chargeModel.max_hold_day = 0

    def printChargeResult(self):
        self.chargeResult.printResult()
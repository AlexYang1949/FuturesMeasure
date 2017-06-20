#-*-coding:utf-8-*-
#趋势跟踪 1、价格包含了所有的基本面信息 2、没有永远的趋势也没有永远的震荡 3、之前发生的以后还会发生
#1、把握进场时机 2、坚守正确的仓位 3、在正确的仓位上加码 4、减仓利润保护 5、转势果断立场
#试单
# 多开 空开 多平 空平

class Charge():
    buy_hold = 1
    sell_hold = -1
    empty = 0
    buy_close = 2
    sell_close = -2

class ChargeStrategy():
    def __init__(self):
        self.preBuyPrice = 0
        self.preSellPrice = 0

    def ma(self, x, list):
        return sum(list) / x

    def maStrategy(self,priceList,index,period):
        if (index > 80):
            price = priceList[index]
            lma = self.ma(period, priceList[(index - period + 1):(index + 1)])
            if price >= lma :
                return Charge.buy_hold
            elif price < lma :
                return Charge.sell_hold
        else:
            return Charge.empty

    def maAvdStrategy(self,hold_direction,priceList,index,period):
        if (index > 80):
            price = priceList[index]
            ref_price = priceList[index-1]
            lma = self.ma(period, priceList[(index - period + 1):(index + 1)])
            ref_lma = self.ma(period, priceList[(index - period ):index])
            if self.preSellPrice!=0 and hold_direction==Charge.empty:
                if price < self.preSellPrice:
                    self.preSellPrice=0
                    self.preBuyPrice=0
                    return Charge.sell_hold

            if self.preBuyPrice != 0 and hold_direction == Charge.empty:
                if price > self.preBuyPrice:
                    self.preSellPrice = 0
                    self.preBuyPrice = 0
                    return Charge.buy_hold
            #下穿
            if price<lma and ref_price>ref_lma:
                self.preSellPrice = price
                #持仓
                if hold_direction==Charge.buy_hold:
                    return Charge.empty
            #上穿
            if price > lma and ref_price < ref_lma:
                self.preBuyPrice = price
                # 持仓
                if hold_direction == Charge.sell_hold:
                    return Charge.empty
            return hold_direction

        else:
            return Charge.empty
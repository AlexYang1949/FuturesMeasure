#-*-coding:utf-8-*-
#趋势跟踪 1、价格包含了所有的基本面信息 2、没有永远的趋势也没有永远的震荡 3、之前发生的以后还会发生
#1、把握进场时机 2、坚守正确的仓位 3、在正确的仓位上加码 4、减仓利润保护 5、转势果断立场
#试单
# 多开 空开 多平 空平

class Charge():
    buy_open = 1
    sell_open = -1
    empty = 0
    buy_close = 2
    sell_close = -2

class ChargeStrategy():
    def ma(self, x, list):
        return sum(list) / x

    def maStrategy(self,priceList,index,period):
        if (index > 80):
            price = priceList[index]
            lma = self.ma(period, priceList[(index - period + 1):(index + 1)])
            if price >= lma :
                return Charge.buy_open
            elif price < lma :
                return Charge.sell_open
        else:
            return Charge.empty

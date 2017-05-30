class ChargeStrategy():
    def ma(self, x, list):
        return sum(list) / x

    def maStrategy(self,priceList,index,period):
        if (index > 100):
            price = priceList[index]
            lma = self.ma(period, priceList[(index - period + 1):(index + 1)])
            # date = priceList[index][
            if price > lma:  # and refLma>lma:
                return 1
            elif price < lma:  # and refLma<lma:
                return -1
        else:
            return 0
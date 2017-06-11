#-*-coding:utf-8-*-

class ChargeResult(object):
    def __init__(self,total_day):
        self.all_assets = 100000
        self.max_lost = 0
        self.max_get = 0
        self.lost_time = 0
        self.get_time = 0
        self.total_lost = 0
        self.total_get = 0
        self.asset_array = []
        self.gap = 0
        self.gapArray = []
        self.gap_lost_array = []
        self.gap_lost_time = 0
        self.big_get_time = 0
        self.big_get = 0
        self.distant_bigGet = 0
        self.big_array = []
        self.total_day = total_day
        self.con_lost = 0

    def clearResult(self):
        self.all_assets = 100000
        self.max_lost = 0
        self.max_get = 0
        self.lost_time = 0
        self.get_time = 0
        self.total_lost = 0
        self.total_get = 0

    def get_median(self,data):
        if len(data)==0: return 0
        data.sort()
        half = len(data) // 2
        avg = sum(data)/len(data)
        return (data[half] + data[~half]) / 2 + avg/2

    def printResult(self):
        min_lost_time = self.get_median(self.gap_lost_array)
        self.big_get_time = 1 if self.big_get_time==0 else self.big_get_time
        print "年均收益 %.2f " %((self.total_get+self.total_lost)*200/self.total_day)+"%"
        print "最大获利比例 = %.2f" % self.max_get + "%"
        print "最大损失比例 = %.2f" % self.max_lost + "%"
        print "总获利次数 = %.f 次" %self.get_time
        print "总损失次数 = %.f 次" %self.lost_time
        print "获利次数比例 = %.f " % (self.get_time * 100 / (self.get_time+self.lost_time)) + "%"
        print "大涨次数 = %.f 次" % self.big_get_time
        print "大涨次数比例 = %.f " % (self.big_get_time*100/self.get_time) +"%"
        print "平均每次大涨比例 = %.2f" % (self.big_get / self.big_get_time) + "%"
        print "平均每次获利比例 = %.2f" %(self.total_get/self.get_time) + "%"
        print "平均每次损失比例 = %.2f" % (self.total_lost/ self.lost_time) + "%"
        print "大涨间隔 = %s " % self.gapArray
        print "平均大涨间隔 = %.f 天" % (self.gap/self.big_get_time)
        print "距离上次大涨次数 = %.f 天" % self.distant_bigGet
        print "大涨间平均失败次数 = %.f 次" % min_lost_time
        print "连续失败次数 = %d 次"%self.con_lost
        print "是否可以交易  ： %s" %("是" if self.con_lost>min_lost_time else "否")
        print "资金总额 = %.2f 元" % self.all_assets
        print "总获利比例 = %.2f" % self.total_get + "%"
        print "总损失比例 = %.2f" % self.total_lost + "%"
        for charge in self.big_array:
            print charge
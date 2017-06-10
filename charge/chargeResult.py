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
        self.bigGet = 0
        self.distant_bigGet = 0
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
        data.sort()
        half = len(data) // 2
        avg = sum(data)/len(data)
        return (data[half] + data[~half]) / 2 + avg/2

    def printResult(self):
        min_lost_time = self.get_median(self.gap_lost_array)
        print "all_assets = %.2f 元" %self.all_assets
        print "年均收益 %.2f " %((self.total_get+self.total_lost)*200/self.total_day)+"%"
        print "total_get = %.2f" % self.total_get + "%"
        print "total_lost = %.2f" % self.total_lost + "%"
        print "max_get = %.2f"%self.max_get + "%"
        print "max_lost = %.2f"%self.max_lost + "%"
        print "get_time = %.f 次" %self.get_time
        print "lost_time = %.f 次" %self.lost_time
        print "percent_get_time = %.f " % (self.get_time * 100 / (self.get_time+self.lost_time)) + "%"
        print "total_bigGet_time = %.f 次" % self.bigGet
        print "percent_bigGet_time = %.f " % (self.bigGet*100/self.get_time) +"%"
        print "average_get = %.2f" %(self.total_get/self.get_time) + "%"
        print "average_lost = %.2f" % (self.total_lost/ self.lost_time) + "%"
        print "gap_array = %s " % self.gapArray
        print "average_gap = %.f 天" % (self.gap/self.bigGet)
        print "distant last_bigGet = %.f 天" % self.distant_bigGet
        print "大涨间平均失败次数 =%.f 次" % min_lost_time
        print "连续失败次数 = %d 次"%self.con_lost
        print "是否可以交易  ： %s" % "是" if self.con_lost>min_lost_time else "否"
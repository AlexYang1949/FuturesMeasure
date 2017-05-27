#-*-coding:utf-8-*-

class chargeResult(object):
    def __init__(self):
        self.all_assets = 100000
        self.max_lost = 0
        self.max_get = 0
        self.lost_time = 0
        self.get_time = 0
        self.total_lost = 0
        self.total_get = 0

    def clearResult(self):
        self.all_assets = 100000
        self.max_lost = 0
        self.max_get = 0
        self.lost_time = 0
        self.get_time = 0
        self.total_lost = 0
        self.total_get = 0

    def printResult(self):
        print "all_assets =" + str(self.all_assets)
        print "max_get =" + str(self.max_get) + "%"
        print "max_lost = " + str(self.max_lost) + "%"
        print "get_time =" + str(self.get_time)
        print "lost_time = " + str(self.lost_time)
        print "total_get =" + str(self.total_get)
        print "total_lost = " + str(self.total_lost)
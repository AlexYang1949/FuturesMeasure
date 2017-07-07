#-*-coding:utf-8-*-
class ChargeModel(object):
    def __init__(self):
        self.hold_price = 0   #持有金额
        self.hold_direct = 0  #持有方向
        self.hold_number = 0  #持有数量
        self.hold_days = 0    #持有天数
        self.ref_hold_days = 0   #上次交易持有时间
        self.max_price = 0    #单次交易最高价格
        self.min_price = 0    #单次交易最低价格
        self.max_hold_day = 0 #最高持有时间
        self.min_hold_day = 0 #最低持有时间
        self.gap_lost_time = 0 #距离亏损的天数
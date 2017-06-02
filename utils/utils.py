#!/usr/local/bin/python
#-*-coding:utf-8-*-

class utils():
    @classmethod
    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

    @classmethod
    def getInfoWithName(self,name):
        shortname = ''
        exchangename = 'dce'
        if name == '玉米':
            shortname = 'c'
        elif name == '棕榈':
            shortname = 'p'
        elif name == '豆一':
            shortname = 'a'
        elif name == '豆二':
            shortname = 'b'
        elif name == '胶合板':
            shortname = 'bb'
        elif name == '纤维板':
            shortname = 'fb'
        elif name == '铁矿石':
            shortname = 'i'
        elif name == '焦炭':
            shortname = 'j'
        elif name == '鸡蛋':
            shortname = 'jd'
        elif name == '焦煤':
            shortname = 'jm'
        elif name == '塑料':
            shortname = 'l'
        elif name == '豆粕':
            shortname = 'm'
        elif name == 'PP':
            shortname = 'pp'
        elif name == 'PVC':
            shortname = 'v'
        elif name == '豆油':
            shortname = 'y'
            # 郑商所  棉花 CF   玻璃  FG   郑醇  MA    菜油  OI    早稻  RI      菜粕  RM      菜籽  RS      硅铁  SF      锰硅  SM
            # 白糖  SR      PTA   TA      强麦  WH      动力煤  ZC
        elif name == '棉花':
            shortname = 'cf'
            exchangename = 'czce'
        elif name == '玻璃':
            shortname = 'fg'
            exchangename = 'czce'
        elif name == '郑醇':
            shortname = 'ma'
            exchangename = 'czce'
        elif name == '菜油':
            shortname = 'oi'
            exchangename = 'czce'
        elif name == '早稻':
            shortname = 'ri'
            exchangename = 'czce'
        elif name == '菜粕':
            shortname = 'rm'
            exchangename = 'czce'
        elif name == '菜籽':
            shortname = 'rs'
            exchangename = 'czce'
        elif name == '硅铁':
            shortname = 'sf'
            exchangename = 'czce'
        elif name == '锰硅':
            shortname = 'sm'
            exchangename = 'czce'
        elif name == '白糖':
            shortname = 'sr'
            exchangename = 'czce'
        elif name == 'PTA':
            shortname = 'ta'
            exchangename = 'czce'
        elif name == '强麦':
            shortname = 'wh'
            exchangename = 'czce'
        elif name == '动力煤':
            shortname = 'zc'
            exchangename = 'czce'

        elif name == '白银':
            shortname = 'ag'
            exchangename = 'shfe'
        elif name == '沪铝':
            shortname = 'al'
            exchangename = 'shfe'
        elif name == '黄金':
            shortname = 'au'
            exchangename = 'shfe'
        elif name == '沥青':
            shortname = 'bu'
        elif name == '沪铜':
            shortname = 'cu'
            exchangename = 'shfe'
        elif name == '燃油':
            shortname = 'fu'
            exchangename = 'shfe'
        elif name == '热扎卷板':
            shortname = 'hc'
            exchangename = 'shfe'
        elif name == '沪镍':
            shortname = 'ni'
            exchangename = 'shfe'
        elif name == '沪铅':
            shortname = 'pb'
            exchangename = 'shfe'
        elif name == '螺纹钢':
            shortname = 'rb'
            exchangename = 'shfe'
        elif name == '橡胶':
            shortname = 'ru'
            exchangename = 'shfe'
        elif name == '沪锡':
            shortname = 'sn'
            exchangename = 'shfe'
        elif name == '线材':
            shortname = 'wr'
            exchangename = 'shfe'
        elif name == '沪锌':
            shortname = 'zn'
            exchangename = 'shfe'

        elif name == '中证500':
            shortname = 'IC'
            exchangename = 'cffex'
        elif name == '沪深300':
            shortname = 'IF'
            exchangename = 'cffex'
        elif name == '上证50':
            shortname = 'IH'
            exchangename = 'cffex'
        elif name == '10年国债':
            shortname = 'T'
            exchangename = 'cffex'
        elif name == '5年国债':
            shortname = 'TF'
            exchangename = 'cffex'
        return shortname,exchangename

    @classmethod
    def getShort(self, name):
        return self.getInfoWithName(name)[0]

    @classmethod
    def getExhouseName(self, name):
        return self.getInfoWithName(name)[1]

if __name__ == '__main__':
    print utils.getShort('菜油')
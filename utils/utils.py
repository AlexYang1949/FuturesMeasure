#!/usr/local/bin/python
#-*-coding:utf-8-*-

class utils():
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
    def getShort(self,name):
        urlname = ''
        if name == '玉米':
            urlname = 'C'
        elif name == '棕榈':
            urlname = 'P'
        elif name == '豆一':
            urlname = 'A'
        elif name == '豆二':
            urlname = 'B'
        elif name == '胶合板':
            urlname = 'BB'
        elif name == '纤维板':
            urlname = 'FB'
        elif name == '铁矿石':
            urlname = 'I'
        elif name == '焦炭':
            urlname = 'J'
        elif name == '鸡蛋':
            urlname = 'JD'
        elif name == '焦煤':
            urlname = 'JM'
        elif name == '塑料':
            urlname = 'L'
        elif name == '豆粕':
            urlname = 'M'
        elif name == 'PP':
            urlname = 'PP'
        elif name == 'PVC':
            urlname = 'V'
        elif name == '豆油':
            urlname = 'Y'
        return urlname.lower()

    # def plot(self):
    #     fig = plt.figure()
    #     ax = fig.add_subplot(111)
    #     ax.plot(range(len(asset_array)), [price[1] for price in asset_array])
    #     ax.set_xticklabels([3, 123, 1, 23, 123, 1, 23, 1, 23, 1, 231, 23], rotation=-30)
    #     plt.show()
#-*-coding:utf-8-*-
import matplotlib.pyplot as plt
from data.dataProvider import DataProvider
class Plot():
    @classmethod
    def plot(self,value_array,xlabel_array):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(value_array)
        ax.set_xticklabels(xlabel_array, rotation=-30)
        plt.show()

if __name__ == '__main__':
    dp = DataProvider('玉米')
    p_list = dp.getData(['date', 'close'])
    price_list = [int(price[1]) for price in p_list]
    date_list = [str(price[0]) for price in p_list]
    print price_list ,date_list
    Plot.plot(price_list,date_list)
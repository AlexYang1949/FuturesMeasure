#-*-coding:utf-8-*-
import matplotlib.pyplot as plt
import numpy as np
from data.dataProvider import DataProvider
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from datetime import datetime
class Plot():
    @classmethod
    def plot(self,array,title):
        xlabel_array = [int(price[1]) for price in array]
        value_array = [datetime.strptime(price[0], "%Y-%m-%d") for price in array]
        figure = plt.figure()
        axes = figure.gca()
        axes.set_title(title)
        axes.plot(value_array, xlabel_array)
        plt.show()

if __name__ == '__main__':
    dp = DataProvider('玉米')
    p_list = dp.getData(['date', 'close'])
    Plot.plot(p_list)
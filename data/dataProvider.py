#!/usr/local/bin/python
#-*-coding:utf-8-*-
from database import Database
from utils.utils import  utils

class DataProvider():
    def __init__(self,name):
        self.db = Database()
        self.db_name = utils.getShort(name)+'_table'

    def getData(self,name_array=[]):
        nameStr = ''
        for name in name_array:
            if nameStr != '':
                nameStr+=' , '+name
            else:
                nameStr += name
        c_list = self.db.select(colume=nameStr,db_name=self.db_name)
        if len(c_list)==0:
            print '需要爬取'
        else:
            p_list = []
            if len(name_array)==1:
                for price in c_list:
                    if price[0]!=0:
                        p_list.append(price[0])
                return p_list
            else:
                return c_list

    def writeData(self,dataDict):
        self.db.write(self.db_name, dataDict[0], dataDict[1], dataDict[2], dataDict[3], dataDict[4], dataDict[5])

    def createTable(self,tablename):
        self.db.create(tablename)

    def cleanData(self,name_array=[]):
        c_list = self.getData(name_array=name_array)
        for index,val in enumerate(c_list,1):
            index = index - 1
            # if val[1] == 0 :
            #     self.db.delete(tablename=self.db_name, condition="date='%s'" % str(val[0]))
            # print str(val[0]),val[1],c_list[index-1][1], (val[1]-c_list[index-1][1])/c_list[index-1][1]
            if index<len(c_list)-1 and abs((val[1]-c_list[index-1][1])/c_list[index-1][1])>0.102 and abs((c_list[index+1][1]-val[1])/val[1])>0.102:
                self.db.delete(tablename=self.db_name,condition="date='%s'"%str(val[0]))

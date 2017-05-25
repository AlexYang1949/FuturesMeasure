#!/usr/local/bin/python
#-*-coding:utf-8-*-

import MySQLdb

class database(object):
    # 连接
    def connect(self):
        self.conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="futures", charset="utf8")
        self.cursor = self.conn.cursor()

    # 写入
    def write(self,tablename,date,open,close,high,low,vol):
        sql = "insert into "+tablename+"(date,open,close,high,low,vol) SELECT %s,%s,%s,%s,%s,%s FROM DUAL WHERE NOT EXISTS(SELECT date FROM  "+tablename+" WHERE date=%s)"
        params = (str(date),float(open),float(close),float(high),float(low),vol,str(date))
        n = self.cursor.execute(sql,params)
        print n

# # 更新
# sql = "update user set name=%s where id=3"
# param = ("bbb")
# n = cursor.execute(sql, param)
# print n
#
    # 查询
    def select(self,colume="*",db_name='c_table'):
        n = self.cursor.execute("select "+colume+" from "+db_name)
        return self.cursor.fetchall()

#
# # 删除
# sql = "delete from user where name=%s"
# param = ("aaa")
# n = cursor.execute(sql, param)
# print n
#
    # 关闭
    def close(self):
        self.conn.close()

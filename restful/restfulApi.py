#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
app = Flask(__name__)
from charge.chargeManager import ChargeManager
from data.dataProvider import DataProvider

@app.route('/')
def hello_world():
    return jsonify(testPreMa(['棉花'],20))

@app.route('/result')
def get_result():
    name = request.args.get('name').encode('utf-8')
    print name
    return jsonify(testPreMa([name], 20))

def testPreMa(nameArray,period):
    for name in nameArray:
        print 'preMa----------------%s--%d周期-------------------' % (name, period)
        dp = DataProvider(name=name)
        p_list = dp.getData(['date', 'close'])
        cm = ChargeManager(p_list, period, nodeStat=False)
        cm.startCharge('preMa')
        return cm.resultJson()

if __name__ == '__main__':
    app.run(host='localhost')
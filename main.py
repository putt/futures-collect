#-*- coding=utf-8 -*-
# from FinalLogger import logger
# from Constant import inst_strategy, suffix_list
import urllib.request
import json
import sqlite3
import pandas as pd
from pvplot import PriceVolumePlotter
import numpy as np

conn = sqlite3.connect('futures.db3', check_same_thread = False)
contracts =  []
with open('contracts.txt') as f:
    contracts = f.read().splitlines()
f.closed

for i in contracts :
    bar_table = i + '_5MBar'
    # cmd = "DROP TABLE IF EXISTS " + bar_table
    # conn.execute(cmd)

    cmd = "CREATE TABLE IF NOT EXISTS " + bar_table \
          + " (id INTEGER PRIMARY KEY NULL, inst TEXT NULL, open DOUBLE NULL, high DOUBLE NULL, low DOUBLE NULL, close DOUBLE NULL, volume INTEGER NULL, TradingTime TEXT NULL)"
    # print(cmd)
    conn.execute(cmd)
    cmd = "CREATE TABLE IF NOT EXISTS " + i + "_VolDistribution" + " (price DOUBLE DOUBLE, volume DOUBLE NULL)"
    conn.execute(cmd)

def dealZhengZhou(symbol):
    if symbol[0].isupper():
        inst = symbol.lower()
        # 郑州商品交易所 CZCE TA001 -> ta2001
        # inst = inst[:-3]+'2'+inst[-3:]
        return inst
    return symbol

def volumeIncrease(pv_data, price, volume):
    if (price in pv_data):
        pv_data[price] += volume
    else:
        pv_data[price] = volume

if __name__=="__main__":
    # 'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesDailyKLine?symbol=M1701'
    base_url = 'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine5m?symbol='
    pvplot = PriceVolumePlotter()
    # for symbol in contracts:
    for symbol in ['ni1910',]:
        inst = dealZhengZhou(symbol)
        # print (inst, symbol)
        url = base_url + inst
        bar_table = symbol + '_5MBar'
        vol_table = symbol + '_VolDistribution'
        print ('url = ' + url)
        trading_data = pd.read_json(url)
        trading_data.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
        trading_data = trading_data.set_index('time')
        trading_data.to_hdf('data/'+symbol+ ".h5")
        results = json.load(urllib.request.urlopen(url))
        c = conn.cursor()
        c.execute("SELECT TradingTime from %s DESC LIMIT 1" %(bar_table))
        last = c.fetchone()

        bar_data = []
        vol_data = []
        pv_data = {}
        for r in results:
            # r -- ["2016-09-05","2896.000","2916.000","2861.000","2870.000","1677366"]  open, high, low, close
            # print (r)
            if not last or r[0] > last[0]:
                bar_data.append((symbol, float(r[1]), float(r[2]), float(r[3]), float(r[4]), int(r[5]), r[0]))
                # conn.execute(
                #     "INSERT INTO %s (inst, open, high, low, close, volume, TradingTime) VALUES ('%s', %f, %f, %f, %f, %d, '%s')"
                #     % (bar_table, symbol, float(r[1]), float(r[2]), float(r[3]), float(r[4]), int(r[5]), r[0]))
                vol_data.append((float(r[1]), float(r[5])/4))
                vol_data.append((float(r[2]), float(r[5])/4))
                vol_data.append((float(r[3]), float(r[5])/4))
                vol_data.append((float(r[4]), float(r[5])/4))
                # conn.execute("INSERT INTO %s (price, volume) VALUES (%f, %f)" %(vol_table, float(r[1]), float(r[5])/4))
                # conn.execute("INSERT INTO %s (price, volume) VALUES (%f, %f)" %(vol_table, float(r[2]), float(r[5])/4))
                # conn.execute("INSERT INTO %s (price, volume) VALUES (%f, %f)" %(vol_table, float(r[3]), float(r[5])/4))
                # conn.execute("INSERT INTO %s (price, volume) VALUES (%f, %f)" %(vol_table, float(r[4]), float(r[5])/4))
        conn.executemany("INSERT INTO %s (inst, open, high, low, close, volume, TradingTime) VALUES (?,?,?,?,?,?,?)"%bar_table ,bar_data)
        conn.executemany("INSERT INTO %s (price, volume) VALUES (?,?)"%vol_table , vol_data)
        conn.commit()
        # a = np.array(vol_data)
        # print (a)
        # b= a[a[:,0].argsort()]
        # print (b)
        # prices, volumes = zip(*vol_data)

        c.execute('SELECT price, sum(volume) from %s group by price order by price'%vol_table)
      
        prices, volumes = zip(*c.fetchall())
        # print( min(prices), max(prices))
        # print (prices)
        # print (volumes)
        

        pvplot.plot(symbol, prices, volumes)
        
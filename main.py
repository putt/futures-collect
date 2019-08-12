#-*- coding=utf-8 -*-
# from FinalLogger import logger
# from Constant import inst_strategy, suffix_list
import urllib.request
import json
import sqlite3
import pandas as pd
from pvplot import PriceVolumePlotter
import numpy as np
from datetime import datetime
import time

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
#    base_url = 'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine5m?symbol='
    base_url = 'https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_{}_{}=/InnerFuturesNewService.getFewMinLine?symbol={}&type=5'
    pvplot = PriceVolumePlotter()
    # for symbol in contracts:
    while 1:
        now = datetime.now()
        hour = now.hour
       # if (hour>8 and hour < 15) or hour >20:
        if 1:
            for symbol in contracts:
                inst = dealZhengZhou(symbol)
                # print (inst, symbol)
                url = base_url.format(inst, now.timestamp(), inst)
                bar_table = symbol + '_5MBar'
                vol_table = symbol + '_VolDistribution'
                print (inst)
                
                results = urllib.request.urlopen(url).read()
                remote_data = pd.read_json(results[results.find(b'(')+1: results.find(b')')]).set_index('d')
                c = conn.cursor()
                c.execute("SELECT TradingTime from %s DESC LIMIT 1" %(bar_table))
                last = c.fetchone()
                
                if not last:
                    new_data = remote_data
                else:
                    new_data = remote_data.loc[]

                bar_data = []
                vol_data = []
                pv_data = {}
                for r in results:
                    # r = ["2019-02-28 23:00:00","2631.000","2631.000","2630.000","2631.000","74"]
                    # datetime, open, high, low, close, volume
                    if not last or r[0] > last[0]:
                        bar_data.append((symbol, float(r[1]), float(r[2]), float(r[3]), float(r[4]), int(r[5]), r[0])) # symbol, o, h, l, c, v, datetime
                        vol_data.append((float(r[1]), float(r[5])/4))
                        vol_data.append((float(r[2]), float(r[5])/4))
                        vol_data.append((float(r[3]), float(r[5])/4))
                        vol_data.append((float(r[4]), float(r[5])/4))
                conn.executemany("INSERT INTO %s (inst, open, high, low, close, volume, TradingTime) VALUES (?,?,?,?,?,?,?)"%bar_table ,bar_data)
                conn.executemany("INSERT INTO %s (price, volume) VALUES (?,?)"%vol_table , vol_data)
                conn.commit()

                c.execute('SELECT price, sum(volume) from %s group by price order by price'%vol_table)
              
                prices, volumes = zip(*c.fetchall())   
                if bar_data:
                    current =  (bar_data[0][6], bar_data[0][4])
                else:
                    current = (results[0][0], results[0][4])
                pvplot.plot(symbol,current , prices, volumes)
        else:
            print("Waiting for trading time.")
            time.sleep(300)
        print ('Waiting next period.')
        time.sleep(100)
        

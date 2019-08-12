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

# sqlite 无法直接处理int64的数据，导致pandas的int64输入sqlite以后变成blob字段
# via: https://stackoverflow.com/questions/49456158/integer-in-python-pandas-becomes-blob-binary-in-sqlite
sqlite3.register_adapter(np.int64, lambda val: int(val))
sqlite3.register_adapter(np.int32, lambda val: int(val))


conn = sqlite3.connect('futures.db3', check_same_thread = False)
contracts =  []
with open('contracts.txt') as f:
    contracts = f.read().splitlines()
f.closed

for i in contracts :
    cmd = "CREATE TABLE IF NOT EXISTS " + i + " 5MBar (id INTEGER PRIMARY KEY NULL, open DOUBLE NULL, high DOUBLE NULL, low DOUBLE NULL, close DOUBLE NULL, volume INTEGER NULL, position INTEGER NULL, TradingTime TEXT NULL)"
    # print(cmd)
    conn.execute(cmd)
    cmd = "CREATE TABLE IF NOT EXISTS " + i + "_VolDistribution(price DOUBLE NULL, volume DOUBLE NULL)"
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
                
                # 更新数据
                results = urllib.request.urlopen(url).read().decode('utf8')
                remote_data = pd.read_json(results[results.find('(')+1: results.find(')')])
                c = conn.cursor()
                c.execute("SELECT TradingTime from %s ORDER by TradingTime DESC LIMIT 1" %(bar_table))
                last = c.fetchone()
                
                if not last:
                    new_data = remote_data.iloc[:-1]
                else:
                    new_data = remote_data.loc[remote_data['d']>last[-1]+'1'].iloc[:-1]
                if not new_data.empty:
                    conn.executemany("INSERT INTO %s (close, TradingTime, high, low, open, position, volume ) VALUES (?,?,?,?,?,?,?)"%bar_table , new_data.values[:-1])
                    
                    pv1 = new_data.loc[:,['o','v']].rename(columns={'o':'price'})
                    pv2 = new_data.loc[:,['h','v']].rename(columns={'h':'price'})  
                    pv3 = new_data.loc[:,['l','v']].rename(columns={'l':'price'})
                    pv4 = new_data.loc[:,['c','v']].rename(columns={'c':'price'})
                    
                    pv_data = pd.concat([pv1, pv2, pv3, pv4])
                    print(new_data)
                    print(pv_data)
                    conn.executemany("INSERT INTO %s (price, volume) VALUES (?,?)"%vol_table , pv_data.values)
                    conn.commit()
                
                
                # 做图
                c.execute('SELECT price, sum(volume) from %s group by price order by price'%vol_table)
                prices, volumes = zip(*c.fetchall())   
                pvplot.plot(symbol, (remote_data.iloc[-1].d,remote_data.iloc[-1].c) , prices, volumes)
        else:
            print("Waiting for trading time.")
            time.sleep(300)
        print ('Waiting next period.')
        time.sleep(100)
        

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
    cmd = "CREATE TABLE IF NOT EXISTS " + i + "_5MBar(d TEXT PRIMARY KEY , o DOUBLE , h DOUBLE, l DOUBLE, c DOUBLE, v INTEGER, p INTEGER)"
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

def collect(symbol):
    inst = dealZhengZhou(symbol)
    url = base_url.format(inst, now.timestamp(), inst)
    bar_table = symbol + '_5MBar'
    print (inst)
    
    #获取本地数据
    local_bars = pd.read_sql("SELECT * from {} ORDER BY d".format(bar_table), conn, index_col='d')
    
    
    # 获取新数据
    results = urllib.request.urlopen(url).read().decode('utf8')
    remote_bars = pd.read_json(results[results.find('(')+1: results.find(')')]).set_index('d')
    
    if local_bars.empty:
        new_bars = remote_bars
    else:
        new_bars = remote_bars.loc[remote_bars.index>local_bars.index[-1]]
        
    # 更新数据,因为最新的bar记录不完整，只更新到倒数第二bar
    update_bars = new_bars.iloc[:-1]
    if not update_bars.empty:
        update_bars.to_sql(bar_table, conn, if_exists='append')
    
    # 整合所有数据
    return pd.concat([local_bars, new_bars], sort=True)
   


if __name__=="__main__":
    base_url = 'https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_{}_{}=/InnerFuturesNewService.getFewMinLine?symbol={}&type=5'
    pvplot = PriceVolumePlotter()
    # for symbol in contracts:
    while 1:
        now = datetime.now()
        hour = now.hour
        if (hour>8 and hour < 15) or hour >20:
#        if 1:
            for symbol in contracts:
                full_bars = collect(symbol)
                pvplot.plot(symbol, full_bars)
        else:
            print("Waiting for trading time.")
            time.sleep(300)
        print ('Waiting next period.')
        time.sleep(30)
        

# -*- coding: utf-8 -*-
import pandas as pd

def traceZig(bars):
#    size = len(bars.index)
    last_bar = bars.iloc[0]
    go_up = True
    go_down = True
    zigzags = []
#    print(bars)
    for t, bar in bars[1:].iterrows():
        # 最低价是否低于last_bar True 继续 | False last_bar为zig 
        if go_down:
            if bar.l > last_bar.l:
                zigzags.append(last_bar)
                go_up = True
                go_down = False
        # 最高价是否高于last_bar
        if go_up:
            if bar.h < last_bar.h:
                zigzags.append(last_bar)
                go_down = True
                go_up = False
        # 重定义last_bar
        last_bar = bar
#    print (zigzags)
    return pd.DataFrame(zigzags)

def volumeDistribution(bars):
    pv1 = bars.loc[:,['o','v']].rename(columns={'o':'price'})
    pv2 = bars.loc[:,['h','v']].rename(columns={'h':'price'})  
    pv3 = bars.loc[:,['l','v']].rename(columns={'l':'price'})
    pv4 = bars.loc[:,['c','v']].rename(columns={'c':'price'})
    
    return pd.concat([pv1, pv2, pv3, pv4])

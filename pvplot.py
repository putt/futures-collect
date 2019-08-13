import matplotlib.pyplot as plt
from common import traceZig, volumeDistribution
import numpy as np

class PriceVolumePlotter():
    def __init__(self):
        plt.rcParams["figure.figsize"] = 2.5,7.5
        self.fig, self.ax = plt.subplots() 

    def plot(self, symbol, bars):
        self.ax.clear()
        pv = volumeDistribution(bars)
        prices = pv.price
        volumes = pv.v
        current_price = bars.iloc[-1].c
        zigzag = traceZig(bars)
        # 找出zig中所有超出当前价格的阻力点
        ceilings = zigzag.loc[zigzag.h > current_price]
        # 找出zig中所有低于当前价格的支撑点
        floors = zigzag.loc[zigzag.l < current_price]
        
        
        maxp = max(prices)
        minp = min(prices)
        size = int(maxp/(maxp - minp))*2

        bins = np.linspace(minp, maxp, size)

        self.ax.hist(prices, bins=bins, weights=volumes, orientation='horizontal', histtype='step')
        self.ax.hist(ceilings.h, bins=bins, weights=ceilings.v*4, orientation='horizontal', histtype='stepfilled', color='g', edgecolor='w')
        self.ax.hist(floors.l, bins=bins, weights=floors.v*4, orientation='horizontal', histtype='stepfilled', color='r', edgecolor='w')
        self.ax.set_title('{} {}'.format(symbol,bars.index[-1]))
        
        plt.axhline(y=current_price, color='r')
        self.ax.text(max(volumes), current_price, current_price, horizontalalignment='left', color='b')
        plt.yticks(rotation=270, fontsize=10) 
        self.fig.savefig('figures/{}.png'.format(symbol), transparent=True, bbox_inches='tight', pad_inches=0) 
        # self.fig.clear()


if __name__=="__main__":
    pass
import numpy as np
import matplotlib.pyplot as plt

class PriceVolumePlotter():
    def __init__(self):
        
        plt.rcParams["figure.figsize"] = 6,14
        self.fig, self.ax = plt.subplots()


    def plot(self, symbol, current, prices, volumes):
        self.ax.clear()
        size =80
        self.ax.hist(prices, bins=size, weights=volumes, orientation='horizontal', histtype='stepfilled')

        self.ax.set_title('{} {}'.format(symbol,current[0]))
        plt.axhline(y=current[1], color='r')
        self.fig.savefig('figures/'+symbol+ ".png") 
        # self.fig.clear()


if __name__=="__main__":
    pass
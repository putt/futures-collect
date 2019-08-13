import numpy as np
import matplotlib.pyplot as plt

class PriceVolumePlotter():
    def __init__(self):
        plt.rcParams["figure.figsize"] = 3,10
        self.fig, self.ax = plt.subplots() 

    def plot(self, symbol, current, prices, volumes):
        self.ax.clear()
        size =80
        self.ax.hist(prices, bins=size, weights=volumes, orientation='horizontal', histtype='stepfilled')

        self.ax.set_title('{} {}'.format(symbol,current[0]))
        
        plt.axhline(y=current[1], color='r')
        self.ax.text(max(volumes), current[1], current[1], horizontalalignment='left', color='g')
        plt.yticks(rotation=270) 
        self.fig.savefig('figures/'+symbol+ ".png") 
        # self.fig.clear()


if __name__=="__main__":
    pass
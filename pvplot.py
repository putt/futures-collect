import numpy as np
import matplotlib.pyplot as plt




class PriceVolumePlotter():
    def __init__(self):
        
        plt.rcParams["figure.figsize"] = 6,14
        self.fig, self.ax = plt.subplots()


    def plot(self, symbol, current, prices, volumes):
        # the histogram of the data
        # print (volumes)
        self.ax.clear()
#        print(current)
#        print(prices)
#        print(volumes)

#        maxprice = max(prices)
#        minprice = min(prices)
        size =80
#        xnew = np.linspace(minprice,maxprice,size) #300 represents number of points to make between T.min and T.max
#         
#        f = ip.interp1d(prices,volumes,kind='nearest')
        # print (xnew)
        # print (f(xnew))
#        width = (maxprice - minprice)/size
#        self.ax.bar(xnew,f(xnew), align='center', width=width)
        self.ax.hist(prices, bins=size, weights=volumes, orientation='horizontal', histtype='stepfilled')
        
        # self.ax.bar([114540., 117685. ,120830. ,123975. ,127120.], [ 3842.5, 15145.61170213 ,55955.84761905 ,14572.375, 15750])

        # width = (maxprice - minprice)/len(prices)
        # self.ax.bar(prices, volumes, width=width)
        self.ax.set_title('{} {}'.format(symbol,current[0]))
        # self.ax.invert_yaxis()

        # Tweak spacing to prevent clipping of ylabel
        # self.fig.tight_layout()
        plt.axhline(y=current[1], color='r')
        self.fig.savefig('figures/'+symbol+ ".png") 
        # self.fig.clear()


if __name__=="__main__":
    PriceVolumePlotter().plot('aaa',[114540., 117685. ,120830. ,123975. ,127120.], [ 3842.5, 15145.61170213 ,55955.84761905 ,14572.375, 15750])
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as ip
import seaborn as sns



class PriceVolumePlotter():
	def __init__(self):
		self.fig, self.ax = plt.subplots()



	def plot(self, symbol, prices, volumes):
		# the histogram of the data
		# print (volumes)
		# points = np.mgrid[min(prices):max(prices):100j]

		# grid_z0 = griddata(prices, volumes, points, method='nearest')
		# grid_z1 = griddata(prices, volumes, points, method='linear')
		# grid_z2 = griddata(prices, volumes, points, method='cubic')
		self.ax.clear()

		maxprice = max(prices)
		minprice = min(prices)
		size = 300
#		xnew = np.linspace(minprice,maxprice,size) #300 represents number of points to make between T.min and T.max
#		 
#		f = ip.interp1d(prices,volumes,kind='nearest')
		# print (xnew)
		# print (f(xnew))
#		width = (maxprice - minprice)/size
#		self.ax.bar(xnew,f(xnew), align='center', width=width)
		self.ax.hist(prices, bins=100, weights=volumes)
		# self.ax.bar([114540., 117685. ,120830. ,123975. ,127120.], [ 3842.5, 15145.61170213 ,55955.84761905 ,14572.375, 15750])

		# width = (maxprice - minprice)/len(prices)
		# self.ax.bar(prices, volumes, width=width)
		self.ax.set_title(symbol)
		# self.ax.invert_yaxis()

		# Tweak spacing to prevent clipping of ylabel
		# self.fig.tight_layout()
		self.fig.savefig('figures/'+symbol+ ".png") 
		# self.fig.clear()


if __name__=="__main__":
	PriceVolumePlotter().plot('aaa',[114540., 117685. ,120830. ,123975. ,127120.], [ 3842.5, 15145.61170213 ,55955.84761905 ,14572.375, 15750])
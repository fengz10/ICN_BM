from numpy import array
from numpy import arange
import matplotlib.pyplot as plt

params = {'legend.fontsize': 20,
          'legend.linewidth': 2}
plt.rcParams.update(params)



avgPathLenghShortest =  (3, 2.1562, 1.5496, 1.1386, 0.855, 0.6512, 0.4896, 0.3158, 0.22, 0.109, 0)
avgPathNoValley =       (5, 3.3362, 2.1664, 1.4502, 0.9786, 0.7064, 0.5256, 0.3178, 0.2216, 0.109, 0)
# Max hops are always 3, and 5 respectively
# When cacheRatio > 0.6, Max hops sometimes are 2 hops
# When cacheRatio > 0.9, Max hops always are 1 hop
# When cacheRatio = 1,0, Max hops all 0.


             
x1 = arange(0.0, 1.1, 0.1)
plt.plot(x1, avgPathLenghShortest, 'bD-', linewidth=2.5, markersize=15, label='SCM model')
plt.plot(x1, avgPathNoValley, 'k^--', linewidth=3.0, markersize=15, label='GR model')


###设置刻度值
#0, 0.1, 0.2, .. 1.0
plt.xticks(arange(0.0, 1.1, 0.2), ('0.0', '0.2', '0.4', '0.6', '0.8', '1.0'), fontsize=20)
#axes.set_xlim(0.0, 1.1)

plt.yticks([0, 1, 2, 3, 4, 5], (' ', '1', '2', '3', '4', '5'), fontsize=20)


plt.xlabel('Replication size ratio (%)', fontsize=22) 
plt.ylabel('AS hops', fontsize=22)
plt.legend(loc='upper right', numpoints = 1) #upper left



#plt.xlabel('AS number', fontsize=20) 
plt.ylabel('AS hops', fontsize=20)
plt.legend(loc='upper right', numpoints = 1) #upper left

#为图的周边保留空白，如不调整,横坐标的名称挡住了
plt.subplots_adjust(left = 0.08, bottom=0.12)

plt.show()


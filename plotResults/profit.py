from numpy import array
from numpy import arange
import matplotlib.pyplot as plt


params = {'legend.fontsize': 20,
          'legend.linewidth': 2}
plt.rcParams.update(params)

profitOfAS_Shortest =  {3209: [0.0, 76.4, 144.2, 159.0, 137.8, 142.2, 79.2, 52.8, 28.8, 5.6, 0.0], 5400: [0.0, 63.6, 81.0, 80.2, 48.2, 32.4, 18.8, 5.4, 2.0, 0.0, 0.0], 3278: [-1000.0, -895.2, -806.4, -711.6, -600.2, -516.6, -400.6, -289.4, -208.0, -108.4, 0.0], 3216: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 209: [0.0, 65.2, 63.4, 65.0, 28.6, 24.2, 6.8, 1.4, 0.2, 0.0, 0.0], 12052: [1000.0, 531.4, 247.4, 93.0, 41.8, 11.6, 7.0, 0.6, 0.0, 0.0, 0.0], 3320: [0.0, 89.2, 166.4, 218.6, 249.4, 251.4, 239.4, 210.8, 167.2, 102.2, 0.0], 2516: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 3356: [0.0, 69.4, 104.0, 95.8, 94.4, 54.8, 49.4, 18.4, 9.8, 0.6, 0.0], 12989: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 8732: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 2687: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}
profitOfAS_NoValley =  {3209: [0.0, 135.0, 205.2, 221.8, 157.8, 158.2, 90.2, 53.2, 29.6, 5.6, 0.0], 5400: [0.0, -58.6, -61.0, -62.8, -20.0, -16.0, -11.0, -0.4, -0.8, 0.0, 0.0], 3278: [-1000.0, -895.2, -806.4, -711.6, -600.2, -516.6, -400.6, -289.4, -208.0, -108.4, 0.0], 3216: [0.0, 58.6, 61.0, 62.8, 20.0, 16.0, 11.0, 0.4, 0.8, 0.0, 0.0], 209: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 12052: [-1000.0, -531.4, -247.4, -93.0, -41.8, -11.6, -7.0, -0.6, 0.0, 0.0, 0.0], 3320: [2000.0, 1291.6, 848.6, 582.8, 484.2, 370.0, 317.4, 236.8, 178.4, 102.8, 0.0], 2516: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 3356: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 12989: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 8732: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 2687: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}


      
x1 = arange(0.0, 1.1, 0.1)
#plt.plot(x1, profitOfAS_Shortest[3320], 'bo--', linewidth=3.0, markersize=15, label='Shortest path')
#plt.plot(x1, profitOfAS_NoValley[3320], 'r^--', linewidth=3.0, markersize=15, label='No-valley path')
plt.plot(x1, profitOfAS_Shortest[3356], 'ro-', linewidth=2.5, markersize=15, label='AS3356 SCM model')
plt.plot(x1, profitOfAS_NoValley[3356], 'ro--', linewidth=3.0, markersize=15, label='AS3356 GR model')
plt.plot(x1, profitOfAS_Shortest[3216], 'b^-', linewidth=2.5, markersize=15, label='AS3216 SCM model')
plt.plot(x1, profitOfAS_NoValley[3216], 'b^--', linewidth=3.0, markersize=15, label='AS3216 GR model')
plt.plot(x1, profitOfAS_Shortest[5400], 'kd-', linewidth=2.5, markersize=15, label='AS5400 SCM model')
plt.plot(x1, profitOfAS_NoValley[5400], 'kd--', linewidth=3.0, markersize=15, label='AS5400 GR model')



# Enlarge fontsize since the plot needs to expand to include the legend
###设置刻度值
#0, 0.1, 0.2, .. 1.0
plt.xticks(arange(0.0, 1.1, 0.2), ('0.0', '0.2', '0.4', '0.6', '0.8', '1.0'), fontsize=25)
#axes.set_xlim(0.0, 1.1)

plt.yticks([-100, -50, 0, 50, 100, 150], ('-100', '-50', '0', '50', '100', '150'), fontsize=25)


plt.xlabel('Replication size ratio (%)', fontsize=25) 
#plt.xlabel('AS number', fontsize=20) 
plt.ylabel('AS profit ($/period)', fontsize=25)
plt.legend(loc='upper right', numpoints = 1) 

#为图的周边保留空白，如不调整,横坐标的名称挡住了
plt.subplots_adjust(left = 0.13, bottom=0.12)

plt.show()


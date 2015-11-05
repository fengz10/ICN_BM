from numpy import array
from numpy import arange
import matplotlib.pyplot as plt

#ASN = {3356, 7018, 5400, 3209, 12052, 3278)
#c1:Max of Shortest path
#c2:Max of NoValley path
#c3:Avg of Shortest path 
#c4:Avg of NoValley path
c1 = (6, 6, 6, 7, 6, 7)
c2 = (6, 6, 12, 12, 12, 13)
c3 = (2.312932, 2.691949, 2.734262, 2.838720, 3.433186, 3.581726)
c4 = (2.348666, 2.745168, 4.892650, 5.201715, 5.265620, 6.176401)

index = arange(6)
bar_width = 0.2
opacity = 0.8

params = {'legend.fontsize': 20,
          'legend.linewidth': 2}
plt.rcParams.update(params)


plt.bar(index, c1, bar_width,
                 alpha=opacity,
                 color='w',
                 linewidth=2,
                 label='Max. of shortest AS hops',
                 hatch = '\\'
                 )

plt.bar(index + bar_width, c2, bar_width,
                 alpha=opacity,
                 color='gray',
                 linewidth=2,
                 label='Max. of no-valley AS hops',
                 hatch = '/'
                 )

plt.bar(index + 2 * bar_width, c3, bar_width,
                 alpha=opacity,
                 color='w',
                 linewidth=2,
                 label='Avg. of shortest AS hops',
                 #hatch = 'x'
                 )

plt.bar(index + 3 * bar_width, c4, bar_width,
                 alpha=opacity,
                 color='gray',
                 linewidth=2,
                 label='Avg. of no-valley AS hops',
                 hatch = 'x'
                 )

###设置刻度值
#3356, 7018, 5400, 3209, 12052, 3278
plt.xticks(index + 0.4, ('AS 3356', 'AS 7018', 'AS 5400', 'AS 3209',
                               'AS 12052', 'AS 3278'), fontsize=18, rotation=45)

plt.yticks([2, 6, 10, 14, 18, 22], ('2', '6', '10', '14' , '18', '22'),
           fontsize=18)

#plt.xlabel('AS number', fontsize=20) 
plt.ylabel('AS hops', fontsize=20)
plt.legend(loc='upper left', numpoints = 1) #upper left

#为图的周边保留空白，如不调整,横坐标的名称挡住了
plt.subplots_adjust(left = 0.1, bottom=0.16)

plt.show()

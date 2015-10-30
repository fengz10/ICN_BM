#!/usr/bin/python
from GenRouteTable import *
import pickle

# Define the structure of our topology
# ASN: [[providers], [customers], [peers]]
# Our initail topology is too simple, so the shortest path and the no-valley path
# always the same. We use the entier Internet topology instead.
##graph_NoValley = {3356: [[], [5400, 209, 3209], [3320]],
##                  3320: [[], [3278], [3356, 5400, 209, 3209]],
##                  5400: [[3356], [12052], [3320, 209]],
##                  209:  [[3356], [12052], [5400, 3320]],
##                  3209: [[3356], [3278], [3320]],
##                  12052:[[5400, 209], [], []],
##                  3278: [[3320, 3209], [], []]
##         }

f = open('./pickles/NoValleyTopography.dat', 'rb')
graph_NoValley = pickle.load(f)
f.close()

#print graph
# Test the graph structure. Make sure every edge is recorded by two nodes
##for u in graph:
##for v in graph[u][0]:
##    if not u in graph[v][1]:
##        print 'error'
##for v in graph[u][1]:
##    if not u in graph[v][0]:
##        print 'error'
##for v in graph[u][2]:
##    if not u in graph[v][2]:
##        print 'error'

# The Dijkstra function takes a different graph structure as input,
# since it do not care the customer, provider, or peer relationships
##graph_Dijk = {3356: {5400:1, 209:1, 3209:1, 3320:1},
##              3320: {3278:1, 3356:1, 5400:1, 209:1, 3209:1},
##              5400: {3356:1, 12052:1, 3320:1, 209:1},
##              209:  {3356:1, 12052:1, 5400:1, 3320:1},
##              3209: {3356:1, 3278:1, 3320:1},
##              12052:{5400:1, 209:1},
##              3278: {3320:1, 3209:1}
##              }

f = open('./pickles/ShortestPathTopography.dat', 'rb')
graph_Dijk = pickle.load(f)
f.close()


#Test the structure
##for u in graph_Dijk:
##    for v in graph_Dijk[u]:
##        if graph_Dijk[u][v] != 1:
##            print 'error'
##        if not u in graph_Dijk[v]:
##            print 'error'

#Calculate the rout from AS3278 to all other ASes
#RouteShortest and RouteNoValley represent different algorithms
#
# Define the structure of routing table
routeTableShortest = {}
routeTableNoValley = {}
# RouteTable of AS 3278 will be routeTable[3278],
# and it is a dict structure and includes all the path to every AS
# For example, routeTable[3287]={12052:[3278, 3320, 209, 12052],
#                                3320:[3278, 12052]}

asnCare = (3356, 3320, 5400, 209, 3209, 12052, 3278)
for u in asnCare:
    routeTableShortest[u] = GenRouteTable(graph_Dijk, u, 0)

f = open('routeTableShortest.txt', 'w')
pickle.dump(routeTableShortest, f)
f.close()


# For Novalley algorith, since the route is non-symmetric.
# The GenRouteTable(graph_Novalley, 3278, 1) will return the routeTable of
# how other nodes get to 3278. However, we want the route from 3278 to all
# other nodes, so we will call the function with every other nodes as end node.
#routeTableNoValley[3278] = {}


for u in asnCare:
    routeTableTemp = GenRouteTable(graph_NoValley, u, 1)    
    for v in asnCare:
        if not v in routeTableNoValley:
            routeTableNoValley[v] = {}
        routeTableNoValley[v][u] = routeTableTemp[v]

f = open('routeTableNoValley.txt', 'w')
pickle.dump(routeTableNoValley, f)
f.close()

#print 'routeTableNoValley[3278][12052]=', routeTableNoValley[3278][12052]
##print routeTableNoValley[12052]
##print routeTableShortest[12052]
##print routeTableNoValley[12052] == routeTableShortest[12052]
##        
##for u in routeTableNoValley:
##    for v in routeTableNoValley:
##        if len(routeTableNoValley[u][v]) == len(routeTableShortest[u][v]):
##            print u, v
#print routeTableNoValley







              

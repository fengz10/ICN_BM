#!/usr/bin/python
import pickle
from NoValley import *
from ShortestPath import *

############################################################################
# Note, when start equals to end, the route list is start
# When, end is one hop away, whether the list is correct
def GenRouteTable(graph, start, algo):

    #Calculate the rout from AS start to all other ASes, return ASes we care for.
    #RouteShortest and RouteNoValley represent different algorithms.
    #algo: 0 for Shortest path algorithm
    #      1 for NoValley path algorithm
    #      2 for ContentDown path alorithm
    if algo == 0:
        dist, pred = dijkstra(graph, start)
    elif algo == 1:
    # Note: in NoValley algorithm, the start node means the end of content,
    # its the node annouceing reachability, and it is different from the requester node.
    # In the dijkstra algorithm, the route is symmetric
        dist, pred = NoValley(graph, start)
    elif algo == 2:
        dist, pred = ContentDown(graph, start)
    else:
        print 'Algo parameter error!'
        exit()
        
    #print pred
    #print dist
    # Define the structure of routing table
    routeTable = {}
    # RouteTable is a dict structure and includes all the path to every AS
    # For example, routeTable={12052:[3278, 3320, 209, 12052],
    #                                3320:[3278, 12052]}
    
    asnCare = (3356, 3320, 5400, 209, 3209, 12052, 3278)
    for u in asnCare:
        routeTable[u] = []
    for u in asnCare:
        uTemp = u
        while pred[uTemp] != -1:  # until u is the starting node
            routeTable[u].append(uTemp)        
            uTemp = pred[uTemp]
    # Stating from the starting node
    for u in asnCare:
        if len(routeTable[u]) > 0 or u == start:   # Neglect u == start will make rt[u][u] = []
        # Lack of this statement can produce a bug for ContentDown algorithm, since it may has no route
        # from u to node start in this algorithm. The other two algorithms always have a route to start node
            routeTable[u].append(start)
        if algo == 0:
            # For Shortest path, the starting node is no located at the last position, need reverse.
            # For NoValley and ContentDown path, the starting node actually is the end nodes of request.
            routeTable[u].reverse()
    return routeTable
############################################################################
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
routeTableContentDown = {}
# RouteTable of AS 3278 will be routeTable[3278],
# and it is a dict structure and includes all the path to every AS
# For example, routeTable[3287]={12052:[3278, 3320, 209, 12052],
#                                3320:[3278, 12052]}

asnCare = (3356, 3320, 5400, 209, 3209, 12052, 3278)
# Generate the shortest path routeTable for all ASes in asnCare, 
# it will output their routeTable to all other ASes in the graph_Dijk.
# The route list is starting from u to all other ASes

for u in asnCare:
    routeTableShortest[u] = GenRouteTable(graph_Dijk, u, 0)

f = open('routeTableShortest.txt', 'w')
pickle.dump(routeTableShortest, f)
f.close()


# For Novalley and ContentDown algorith, since the route is non-symmetric.
# The GenRouteTable(graph_Novalley, 3278, 1) will return the routeTable of
# how other nodes get to 3278. However, we want the route from 3278 to all
# other nodes, so we will call the function with every other nodes as end node.
#routeTableNoValley[3278] = {}


for u in asnCare:
    routeTableTemp1 = GenRouteTable(graph_NoValley, u, 1) 
    routeTableTemp2 = GenRouteTable(graph_NoValley, u, 2)     
    for v in asnCare:    
    # Only output the route from ASes we care to ASes we care, different from shortest path, which is ASes we care to all ASes
        if not v in routeTableNoValley:
            routeTableNoValley[v] = {}
        routeTableNoValley[v][u] = routeTableTemp1[v]
        if not v in routeTableContentDown:
            routeTableContentDown[v] = {}
        routeTableContentDown[v][u] = routeTableTemp2[v]

f = open('routeTableNoValley.txt', 'w')
pickle.dump(routeTableNoValley, f)
f.close()

f = open('routeTableContentDown.txt', 'w')
pickle.dump(routeTableContentDown, f)
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


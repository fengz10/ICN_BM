#!/usr/bin/python
import string
from ShortestPath import *
graph = {0 : {1:6, 2:8},
         1 : {4:11},
         2 : {3: 9},
         3 : {},
         4 : {5:3},
         5 : {2: 7, 3:4}}

dist, pred = dijkstra(graph, 0)
#dist, pred = floydwarshall(graph)
print 'Shortest distance from each vertex:'
for v in dist:
    print '%s: %s' %(v, dist[v])

#!/usr/bin/python
import string
from ShortestPath import *
import pickle
import sys


if len(sys.argv) < 2:
    print 'No AS number as input!'
    print sys.argv[0] + ' ' + 'ASN'
    sys.exit()


f=open('./20151001.as-rel.txt')
# Storing the AS relationship data into a dictionary struction: graph
# This program treat the data as the following format for the convenience of Floyed-Warshall Algorithms
##graph = {0 : {1:6, 2:8},
##         1 : {4:11},
##         2 : {3: 9},
##         3 : {},
##         4 : {5:3},
##         5 : {2: 7, 3:4}}
# Of course the weight is all 1

graph = {}
while True:    
    line = f.readline()
    if not line:
        break
    if (line[0] == '#'):
        continue
    line = line.split('|')

    # if the relationship flag is error, exit   
    if (string.atoi(line[2]) != 0 and string.atoi(line[2]) != -1):
        print 'the relationship flag error. %s is not allowed'%string.atoi(line[2])
        exit()

    # Adding the provider-customer and p2p relationship
    asn1 = string.atoi(line[0])
    asn2 = string.atoi(line[1])
    # if the asn has alread exit, or been added to graph
    if not (asn1 in graph):
        # Treate an element for the asn        
        graph[asn1] = {}
    if not (asn2 in graph):
        graph[asn2] = {}

    # Adding the edge, and weight is always 1    
    graph[asn1][asn2] = 1
    # A relationship is added twince, for both vetexs
    graph[asn2][asn1] = 1
f.close()
##print 'vertexs connecting to node 1 are:'
##print graph[1]
##print 'All AS number is:'
##print len(graph)
##list = []
##for k in graph:
##    list.append(k)
##print max(list)
##print min(list)
##print len(list)


str = './dist_graph'+sys.argv[1]+'.txt'

#dist, pred = floydwarshall(graph)
dist, pred = dijkstra(graph, string.atoi(sys.argv[1]))
#dist={1:{2:5}}
#print 'the distances of node 1 are:'
#print dist[1]
f = open(str, 'w')
pickle.dump(dist, f)
f.close()

#Print the path to AS 3278
#u = 3278
#while pred[u] > 0:
#    print pred[u]
#    u = pred[u]

    
    

        


       
	   
       
    
       

        

    
       
       


        				

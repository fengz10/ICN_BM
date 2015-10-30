#!/usr/bin/python
import string
from NoValley import *
import pickle
import sys


if len(sys.argv) < 2:
    print 'No AS number as input!'
    print sys.argv[0] + ' ' + 'ASN'
    sys.exit()

f=open('./20151001.as-rel.txt')
# Storing the AS relationship data into a dictionary struction: graph

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
        # Its value is a list, and the list has a provider, customer list, and a peer list in it
        graph[asn1] = [[], [], []]
    if not (asn2 in graph):
        graph[asn2] = [[], [], []]

    if (string.atoi(line[2]) == -1):
        # Add it to customer ASes
        graph[asn1][1].append(asn2)
	# Add it to provider ASes
        graph[asn2][0].append(asn1)
    elif (string.atoi(line[2]) == 0):
        # Add it to peer ASes
        graph[asn1][2].append(asn2)
        graph[asn2][2].append(asn1)
    else:
        print 'relationship flag error!'
        exit()
# The graph structure now has the topology data of the following format:
# graph = {1:[[2,3], [4,5], [6, 7]]}
# The AS 1 has providers of AS 2 and AS 3, customers of AS 4, and 5, and peers of 6 and 7
#print graph        
f.close()

str = './dist_graph_novalley' + sys.argv[1] + '.txt'
#str = './dist_graph_novalley5400.txt'

#dist, pred = floydwarshall(graph)
dist, pred = NoValley(graph, string.atoi(sys.argv[1]))
#dist={1:{2:5}}
#print 'the distances of node 1 are:'
#print dist
f = open(str, 'w')
pickle.dump(dist, f)
f.close()

#Print the path to AS 3278
##print 'Path from AS 3278 to AS %d:'%string.atoi(sys.argv[1])
##u = 3278
##while pred[u] > 0:
##    print pred[u]
##    u = pred[u]

print 'Path from AS 12052 to AS %d:'%string.atoi(sys.argv[1])
u = 12052
while pred[u] > 0:
    print pred[u]
    u = pred[u]
      
            
            
            
        
        
    




           
        

    
    

        


       
	   
       
    
       

        

    
       
       


        				

#!/usr/bin/python
import pickle

#f = open('./pickles/routeTableContentDown.txt', 'r') #pass test
#f = open('./pickles/routeTableNoValley.txt', 'r')   # pass test
f = open('./pickles/routeTableShortest.txt', 'r')  # pass test
rt = pickle.load(f)
f.close()

for u in rt:
    for v in rt[u]:
        if len(rt[u][v]) == 1:
            #print u, '-->', v, rt[u][v]
            assert(u == v)
            assert(rt[u][v][0] == v)
        elif len(rt[u][v]) > 1:
            assert(u != v)
            assert(rt[u][v][0] == u)
            assert(rt[u][v][-1] == v)
        else:
            print '%d to %d has no route'%(u, v) 
        
        

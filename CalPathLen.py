#!/usr/bin/python
import string
import pickle
import sys
import os

asnCare = (8002, 25973, 5400, 14744, 3209, 7713, 1239, 3356, 7018)
# Found Tier3 AS number from Tier2 above
# Tier2: 8002, 25973, 5400, 14744, 3209, 7713
# Tier1: 1239, 3356, 7018
# Tier3: 18854(from 8002), 9304, 19080, 19740, 19854(from 25973)
#        11003, 12052, 12298, 12422 (from 5400)
#        10966, 11922, 13412, 13792, 14216(from 14744)
#        3211, 3278, 8351, 8373 (from 3209)
#        3181, 3382, 4809, 4855 (from 7713)
asnTier3 = (18854, 9304, 11003, 12052, 12298, 10966, 3211, 3278, 8351, 3181)       


for asn in asnCare+asnTier3:
    str1 = './results/dist_graph%s.txt'%asn
    str2 = './results/dist_graph_novalley%s.txt'%asn
    if (not os.path.exists(str1)) or (not os.path.exists(str2)):
        print str1 + 'or' + str2 +' do not exist!'
        continue
    f = open(str1, 'r')
    distFloyd = pickle.load(f)
    f.close()

    f = open(str2, 'r')
    distNoValley = pickle.load(f)
    f.close()

    # dist is a dic structure, the key is destination ASN, the value is the distance to it
    #print type(dist)
    print 'AS number%d'%asn
    print 'The min, max, and average path length of two algorithms to all Internet ASes is:'
    distList1 = distFloyd.values()
    distList2 = distNoValley.values()
    distList1 = [x for x in distList1 if x < 10000] #exclude some unreachable ASes
    distList2 = [x for x in distList2 if x < 10000]
    # To get a average, add a float value
    num1 = 0.0 + len(distList1)
    num2 = 0.0 + len(distList2)
    print 'Shortest Path results: min=%d, max=%d, avg=%f'%(min(distList1), max(distList1), sum(distList1)/num1)
    print 'NoValley Path results: min=%d, max=%d, avg=%f'%(min(distList2), max(distList2), sum(distList2)/num2)


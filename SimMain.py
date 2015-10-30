#!/usr/bin/python
import pickle
import random
import math
import bisect


############################Zipf Generater################################
# The library of numpy.random.zipf or scipy.stats.zipf only work when
# alph > 1
class ZipfGenerator:
    def __init__(self, n, alpha): 
        # Calculate Zeta values from 1 to n: 
        tmp = [1. / (math.pow(float(i), alpha)) for i in range(1, n+1)] 
        zeta = reduce(lambda sums, x: sums + [sums[-1] + x], tmp, [0]) 

        # Store the translation map: 
        self.distMap = [x / zeta[-1] for x in zeta] 

    def next(self): 
        # Take a uniform 0-1 pseudo-random value: 
        u = random.random()  

        # Translate the Zipf variable: 
        return bisect.bisect(self.distMap, u) - 1
#########################################################################
def main(cacheRatio=0.1):
    # Load the routeTable structures
    # For exmple, the routeTable of node 3356
    # routeTable[3356] = {3320:[3356, 209, 2559, 3320], 209:[3356, 3278, 209]}
    asnCare = (3356, 3320, 5400, 209, 3209, 12052, 3278)
    f = open('./pickles/routeTableShortest.txt', 'r')
    routeTableShortest = pickle.load(f)
    f.close()

    f = open('./pickles/routeTableNoValley.txt', 'r')
    routeTableNoValley = pickle.load(f)
    f.close()

    # Compare the path length
    ##for u in asnCare:
    ##    for v in asnCare:
    ##        if routeTableShortest[u][v] != routeTableNoValley[u][v]:
    ##            print '%d---->%d'%(u, v)
    ##            print 'routeTable of Shortest Path:'
    ##            print routeTableShortest[u][v]
    ##            print 'length = ', len(routeTableShortest[u][v])
    ##            print 'routeTable of NoValley Path:'
    ##            print routeTableNoValley[u][v]
    ##            print 'length = ', len(routeTableNoValley[u][v])

    # Generate requests
    cID_MAX = 1000          # Content ID
    alpha = 0.7             # Zipf parameter alpha
    requestNum = 1000        # Number of all requests
    requestNumOfID = [0] * cID_MAX
    zipfGen = ZipfGenerator(cID_MAX-1, alpha)
    for i in range(requestNum):    
        requestNumOfID[zipfGen.next()] += 1

    requestID = [x for x in range(cID_MAX) if requestNumOfID[x] > 0] 
    #print requestID
    #print requestNumOfID

    # Random cache strategy
    cacheSize = cacheRatio * cID_MAX       # Suppose every AS can cache 1% of all contents
    # random.sample for no repeat IDs
    #
    cachedInAS = {}
    for asn in asnCare:
        cachedInAS[asn] = random.sample(range(cID_MAX), int(cacheSize))

    # Generating the path from every node to every contentID according to routeTables
    cRouteTableShortest = {}
    cRouteTableNoValley = {}
    # Suppose all content can be found at desAS
    desAS = 12052

    # Generate content routTables, from node u to content cID
    for u in asnCare:
        cRouteTableShortest[u] = {}
        cRouteTableNoValley[u] = {}
        for cID in range(cID_MAX):
            # Choose the shortest path to cID, and node v has cID cached
            for v in asnCare:
                if cID in cachedInAS[v]:
                    if not cID in cRouteTableShortest[u]:
                        # First encouter cID
                        cRouteTableShortest[u][cID] = routeTableShortest[u][v]
                    else:
                        # There has already a path to cID. Compare the length and
                        # reserve the shortest path
                        if len(routeTableShortest[u][v]) < len(cRouteTableShortest[u][cID]):
                            cRouteTableShortest[u][cID] = routeTableShortest[u][v]
                    # The same process for NoValley path
                    if not cID in cRouteTableNoValley[u]:
                        # First encouter cID
                        cRouteTableNoValley[u][cID] = routeTableNoValley[u][v]
                    else:
                        if len(routeTableNoValley[u][v]) < len(cRouteTableNoValley[u][cID]):
                            cRouteTableNoValley[u][cID] = routeTableNoValley[u][v]

    # Set a default path.
    # Suppose all content can be found at desAS
    # Suppose cID = -1 designate the deault content path
    for u in asnCare:
        cRouteTableShortest[u][-1] = routeTableShortest[u][desAS]
        cRouteTableNoValley[u][-1] = routeTableNoValley[u][desAS]
        
    # Caculate the path length of different requests
    # cPathLength = {3209: {0:3, 1:2}} for {ASN: {cID: pathLength}}
    cPathLengthShortest = {}
    cPathLengthNoValley = {}
    for u in asnCare:
        cPathLengthShortest[u] = {}
        cPathLengthNoValley[u] = {}        
        # Calculate path fro every requested ID    
        for cID in requestID:
            if cID in cRouteTableShortest[u]:
                cPathLengthShortest[u][cID] = len(cRouteTableShortest[u][cID])-1
                # len-1 since the path includes both the source and destination nodes
            else:
                cPathLengthShortest[u][cID] = len(cRouteTableShortest[u][-1])-1
            # The same priciple for cPathLengthNoValley
            if cID in cRouteTableNoValley[u]:
                cPathLengthNoValley[u][cID] = len(cRouteTableNoValley[u][cID])-1
                # len-1 since the path includes both the source and destination nodes
            else:
                cPathLengthNoValley[u][cID] = len(cRouteTableNoValley[u][-1])-1            

    # Substract every length path by one, since the request AS will be one hop away.
    # So the path length will no zeros
    # Commented later, we suppose requester is located in 3278, so zero hops are allowed
##    for u in asnCare:
##        for cID in requestID:
##            cPathLengthShortest[u][cID] += 1
##            cPathLengthNoValley[u][cID] += 1

    print 'On average hops:'
    # Request number times the path length, then divided by request number is the avg hos
    lenTemp = 0.0
    reqNum = 0
    for cID in requestID:
        lenTemp += (requestNumOfID[cID]*cPathLengthShortest[3278][cID])
        reqNum += requestNumOfID[cID]
    avgPathLenghShortest = lenTemp/reqNum

    lenTemp = 0.0
    reqNum = 0
    for cID in requestID:
        lenTemp += (requestNumOfID[cID]*cPathLengthNoValley[3278][cID])
        reqNum += requestNumOfID[cID]
    avgPathLenghNoValley = lenTemp/reqNum

         
                        
    # Calculate the profit of different ASes
    # Pickle load the relatinship structure to judge AS relationship
    # For shortest path algorithm, the requester AS pays the requested AS.
    # For no-valley algorithm, it is determined by their business relationship

    f = open('./pickles/NoValleyTopography.dat', 'rb')
    relationshipGraph = pickle.load(f)
    f.close()

    # Set staring node 3278
    # If want all the ASes nodes as start node, add a level of loop just like the
    # above path length loop. For efficience, we omit it here.
    start = 3278
    profitShortest = {}
    profitNoValley = {}
    for cID in requestID:
        profitShortest[cID] = {}
        profitNoValley[cID] = {}
        
        if cID in cRouteTableShortest[3278]:
            # Calculate profit according to the pat
            rtTemp = cRouteTableShortest[3278][cID]
            # Debug this bug for a while. When content is located in 3278, should continue, unless the total profit will be non-zero
            if len(rtTemp) == 1:
                continue        
            for i in range(len(rtTemp)):
                # The starting AS will pay 1, all other ASes will earn 0 except the last one
                if i == 0:
                    assert(rtTemp[0] == 3278)
                    profitShortest[cID][3278] = -1
                elif i == len(rtTemp)-1:              
                    profitShortest[cID][rtTemp[i]] = 1
                else:
                    profitShortest[cID][rtTemp[i]] = 0
                    
        else:
            rtTemp = cRouteTableShortest[3278][-1]
            if len(rtTemp) == 1:
                continue
            for i in range(len(rtTemp)):
                # The starting AS will pay 1, all other ASes will earn 0 except the last one
                if i == 0:
                    assert(rtTemp[0] == 3278)
                    profitShortest[cID][3278] = -1
                elif i == len(rtTemp)-1:              
                    profitShortest[cID][rtTemp[i]] = 1
                else:
                    profitShortest[cID][rtTemp[i]] = 0


        if cID in cRouteTableNoValley[3278]:
            # Calculate profit according to the path
            # Calculate payment according to relationship
            for asn in cRouteTableNoValley[3278][cID]:
                # Initilizing for accumulating
                profitNoValley[cID][asn] = 0

            rtTemp = cRouteTableNoValley[3278][cID]
            for i in range(len(rtTemp)-1):
                # Judging the relationship between neighbor ASes
                if rtTemp[i+1] in relationshipGraph[rtTemp[i]][0]:
                    profitNoValley[cID][rtTemp[i]] -= 1
                    profitNoValley[cID][rtTemp[i+1]] += 1
                elif rtTemp[i+1] in relationshipGraph[rtTemp[i]][1]:
                    profitNoValley[cID][rtTemp[i]] += 1
                    profitNoValley[cID][rtTemp[i+1]] -= 1
                elif rtTemp[i+1] in relationshipGraph[rtTemp[i]][2]:
                    pass
                else:
                    print 'Neighbor relationship error, %d and %d.'%(profitNoValley[cID][rtTemp[i]], profitNoValley[cID][rtTemp[i+1]])
                    exit()
        else:
            for asn in cRouteTableNoValley[3278][-1]:
                # Initilizing for accumulating
                profitNoValley[cID][asn] = 0

            rtTemp = cRouteTableNoValley[3278][-1]
            for i in range(len(rtTemp)-1):
                # Judging the relationship between neighbor ASes
                if rtTemp[i+1] in relationshipGraph[rtTemp[i]][0]:
                    profitNoValley[cID][rtTemp[i]] -= 1
                    profitNoValley[cID][rtTemp[i+1]] += 1
                elif rtTemp[i+1] in relationshipGraph[rtTemp[i]][1]:
                    profitNoValley[cID][rtTemp[i]] += 1
                    profitNoValley[cID][rtTemp[i+1]] -= 1
                elif rtTemp[i+1] in relationshipGraph[rtTemp[i]][2]:
                    pass
                else:
                    print 'Neighbor relationship error, %d and %d.'%(profitNoValley[cID][rtTemp[i]], profitNoValley[cID][rtTemp[i+1]])
                    exit()

    profitSumShortest = {}
    profitSumNoValley = {}
    # Initializaing profitSumShortest, its structure like {ASN: value}
    for cID in requestID:
        for asn in profitShortest[cID]:
            profitSumShortest[asn] = 0
    for cID in requestID:
        for asn in profitNoValley[cID]:
            profitSumNoValley[asn] = 0
    # Accumulating the profit
    for cID in requestID:
        for asn in profitShortest[cID]:
            profitSumShortest[asn] += profitShortest[cID][asn]* requestNumOfID[cID]

    for cID in requestID:
        for asn in profitNoValley[cID]:
            profitSumNoValley[asn] += profitNoValley[cID][asn]* requestNumOfID[cID]



    print avgPathLenghShortest
    print avgPathLenghNoValley

    print 'Max hops: '
    print max(cPathLengthShortest[3278].values())
    print max(cPathLengthNoValley[3278].values())
            
    print profitSumShortest
    print profitSumNoValley
            
    print 'sum'
    print sum(profitSumShortest.values())
    print sum(profitSumNoValley.values())

    return avgPathLenghShortest, avgPathLenghNoValley, profitSumShortest, profitSumNoValley
###############################################################################################                
# Record the average results by running 5 times
avgPL_Shortest = []
avgPL_NoValley = []
profitSumShortestSum = {}
profitSumNoValleySum = {}
for i in range(5):
    avgPathLenghShortest, avgPathLenghNoValley, profitSumShortest, profitSumNoValley = main(1.0)
    avgPL_Shortest.append(avgPathLenghShortest)
    avgPL_NoValley.append(avgPathLenghNoValley)
    for asn in (profitSumShortest):
        if not asn in profitSumShortestSum:
            profitSumShortestSum[asn] = profitSumShortest[asn]
        else:
            profitSumShortestSum[asn] += profitSumShortest[asn]

    for asn in (profitSumNoValley):
        if not asn in profitSumNoValleySum:
            profitSumNoValleySum[asn] = profitSumNoValley[asn]
        else:
            profitSumNoValleySum[asn] += profitSumNoValley[asn]

# Calculate Avg
print 'Average result of 5 times: '
print 'avgPathLenghShortest = ', sum(avgPL_Shortest)/5
print 'avgPathNoValley = ', sum(avgPL_NoValley)/5
print 'Original List data:'
print 'avgPL_Shortest', avgPL_Shortest
print 'avgPL_NoValley',  avgPL_NoValley


profitSumShortestAvg = {}
for asn in profitSumShortestSum:
    profitSumShortestAvg[asn] = profitSumShortestSum[asn]/5.0

profitSumNoValleyAvg = {}
for asn in profitSumNoValleySum:
    profitSumNoValleyAvg[asn] = profitSumNoValleySum[asn]/5.0

print 'profitSumShortestAvg =', profitSumShortestAvg
print 'profitSumNoValleyAvg =', profitSumNoValleyAvg








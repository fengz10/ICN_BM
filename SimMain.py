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
# Judge the relationship between asn1 and asn2 
# Return -1: asn1 is asn2's provider  #Same as the value in CAIDA dataset
#         0: asn1 is asn2's peer
#         1: asn1 is asn2's customer
#        -2: no direction relationship
def RelationshipAS(graph, asn1, asn2):
    if asn1 in graph[asn2][0]:    # 0 for asn2's provider list
        assert(asn2 in graph[asn1][1])
        return -1
    elif asn1 in graph[asn2][1]:
        assert(asn2 in graph[asn1][0])
        return 1
    elif asn1 in graph[asn2][2]:
        assert(asn2 in graph[asn1][2])
        return 0
    else:
        return -2
####################################################################################
# Input algorithm, output its path length and profit
# algo = 0:  shortest path
#      = 1:  NoValley path
#      = 2:  ContentDown path
def CalculatePathLenProfit(asnCare, cachedInAS, requestID, algo = 0, desAS = 12052, start = 3278):
    # Load the routeTable structures
    # For exmple, the routeTable of node 3356
    # routeTable[3356] = {3320:[3356, 209, 2559, 3320], 209:[3356, 3278, 209]}
    # Suppose all content can be found at desAS
    
    if algo == 0:
        f = open('./pickles/routeTableShortest.txt', 'r')
    elif algo == 1:
        f = open('./pickles/routeTableNoValley.txt', 'r')
    elif algo == 2:
        f = open('./pickles/routeTableContentDown.txt', 'r')
    else:
        print 'Algo error!'
        exit()
    rt = pickle.load(f)
    f.close()                

    # Generating the path from every node to every contentID according to routeTables
    cRT = {}
    
    # Pickle load the relatinship structure to judge AS relationship
    f = open('./pickles/NoValleyTopography.dat', 'rb')
    graph_relation = pickle.load(f)
    f.close()

    # Generate content routTables, from node u to content cID
    # Pay special attention to the following loop, since it has bugs easily
    for u in asnCare:
        cRT[u] = {}
        for cID in requestID:   # Only need to generate routeTable for requestID #range(cID_MAX):
            # Choose the shortest path to cID, and node v has cID cached
            for v in asnCare:
                if not cID in cachedInAS[v]:
                    break
                
                if algo == 0:
                    # Shortest path is relatively easy, since the routing is symmetric
                    # cID is replicated in AS v
                    if not cID in cRT[u]:
                        # First encouter cID
                        cRT[u][cID] = rt[u][v]
                    else:
                        # There has already a path to cID. Compare the length and
                        # keep the shortest path
                        if len(rt[u][v]) < len(cRT[u][cID]):
                            cRT[u][cID] = rt[u][v]
                elif algo == 1 or algo == 2:
                    # The same process for NoValley and ContentDown path
                    if not cID in cRT[u]:
                        # First encouter cID
                        if len(rt[u][v]) > 0:
                            cRT[u][cID] = rt[u][v]
                    else:
                        # If the new route's first step is from peer, and the old one is not, use the peer one
                        # If they all are from providers, use shorter one
                        assert(len(cRT[u][cID]) >= 1)
                        if len(rt[u][v]) == 0:
                            pass    # No route from u to v
                        elif len(cRT[u][cID]) == 1:
                            pass    # Content is in AS u, already is the best route
                        elif len(rt[u][v]) == 1:
                            assert(rt[u][v][0] == u)
                            cRT[u][cID] = [u]   # Best route appears
                        elif RelationshipAS(graph_relation, cRT[u][cID][1], u)==0:
                            pass     # Peer route for AS u is the second best route, and keep it
                        elif RelationshipAS(graph_relation, rt[u][v][1], u) == 0:
                            cRT[u][cID] = rt[u][v]  # Found peer route
                        elif len(rt[u][v]) < len(cRT[u][cID]):  
                            cRT[u][cID] = rt[u][v]
                        else:
                            pass
                else:
                    print 'Algo value error!'
                    exit()

    # Set a default path.
    # Suppose all content can be found at desAS
    # Suppose cID = -1 designate the deault content path
    for u in asnCare:
        if algo == 0 or algo == 1:
            cRT[u][-1] = rt[u][desAS]
        elif algo == 2:
            # The default route is not in routeTableNoValley[u][desAS]
            # Since in the content down path algorithm, not all content are reachable (i.e. not all node are reachable)
            # We should use the NoValley path ot destination AS
            fTemp = open('./pickles/routeTableNoValley.txt', 'r')
            rtNoValley = pickle.load(f)            
            fTemp.close()
            cRT[u][-1] = rtNoValley[u][desAS] 
        else:
            print 'Algo value error!'
            exit()
        
       
    # Caculate the path length of different requests
    # cPathLength = {3209: {0:3, 1:2}} for {ASN: {cID: pathLength}}
    cPathLen = {} 
    for u in asnCare:
        cPathLen[u] = {}
        # Calculate path fro every requested ID    
        for cID in requestID:
            if cID in cRT[u]:
                cPathLen[u][cID] = len(cRT[u][cID])-1
                # len-1 since the path includes both the source and destination nodes
            else:
                cPathLen[u][cID] = len(cRT[u][-1])-1
    

    # Substract every length path by one, since the request AS will be one hop away.
    # So the path length will no zeros
    # Commented out later, we suppose requester is located in 3278, so zero hops are allowed
##    for u in asnCare:
##        for cID in requestID:
##            cPathLengthShortest[u][cID] += 1
##            cPathLengthNoValley[u][cID] += 1
    
    ### Calculating profit below
    # If want all the ASes nodes as start node, add a level of loop just like the
    # above path length loop. For efficience, we omit it here.
    
    profit = {}
    # The business model of SCM or NoValley
    # The shortest path and Content down path belong to the SCM catogory
    if algo == 0:   
        for cID in requestID:
            profit[cID] = {}    
            if cID in cRT[start]:
                # Calculate profit according to the pat
                rtTemp = cRT[start][cID]
            else:
                rtTemp = cRT[start][-1]
                
            # Debug this bug for a while. When content is located in 3278, should continue, unless the total profit will be non-zero
            if len(rtTemp) == 1:
                continue        
            for i in range(len(rtTemp)):
                # The starting AS will pay 1, all other ASes will earn 0 except the last one
                if i == 0:
                    assert(rtTemp[0] == start)
                    profit[cID][start] = -1
                elif i == len(rtTemp)-1:              
                    profit[cID][rtTemp[i]] = 1
                else:
                    profit[cID][rtTemp[i]] = 0
    elif algo == 1 or algo == 2:
        for cID in requestID:
            profit[cID] = {}
            
            if cID in cRT[start]:
                # Calculate profit according to the path
                # Calculate payment according to relationship
                for asn in cRT[start][cID]:
                    # Initilizing for accumulating
                    profit[cID][asn] = 0
                rtTemp = cRT[start][cID]
            else:
                for asn in cRT[start][-1]:
                    # Initilizing for accumulating
                    profit[cID][asn] = 0
                rtTemp = cRT[start][-1]            
               
            for i in range(len(rtTemp)-1):
                # Judging the relationship between neighbor ASes
                relationFlg = RelationshipAS(graph_relation, rtTemp[i+1], rtTemp[i])
                if relationFlg == -1:
                    profit[cID][rtTemp[i]] -= 1
                    profit[cID][rtTemp[i+1]] += 1
                elif relationFlg == 1:
                    profit[cID][rtTemp[i]] += 1
                    profit[cID][rtTemp[i+1]] -= 1
                elif relationFlg == 0:
                    pass
                else:
                    print 'Neighbor relationship error, %d and %d.'%(profitNoValley[cID][rtTemp[i]], profitNoValley[cID][rtTemp[i+1]])
                    exit()
 
    else:
        print 'Algo value error!'
        exit()


    return cPathLen, profit

######################################################################################
# Generate different distributions, and return the results
# input cacheRatio: the percentage of replication from 0.0 to 1.0
#
def main(cacheRatio=0.1):

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
    asnCare = (3356, 3320, 5400, 209, 3209, 12052, 3278)
    cachedInAS = {}
    for asn in asnCare:
        cachedInAS[asn] = random.sample(range(cID_MAX), int(cacheSize))
    # Set staring node 3278
    start = 3278

    cPathLengthShortest, profitShortest = CalculatePathLenProfit(asnCare, cachedInAS, requestID, 0)
    cPathLengthNoValley, profitNoValley = CalculatePathLenProfit(asnCare, cachedInAS, requestID, 1)
    print 'On average hops:'
    # Request number times the path length, then divided by request number is the avg hos
    lenTemp = 0.0
    reqNum = 0
    for cID in requestID:
        lenTemp += (requestNumOfID[cID]*cPathLengthShortest[start][cID])
        reqNum += requestNumOfID[cID]
    avgPathLenghShortest = lenTemp/reqNum

    lenTemp = 0.0
    reqNum = 0
    for cID in requestID:
        lenTemp += (requestNumOfID[cID]*cPathLengthNoValley[start][cID])
        reqNum += requestNumOfID[cID]
    avgPathLenghNoValley = lenTemp/reqNum
                        
    # Calculate the profit of different ASes    
    # For shortest path algorithm, the requester AS pays the requested AS.
    # For contentDown algorithm, it is determined by their business relationship

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
    print max(cPathLengthShortest[start].values())
    print max(cPathLengthNoValley[start].values())
            
    print profitSumShortest
    print profitSumNoValley
            
    assert(sum(profitSumShortest.values()) == 0)
    assert(sum(profitSumNoValley.values()) ==0)

    return avgPathLenghShortest, avgPathLenghNoValley, profitSumShortest, profitSumNoValley
###############################################################################################                
# Record the average results by running 5 times
avgPL_Shortest = []
avgPL_NoValley = []
profitSumShortestSum = {}
profitSumNoValleySum = {}
for i in range(5):
    avgPathLenghShortest, avgPathLenghNoValley, profitSumShortest, profitSumNoValley = main(0.1)
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








# The graph structure now has the topology data of the following format:
# graph = {1:[[2,3], [4,5]]}
# The AS 1 has custumers of AS 2 and AS 3, and peers of AS 4, and 5
#print graph
# NoValley and prefer-customer algorithm
# Refer to paper "The Extent of Path Inflation by Routing Policies"
# The idea of the algorithm
# 1. Intitialize S = {s}, all path be infinity
# 2. Propagate routes from customers to provider and sibling iteratively
# Select the node with smallest path length and add the node into S
# 3. Propagate routes to peers
# 4. Propagate routes from providers to customers and from sibling to sibling iteratively
############################################################################################
def popmin(pqueue):
    # A (ascending or min) priority queue keeps element with
    # lowest priority on top. So pop function pops out the element with
    # lowest value. It can be implemented as sorted or unsorted array
    # (dictionary in this case) or as a tree (lowest priority element is
    # root of tree)
    lowest = 100000
    keylowest = None
    for key in pqueue:
        if pqueue[key] < lowest:
            lowest = pqueue[key]
            keylowest = key
    if keylowest == None:
        return None
    del pqueue[keylowest]
    return keylowest
################################################################################
def popElem(pqueue, v):
    del pqueue[v]

############################################################################################
def NoValley(graph, start):
    # Using priority queue to keep track of minium distance from start
    # to a vertex.
    pqueue = {} # vertex: distance to start
    dist = {}   # vertex: distance to start
    pred = {}   # vertex: previous (predecesor) vertex in shortest path
    MAX_DIST = 100000
    
    # initializing dictionaries
    for v in graph:
        dist[v] = MAX_DIST
        pred[v] = -1
    dist[start] = 0
    for v in graph:
        pqueue[v] = dist[v] # equivalent to push into queue

    while pqueue:
        # for priority queues, pop will get the element with smallest value
        u = popmin(pqueue)
        if u == None:
            break
        # 1. Propagate to providers
        for v in graph[u][0]:
            newdist = dist[u] + 1
            if (newdist < dist[v]):
                pqueue[v] = newdist
                dist[v] = newdist
                pred[v] = u
        # If all the distance is larger than MAX, go phase 2
        #if min(pqueue.values()) == MAX_DIST:
        #    break


        
    # 2. Propagate to peers
    # Nodes that has been poped from the queue in the above process
    # Inxcludeing node start
    # Find their peer nodes
    for u in set(graph.keys())-set(pqueue.keys()):
        for v in [x for x in graph[u][2] if x in pqueue]:
            dist[v] = dist[u] + 1
            pred[v] = u
            pqueue[v] = dist[u] + 1
            popElem(pqueue, v)
    # 3. Propagate to customers
    # Firstly, we should initialize the node in pqueue again.
    # For now they are all MAX_DIST
    # Use the nodes outside the pqueue to initiate it

##    uu = 3320  #for test
##    print 'After customer'
##    while pred[uu] > 0:
##        print pred[uu]
##        uu = pred[uu]


    for u in set(graph.keys())-set(pqueue.keys()): #Initializing
        for v in [x for x in graph[u][1] if x in pqueue]:
            newdist = dist[u] + 1
            if newdist < dist[v]:
                dist[v] = newdist                
                pqueue[v] = newdist
                pred[v] = u


    # Finding the shortest length of customers            
    while pqueue:
        u = popmin(pqueue)
        if u == None:
            break
        for v in graph[u][1]:
            newdist = dist[u] + 1
            if (newdist < dist[v]):
                pqueue[v] = newdist
                dist[v] = newdist
                pred[v] = u
    return dist, pred
##############################################################################  

from NoValley import *
from ShortestPath import *

############################################################################
def GenRouteTable(graph, start, algo):

    #Calculate the rout from AS start to all other ASes
    #RouteShortest and RouteNoValley represent different algorithms
    #algo: 0 for Shortest path algorithm
    #      1 for NoValley path algorithm
    if algo == 0:
        dist, pred = dijkstra(graph, start)
    elif algo == 1:
    # Note: in NoValley algorithm, the start node means the end of content,
    # its the node annouceing reachability, and it is different from the requester node.
    # In the dijkstra algorithm, the route is symmetric
        dist, pred = NoValley(graph, start)
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
        routeTable[u].append(start)
        if algo == 0:
            # For Shortest path, the starting node is no located at the last position, need reverse.
            # For NoValley path, the starting node actually is the end nodes of request.
            routeTable[u].reverse()
    return routeTable
############################################################################


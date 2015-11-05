import pickle
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
    #from SimMain import RelationshipAS
f = open('./pickles/NoValleyTopography.dat', 'rb')
graph_relation = pickle.load(f)
f.close()

print RelationshipAS(graph_relation, 3356, 5400)

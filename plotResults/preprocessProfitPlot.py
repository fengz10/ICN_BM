
# The original data, profitSumShortestAvg1 means cache ratio of 0.1, profitSumShortestAvg2 means 0.2
profitSumShortestAvg0 = {3320: 0.0, 209: 0.0, 12052: 1000.0, 3278: -1000.0}
profitSumNoValleyAvg0 = {3278: -1000.0, 2516: 0.0, 3320: 2000.0, 12052: -1000.0, 12989: 0.0, 2687: 0.0}
profitSumShortestAvg1 = {3209: 76.4, 3278: -895.2, 209: 65.2, 12052: 531.4, 5400: 63.6, 3356: 69.4, 3320: 89.2}
profitSumNoValleyAvg1 = {3209: 135.0, 8732: 0.0, 3278: -895.2, 3216: 58.6, 209: 0.0, 12052: -531.4, 3320: 1291.6, 2516: 0.0, 3356: 0.0, 12989: 0.0, 5400: -58.6, 2687: 0.0}
profitSumShortestAvg2 = {3209: 144.2, 3278: -806.4, 209: 63.4, 12052: 247.4, 5400: 81.0, 3356: 104.0, 3320: 166.4}
profitSumNoValleyAvg2 = {3209: 205.2, 3278: -806.4, 3216: 61.0, 209: 0.0, 12052: -247.4, 3320: 848.6, 5400: -61.0, 2516: 0.0, 3356: 0.0, 12989: 0.0, 8732: 0.0, 2687: 0.0}
profitSumShortestAvg3 = {3209: 159.0, 3278: -711.6, 209: 65.0, 12052: 93.0, 3320: 218.6, 3356: 95.8, 5400: 80.2}
profitSumNoValleyAvg3 = {3209: 221.8, 3278: -711.6, 3216: 62.8, 209: 0.0, 12052: -93.0, 3320: 582.8, 5400: -62.8, 2516: 0.0, 3356: 0.0, 12989: 0.0, 8732: 0.0, 2687: 0.0}
profitSumShortestAvg4 = {3209: 137.8, 3278: -600.2, 209: 28.6, 12052: 41.8, 5400: 48.2, 3356: 94.4, 3320: 249.4}
profitSumNoValleyAvg4 = {3209: 157.8, 3278: -600.2, 12989: 0.0, 3216: 20.0, 209: 0.0, 12052: -41.8, 5400: -20.0, 2516: 0.0, 3356: 0.0, 3320: 484.2, 8732: 0.0, 2687: 0.0}
profitSumShortestAvg5 = {3209: 142.2, 3278: -516.6, 209: 24.2, 12052: 11.6, 5400: 32.4, 3356: 54.8, 3320: 251.4}
profitSumNoValleyAvg5 = {3209: 158.2, 3278: -516.6, 3216: 16.0, 209: 0.0, 12052: -11.6, 3320: 370.0, 5400: -16.0, 2516: 0.0, 3356: 0.0, 12989: 0.0, 8732: 0.0, 2687: 0.0}
profitSumShortestAvg6 = {3209: 79.2, 3278: -400.6, 209: 6.8, 12052: 7.0, 3320: 239.4, 3356: 49.4, 5400: 18.8}
profitSumNoValleyAvg6 = {3209: 90.2, 3278: -400.6, 3216: 11.0, 209: 0.0, 12052: -7.0, 3320: 317.4, 5400: -11.0, 2516: 0.0, 3356: 0.0, 12989: 0.0, 8732: 0.0, 2687: 0.0}
profitSumShortestAvg7 = {3209: 52.8, 3278: -289.4, 209: 1.4, 12052: 0.6, 5400: 5.4, 3356: 18.4, 3320: 210.8}
profitSumNoValleyAvg7 = {3209: 53.2, 3278: -289.4, 3216: 0.4, 209: 0.0, 12052: -0.6, 3320: 236.8, 2516: 0.0, 2687: 0.0, 3356: 0.0, 12989: 0.0, 5400: -0.4, 8732: 0.0}
profitSumShortestAvg8 = {3209: 28.8, 3278: -208.0, 209: 0.2, 5400: 2.0, 3356: 9.8, 3320: 167.2}
profitSumNoValleyAvg8 = {3209: 29.6, 3278: -208.0, 3216: 0.8, 209: 0.0, 3320: 178.4, 3356: 0.0, 5400: -0.8, 8732: 0.0}
profitSumShortestAvg9 = {3320: 102.2, 3209: 5.6, 3356: 0.6, 3278: -108.4}
profitSumNoValleyAvg9 = {3320: 102.8, 3209: 5.6, 3356: 0.0, 3278: -108.4}
profitSumShortestAvg10 = {}
profitSumNoValleyAvg10 = {}

profitSumShortestAvg = []
profitSumNoValleyAvg = []
# We want know for each AS, its profit change trend.
for i in range(11):
    print 'profitSumNoValleyAvg%d'%i
    exec('profitSumShortestAvg.append(profitSumShortestAvg%d)'%i)
    exec('profitSumNoValleyAvg.append(profitSumNoValleyAvg%d)'%i)



# Firstly, generate the AsnCare list, and insert 0.0 for non existed ASNs in profitSum structures
asnCare = []
for dic in profitSumShortestAvg:
    asnCare += dic.keys()
    
for dic in profitSumNoValleyAvg:
    asnCare += dic.keys()

asnCare = set(asnCare)
print asnCare
print len(asnCare)

for dic in profitSumShortestAvg:
    for asn in asnCare:
        if not asn in dic:
            dic[asn] = 0.0

for dic in profitSumNoValleyAvg:
    for asn in asnCare:
        if not asn in dic:
            dic[asn] = 0.0

######################################################
# Calculate profit for each AS

profitOfAS_Shortest = {}
for dic in profitSumShortestAvg:
    for asn in dic:
        if not asn in profitOfAS_Shortest:
            profitOfAS_Shortest[asn] = []            
        profitOfAS_Shortest[asn].append(dic[asn])

profitOfAS_NoValley = {}
for dic in profitSumNoValleyAvg:
    for asn in dic:
        if not asn in profitOfAS_NoValley:
            profitOfAS_NoValley[asn] = []            
        profitOfAS_NoValley[asn].append(dic[asn])

print 'profitOfAS_Shortest = ', profitOfAS_Shortest
print 'profitOfAS_NoValley = ', profitOfAS_NoValley

##print 'len'
##for asn in asnCare:
##    print len(profitOfAS_Shortest[asn])
##    print len(profitOfAS_NoValley[asn])


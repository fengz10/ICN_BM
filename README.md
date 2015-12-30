## Copyright 
Written by Zhen Feng of Tsinghua University
Copyright GPLv2
The code is written for the simulation experiment of my research papers.
Dataset is from CAIDA

## File description
### 1. ShortestPath.py
Define two algorithms to calculate the shortest path: Dijkstra and Floyd.
### 2. NoValley.py
Calculate all the no-valley path from a given AS to all ASes in the Internet.
### 3. AlgoShortestPath.py
Read the topology data into a dict structure, then recall the shortest path functions to compute the shortest path from a input AS to all ASes in the Internet, finally store the result into a pickle file of the current directory.
### 4. AlgoNoValley.py
The differences from the above the AlgoShortestPath.py file is that it calculate the no-valley path rather than the shortest path, also, the graph structure is different for the two algorithms.
### 5. CalPathLen.py
For a given AS, read the corresponding pickle file, calculate the average, max, and min AS hops.

### The above programs calculate the path length from designated ASes to all other ASes.
### The below programs calculate the path length and profit in a scoped topology around ASes we care for.

### 6. GenRouteTable.py
Generate route table for all ASes you care.
algo=0 for shortest path.
algo=1 for no-valley path.
algo=2 for content-down path. Contents replicated only announce to peers and customers.
Since the shortest path is symmetric, so the route is recored in pred structure, but it needs to reverse.
For NoValley path, the start node of the function is actually the sink node, so additional loops are needed to record every node. The pred structure does not need to reverse.
### 7. SimMain
The main simulation procedure.
Generate request number, distribution, cache size, cache ratio, and etc.
It will output the path length and profit of the two different algorithms (shortest or no-valley) for ASes you care for.

### 8. Fixed bugs:
pickle reads error: caused by without write it correctly, such as close file uncorrectly.
content route table error: without consider that the route table might be empty (i.e., some nodes are unreachable). This situation happens in the content down path algorithm. Since I add the origin node for all path, it makes that some unreachable path is reachable one step away.
Too simple topology: it makes the differet algorithm nearly the same performance. Later I use the real Internet dataset, and focus on several ASes.

## Note: test every function before use it. Make sure it works right, especially for some particular parameters. For example, whether the first step and last step nodes is the same as we expected.





from generateNeighbours import GenerateGraph
from tabuSearch import tabu

graph = GenerateGraph('FULL_MATRIX', 5, 50)
dist, path = graph.two_opt()
iterations = 50
maxSizeTabu = 100
print(graph)
print(dist)
print(path)
tabu(graph, dist, path, iterations, maxSizeTabu)
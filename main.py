from generateNeighbours import GenerateGraph
from tabuSearch import tabuAlgorithm

graph = GenerateGraph('FULL_MATRIX', 10, 50)
#GenerateGraph.neighbourhood(graph)
path = graph.two_opt()
iterations = 1000
maxSizeTabu = 1000
# print(graph.matrix)
# print(dist)
print(path)
print(graph.cost(path))
tabuAlgorithm(graph, path, iterations, maxSizeTabu)
from generateNeighbours import GenerateGraph
from tabuSearch import tabu

graph = GenerateGraph('FULL_MATRIX', 5, 50)
#GenerateGraph.neighbourhood(graph)
path = graph.two_opt()
iterations = 50
maxSizeTabu = 7
# print(graph.matrix)
# print(dist)
# print(path)
tabu(graph, path, iterations, maxSizeTabu)
import generateNeighbours


def getNeighborhood(graph, solution):
    save = []

    path = solution
    firstCost = graph.cost(path) #nie trzeba liczyc drugi raz, można przekazać
    save.append([0,0,firstCost])

    for i in range(len(path)-1):
        for j in range(len(path)-(i+1)):
            path[i:(i+j+2)] = path[i:(i+j+2)][::-1]
            Cost = graph.cost(path)

            save.append([i,i+j+1,Cost])
            path[i:(i+j+2)] = path[i:(i+j+2)][::-1]

    print(save)
    return save

def decodeNeighbour(solution, candidate):
    path = []
    index1 = candidate[0]
    index2 = candidate[1]
    # solution = [0, 1, 2, 3, 4, 5]
    # index1 = 0
    # index2 = 4
    for i in range(0, index1):
        path.append(solution[i])
    for i in range(index2, index1-1, -1):
        path.append(solution[i])
    for i in range(index2+1, len(solution)):
        path.append(solution[i])

    print(path)
    return path

def getBestCandidate(neighborhood, tabuList, solution):
    bestCandidate = neighborhood[0]
    for i in range(0,len(neighborhood)): #dla każdego sąsiada
        neighbour = decodeNeighbour(solution, neighborhood[i])
        if (neighbour not in tabuList) and (neighborhood[i][2] < bestCandidate[2]): #mniejszy cost
            bestCandidate = neighbour

    return neighbour

def tabu(graph, firstPath, iterations, maxSizeTabu):
    solution = firstPath #bieżące rozw
    bestSolutionInProgram = solution #najlepsze do tej pory
    tabuList = list()
    tabuList.append(solution)
    numberOfIterations = 0

    while numberOfIterations < iterations: # wypróbować inne warunki stopu
        neighborhood = getNeighborhood(graph, solution) #w czasie generowania neighborhood można by nie liczyć cost
        #można by najpierw usunąc z neighborhood te elemnty ktore są w tabu i dopiero liczyć koszty

        solution = getBestCandidate(neighborhood, tabuList, solution) # best solution in this iteration
        tabuList.append(solution)
        if (graph.cost(solution) < graph.cost(bestSolutionInProgram)):
            bestSolutionInProgram = solution

        if(len(tabuList) > maxSizeTabu):
            tabuList.pop(0)

        numberOfIterations += 1

    return bestSolutionInProgram, graph.cost(bestSolutionInProgram)

from copy import deepcopy
from generateNeighbours import GenerateGraph


def pathToString(path):
    s = ""
    for i in range(0, len(path)):
        s += str(path[i])
        s += ","

    #print(s)
    return s

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

#funkcja łączy krok tworzenia sąsiedztwa i wybór najlepszego kandydata, czyli jest zamiennikiem funkcji getNeighborhood,
# i getBestCandidate, tzw. akceleracja
def getBestCandidateFromNeighborhood(graph, tabu, solution):

    firstPath = solution
    path = solution
    bestCandidate = None
    bestCandidateCost = 0

# dodać ograniczenie generowania sasiadów, np. zliczanie ile już ich jest i przerwanie pętli po osiągnięciu liczby
# sąsiadów, którą chcemy albo ograniczenie for - range(0.2*len(path)-1)
    #print("przeszukuje sąsiedztwo")
    for i in range(len(path)-1):
        for j in range(len(path)-(i+1)):
            path[i:(i+j+2)] = path[i:(i+j+2)][::-1]
            if pathToString(path) not in tabu:
                #print("path", path, " not in tabu")
                if bestCandidate == None:
                    #print("najlepszy kandydat jest None, podmieniam o długości ",graph.cost(path))
                    bestCandidate = deepcopy(path)
                    bestCandidateCost = graph.cost(bestCandidate)
                elif graph.cost(path) < bestCandidateCost:
                    #print("znalazłam lepszego kandydata ", path)
                    #print("jego długość ", graph.cost(path))
                    bestCandidate = deepcopy(path)
                    bestCandidateCost = graph.cost(bestCandidate)
            # kryterium aspiracji
            # else:
            #   if graph.cost(path) < graph.cost(firstPath)
            #      bestCandidate = deepcopy(path)
            #      bestCandidateCost = graph.cost(bestCandidate)

            path[i:(i+j+2)] = path[i:(i+j+2)][::-1]

    #print("najlepszy z sąsiadów to: ", bestCandidate)
    return bestCandidate, bestCandidateCost

def getRandomNotTabuSolution(graph, tabu):
    path = graph.k_random_method()
    counter = 0
    while (pathToString(path) in tabu) and counter < len(path):
        path = graph.k_random_method()
        counter += 1

    if counter == len(path):
        print("prawie wszystkie dostępne rozwiązania są w tabu")
        return None
    else:
        return path

def getLastGoodSolution(graph, tabu, backTrackingList):
    if not backTrackingList:
        print("losuję nowe rozwiązanie początkowe")
        path = getRandomNotTabuSolution(graph, tabu)
        if path == None:
            return None, 0
        else:
            return path, graph.cost(path)
    else:
        print("backtarcking nie jest pusta")
        solution, solutionCost = getBestCandidateFromNeighborhood(graph, tabu, backTrackingList[-1])
        if solution == None:
            print("to rozwiązanie nie ma sąsiadów")
            backTrackingList.pop()
            return getLastGoodSolution(graph, tabu, backTrackingList)
        else:
            return solution, solutionCost

def tabuAlgorithm(graph, firstPath, iterations, maxSizeTabu):
    #największy problem, że niektóre takie same ścieżki wykrywa jako różne, np. 1,2,3,4,5 a 3,4,5,1,2 - jest to cykl
    #Hamiltona mają taką samą długość, ta sama ścieżka tylko w innym miejscu zaczynamy

    solution = firstPath #bieżące rozwiązanie
    bestSolutionInProgram = solution #najlepsze do tej pory
    backTrackingList = [] #lista najlepszych rozwiązań, można by ustalić jej maksymalną długość i usuwać najstarsze
    backTrackingList.append(bestSolutionInProgram)

    tabu = {} #tabu jako dictionary - w pythonie dict jest hash table, przeszukiwanie w niej jest w czasie stałym
    # klucze - ściezki jako stringi, wartości - długości ścieżek
    # system nawrotów przy użyciu backtracking działa dobrze, gdy lista tabu jest długa(czyli znajduje się na niej kilka
    # rozwiązań które były tuż po ostatnim najlepszym rozwiązaniu, przy krótkiej liście tabu należy dla każdego elementu
    # z backtrackinglist przypisać kilka rozwiązań, które były po nim (ozn. przez listAfter), wtedy gdy wybierzemy
    # jakieś rozwiązanie z backTrackingList to do tabu należałoby wstawić właśnie listAfter

    tabuOrderList = [] # w niej w kolejności wstawiane ścieżki jako stringi, pomaga przy usuwaniu ostatniego elementu
    # z tabu

    tabu[pathToString(solution)] = graph.cost(solution)
    tabuOrderList.append(pathToString(solution))
    numberOfIterations = 0
    maxNumberOfIterationWithoutProgress = 5*len(firstPath) #należy zastanowić się jaka duża
    numberOfIterationWithoutProgress = 0

    while numberOfIterations < iterations: # wypróbować inne warunki stopu
        print("iteracja", numberOfIterations)

        solution, solutionCost = getBestCandidateFromNeighborhood(graph, tabu, solution) # best solution in this iteration
        if solution == None:
            print("cofam się do ostatniego dobrego rozwiązania, backtrackinglist: ", backTrackingList)
            solution, solutionCost = getLastGoodSolution(graph, tabu, backTrackingList)
        if solution == None:
            print("kończę program")
            return bestSolutionInProgram, graph.cost(bestSolutionInProgram)

        tabu[pathToString(solution)] = solutionCost
        tabuOrderList.append(pathToString(solution))
        if solutionCost < graph.cost(bestSolutionInProgram):
            bestSolutionInProgram = solution
            backTrackingList.append(bestSolutionInProgram)
            print("znalazłam nowego globalnie najlepszego", solution)
            print("długość ", solutionCost)
            numberOfIterationWithoutProgress = 0
        else:
            numberOfIterationWithoutProgress += 1


        if(len(tabu) > maxSizeTabu):
            pathToDelete = tabuOrderList[0]
            tabuOrderList.pop(0)
            tabu.pop(pathToDelete)
            #print("tabuOrderList ", tabuOrderList)

        numberOfIterations += 1
        if numberOfIterationWithoutProgress > maxNumberOfIterationWithoutProgress:
            print("przekroczono maksymalną liczbę iteracji bez poprawy")
            numberOfIterationWithoutProgress = 0
            solution, solutionCost = getLastGoodSolution(graph, tabu, backTrackingList)
            if solution == None:
                print("kończę program")
                return bestSolutionInProgram, graph.cost(bestSolutionInProgram)

    print("best solution ", bestSolutionInProgram)
    print("best cost ", graph.cost(bestSolutionInProgram))
    return bestSolutionInProgram, graph.cost(bestSolutionInProgram)

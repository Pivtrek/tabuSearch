def getNeighborhood(graph, solution):
    pass


def tabu(graph, dist, firstPath, iterations, maxSizeTabu):
    solution = firstPath
    bestSolutionInProgram = solution
    tabuList = list()
    bestCost = dist
    numberOfIterations = 0

    while numberOfIterations < iterations :
        neighborhood = getNeighborhood(graph, solution)
        bestSolution = neighborhood[0] # best solution in this iteration
        #neighborhood jako posortowana lista invertowanych dwóch indeksów i kosztu tak uzyskanej ścieżki
        bestCostIndex = len(bestSolution) - 1

        ifNewSolutionFound = False # uniemożliwia przyjęcie rozwiązania wcześniejszego
        while ifNewSolutionFound is False:
            i = 0
    #         first_exchange_node, second_exchange_node = [], []
    #         n_opt_counter = 0
    #         while i < len(best_solution):
    #             if best_solution[i] != solution[i]:
    #                 first_exchange_node.append(best_solution[i])
    #                 second_exchange_node.append(solution[i])
    #                 n_opt_counter += 1
    #                 if n_opt_counter == n_opt:
    #                     break
    #             i = i + 1
    #
    #         exchange = first_exchange_node + second_exchange_node
    #         if first_exchange_node + second_exchange_node not in tabu_list and second_exchange_node + first_exchange_node not in tabu_list:
    #             tabu_list.append(exchange)
    #             found = True
    #             solution = best_solution[:-1]
    #             cost = neighborhood[index_of_best_solution][best_cost_index]
    #             if cost < best_cost:
    #                 best_cost = cost
    #                 best_solution_ever = solution
    #         elif index_of_best_solution < len(neighborhood):
    #             best_solution = neighborhood[index_of_best_solution]
    #             index_of_best_solution = index_of_best_solution + 1
    #
    #     while len(tabu_list) > size:
    #         tabu_list.pop(0)
    #
    #     count = count + 1
    # best_solution_ever.pop(-1)
    # return best_solution_ever, best_cost

import random, sys

class GenerateGraph:
    matrix=[]
    supported_formats = ['FULL_MATRIX', 'EUC_2D', 'LOWER_DIAG_ROW']
    supported_format_keys = ['EDGE_WEIGHT_FORMAT', 'EDGE_WEIGHT_TYPE']
    supported_header_delimiters = ['NODE_COORD_SECTION', 'EDGE_WEIGHT_SECTION']
    edge_weight_format = ""


    def __init__(self, variant, dimension, seed, upper_bound=100):
        self.variant = variant
        self.dimension = dimension
        self.seed= random.randrange(seed)
        self.upper_bound=upper_bound
        self.generate()

    def generate(self):
        if(self.variant=='FULL_MATRIX'):
            for i in range(self.dimension):
                row=[]
                for j in range(self.dimension):
                    if i==j:
                        row.append(9999)
                    else:
                        row.append(random.randint(1,self.upper_bound))
                self.matrix.append(row)

        elif(self.variant=='EUC_2D'):
            for i in range(self.dimension):
                row=[]
                for j in range(self.dimension):
                    if i==j:
                        row.append(0)
                        break
                    else:
                        value=random.randint((self.upper_bound/2)+1,self.upper_bound)
                        row.append(value)
                self.matrix.append(row)
            for i in range(self.dimension):
                for j in range(i+1,self.dimension):
                    self.matrix[i].append(self.matrix[j][i])

        elif(self.variant=='LOWER_DIAG_ROW'):
            for i in range(self.dimension):
                row=[]
                for j in range(self.dimension):
                    if(i==j):
                        row.append(0)
                        break
                    else:
                        row.append(random.randint(1,self.upper_bound))
                self.matrix.append(row)
            for i in range(self.dimension):
                for j in range(i+1,self.dimension):
                    self.matrix[i].append(self.matrix[j][i])

        else:
            print("Unsupported type of problem, please choose one from list down below: ")
            for item in self.supported_formats:
                print(item)
            return




    def k_random_method(self, k):
        #k=100
        print("k: ",k)
        min_dist=sys.maxsize
        vertex=[x for x in range(self.dimension)]
        path=[]
        for j in range(k):
            random.shuffle(vertex)
            distance=0
            for i in range(len(vertex)):
                if i+1==len(vertex):
                    distance=distance+int(self.matrix[vertex[i]][vertex[0]])
                    break
                if(int(self.matrix[vertex[i]][vertex[i+1]])==0):
                    continue
                distance=distance+int(self.matrix[vertex[i]][vertex[i+1]])
            if(distance<min_dist):
                min_dist=distance
                path=vertex.copy()

        return min_dist, path

    def two_opt(self):
        path = [x for x in range(self.dimension)]
        best = path
        improved = True
        while improved:
            improved = False
            #path = [1, 2, 3, 4, 5]
            for i in range(0, len(path)-1):
                for j in range(i+1, len(path)):
                    #print(i, j)
                    if j-i == 1: continue
                    new_route = path[:]
                    new_route[i:j] = reversed(new_route[i:j])
                    if self.cost(new_route) < self.cost(best):
                        best = new_route
                        improved = True
            path = best

        return path

    def cost(self,vertex):
        distance=0
        for i in range(len(vertex)):
            if i+1==len(vertex):
                distance=distance+self.matrix[vertex[i]][vertex[0]]
                break
            distance=distance+self.matrix[vertex[i]][vertex[i+1]]
        return distance

    def generate_path(self, flag):
        if(flag == 0):
            self.k_random_method()
        if(flag == 1):
            self.two_opt()

    def neighbourhood(self):

        save = []

        path = self.two_opt()
        firstCost = self.cost(path)

        save.append([0,0,firstCost])


        #path = [1, 2, 3, 4, 5]
        for i in range(len(path)-1):
            for j in range(len(path)-(i+1)):
                #print(i, j)
                path[i:(i+j+2)] = path[i:(i+j+2)][::-1]
                Cost = self.cost(path)

                save.append([i,i+j+1,Cost])
                path[i:(i+j+2)] = path[i:(i+j+2)][::-1]

        print(save)
        return save











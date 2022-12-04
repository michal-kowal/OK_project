import random
import math
import copy
# REPREZENTACJA POPULACJI: [ [zestaw chromosomow], fitness, [ lista zlych wierzcholkow ] ]
def genetic_algorithm2(matrix):
    upper_bound = find_max_degree(matrix)
    population_size = 15
    population = generate_population(population_size, upper_bound, matrix)  # [ [zestaw chromosomow], fitness, [ lista zlych wierzcholkow ] ]
    n_generations = 1000
    population.sort(key=lambda x: x[1]) 
    for i in range(n_generations):
        print("generacja: " + str(i + 1))
        population=crossover3(population, matrix)
        population.sort(key=lambda x: x[1]) 
    res = len(matrix)
    best_chromosome = []
    for i in range(1, len(population)):
        res_temp = []
        for j in range(len(population[i][0])):
            if population[i][0][j] not in res_temp:
                res_temp.append(population[i][0][j])
        max_color = len(res_temp)
        if max_color < res and population[i][1] == 0:
            res = max_color
            best_chromosome = population[i][0]

    print("Wynik: " + str(res) + " kolorow")
    print("Pokolorowanie: ")
    print(best_chromosome)
    print(" ")
    population.sort(key=lambda x: x[1])
    [print(*population[i]) for i in range(len(population))]

def genetic_algorithm3(matrix):
    wynik=1000
    tab=[]
    upper_bound = find_max_degree(matrix)
    while(upper_bound>0):
        population_size = 15
        population = generate_population(population_size, upper_bound, matrix)  # [ [zestaw chromosomow], fitness, [ lista zlych wierzcholkow ] ]
        n_generations = 1000
        upper_bound-=1
        population.sort(key=lambda x: x[1]) 
        for i in range(n_generations):
            population=crossover3(population, matrix)
            population.sort(key=lambda x: x[1]) 
        res = len(matrix)
        best_chromosome = []
        for i in range(1, len(population)):
            res_temp = []
            for j in range(len(population[i][0])):
                if population[i][0][j] not in res_temp:
                    res_temp.append(population[i][0][j])
            max_color = len(res_temp)
            if max_color < res and population[i][1] == 0:
                res = max_color
                best_chromosome = population[i][0]
        if(res<wynik):
            wynik=res
            tab=copy.copy(best_chromosome)
        print("Wynik: " + str(res) + " kolorow")
        print("Pokolorowanie: ")
        print(best_chromosome)
        print(" ")
    print("Wynik: " + str(wynik) + " kolorow")
    print("Pokolorowanie: ")
    print(tab)
    print(" ")


def find_max_degree(matrix):
    max_degree = 0
    for i in range(len(matrix)):
        x = sum(matrix[i])
        if x > max_degree:
            max_degree = x
    return max_degree


def find_fitness_score(chromosome, matrix):
    fit = 0
    bad_colorings = []
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            if matrix[i][j] == 1 and chromosome[i] == chromosome[j]:
                fit += 1
                bad_colorings.append(j)
    return fit, bad_colorings


def generate_population(size, k, matrix):
    population = []
    individual = [] # [ [zestaw chromosomow], fitness ]
    for i in range(size):
        for j in range(len(matrix)):
            individual.append(random.randint(0, k))
        fitness = list(find_fitness_score(individual, matrix))
        population.append([individual, fitness[0], fitness[1]])
        individual = []
    return population

def crossover3(population, matrix):
    size = len(population)
    midpoint = math.floor(size/2)
    for i in range(midpoint, size):
        parent_index1 = random.randint(0, midpoint-1)
        parent1 = copy.copy(population[parent_index1][0])
        parent_index2 = random.randint(0, midpoint-1)
        while parent_index2 == parent_index1:
            parent_index2 = random.randint(0, midpoint - 1)
        parent2 = copy.copy(population[parent_index2][0])
        child=parent2
        for j in range(len(child)):
            if (random.randint(0,1)==0):
                child[j]=parent1[j]
        #child = mutation3(child, matrix)
        child = mutation2(child, matrix)
        fitness = list(find_fitness_score(child, matrix))
        population[i] = [child, fitness[0], fitness[1]]
    return population

def crossover4(population, matrix):
    size = len(population)
    midpoint = math.floor(size/2)
    for i in range(midpoint, size):
        parent_index1 = random.randint(0, midpoint-1)
        parent_index2 = random.randint(0, midpoint-1)
        if(population[parent_index1][1]<population[parent_index2][1]):
            parent1=copy.copy(population[parent_index1][0])
            p_id=parent_index1
        else:
            parent1 = copy.copy(population[parent_index2][0])
            p_id=parent_index2
        parent_index1 = random.randint(0, midpoint-1)
        parent_index2 = random.randint(0, midpoint-1)
        while parent_index1 == p_id:
            parent_index1 = random.randint(0, midpoint-1)
        while parent_index2 == p_id:
            parent_index2 = random.randint(0, midpoint-1)
        if(population[parent_index1][1]<population[parent_index2][1]):
            parent2= copy.copy(population[parent_index1][0])
        else:
            parent2 = copy.copy(population[parent_index2][0])
        child=parent2
        for j in range(len(child)):
            if (random.randint(0,1)==0):
                child[j]=parent1[j]
        child = mutation2(child, matrix)
        fitness = list(find_fitness_score(child, matrix))
        population[i] = [child, fitness[0], fitness[1]]
    return population


def mutation2(child, matrix):
    for i in range(len(child)):
        if (random.randint(0,100)<=30):
            color=0
            flag=0
            while(flag==0):
                for j in range(len(matrix[i])):
                    flag=1
                    if(matrix[i][j]==1)and(child[j]==color):
                        color+=1
                        flag=0
            if(color<child[i]):
                child[i]==color
    return child

def mutation3(child, matrix):
    if (random.randint(0,100)<=30):
        color=random.randint(1,max(child))
        for i in range (len(child)):
            if(child[i]==color):
                child[i]-=1
    return child


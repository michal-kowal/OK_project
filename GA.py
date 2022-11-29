import random

def genetic_algorithm(matrix):
    upper_bound = find_max_degree(matrix)
    population = generate_population(50, upper_bound, matrix)   # [ [zestaw chromosomow], fitness ]
    n_generations = 6000
    for i in range(n_generations):
        print("generacja: " + str(i + 1))
        population.sort(key=lambda x: x[-1])    # sortuje populacje od najmniejszego fitness index
        crossover(population, matrix)
    res = max(population[0][0])
    for i in range(1, len(population)):
        m = max(population[i][0])
        if m < res:
            res = m
    print("Wynik: " + str(res + 1) + " kolorow")
    #population.sort(key=lambda x: x[-1])
    #print(population)


def find_max_degree(matrix):
    max_degree = 0
    for i in range(len(matrix)):
        x = sum(matrix[i])
        if x > max_degree:
            max_degree = x
    return max_degree


def find_fitness_score(chromosome, matrix):
    fit = 0
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            if matrix[i][j] == 1 and chromosome[i] == chromosome[j]:
                fit += 1
    return fit


def generate_population(size, k, matrix):
    population = []
    individual = [] # [ [zestaw chromosomow], fitness ]
    for i in range(size):
        n = 0
        for j in range(len(matrix)):
            if n <= k:
                individual.append(random.randint(0, n))
                n += 1
            else:
                individual.append(random.randint(0, k))
        population.append([individual, find_fitness_score(individual, matrix)])
        individual = []
    return population


def crossover(population, matrix):
    for i in range(1, len(population)):
        parent1 = population[0][0]
        parent2 = population[i][0]
        div = random.randint(2, len(matrix) - 1)
        child = parent1[:div] + parent2[div:]
        if random.randint(1, 100) <= 90:
            child = mutation(child, matrix)
        population[i] = [child, find_fitness_score(child, matrix)]


def mutation(child, matrix):
    for i in range(len(child)):
        for j in range(i + 1, len(child)):
            if matrix[i][j] == 1 and child[i] == child[j]:
                child[j] = random.randint(0, max(child))
    return child

import random
# REPREZENTACJA POPULACJI: [ [zestaw chromosomow], fitness, [ lista zlych wierzcholkow ] ]
def genetic_algorithm(matrix):
    upper_bound = find_max_degree(matrix)
    population_size = 50
    population = generate_population(population_size, upper_bound, matrix)  # [ [zestaw chromosomow], fitness, [ lista zlych wierzcholkow ] ]
    n_generations = 20000
    population.sort(key=lambda x: x[1])
    for i in range(n_generations):
        print("generacja: " + str(i + 1))
        crossover(population, matrix)
        population.sort(key=lambda x: x[1])    # sortuje populacje od najmniejszego fitness index
        population = population[:population_size//2] + generate_population(population_size//2, upper_bound, matrix)
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
    population.sort(key=lambda x: x[1])
    [print(*population[i]) for i in range(len(population))]


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


def crossover(population, matrix):
    for i in range(1, len(population)):
        parent1 = population[len(population) - i][0]
        parent2 = population[i][0]
        # div = random.randint(0, len(matrix) - 1)
        div = len(matrix) // 2
        child = parent1[:div] + parent2[div:]
        fitness = list(find_fitness_score(child, matrix))
        if random.randint(1, 100) <= 70:
            child = mutation(child, matrix, fitness[1])
            fitness = list(find_fitness_score(child, matrix))
        population[i] = [child, fitness[0], fitness[1]]


# chyba nie tedy droga
def crossover2(population, matrix):
    size = len(population)
    for i in range(len(population) - 1, 0, -1):
        parent_index1 = random.randint(0, i)
        parent1 = population[parent_index1][0]
        parent_index2 = random.randint(0, i)
        while parent_index2 == parent_index1 and i != 1:
            parent_index2 = random.randint(0, i - 1)
        parent2 = population[parent_index2][0]
        div = random.randint(2, len(matrix) - 1)
        #div = len(matrix) // 2
        child = parent1[:div] + parent2[div:]
        fitness = list(find_fitness_score(child, matrix))
        if random.randint(1, 100) <= 50:
            child = mutation(child, matrix, fitness[1])
            fitness = list(find_fitness_score(child, matrix))
        population.append([child, fitness[0], fitness[1]])
        population = population[:size]


def mutation(child, matrix, prohibited_colors):
    colors = []
    for i in range(len(child)):
        if i not in prohibited_colors:
            colors.append(i)
    for i in range(len(child)):
        for j in range(i + 1, len(child)):
            if matrix[i][j] == 1 and child[i] == child[j]:
                child[j] = colors[random.randint(0, len(colors) - 1)]
    return child

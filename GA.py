import random
# REPREZENTACJA POPULACJI: [ [zestaw chromosomow], fitness, [ lista zlych wierzcholkow ] ]
def genetic_algorithm(matrix):
    upper_bound = find_max_degree(matrix)
    population = generate_population(50, upper_bound, matrix)  # [ [zestaw chromosomow], fitness, [ lista zlych wierzcholkow ] ]
    n_generations = 100
    for i in range(n_generations):
        print("generacja: " + str(i + 1))
        population.sort(key=lambda x: x[1])    # sortuje populacje od najmniejszego fitness index
        crossover(population, matrix)
    res = upper_bound
    for i in range(1, len(population)):
        res_temp = []
        for j in range(len(population[i][0])):
            if population[i][0][j] not in res_temp:
                res_temp.append(population[i][0][j])
        max_color = max(res_temp)
        if max_color < res and population[i][1] == 0:
            res = max_color

    print("Wynik: " + str(res + 1) + " kolorow")
    population.sort(key=lambda x: x[1])
    print(population)


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
        n = 0
        for j in range(len(matrix)):
            if n <= k:
                individual.append(random.randint(0, n))
                n += 1
            else:
                individual.append(random.randint(0, k))
        fitness = list(find_fitness_score(individual, matrix))
        population.append([individual, fitness[0], fitness[1]])
        individual = []
    return population


def crossover(population, matrix):
    for i in range(1, len(population)):
        parent1 = population[0][0]
        parent2 = population[random.randint(i, len(population) - 1)][0]
        # div = random.randint(2, len(matrix) - 1)
        div = len(matrix) // 2
        child = parent1[:div] + parent2[div:]
        fitness = list(find_fitness_score(child, matrix))
        if random.randint(1, 100) <= 20:
            child = mutation(child, matrix, fitness[1])
            fitness = list(find_fitness_score(child, matrix))
        population[i] = [child, fitness[0], fitness[1]]


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

import random
# REPREZENTACJA POPULACJI: [ [zestaw chromosomow], fitness, [ lista zlych wierzcholkow ] ]
def genetic_algorithm(matrix, greedy_result):
    upper_bound = find_max_degree(matrix)
    if greedy_result < upper_bound:
        upper_bound = greedy_result
    population_size = 50
    population = generate_population(population_size, upper_bound, matrix)  # [ [zestaw chromosomow], fitness, [ lista zlych wierzcholkow ] ]
    n_generations = 4000
    population.sort(key=lambda x: (x[1], x[3]))
    it = 0
    best_chromosome = []
    res = upper_bound
    res = len(matrix)
    while it < n_generations:
        print("generacja: " + str(it + 1))
        for i in range(population_size):
            if population[i][1] < 4:
                crossover1(population, matrix, upper_bound)
            else:
                crossover2(population, matrix, upper_bound)
        population = population[population_size:]
        population.sort(key=lambda x: (x[1], x[3]))    # sortuje populacje od najmniejszego fitness index
        population = population[:population_size] + generate_population(population_size//2, upper_bound, matrix)
        it += 1
        print("Wynik: " + str(population[0][3]))
        best_chromosome = population[0][0]
        if res < greedy_result and population[0][1] == 0:
            break
    print("Wynik: " + str(res) + " kolorow")
    print("Pokolorowanie: ")
    print(best_chromosome)
    population.sort(key=lambda x: (x[1], x[3]))
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
    individual = [] # [ [zestaw chromosomow], fitness, [lista zlych wierz], ilosc kolorow ]
    for i in range(size):
        res_temp = []
        for j in range(len(matrix)):
            individual.append(random.randint(0, k-1))
            if individual[j] not in res_temp:
                res_temp.append(individual[j])
        fitness = list(find_fitness_score(individual, matrix))
        population.append([individual, fitness[0], fitness[1], len(res_temp)])
        individual = []
    return population


def count_colors(individual, matrix):
    res_temp = []
    for j in range(len(matrix)):
        if individual[j] not in res_temp:
            res_temp.append(individual[j])
    return len(res_temp)


def crossover(population, matrix, upper_bound):
    for i in range(1, len(population)):
        parent1 = population[len(population) - i][0]
        parent2 = population[i][0]
        # div = random.randint(0, len(matrix) - 1)
        div = len(matrix) // 2
        child = parent1[:div] + parent2[div:]
        fitness = list(find_fitness_score(child, matrix))
        if random.randint(1, 100) <= 100:
            child = mutation1(child, matrix, fitness[1], upper_bound)
            fitness = list(find_fitness_score(child, matrix))
        population[i] = [child, fitness[0], fitness[1]]


def crossover1(population, matrix, upper_bound):
    n = len(population)
    parent1 = select_parent1(population, n)
    parent2 = select_parent1(population, n)
    crosspoint = random.randint(0, len(matrix) - 1)
    child = parent1[:crosspoint] + parent2[crosspoint:]
    fitness = list(find_fitness_score(child, matrix))
    child = mutation1(child, matrix, fitness[1], upper_bound)
    child = mutation3(child, matrix)
    child = mutation4(child, matrix)
    fitness = list(find_fitness_score(child, matrix))
    population.append([child, fitness[0], fitness[1], count_colors(child, matrix)])


def crossover2(population, matrix, upper_bound):
    n = len(population)
    parent1 = population[0][0]
    parent2 = select_parent1(population, n)
    crosspoint = random.randint(0, len(matrix) - 1)
    child = parent1[:crosspoint] + parent2[crosspoint:]
    fitness = list(find_fitness_score(child, matrix))
    child = mutation2(child, matrix, upper_bound)
    child = mutation3(child, matrix)
    child = mutation4(child, matrix)
    fitness = list(find_fitness_score(child, matrix))
    population.append([child, fitness[0], fitness[1], count_colors(child, matrix)])


def mutation1(child, matrix, prohibited_colors, upper_bound):
    colors = []
    for i in range(upper_bound):
        if i not in prohibited_colors:
            colors.append(i)
    for i in range(len(child)):
        for j in range(i, len(child)):
            if matrix[i][j] == 1 and child[i] == child[j]:
                child[j] = colors[random.randint(0, len(colors) - 1)]
    return child


def mutation2(child, matrix, upper_bound):
    for i in range(len(child)):
        for j in range(i, len(child)):
            if matrix[i][j] == 1 and child[i] == child[j]:
                child[j] = random.randint(0, upper_bound - 1)
    return child


def select_parent1(population, n):
    temp_parents = [population[random.randint(0, n - 1)], population[random.randint(0, n - 1)]]
    if temp_parents[0][1] > temp_parents[1][1]:
        parent = temp_parents[0][0]
    else:
        parent = temp_parents[1][0]
    return parent

def mutation3(child, matrix):
    if (random.randint(0,100)<=10):
        color=random.randint(1,max(child))
        for i in range (len(child)):
            if(child[i]==color):
                child[i]-=1
    return child

def mutation4(child, matrix):
    if (random.randint(0,100)<=50):
        color=random.randint(1,max(child))
        color2 = random.randint(1, max(child))
        for i in range (len(child)):
            if(child[i]==color):
                child[i]=color2
            elif(child[i]==color2):
                child[i] = color
    return child
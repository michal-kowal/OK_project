import random
# REPREZENTACJA POPULACJI: [ [zestaw chromosomow], fitness, [ lista zlych wierzcholkow ] ]
def genetic_algorithm(matrix, greedy_result, kolory):
    upper_bound = find_max_degree(matrix)
    if greedy_result < upper_bound:
        upper_bound = greedy_result
    population_size = 50
    population = generate_population(population_size, upper_bound, matrix)  # [ [zestaw chromosomow], fitness, [ lista zlych wierzcholkow ] ]
    population.append([kolory, 0, []])
    n_generations = 2000
    # population.sort(key=lambda x: x[1])
    it = 0
    best_chromosome = []
    res = upper_bound
    population.sort(key=lambda x: x[1])
    del population[population_size]
    while it < n_generations or population[0][1] != 0:
        print("generacja: " + str(it + 1))
        for i in range(population_size):
            random.shuffle(population)
            crossover(population, matrix, res, it, n_generations)
        not_fit_index = []
        for i in range(len(population)):
            if population[i][1] != 0:
                not_fit_index.append(population[i])
        if len(not_fit_index) >= 2:
            #print("MUTACJA 5")
            mutation5(matrix, not_fit_index, population)
        if random.randint(1, 100) < 50:
            for i in range(population_size // 4):
                population.append(generate_population(1, res - random.randint(1, 3), matrix)[0])
        # Mozna jeszcze wymyslic jakas mutacje dla najlepszego chromosomu zachodzaca od czasu do czasu, wybierac 1 kolor i zastepujac go pozostalymi dostepnymi
        population.sort(key=lambda x: x[1])    # sortuje populacje od najmniejszego fitness index
        population = population[:population_size]
        for i in range(len(population)):
            res_temp = []
            for j in range(len(population[i][0])):
                if population[i][0][j] not in res_temp:
                    res_temp.append(population[i][0][j])
            max_color = len(res_temp)
            if max_color <= res and population[i][1] == 0:
                res = max_color
                best_chromosome = population[i][0]
        it += 1
        print("Wynik: " + str(res))
        #print(population)
        print(population[1][1])
    print("Wynik: " + str(res) + " kolorow")
    print("Pokolorowanie: ")
    print(best_chromosome)
    population.sort(key=lambda x: x[1])
    print("\n")
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
                if j not in bad_colorings:
                    fit += 1
                    bad_colorings.append(j)
    bad_colorings.sort()
    return fit, bad_colorings


def generate_population(size, k, matrix):
    population = []
    individual = []  # [ [zestaw chromosomow], fitness ]
    for i in range(size):
        for j in range(len(matrix)):
            individual.append(random.randint(0, k))
        fitness = list(find_fitness_score(individual, matrix))
        population.append([individual, fitness[0], fitness[1]])
        individual = []
    return population


def crossover(population, matrix, upper_bound, generation, number_of_generations):
    n = len(population)
    if population[1][1] > len(matrix) / 4 and random.randint(1, 100) > 0:
        parent1 = population[random.randint(0, n // 8)][0]
        parent2 = population[random.randint(0, n // 8)][0]
    else:
        parent1 = population[random.randint(0, n // 4)][0]
        #parent2 = population[random.randint(0, n // 4)][0]
        # parent1 = select_parent1(population, n)
        parent2 = select_parent1(population, n)
    crosspoint1 = random.randint(0, len(matrix) - 1)
    crosspoint2 = random.randint(crosspoint1, len(matrix) - 1)
    crosspoint3 = random.randint(crosspoint2, len(matrix) - 1)
    #crosspoint = len(matrix) // 2
    child = parent1[:crosspoint1] + parent2[crosspoint1:crosspoint2] + parent1[crosspoint2:crosspoint3] + parent1[crosspoint3:]
    fitness = list(find_fitness_score(child, matrix))
    other = False
    if fitness[0] > 2:
        if random.randint(1, 100) > 20:
            #print("MUTACJA 1")
            child = mutation1(child, matrix, fitness[1], upper_bound)
        else:
            #print("MUTACJA 2")
            child = mutation2(child, matrix, upper_bound)
            if random.randint(1, 100) < 15:
                child = child[::-1]
    else:
        if generation / number_of_generations < 0.1:
            #print("MUTACJA 3")
            for i in range(4):
                child = mutation3(child, 1, other)
            # child = mutation3(child, 4, other)
        elif 0.1 < generation / number_of_generations < 0.25:
            #print("MUTACJA 3")
            for i in range(3):
                child = mutation3(child, 1, other)
            #child = mutation3(child, 3, other)
        elif 0.3 < generation / number_of_generations < 0.5:
            #print("MUTACJA 3")
            # child = mutation3(child, 2, other)
            for i in range(2):
                child = mutation3(child, 1, other)
        else:
            if random.randint(1, 100) < 20:
                #print("MUTACJA 4")
                child = mutation4(child)
            else:

                if random.randint(1, 100) < 5:
                    other = True
                    child = mutation3(child, 1, other)
                else:
                    #print("MUTACJA 3")
                    child = mutation3(child, 1, other)
    fitness = list(find_fitness_score(child, matrix))
    population.append([child, fitness[0], fitness[1]])


def select_parent1(population, n):
    temp_parents = [population[random.randint(0, n - 1)], population[random.randint(0, n - 1)]]
    if temp_parents[0][1] > temp_parents[1][1]:
        parent = temp_parents[0][0]
    else:
        parent = temp_parents[1][0]
    return parent


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


def mutation3(child, n, other):
    colors = []
    colors_to_cut = []
    for i in child:
        if i not in colors:
            colors.append([i, child.count(i)])
    colors.sort(key=lambda x: x[1])
    for i in range(n):
        if not other:
            colors_to_cut.append(colors[i][0])
            del colors[i]
        else:
            x = random.randint(0, len(colors) - 1)
            colors_to_cut.append(colors[x][0])
            del colors[x]
    for i in range(len(child)):
        if child[i] in colors_to_cut:
            child[i] = colors[random.randint(0, len(colors) - 1)][0]
    return child


def mutation4(child):
    color1 = random.randint(0, len(child) - 1)
    color2 = random.randint(0, len(child) - 1)
    while color1 == color2:
        color2 = random.randint(0, len(child) - 1)
    for i in range(len(child)):
        if child[i] == child[color1]:
            child[i] = child[color2]
        elif child[i] == child[color2]:
            child[i] = child[color1]
    return child


def mutation5(matrix, not_fit_index, population):
    index1 = 0
    index2 = 0
    i = 0
    chromosome1_index = random.randint(0, len(not_fit_index) - 1)
    chromosome2_index = random.randint(0, len(not_fit_index) - 1)
    while chromosome1_index == chromosome2_index:
        chromosome2_index = random.randint(0, len(not_fit_index) - 1)
    chromosome1 = not_fit_index[chromosome1_index]
    chromosome2 = not_fit_index[chromosome2_index]
    while i < len(chromosome1[0]) and (index1 < len(chromosome1[2]) or index2 < len(chromosome2[2])):
        if index1 < len(chromosome1[2]) and i in chromosome1[2]:
            chromosome1[0][i], chromosome2[0][i] = chromosome2[0][i], chromosome1[0][i]
            index1 += 1
        if index2 < len(chromosome2[2]) and i in chromosome2[2]:
            chromosome1[0][i], chromosome2[0][i] = chromosome2[0][i], chromosome1[0][i]
            index2 += 1
        i += 1
    fitness = list(find_fitness_score(chromosome1[0], matrix))
    population.append([chromosome1[0], fitness[0], fitness[1]])
    fitness = list(find_fitness_score(chromosome2[0], matrix))
    population.append([chromosome2[0], fitness[0], fitness[1]])

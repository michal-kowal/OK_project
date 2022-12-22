import random
# REPREZENTACJA POPULACJI: [ [zestaw chromosomow], fitness, [ lista zlych wierzcholkow ] ]
def genetic_algorithm(matrix, greedy_result, kolory):
    upper_bound = greedy_result-1
    population_size = 50
    population = generate_population(population_size, upper_bound, matrix)  # [ [zestaw chromosomow], fitness, [ lista zlych wierzcholkow ] ]
    population.append([kolory, 0, [], greedy_result])
    n_generations = 1000
    # population.sort(key=lambda x: x[1])
    it = 0
    best_chromosome = []
    res = upper_bound
    population.sort(key=lambda x: (x[1], x[3]))
    best_colors=population[0][3]
    del population[population_size]
    [print(*population[i]) for i in range(len(population))]
    while it < n_generations or population[0][1] != 0:
        print("generacja: " + str(it + 1))
        for i in range(population_size):
            crossover(population, matrix, res, it, n_generations)
        not_fit_index = []
        # for i in range(len(population)):
        #     if population[i][1] != 0:
        #         not_fit_index.append(population[i])
        # if len(not_fit_index) >= 2:
        #     #print("MUTACJA 5")
        #     mutation5(matrix, not_fit_index, population)
        if random.randint(1, 100) < 0:
            for i in range(population_size // 4):
                population.append(generate_population(1, res - random.randint(1, 3), matrix)[0])
        # Mozna jeszcze wymyslic jakas mutacje dla najlepszego chromosomu zachodzaca od czasu do czasu, wybierac 1 kolor i zastepujac go pozostalymi dostepnymi
        population=population[::-1]
        population.sort(key=lambda x: (x[1], x[3]))    # sortuje populacje od najmniejszego fitness index
        population = population[:population_size]
        if(population[0][3]<best_colors):
            best_colors=population[0][3]
            for i in range(1, len(population)):
                if population[i][3]>=best_colors:
                    population[i][0]=mutation3(population[i][0], (population[i][3]-best_colors)+1,)
                    fitness = list(find_fitness_score(population[i][0], matrix))
                    population[i][1]=fitness[0]
                    population[i][2]=fitness[1]
                    population[i][3]=count_colors(population[i][0])
                #UWAGA
                # population[i][0] = mutation1(population[i][0], matrix, fitness[1], population[i][3])
                # fitness = list(find_fitness_score(population[i][0], matrix))
                # population[i][1] = fitness[0]
                # population[i][2] = fitness[1]
                # population[i][3] = count_colors(population[i][0], matrix)

        it += 1
        print("Wynik: " + str(population[0][3]))
        print(population[1][1], population[1][3])
        #print(population)
        #print(population[1][1])

    print("Wynik: " + str(population[0][3]) + " kolorow")
    print("Pokolorowanie: ")
    print(best_chromosome)
    population.sort(key=lambda x: (x[1], x[3]))
    print("\n")
    [print(*population[i]) for i in range(len(population))]

def count_colors(individual):
    return len(list(set(individual)))


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
            individual.append(random.randint(0, k-1))
        fitness = list(find_fitness_score(individual, matrix))
        population.append([individual, fitness[0], fitness[1], count_colors(individual)])
        individual = []
    return population


def crossover(population, matrix, upper_bound, generation, number_of_generations):
    n = len(population)
    if population[1][1] > len(matrix) / 4 and random.randint(1, 100) > 0:
        parent1 = population[random.randint(0, n // 9)][0]
        parent2 = population[random.randint(0, n // 9)][0]
    else:
        parent1 = population[random.randint(0, n // 4)][0]
        #parent2 = population[random.randint(0, n // 4)][0]
        # parent1 = select_parent1(population, n)
        parent2 = select_parent1(population, n)
    #można by zmienić sposób losowania crosspointów np. c1=(0, len(matrix)//4), c2=(c1, len(matrix)//2) c3=(c2, len(matrix)//1.3)
    crosspoint1 = random.randint(0, len(matrix)//4)
    crosspoint2 = random.randint(crosspoint1, len(matrix)//2)
    crosspoint3 = random.randint(crosspoint2, len(matrix)//1.3)
    #crosspoint = len(matrix) // 2
    child = parent1[:crosspoint1] + parent2[crosspoint1:crosspoint2] + parent1[crosspoint2:crosspoint3] + parent2[crosspoint3:]
    colors=count_colors(child)
    if colors>=population[0][3]:
        child=mutation3(child, (colors-population[0][3])+1)
    fitness = list(find_fitness_score(child, matrix))
    if fitness[0] > 2:
        if random.randint(1, 100) > 20:
            child = mutation2(child, fitness[1])
        else:
            child = mutation8(child, matrix, fitness[1])
            # if random.randint(1, 100) < 15:
            #     child = child[::-1]
    else:
        child=mutation8(child, matrix, fitness[1])
    #     if generation / number_of_generations < 0.1:
    #         #print("MUTACJA 3")
    #         for i in range(4):
    #             child = mutation3(child, 1, other)
    #         # child = mutation3(child, 4, other)
    #     elif 0.1 < generation / number_of_generations < 0.25:
    #         #print("MUTACJA 3")
    #         for i in range(3):
    #             child = mutation3(child, 1, other)
    #         #child = mutation3(child, 3, other)
    #     elif 0.3 < generation / number_of_generations < 0.5:
    #         #print("MUTACJA 3")
    #         # child = mutation3(child, 2, other)
    #         for i in range(2):
    #             child = mutation3(child, 1, other)
    #     else:
    #         if random.randint(1, 100) < 20:
    #             #print("MUTACJA 4")
    #             child = mutation4(child)
    #         else:
    #
    #             if random.randint(1, 100) < 5:
    #                 other = True
    #                 child = mutation3(child, 1, other)
    #             else:
    #                 #print("MUTACJA 3")
    #                 child = mutation3(child, 1, other)
    #     if random.randint(1, 100) < 10:
    #         child = mutation7(child, matrix)
    #child=mutation4(child)
    colors=count_colors(child)
    if colors>=population[0][3]:
        child=mutation3(child, (colors-population[0][3])+1)
    fitness = list(find_fitness_score(child, matrix))
    population.append([child, fitness[0], fitness[1], count_colors(child)])


def select_parent1(population, n):
    temp_parents = [population[random.randint(0, n - 1)], population[random.randint(0, n - 1)]]
    if temp_parents[0][1] > temp_parents[1][1]:
        parent = temp_parents[0][0]
    else:
        parent = temp_parents[1][0]
    return parent


def mutation1(child, matrix, prohibited_colors, upper_bound):
    colors = set(child)
    for i in range(upper_bound):
        if i not in prohibited_colors:
            colors.append(i)
    for i in range(len(child)):
        for j in range(i, len(child)):
            if matrix[i][j] == 1 and child[i] == child[j]:
                child[j] = child[colors[random.randint(0, len(colors) - 1)]]
    return child


def mutation2(child, fitness):
    colors = list(set(child))
    for i in (fitness):
        child[i]=colors[random.randint(0, len(colors)-1)]
    return child


def mutation3(child, n):
    colors = []
    colors1d = list(set(child))
    colors_to_cut = []
    for i in colors1d:
        colors.append([i, child.count(i)])
    colors.sort(key=lambda x: x[1])
    for i in range(n):
            colors_to_cut.append(colors[i][0])
    # zmienic na to wybieral drugi najmniej uzywany kolor a nie losowy z dopuszczalnych
    for i in range(len(child)):
        if child[i] in colors_to_cut:
            child[i] = colors[n][0]
    return child

def mutation4(child):
    colors=list(set(child))
    chance=100
    while (random.randint(10, 100)<=chance):
        random.shuffle(colors)
        for i in range(len(child)):
            if child[i] == colors[0]:
                child[i] = colors[1]
            elif child[i] == colors[1]:
                child[i] = colors[0]
        chance=chance//1.5
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
    population.append([chromosome1[0], fitness[0], fitness[1],count_colors(chromosome1[0])])
    fitness = list(find_fitness_score(chromosome2[0], matrix))
    population.append([chromosome2[0], fitness[0], fitness[1],count_colors(chromosome2[0])])
    
def mutation6(child, matrix): #szansa, by zmienić kolor złego wierzchołka na inny użyty w grafie
    colors = []
    for i in range(len(child)):
        if child[i] not in colors:
            colors.append(child[i])
    if random.randint(0,100)<50:
        for i in range(len(child)):
            prohibited = []
            for j in range(len(child)):
                if matrix[i][j] == 1 and child[j] not in prohibited:
                    prohibited.append(child[j])
            for j in range (3):
                if child[i] not in prohibited:
                    break
                else:
                    child[i] = colors[random.randint(0, len(colors) - 1)]
    return child

def mutation7(child, matrix): #zmienia numery kolorów na n pierwszych liczb naturalnych (n - liczba kolorów chromosomu), ale sprawia, że chromosomy są zbyt podobne
    colors = []
    for i in range(len(child)):
        if child[i] not in colors:
            colors.append(child[i])
    i=0
    while 1:
        maximum=max(colors)
        while i in colors:
            i+=1
        if(i>maximum):
            break
        else:
            for j in range(len(child)):
                if child[j]==maximum:
                    child[j]=i
            colors[colors.index(maximum)]=i
    return child

def mutation8(child, matrix, fitness):
    random.shuffle(fitness)
    allowed_colors = set(child)
    for i in fitness:
        prohibited = {child[j] for j in (fitness) if matrix[i][j] == 1}
        allowed = list(allowed_colors - prohibited)
        if allowed:
            child[i] = allowed[random.randint(0, len(allowed)-1)]
        else:
            child[i] = child[random.randint(0, len(child)-1)]
    return child

import random
import main

# REPREZENTACJA POPULACJI: [ [zestaw chromosomow], fitness, [ lista zlych wierzcholkow ] ]
def genetic_algorithm(matrix, greedy_result, kolory):
    upper_bound = greedy_result - 1
    population_size = 50
    population = generate_population(population_size, upper_bound,
                                     matrix)  # [ [zestaw chromosomow], fitness, [ lista zlych wierzcholkow ] ]
    population.append([kolory, 0, [], greedy_result])

    for i in range(1, 10):
        res_zachlanny = list(main.zachlanny(matrix, len(matrix), 1))
        population.append([res_zachlanny[1], 0, [], res_zachlanny[0]])

    n_generations = 1000
    it = 0
    best_chromosome = []
    res = upper_bound
    population.sort(key=lambda x: (x[1], x[3]))
    best_colors = population[0][3]
    del population[population_size:]
    [print(*population[i]) for i in range(len(population))]
    repeat_control = 0
    while it < n_generations or population[0][1] != 0:
        print("generacja: " + str(it + 1))
        for i in range(population_size):
            crossover(population, matrix, res, it, n_generations)
        population = population[::-1]
        population.sort(key=lambda x: (x[1], x[3]))  # sortuje populacje od najmniejszego fitness index
        population = population[:population_size]
        if population[0][3] < best_colors:
            best_colors = population[0][3]
            for i in range(1, len(population)):
                if population[i][3] >= best_colors:
                    population[i][0] = mutation3(population[i][0], (population[i][3] - best_colors) + 1, )
                    fitness = list(find_fitness_score(population[i][0], matrix))
                    population[i][1] = fitness[0]
                    population[i][2] = fitness[1]
                    population[i][3] = count_colors(population[i][0])
        if it > 1 and previous == population[1][1]:
            repeat_control += 1
        elif it > 1 and previous != population[1][1]:
            repeat_control = 0
        previous = population[1][1]
        if repeat_control == 5 or repeat_control == 10:
            print(population[1])
            print("DZIAlam")
            population[1] = mutation1(population[1], matrix)
            print(population[1])
        if repeat_control >= 15:
            del population[1:]
            res_zachlanny = list(main.zachlanny(matrix, len(matrix), 1))
            if res_zachlanny[0] <= population[0][3]:
                population[0] = [res_zachlanny[1], 0, [], res_zachlanny[0]]
            population = population + generate_population(population_size - 1, population[0][3], matrix)
            # population[1:].sort(key=lambda x: (x[3], x[1]))
        it += 1
        print("Wynik: " + str(population[0][3]))
        print(population[1][1], population[1][3])
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
            individual.append(random.randint(0, k - 1))
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
        parent2 = select_parent1(population, n)
    crosspoint1 = random.randint(0, len(matrix) // 4)
    crosspoint2 = random.randint(crosspoint1, len(matrix) // 2)
    crosspoint3 = random.randint(crosspoint2, len(matrix) // 1.3)
    child = parent1[:crosspoint1] + parent2[crosspoint1:crosspoint2] + parent1[crosspoint2:crosspoint3] + parent2[
                                                                                                          crosspoint3:]
    colors = count_colors(child)
    if colors >= population[0][3]:
        child = mutation3(child, (colors - population[0][3]) + 1)
    fitness = list(find_fitness_score(child, matrix))
    if fitness[0] > 2:
        if random.randint(1, 100) > 20:
            child = mutation2(child, fitness[1])
        else:
            child = mutation8(child, matrix, fitness[1])
    else:
        child = mutation8(child, matrix, fitness[1])
    colors = count_colors(child)
    if colors >= population[0][3]:
        child = mutation3(child, (colors - population[0][3]) + 1)
    fitness = list(find_fitness_score(child, matrix))
    population.append([child, fitness[0], fitness[1], count_colors(child)])


def select_parent1(population, n):
    temp_parents = [population[random.randint(0, n - 1)], population[random.randint(0, n - 1)]]
    if temp_parents[0][1] > temp_parents[1][1]:
        parent = temp_parents[0][0]
    else:
        parent = temp_parents[1][0]
    return parent


def mutation1(individual, matrix):
    random.shuffle(individual[2])
    for i in individual[2]:
        colors = set(individual[0])
        print(colors)
        for j in range(len(matrix)):
            if matrix[i][j] == 1 and individual[0][j] in colors:
                colors.remove(individual[0][j])
        print(colors)
        if len(colors) > 0:
            new = random.randint(0, len(colors) - 1)
            individual[0][i] = list(colors)[new]
        else:
            inverted_chromosome = []
            for color in individual[0]:
                inverted_chromosome.append(count_colors(individual[0]) - color)
            print("inverted len:"+str(len(inverted_chromosome)))
            print("inverted len:"+str(len(individual[0])))
            individual[0] = inverted_chromosome
            break
    fitness = list(find_fitness_score(individual[0], matrix))
    return [individual[0], fitness[0], fitness[1], count_colors(individual[0])]


def mutation2(child, fitness):
    colors = list(set(child))
    for i in fitness:
        child[i] = colors[random.randint(0, len(colors) - 1)]
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


def mutation8(child, matrix, fitness):
    random.shuffle(fitness)
    allowed_colors = set(child)
    for i in fitness:
        prohibited = {child[j] for j in (fitness) if matrix[i][j] == 1}
        allowed = list(allowed_colors - prohibited)
        if allowed:
            child[i] = allowed[random.randint(0, len(allowed) - 1)]
        else:
            child[i] = child[random.randint(0, len(child) - 1)]
    return child

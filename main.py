import random
import GA


def generuj_macierz(n):
    # generuj pusta macierz sasiedztwa
    matrix = []
    for i in range(n):
        matrix.append([])
        for j in range(n):
            matrix[i].append(0)
    return matrix


def plik():
    krawedzie = []
    with open('graf.txt') as file:
        for line in file:
            krawedzie.append(list(map(int, line.rstrip().split())))
    n = krawedzie[0][0]  # liczba krawedzi
    del krawedzie[0]
    file.close()
    matrix = generuj_macierz(n)
    for krawedz in krawedzie:
        matrix[krawedz[0] - 1][krawedz[1] - 1] = 1
        matrix[krawedz[1] - 1][krawedz[0] - 1] = 1
    return matrix


def generuj_graf(n):
    matrix = generuj_macierz(n)
    for i in range(n):
        for j in range(i + 1, n):
            rand = random.randint(0, 1)
            if rand == 1:
                matrix[i][j] = 1
                matrix[j][i] = 1
    file = open("generuj.txt", "x")
    file.write(str(n) + "\n")
    for i in range(n):
        for j in range(i, n):
            if matrix[i][j] == 1:
                file.write(str(i + 1) + " " + str(j + 1) + "\n")
    return matrix


def zachlanny(matrix, n, mode):     # mode = 0 (standardowy algorytm); mode = 1 (losowy wybor wierzcholkow)
    kolory = [0] * n
    if mode == 0:
        print("Wierzchołki i ich kolory:\n")
    r = list(range(n))
    if mode == 1:
        random.shuffle(r)
    for i in r:
        if (kolory[i] == 0):
            check = 0
            barwa = 1
            while (check == 0):
                check = 1
                for j in range(n):
                    if (matrix[i][j] == 1):
                        if (kolory[j] == barwa):
                            check = 0
                            barwa += 1
                            break
            kolory[i] = barwa
        if mode == 0:
            print(i, "\t", kolory[i])
    if mode == 0:
        print("Użyto", max(kolory), "kolorów")
    return max(kolory), kolory


def menu():
    wczytaj = False
    generuj = False
    while (1 == 1):
        print(
            "[1] Wczytaj z pliku graf.txt\n[2] Generuj graf\n[3] Wypisz macierz grafu\n[4] Pokoloruj zachłannie\n[5] GA\n[0] Zakończ program")
        wybor = input()
        if wybor == '1':
            matrix = plik()
            wczytaj = True
        elif wybor == '2':
            try:
                n = int(input("Podaj liczbę wierzchołków: "))
                matrix = generuj_graf(n)
                generuj = True
            except ValueError:
                print("Musi być int")
        elif wybor == '3' and (wczytaj or generuj):
            [print(*matrix[i]) for i in range(len(matrix))]
        elif wybor == '4' and (wczytaj or generuj):
            zachlanny(matrix, len(matrix), 0)
        elif wybor == '5' and (wczytaj or generuj):
            res_zachlanny = list(zachlanny(matrix, len(matrix), 0))
            GA.genetic_algorithm(matrix, res_zachlanny[0], res_zachlanny[1])
            break
        elif wybor == '0':
            print("Koniec pracy programu")
            break
        else:
            print("Wybierz poprawną wartość")


if __name__ == '__main__':
    menu()

import random


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
    n = krawedzie[0][0]     # liczba krawedzi
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
    return matrix

def menu():
    print("[1] Wczytaj z pliku graf.txt\n[2] Generuj graf\n")
    wybor = input()
    if wybor == '1':
        matrix = plik()
    elif wybor == '2':
        try:
            n = int(input("Podaj liczbe wierzcholkow: "))
            matrix = generuj_graf(n)
        except ValueError:
            print("Musi byc int")
    else:
        print("Wybierz poprawna wartosc")
    [print(*matrix[i]) for i in range(len(matrix))]


if __name__ == '__main__':
    menu()
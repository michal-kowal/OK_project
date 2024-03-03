### Genetic algorithm solving graph coloring problem
**Opis algorytmu**

Nasza metaheurystyka bazuje na algorytmie genetycznym. Na podstawie wyniku algorytmu zachłannego generuje początkową populację wielkości 50 chromosomów - jednym z nich jest wynik algorytmu zachłannego, a inne pokolorowane są losowo, liczbą kolorów o 1 mniejszą niż w przypadku algorytmu zachłannego. Populacja sortowana jest pod względem liczby wadliwych krawędzi, oraz liczby zastosowanych kolorów. W każdym pokoleniu na drodze crossoverów i mutacji tworzone jest 50 nowych chromosomów a po posortowaniu w populacji zostawiamy 50 najlepszych chromosomów. Gdy algorytm znajdzie nowe najlepsze rozwiązanie dopuszczalne, liczba kolorów w pozostałych chromosomach ograniczana jest do o 1 mniejszej niż w rozwiązaniu dopuszczalnym. W przypadku, gdy populacja nie wykazuje popraw przez 15 pokoleń, wszystkie chromosomy generowane są na nowo, zachowując obecny limit kolorów.


**Pseudokod**
```
Algorytm1: genetic_algorithm
populacja = wynik algorytmu zachłannego i losowo wygenerowane chromosomy
for chromosomy in populacja
	znajdź wadliwe wierzchołki
	znajdź liczba zastosowanych kolorów
while(pokolenie<1000)
	sortuj populacja
	for (i = 0,  i < długość populacji)
		crossover()
	sortuj populacja
	populacja = 50 pierwszych chromosomów
	if (chromosom 1 jest dopuszczalny) i (liczba kolorów chromosomu 1 < limit kolorów)
		limit kolorów = liczba kolorów chromosomu 1
		najlepsze rozwiązanie = chromosom 1
		for (i = 1, i<długość populacji)
			chromosom i = mutation3(n = liczba kolorów - limit kolorów + 1)
	if (pokolenia bez poprawy == 15)
		populacja = najlepszy chromosom i losowo wygenerowane chromosomy
print (limit kolorów i najlepsze rozwiązanie)

Algorytm2: crossover
wylosuj 3 crosspointy (c1, c2, c3)
dziecko = rodzic1[początek do c1] + rodzic2[c1 do c2] + rodzic1[c2 do c3] + rodzic2[c3 do koniec]
znajdź liczba kolorów
if (liczba kolorów >= limit kolorów)
	chromosom = mutation3(n = liczba kolorów - limit kolorów + 1)
znajdź wadliwe wierzchołki
if (wadliwe wierzchołki>2 i losowa liczba(od 0 do 100)>20)
	chromosom = mutation2()
else
	chromosom = mutation4()
znajdź liczba kolorów
znajdź wadliwe wierzchołki
dodaj chromosom do populacji

Algorytm3: mutation2
znajdź kolory w chromosomie
for (wierzchołki in wadliwe wierzchołki)
	kolor wierzchołka = losowy z kolorów w chromosomie
return chromosom

Algorytm4: mutation3
znajdź n najmniej używanych kolorów
for (wierzchołki in chromosom)
	if (kolor wierzchołka należy do [1, n-1])
		kolor wierzchołka = kolor(n)
return chromosom

										
Algorytm5: mutation4
znajdź kolory w chromosomie
for (wierzchołki in wadliwe wierzchołki)
	znajdź zakazane kolory
	dopuszczalne kolory = kolory w chromosomie - zakazane kolory
	kolor wierzchołka = losowy z dopuszczalnych kolorów
return chromosom
```

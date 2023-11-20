"""
Funkcje te sluza do znajdowania zalezności i niezaleznosci w alfabcie A.
"""


def find_dependencies(operations, variables):
    n = len(operations)
    main = [operation[0] for operation in operations]  # zbiera nam jaka zmienna jest przypisana
    new = [[] for _ in range(n)]

    for i in range(n):
        for c in operations[i][2:]:
            if c in variables:
                new[i].append(c)  # zbiera nam od czego zalezy dana zmienna

    depe = set()
    for i in range(n):
        for var in new[i]:
            for k, main_var in enumerate(main):  # enumerate zwraca nam indeks i wartosc
                if var == main_var:
                    depe.add((chr(97 + i),
                              chr(97 + k)))  # chr zamienia nam liczbe na znak, 97 to a w ascii, w ten sposob
                    # zamieniamy zmienne na litery alfabety
                    depe.add((chr(97 + k), chr(97 + i)))  # dodajemy zaleznosci w obie strony

    return sorted(list(depe))  # zwracamy posortowana liste


def find_independencies(dependencies, A):
    n = len(A)
    independencies = []
    for i in range(n):
        for j in range(n):
            if (chr(97 + i),
                chr(97 + j)) not in dependencies:  # sprawdzamy czy dana zaleznosc jest w zbiorze
                # zaleznosci, jesli nie to dodajemy do niezaleznosci
                independencies.append((chr(97 + i), chr(97 + j)))
    return independencies

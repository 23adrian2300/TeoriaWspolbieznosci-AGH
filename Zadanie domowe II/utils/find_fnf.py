"""
Funkcja find_FNF(w, D, A) znajduje forme normalna FNF dla slowa w, deterministycznego DFA D i alfabetu A.
Dzieje sie to wedlug algorytmu opisanego w ksiazce: V. Diekert, Y. Metivier– Partial commutation and traces, [w:] Handbook of Formal Languages, Springer, 1997
na stronie 10.
"""


def print_tab(T): # funkcja pomocnicza do wypisywania tablicy
    for line in T:
        print(line)


def find_FNF(w, D, A):
    print("Obliczanie FNF dla slowa: ", w)
    n = len(A)
    tab = [[] for _ in range(n)]
    depen = [[] for _ in range(n)]

    for i in range(len(D)):
        if D[i][1] != D[i][0]:
            depen[ord(D[i][0]) - 97].append(D[i][1])  # zaleznosci miedzy zmiennymi w D

    w = w[::-1]  # odwrocenie slowa bo slowo procedujemy od konca

    for ver in w:
        idx = ord(ver) - 97
        tab[idx].append(ver)  # wypelnianie tablicy zmiennymi
        dependencies = depen[idx]
        for dep in dependencies:
            tab[ord(dep) - 97].append('*')  # wypelnianie tablicy gwiazdkami

    print("Wypelniona tablica: ")
    print_tab(tab)

    FNF = ''
    x = 1
    while any(len(tab[i]) > 0 for i in range(n)):  # dopoki kazda tablica w tablicy tablic nie jest pusta
        flag = False  # flaga sprawdzajaca czy w danym kroku petli zostanie dodana jakas zmienna do FNF
        for i in range(n):
            if tab[i] and tab[i][-1] in A:
                flag = True

        if flag:  # dodajmy kalse do fnf, zbieramy zmienne z tablic gdzie sa one na pierwszym miejscu
            FNF += '('
            for i in range(n):
                if tab[i] and (len(tab[i]) > 0 and tab[i][-1] in A):
                    FNF += tab[i][-1]
                    tab[i].pop()
            FNF += ')'

        if not flag:  # usuwamy gwiazdki
            for i in range(n):
                if tab[i] and (len(tab[i]) > 0 and tab[i][-1] == '*'):
                    tab[i].pop()

        print(f"Tablica po {x} krokach: ")  # wypisanie tablicy po x krokach
        print_tab(tab)
        x += 1  # zwiekszenie liczby krokow

    return FNF

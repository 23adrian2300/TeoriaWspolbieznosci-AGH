"""
Funkcja tworzy zbior operacji, ktore bedziemy wykonywac, czyli jak w przykladzie A1,2 A1,3 A2,3 B1,2,2 itp.
Z racji iz w przykladzie mozna bylo zauwazyc schemat ich powstawania go wykorzystalem, zatem najpierw majac juz factors czyli nasze czynniki
latwo nam bylo stworzyc dzialania A np. A1,2. Nastepnie zauwazylem ze B i C wystepuja parami w sensie maja takie same indeksy, dlatego
dodajemy je na raz. Indeksy tez wydaja sie w miare latwe do zrobienia. Na podstawie przykladu stwierdzilem, ze pierwszy i trzeci sa takie same jak
indesky A. Srodkowy natomiast jest to liczba z przedzialu [pierwszy indeks A, dlugosc wiersza macierzy). Znaczek "*" jest pomocniczy i na konsoli jest on pomijany.
"""

def construct_sigma(mat, factors):
    sigma = []
    n = len(mat[0])
    for i in range(len(factors)):
        sigma.append(f"A{factors[i][0][0]},{factors[i][0][1]}")  # A1,2
        for j in range(factors[i][0][0], n + 1):
            sigma.append(f"B{factors[i][0][0]},{j},{factors[i][0][1]}")  # B1,1,3
            sigma.append(f"C{factors[i][0][0]},{j},{factors[i][0][1]}")  # C1,1,3
        sigma.append("*")
    return sigma


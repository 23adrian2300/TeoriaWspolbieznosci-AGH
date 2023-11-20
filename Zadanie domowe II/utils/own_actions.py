from utils.check_operations import check_operations
from utils.dependencies_independencies import find_dependencies, find_independencies
from utils.find_fnf import find_FNF
from utils.graph import process_tables, show_minimal_graph_dot, show_minimal_graph


"""
Mozna samemu stworzyc operacje, alfabet, slowo itd. Wszytsko odbywa sie zgdonie ze schematem i pewnymi zalozeniami.
Alafabet moze byc tylko z zakresu a-z, operacje musza byc w formacie: x=x+y, x=3x+z itd. Zmienne moga byc takie same jak
litery alfabetu, jednak dla czytelnosci nie jest to zalecane. Slowo musi byc zlozone z liter alfabetu.
Mozna wykorzystac dot do tworzenia grafow, ale nie jest to wymagane, gdyz potrzeba do tego na sciezce PATH programu dot.
"""

def create_own_actions():
    print("Jak duzo operacji chcialbys wykonac? Mozliwy zakres to 1-26")
    while True:
        try:
            n = int(input("Liczba operacji: "))
            if n < 1 or n > 26:
                print("Liczba operacji musi byc z zakresu 1-26")
                print("Sprobuj ponownie")
            else:
                break
        except ValueError:
            print("To nie jest liczba")

    print("Zatem twoj alfabet A to: ")
    A = []
    for i in range(n):
        print(chr(97 + i), end=" ")
        A.append(chr(97 + i))
    print()

    print("Teraz podaj z jakich zmiennych chcesz skorzystac, podaj je w formacie: x,x,x,x,....")
    while True:  # sprawdzanie poprawnosci wprowadzonych zmiennych
        variables = input("Zmienne: ").split(",")
        if all(var.isalpha() and len(var) == 1 for var in variables):
            break
        else:
            print("Podane zmienne musza byc literami. Sprobuj ponownie.")
    print("Twoje zmienne to: ")
    for i in variables:
        print(i, end=" ")

    operations = []
    print("Teraz podaj jakie operacje chcesz wykonac")
    for i in range(n):
        flag = False
        while not flag:
            print(chr(97 + i), end=" ")
            print("->", end=" ")
            op = input()
            op.replace(" ", "")
            flag = check_operations(op, variables) # sprawdzanie poprawnosci wprowadzonych operacji
            if flag:
                operations.append(op)

    dependencies = find_dependencies(operations, variables)  # obliczenie niezaleznosci
    print("D =", dependencies)

    independencies = find_independencies(dependencies, A)  # obliczenie zaleznosci
    print("I =", independencies)

    print("Teraz podaj slowo, ktore chcesz zapisac w FNF")
    while True:
        word = input("Slowo: ")
        if all(var.isalpha() and var in A for var in word):  # sprawdzanie poprawnosci wprowadzonego slowa
            break
        else:
            print("Podane slowo musi skladac sie z liter. Sprobuj ponownie.")

    result = find_FNF(word, dependencies, A) # obliczenie FNF
    print(f"FNF[{word}]:", result)
    vertexes, zal = process_tables(result, dependencies, A) # obliczenie tablic do tworzenia grafu

    print("Czy chcesz wyswietlic graf z pomoca dot? (tak/nie)")
    while True:
        s = input()
        if s == 'tak' or s == 'TAK' or s == 'Tak' or s == 'nie' or s == 'NIE' or s == 'Nie':
            break
        else:
            print("Bledna odpowiedz")

    if s == 'tak' or s == 'TAK' or s == 'Tak':
        show_minimal_graph_dot(vertexes, zal)  # wyswietlenie grafu z pomoca dot
    else:
        show_minimal_graph(vertexes, zal)  # wyswietlenie grafu bez pomocy dot

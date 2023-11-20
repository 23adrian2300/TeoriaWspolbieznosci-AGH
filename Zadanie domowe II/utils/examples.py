from utils.dependencies_independencies import find_dependencies, find_independencies
from utils.find_fnf import find_FNF
from utils.graph import process_tables, show_minimal_graph_dot, show_minimal_graph

"""
Przykladowe rozwiazania, zawarte w poleceniu. Wszystkie funkcje wykonuja sie same, nie potrzeba nic wprowadzac.
Mozna wykorzystac dot do tworzenia grafow, ale nie jest to wymagane, gdyz wymaga posiadania na sciezce PATH programu dot.
"""


def show_examples():
    print("Przyklad 1")

    A1 = ['a', 'b', 'c', 'd']
    print("A =", A1)

    operations1 = ['x=x+y', 'y=y+2z', 'x=3x+z', 'z=y-z']
    print("Operacje:")
    for i in range(len(operations1)):
        print(chr(i + 97), ") ", operations1[i])

    variables1 = ['x', 'y', 'z']
    print('Zmienne:', variables1)

    dependencies1 = find_dependencies(operations1, variables1)  # obliczenie niezaleznosc
    print("D =", dependencies1)

    independencies1 = find_independencies(dependencies1, A1)  # obliczenie zaleznosci
    print("I =", independencies1)

    word1 = 'baadcb'
    print("w =", word1)

    fnf1 = find_FNF(word1, dependencies1, A1)  # obliczenie FNF
    print(f"FNF[{word1}]:", fnf1)
    print("\n")

    vertexes1, zal1 = process_tables(fnf1, dependencies1, A1)  # obliczenie tablic do tworzenia grafu

    print("Czy chcesz wyswietlic graf z pomoca dot? (tak/nie)")
    while True:
        s = input()
        if s == 'tak' or s == 'TAK' or s == 'Tak' or s == 'nie' or s == 'NIE' or s == 'Nie':
            break
        else:
            print("Bledna odpowiedz")

    if s == 'tak' or s == 'TAK' or s == 'Tak':
        show_minimal_graph_dot(vertexes1, zal1)  # wyswietlenie grafu z pomoca dot
    else:
        show_minimal_graph(vertexes1, zal1)  # wyswietlenie grafu bez pomocy dot
    print()
    print("Przyklad 2")

    A2 = ['a', 'b', 'c', 'd', 'e', 'f']
    print("A =", A2)

    variables2 = ['x', 'y', 'z', 'w', 'v']
    print('Zmienne:', variables2)

    operations2 = ['x=x+1', 'y=y+2z', 'x=3x+z', 'w=w+v', 'z=y-z', 'v=x+v']
    print("Operacje:")
    for i in range(len(operations2)):
        print(chr(i + 97), ") ", operations2[i])

    dependencies2 = find_dependencies(operations2, variables2)  # obliczenie niezaleznosci
    print("D =", dependencies2)

    independencies2 = find_independencies(dependencies2, A2)  # obliczenie zaleznosci
    print("I =", independencies2)

    word2 = 'acdcfbbe'
    print("w =", word2)

    fnf2 = find_FNF(word2, dependencies2, A2)  # obliczenie FNF
    print(f"FNF[{word2}] =", fnf2)

    vertexes2, zal2 = process_tables(fnf2, dependencies2, A2)  # obliczenie tablic do tworzenia grafu

    if s == 'tak' or s == 'TAK' or s == 'Tak':
        show_minimal_graph_dot(vertexes2, zal2)  # wyswietlenie grafu z pomoca dot
    else:
        show_minimal_graph(vertexes2, zal2)  # wyswietlenie grafu bez pomocy dot

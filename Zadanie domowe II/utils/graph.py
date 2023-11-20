import networkx as nx
import matplotlib.pyplot as plt

"""
Poczatkowo przetwarzamy tablice FNF, D, A, aby stworzyc tablice wierzcholkow i tablice zaleznosci. 
Nastepnie tworzymy za pomoca networkx graf skierowany dla slowa.
Jego redukcje do minimalnej postaci wykonujemy dzieki pomocy funkcji transitive_reduction.
Funkcja ta dziala tak ze najpierw sprawdza czy graf jest skierowany, nastepnie tworzy sobie nowy graf ze wszytskimi wierzcholkami.
Pozniej zapisuje sobie w slowniku potomkow dla wierzcholkow. Iteruje po wierzcholkach od u do v (wierzcholek docelowy) i sprawdza czy wirzcholek docelowy jest juz w slowniku potomkow. 
Jesli tak to pomija taka krawedz, a jesli nie to dodaje krawedz do grafu.

Dodatakowo w celu rysowania wykresow stworzylem dwie funkcje show_graph i show_graph_with_dot.
Pierwsza z nich rysuje graf bez pomocy dot, a pozycje wierzcholkow sa tworzone za pomoca funkcji pos uwzgledniajac klase.
Druga korzysta z programu dot. W tym celu nalezy miec zainstalowany program dot i miec go na sciezce PATH.
Program mozna pobrac ze strony: https://graphviz.gitlab.io/download/.
Nastpenie rozpakowane archiwum nalezy dodac do zmiennej srodowiskowej PATH. np. PATH = C:\Graphviz\bin. 
Po ponownym uruchomieniu terminala wszytsko powinno dzialc poprawnie
"""
def process_tables(FNF, D, A):
    vertexes = []
    n = len(FNF)
    h = 0
    dep = [[] for i in range(len(A))]
    for i in range(len(D)):
        dep[ord(D[i][0]) - 97].append(D[i][1])  # tworzymy tablice gdzie w kazdej komorce jest lista zaleznosci

    x = 0  # zmienna okreslajaca klase - wykorzystawane w rysowaniu grafu bez dot

    for i in range(n):
        if FNF[i] in A:
            vertexes.append((FNF[i], h, x))  # tworzymy tablice wierzcholkow z ich indeksami i klasami
            h += 1
        if FNF[i] == '(':
            x += 1

    return vertexes, dep  # zwracamy tablice wierzcholkow i tablice zaleznosci


def create_word_graph(vertexes, dep):
    G = nx.DiGraph(strict=True)  # tworzymy graf skierowany

    for i in range(len(vertexes)):
        letter1 = vertexes[i][0] + str(vertexes[i][1])
        letter_label = vertexes[i][0]
        G.add_node(letter1, label=letter_label, instance=vertexes[i][2])  # tworzymy wierzcholki w grafie, letter1 okresla nam wierzcholek, letter_label to jego etykieta w grafie, instance to klasa wierzcholka

    n = len(vertexes)

    for i in range(n):
        idx = ord(vertexes[i][0]) - 97
        v = dep[idx]
        for j in range(i + 1, n):
            if vertexes[j][0] in v:
                G.add_edge(vertexes[i][0] + str(vertexes[i][1]), vertexes[j][0] + str(vertexes[j][1]))  # dodajemy tylko krawedzie, wtedy gdy litera zalezy od innej ktora jest dalej polozona w slowie np a1 -> b2, a1 -> c3, b2 -> c3, oczywiscie pod warunkiem ze zaleznosc istnieje

    return G


def show_graph(G, title, G_old):
    plt.figure(figsize=(8,6))

    pos = {
        node: (G_old.nodes[node]['instance'], G_old.nodes[node]['instance'] + ord(G_old.nodes[node]['label']))
        for node in G_old.nodes  # stworzeie pozycji dla wierzcholkow tak aby graf byl czytelny
    }

    labels = nx.get_node_attributes(G, 'label')  # Pobranie atrybutu 'label' dla wierzcholkow

    nx.draw(G, pos, with_labels=True, labels=labels, font_weight='bold', node_size=1000, node_color='white',
            edgecolors='black')  # rysowanie grafu

    plt.title(title)
    plt.show()  # wyswietlenie grafu


def show_graph_with_dot(G, title):
    plt.figure(figsize=(8, 6))

    pos = nx.nx_pydot.pydot_layout(G, prog="dot")  # stworzenie pozycji dla wierzcholkow za pomoca dot - wymaga posiadania na sciezce PATH programu dot

    labels = nx.get_node_attributes(G, 'label')

    nx.draw(G, pos, with_labels=True, labels=labels, font_weight='bold', node_size=1000, node_color='white',
            edgecolors='black')  # rysowanie grafu

    plt.title(title)
    plt.show()  # wyswietlenie grafu


def show_minimal_graph_dot(vertexes, dep):
    # Stworzenie grafu slowa
    word_graph = create_word_graph(vertexes, dep)
    # Usuwanie krawedzi, ktore nie sa konieczne za pomoca funkcji transitive_reduction
    minimalny_graf = nx.transitive_reduction(word_graph)

    # Przypisanie etykiet wierzcholkom
    for node in minimalny_graf.nodes():
        minimalny_graf.nodes[node]['label'] = word_graph.nodes[node]['label']

    # Wyswietlenie minimalnego grafu slowa
    show_graph_with_dot(minimalny_graf, 'Minimal word graph with dot')


def show_minimal_graph(vertexes, dep):
    # Stworzenie grafu slowa
    word_graph = create_word_graph(vertexes, dep)

    # Usuwanie krawedzi, ktore nie sa konieczne za pomoca funkcji transitive_reduction
    minimalny_graf = nx.transitive_reduction(word_graph)

    # Przypisanie etykiet wierzcholkom
    for node in minimalny_graf.nodes():
        minimalny_graf.nodes[node]['label'] = word_graph.nodes[node]['label']

    # Wyswietlenie minimalnego grafu slowa
    show_graph(minimalny_graf, 'Minimal word graph', word_graph)

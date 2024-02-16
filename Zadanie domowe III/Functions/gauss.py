"""
Eliminacje Gaussa wykonujemy standardowo. Jesli mamy 0 w sprawdzanym elemencie to nie ma sensu tam nic robic dlatego pomijamy.
Do obliczen wykorzystujemy concurrent.futures. Odpalamy sobie dla kazdego rzedu osobny watek aby przyspieszyc dzialanie.
"""

import concurrent.futures


def gauss_elimination(mat, row, factors):
    pivot = mat[row][row]
    for i in range(row + 1, len(mat)):
        if mat[i][row] == 0:
            continue
        factor = mat[i][row] / pivot
        factors.append(((row + 1, i + 1), factor))
        for j in range(row, len(mat[row])):
            mat[i][j] -= factor * mat[row][j]


def parallel_gauss_elimination(mat, factors):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(gauss_elimination, mat, row, factors) for row in range(len(mat))]
        concurrent.futures.wait(futures)







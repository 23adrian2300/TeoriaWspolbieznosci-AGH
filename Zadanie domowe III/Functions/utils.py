"""
Funkcje pomocnicze sluzace glownie do wypisywania na konsoli ladniej wynikow oraz danych. Dodatkowo funkcje extract_x_numbers(s)
sa do wydobycia z napisow potrzebnych liczb
"""


def extract_two_numbers(s):
    parts = ''.join(filter(lambda x: x.isdigit() or x == ',', s)).split(',')
    numbers = [int(part) for part in parts if part.isdigit()]
    return tuple(numbers)


def extract_three_numbers(s):
    parts = ''.join(filter(lambda x: x.isdigit() or x == ',', s)).split(',')
    numbers = [int(part) for part in parts if part.isdigit()]
    return numbers


def print_sigma(sigma):
    sigma1 = []
    for i in range(len(sigma)):
        if sigma[i] != "*":
            sigma1.append(sigma[i])
    print(sigma1)


def print_matrix(mat):
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            mat[i][j] = round(mat[i][j], 2)
            if j == len(mat[i]) - 1:
                print("|", mat[i][j], end=" ")
            else:
                print(mat[i][j], end=" ")
        print()


def print_factors(factors):
    for i in range(len(factors)):
        print("A" + str(factors[i][0][0]) + "," + str(factors[i][0][1]), "->", round(factors[i][1], 2))

"""
Glowna czesc programu, ktora pozwala na wybor przykladowych macierzy lub wprowadzenie wlasnej. Nastepnie wywoluje funkcje z Functions
"""
from Functions.dependencies import construct_D
from Functions.foata import construct_FNF
from Functions.gauss import parallel_gauss_elimination
from Functions.graph import draw_directed_graph
from Functions.sigma import construct_sigma
from Functions.utils import print_matrix, print_sigma, print_factors

mat = [[2.0, 1.0, 3.0, 6.0],
       [4.0, 3.0, 8.0, 15.0],
       [6.0, 5.0, 16.0, 27.0]]

mat1 = [[2.0, 4.0, 5.0, 6.0, 7.0, 1.0],
        [0.0, 5.0, 6.0, 7.0, 8.0, 2.0],
        [5.0, 6.0, 0.0, 8.0, 0.0, 3.0],
        [0.0, 7.0, 8.0, 9.0, 10.0, 4.0],
        [7.0, 8.0, 9.0, 10.0, 11.0, 5.0]]

mat2 = [[90.0, 14.0, 22.0],
        [14.0, 50.0, 4.0]]

matrixes = [mat, mat1, mat2]

if __name__ == "__main__":
    while True:
        n = input("Do you want to enter your own matrix or examples? (own/examples): ")
        if n == "own" or n == "examples":
            break
        else:
            print("Wrong input")
    if n == "own":
        n = int(input("Size of matrix: "))
        mat = []
        for i in range(n):
            row = list(map(float, input(f"Enter row {i + 1} (space-separated values): ").split()))
            while len(row) != n:
                print("Wrong input")
                row = list(map(float, input(f"Enter row {i + 1} (space-separated values): ").split()))
            mat.append(row)

        vector = list(map(float, input(f"Enter vector (space-separated values): ").split()))
        mat = [row + [vector[i]] for i, row in enumerate(mat)]
        print("Original matrix:")
        print_matrix(mat)
        factors = []
        parallel_gauss_elimination(mat, factors)
        print("\nFactors:")
        print_factors(factors)
        print("\nMatrix after parallel Gauss elimination:")
        print_matrix(mat)
        print("\nSigma:")
        sigma = construct_sigma(mat, factors)
        print_sigma(sigma)
        print("\nDependencies:")
        D = construct_D(construct_sigma(mat, factors))
        print(D)
        FNF = construct_FNF(sigma, D)
        print("\nFNF:")
        print(FNF)
        print("Graph saved to graphs/directed_graph_own.png")
        print("\n\n")

        draw_directed_graph(D, "own", FNF)
    if n == "examples":
        i = 0
        for mat in matrixes:
            i += 1
            print("Original matrix:")
            print_matrix(mat)
            factors = []
            parallel_gauss_elimination(mat, factors)
            print("\nFactors:")
            print_factors(factors)
            print("\nMatrix after parallel Gauss elimination:")
            print_matrix(mat)
            print("\nSigma:")
            sigma = construct_sigma(mat, factors)
            print_sigma(sigma)
            print("\nDependencies:")
            D = construct_D(construct_sigma(mat, factors))
            print(D)
            FNF = construct_FNF(sigma, D)
            print("\nFNF:")
            print(FNF)
            draw_directed_graph(D, "example" + str(i), FNF)
            print("Graph saved to graphs/directed_graph_example" + str(i) + ".png")
            print("\n\n")

"""
Funkcja ta tworzy nam postac normana Foaty. Z przykladu mozna wyciagnac wnioski, ze idziemy w kolejnosci dzialan oraz z racji, iz
np. A1,2 jest niezalezne od A1,3 to sa one w tej samej klasie. Nastepnie musia byc elementy z B, pozniej z C. Po tych operacjach
znowu wykonujemy A tak jak w przykladzie, zatem idac tym schematem mozemy stworzyc cale FNF
"""

from Functions.utils import extract_two_numbers, extract_three_numbers


def construct_FNF(sigma, D):
    FNF = []
    D.sort()
    A = []
    B = []
    C = []
    for i in range(len(sigma)):
        if "A" in sigma[i]:
            A.append(sigma[i])
        if "B" in sigma[i]:
            B.append(sigma[i])
        if "C" in sigma[i]:
            C.append(sigma[i])

    while A or B or C:
        x_max = float("inf")
        for i in range(len(A)):
            x, _ = extract_two_numbers(A[i])
            if x < x_max:
                x_max = x

        A1 = []
        i = 0
        while i < len(A):
            x, _ = extract_two_numbers(A[i])
            if x == x_max:
                A1.append(A[i])
                A.pop(i)
            else:
                i += 1

        FNF.append(A1)
        B1 = []
        i = 0

        while i < len(B):
            x, _, _ = extract_three_numbers(B[i])
            if x == x_max:
                B1.append(B[i])
                B.pop(i)
            else:
                i += 1

        C1 = []
        i = 0
        while i < len(C):
            x, _, _ = extract_three_numbers(C[i])
            if x == x_max:
                C1.append(C[i])
                C.pop(i)
            else:
                i += 1

        FNF.append(B1)
        FNF.append(C1)

    return FNF
"""
Funkcja tworzaca zaleznosci D. W tym celu pomagam sobie znaczkami "*", gdyz licze sobie ile poszczegole operacje maja elementow
oraz pozycje gwiazdek. Nastepnie odpowiednimi operacjami dodajemy sobie zaleznosci. Warto zauwazyc, iz momentami trudno dodac niektore
elementy i trzeba nieco kombinowac, stad chociazby flagi czy sortowania. Dodatkowo dzieki nim udalo sie zachowac calkiem dobra kolejnosc
elementow w D.
"""

from Functions.utils import extract_two_numbers, extract_three_numbers


def construct_D(sigma):
    D = []
    n = len(sigma)
    stars = [-1]
    k = 0
    for i in range(n):
        if sigma[i] != "*":
            k += 1
        else:
            stars.append(k)
            k += 1

    for i in range(1, len(stars)):
        A = sigma[stars[i - 1] + 1]
        for j in range(stars[i - 1] + 1, stars[i] + 1):
            if "B" in sigma[j]:
                D.append((A, sigma[j]))
                D.append((sigma[j], sigma[j + 1]))

        x, y = extract_two_numbers(A)
        for j in range(1, i):
            x1, y1 = extract_two_numbers(sigma[stars[j - 1] + 1])
            if x - 1 == x1 and y - 1 == y1:
                k = (f"C{x - 1},{x},{y - 1}", A)
                k1 = (f"C{x - 1},{x},{y}", A)
                if k not in D and k1 not in D:
                    D.append(k)
                    D.append(k1)
    sigma = sorted(sigma, reverse=True)
    for i in range(n):
        if sigma[i] == "*" or "A" in sigma[i] or "B" in sigma[i]:
            continue
        x, y, z = extract_three_numbers(sigma[i])
        for j in range(0, n):
            flag = True
            if sigma[j] == "*" or "A" in sigma[j]:
                continue

            for k in D:
                if k[0] == sigma[i] and "A" in k[1] and "C" in k[0] and "C" in sigma[j]:
                    flag = False
                    break

            if not flag:
                continue

            x1, y1, z1 = extract_three_numbers(sigma[j])

            if "C" in sigma[j] and "C" in sigma[i]:
                if x + 1 == x1 and y == y1 and z == z1:
                    k = (sigma[i], sigma[j])
                    if k not in D:
                        D.append(k)

            if (sigma[i], f"C{x + 1},{y},{z}") in D:
                continue

            if "C" in sigma[i] and "B" in sigma[j]:
                if (x + 1 == x1 and y == y1 and z + 1 == z1) or (x + 1 == x1 and y == y1 and z == z1):
                    k = (sigma[i], sigma[j])
                    if k not in D:
                        D.append(k)
    return D

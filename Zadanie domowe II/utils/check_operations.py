"""
Funkacja sprawdzajaca poprawnosc wprowadzonych operacji, musza byc one formatu: x=x+x,
gdzie x to zmienne a + to znak dzialania - dodawanie, - odejmowanie, innych nie obsluguje
"""
def check_operations(operations, variables):
    n = len(operations)
    if operations[1] != '=': # sprawdzanie czy drugi znak jest =
        print("Bledna operacja bo 2 znak nie jest =, a jest to", operations[1])
        return False
    chars = ['-', '+', '=', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] # lista znakow ktore moga wystapic w operacji
    for i in range(len(variables)):
        chars.append(variables[i]) # dodajemy zmienne do listy znakow
    for i in range(n):
        if operations[i] not in chars:
            print("Bledna operacja bo: ", operations[i], " nie jest zmienna")
            return False
    return True

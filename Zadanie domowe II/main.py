from utils.examples import show_examples
from utils.own_actions import create_own_actions

"""
Glowny plik programu. Umozliwia wybor czy chcemy skorzystac z przykladow z polecenia, czy chcemy sami wprowadzic dane.
Uruchamia odpowiednie funkcje w zaleznosci od wyboru
"""


if __name__ == '__main__':
    print("Czy chcesz skorzystac z przykladow? (tak/nie)")
    while True:
        flag = input()
        if flag == 'tak' or flag == 'TAK' or flag == 'Tak' or flag == 'nie' or flag == 'NIE' or flag == 'Nie':
            break
        else:
            print("Bledna odpowiedz")

    if flag == 'nie' or flag == 'NIE' or flag == 'Nie':
        create_own_actions()

    elif flag == 'tak' or flag == 'TAK' or flag == 'Tak':
        show_examples()

    print("Koniec programu")

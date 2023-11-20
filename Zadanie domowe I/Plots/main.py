import os

import matplotlib.pyplot as plt

sciezka = os.path.join(os.pardir, "Project", "Symulacja")

miejsceZapisu = os.path.join(os.getcwd(), "Wykresy")

for plik in os.listdir(miejsceZapisu):
    scPliku = os.path.join(miejsceZapisu, plik)
    try:
        if os.path.isfile(scPliku):
            os.unlink(scPliku)
    except Exception as e:
        print(f"Nie można usunąć pliku {scPliku}. Blad: {e}")

def wydostanieDanych(nazwaPliku):
    data = {}
    with open(os.path.join(sciezka, nazwaPliku), 'r', encoding='utf-8') as file:
        linie = file.readlines()
        klucz = None
        for line in linie:
            line = line.replace('Ăł', 'ó')
            if line.startswith("Wyniki dla"):
                klucz = line.strip()
                data[klucz] = []
            elif klucz is not None and "sredni czas oczekiwania" in line:
                time_str = line.split(": ")[1].split(" ms")[0]
                data[klucz].append(float(time_str))
    return data

file_names = ["wyniki2.txt", "wyniki3.txt", "wyniki4.txt", "wyniki5.txt","wyniki6.txt"]


for file_name in file_names:
    data = wydostanieDanych(file_name)
    fig, ax = plt.subplots()
    ax.boxplot(data.values())
    ax.set_xticklabels([f'N={int(key.split()[-2])}' for key in data.keys()], rotation=45)
    ax.set_ylabel('Czas oczekiwania (ms)')
    n_value = int(file_name.replace("wyniki", "").replace(".txt", ""))
    ax.set_xlabel(f'N = {n_value}')
    ax.set_title(f'Wykres pudełkowy czasu oczekiwania filozofów dla zadania {n_value}')
    output_file = os.path.join(miejsceZapisu, file_name.replace(".txt", ".png"))
    plt.savefig(output_file)
    plt.close() 


n_values = [5, 10, 15,100]
n_averages = []

for n in n_values:
    n_data = [wydostanieDanych(file_name) for file_name in file_names]
    n_averages.append(
        [sum(n_data[i][f'Wyniki dla {n} filozofow:']) / len(n_data[i][f'Wyniki dla {n} filozofow:']) for i in range(len(file_names))])

    labels = [f"Zadanie {i + 2}" for i in range(len(file_names))]

    task_colors = {'Zadanie 2': 'r', 'Zadanie 3': 'g', 'Zadanie 4': 'b', 'Zadanie 5': 'c', 'Zadanie 6': 'm'}

    for n, values in zip(n_values, n_averages):
        plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, alpha=0.7, color=[task_colors[label] for label in labels], label=f"N={n}")
    # plt.xlabel('Zadanie')
    plt.ylabel('Średni czas oczekiwania (ms)')
    plt.title(f'Średni czas oczekiwania dla N={n} w różnych zadaniach')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, value, round(value, 2), ha='center', va='bottom')

    output_file = os.path.join(miejsceZapisu, f"n_{n}_srednie.png")
    plt.savefig(output_file)
    plt.close()
print("Zapisano wykresy jako pliki PNG w katalogu 'wykresy'.")

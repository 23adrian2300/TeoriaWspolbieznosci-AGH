package agh.tw.Zadanie2;

import java.io.File;
import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.util.concurrent.Semaphore;

/* Poczatkowo uzywalem jeszcze jedengo dodatkowego semafor z dostepem do widelcow, jednak po zastanowieniu wydaje sie on byc zbedny
* dlatego też jego pozostałosci zakomentowałem.*/

class Widelec2 {
    int id;
    Boolean czyUzywany;
    public Semaphore semafor;

    public Widelec2(int id) {
        this.id = id;
        czyUzywany = false;
        semafor = new Semaphore(1);
    }

    void podnies() {
        try {
            if (!czyUzywany) {
            semafor.acquire();
            czyUzywany = true;}
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    void odloz() {
        czyUzywany = false;
        semafor.release();
    }
}

class Filozof2 extends Thread {
    int id;
    Widelec2 lewy;
    Widelec2 prawy;
//    Semaphore dostepDoWidelcow; // Dodatkowy semafor dla dostępu do obu widelców

    public Filozof2(int id) {
        this.id = id;
//        this.dostepDoWidelcow = dostepDoWidelcow;
    }

    private volatile boolean zastopowany = false;

    public void zatrzymajFilozofa() {
        zastopowany = true;
    }
    private long calkowityCzasOczekiwania = 0;
    private int liczbaOczekiwan = 0;

    public long getCalkowityCzasOczekiwania() {
        return calkowityCzasOczekiwania;
    }

    public int getLiczbaOczekiwan() {
        return liczbaOczekiwan;
    }
    void jedz() throws InterruptedException {
        long poczatek = System.currentTimeMillis();
//        dostepDoWidelcow.acquire();
        boolean acquired = false;
        while (!acquired) {
            if (!lewy.czyUzywany && !prawy.czyUzywany) {
                lewy.podnies();
                prawy.podnies();
                acquired = true;
            } else {
                // Filozof nie ma dostępu do obu widelców, więc kontynuuje oczekiwanie.
                Thread.sleep(10);
            }
        }
        long koniec = System.currentTimeMillis();
        System.out.println("Filozof " + id + " je");
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        lewy.odloz();
        prawy.odloz();
//        dostepDoWidelcow.release();
        calkowityCzasOczekiwania += (koniec - poczatek);
        liczbaOczekiwan++;
    }

    void mysl() {
        System.out.println("Filozof " + id + " mysli");
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    public void run() {
        while (!zastopowany) {
            mysl();
            try {
                jedz();
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
    }
}

public class Zadanie2 {
    public static void main(String[] args) {
        String sciezka;
        String currentDirectory = System.getProperty("user.dir");
        if (currentDirectory.endsWith("Project")) {
            sciezka = "Symulacja/wyniki2.txt";
        } else {
            sciezka = "../../../Symulacja/wyniki2.txt";
        }
        try {
            File file = new File(sciezka);
            FileOutputStream fos = new FileOutputStream(file, false);
            PrintWriter writer = new PrintWriter(fos);

            for (int N = 5; N < 21; N += 5) {
                if (N>15){
                    N=100;
                }
                System.out.println("Symulacja dla " + N + " filozofow");
                Widelec2[] widelce = new Widelec2[N];
                for (int i = 0; i < N; i++) {
                    widelce[i] = new Widelec2(i);
                }

//                Semaphore dostepDoWidelcow = new Semaphore(N - 1);

                Filozof2[] filozofowie = new Filozof2[N];
                for (int i = 0; i < N; i++) {
                    filozofowie[i] = new Filozof2(i);
                    filozofowie[i].lewy = widelce[i];
                    filozofowie[i].prawy = widelce[(i + 1) % N];
                }

                for (int i = 0; i < N; i++) {
                    filozofowie[i].start();
                }

                long czasSymulacji = 20000;

                try {
                    Thread.sleep(czasSymulacji);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                for (int i = 0; i < N; i++) {
                    filozofowie[i].zatrzymajFilozofa();
                }

                for (int i = 0; i < N; i++) {
                    try {
                        filozofowie[i].join();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }

                writer.println("Wyniki dla " + N + " filozofow:");
                for (int i = 0; i < N; i++) {
                    Filozof2 filozof = filozofowie[i];
                    long calkowityCzasOczekiwania = filozof.getCalkowityCzasOczekiwania();
                    int liczbaOczekiwan = filozof.getLiczbaOczekiwan();
                    if (liczbaOczekiwan > 0) {
                        double sredniCzasCzekania = (double) calkowityCzasOczekiwania / liczbaOczekiwan;
                        writer.println("Filozof " + i + " sredni czas oczekiwania na dostep do widelcow: " + sredniCzasCzekania + " ms");
                    } else {
                        writer.println("Filozof " + i + " nie czekal na dostep do widelcow.");
                    }
                }
            }
            writer.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}


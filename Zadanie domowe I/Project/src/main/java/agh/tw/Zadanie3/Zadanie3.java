package agh.tw.Zadanie3;

import java.io.File;
import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.util.Objects;
import java.util.concurrent.Semaphore;

class Widelec3 {
    int id;
    Boolean czyUzywany;
    public Semaphore semafor;

    public Widelec3(int id) {
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

class Filozof3 extends Thread {
    int id;
    Widelec3 lewy;
    Widelec3 prawy;

    public Filozof3(int id) {
        this.id = id;
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
        boolean lewyZajety = false;
        boolean prawyZajety = false;
        while (!(lewyZajety && prawyZajety)) {
            if (id % 2 == 0) {
                // Filozof o parzystym numerze zaczyna od podniesienia prawego widelca.
                if (!prawy.czyUzywany && !prawyZajety) {
                    prawy.podnies();
                    prawyZajety = true;
                }
                if (!lewy.czyUzywany && prawyZajety) {
                    lewy.podnies();
                    lewyZajety = true;
                }
            } else {
                // Filozof o nieparzystym numerze zaczyna od podniesienia lewego widelca.
                if (!lewy.czyUzywany && !lewyZajety) {
                    lewy.podnies();
                    lewyZajety = true;
                }
                if (!prawy.czyUzywany && lewyZajety) {
                    prawy.podnies();
                    prawyZajety = true;
                }
            }

            if (!(lewyZajety && prawyZajety)) {
                // Filozof nie ma dostępu do obu widelców, więc kontynuuje oczekiwanie.
                Thread.sleep(10); // Odczekaj krótki czas i sprawdź ponownie.
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

public class Zadanie3 {
    public static void main(String[] args) {
        String sciezka;
        String currentDirectory = System.getProperty("user.dir");
        if (currentDirectory.endsWith("Project")) {
            sciezka = "Symulacja/wyniki3.txt";
        } else {
            sciezka = "../../../Symulacja/wyniki3.txt";
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
                Widelec3[] widelce = new Widelec3[N];
                for (int i = 0; i < N; i++) {
                    widelce[i] = new Widelec3(i);
                }

                Filozof3[] filozofowie = new Filozof3[N];
                for (int i = 0; i < N; i++) {
                    filozofowie[i] = new Filozof3(i);
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
                    Filozof3 filozof = filozofowie[i];
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


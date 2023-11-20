package agh.tw.Zadanie4;

import java.io.File;
import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.util.Random;
import java.util.concurrent.Semaphore;

class Widelec4 {
    int id;
    Boolean czyUzywany;
    public Semaphore semafor;

    public Widelec4(int id) {
        this.id = id;
        czyUzywany = false;
        semafor = new Semaphore(1);
    }

    void podnies() {
        try {
            if (!czyUzywany) {
                semafor.acquire();
                czyUzywany = true;
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    void odloz() {
        czyUzywany = false;
        semafor.release();
    }

}

class Filozof4 extends Thread {
    int id;
    Widelec4 lewy;
    Widelec4 prawy;

    public Filozof4(int id) {
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
        Random generator = new Random();
        int losowaLiczba = generator.nextInt(2);
        boolean lewyZajety = false;
        boolean prawyZajety = false;

        while (!(lewyZajety && prawyZajety)) {
            if (losowaLiczba == 0) {
                // Filozof z losem 0 zaczyna od podniesienia prawego widelca
                if (!prawy.czyUzywany && !prawyZajety) {
                    prawy.podnies();
                    prawyZajety = true;
                }
                if (!lewy.czyUzywany && prawyZajety) {
                    lewy.podnies();
                    lewyZajety = true;
                }
            } else {
                // Filozof z losem 1 zaczyna od podniesienia lewego widelca
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

public class Zadanie4 {
    public static void main(String[] args) {
        String sciezka;
        String currentDirectory = System.getProperty("user.dir");
        if (currentDirectory.endsWith("Project")) {
            sciezka = "Symulacja/wyniki4.txt";
        } else {
            sciezka = "../../../Symulacja/wyniki4.txt";
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
                Widelec4[] widelce = new Widelec4[N];
                for (int i = 0; i < N; i++) {
                    widelce[i] = new Widelec4(i);
                }

                Filozof4[] filozofowie = new Filozof4[N];
                for (int i = 0; i < N; i++) {
                    filozofowie[i] = new Filozof4(i);
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
                    Filozof4 filozof = filozofowie[i];
                    long calkowityCzasCzekania = filozof.getCalkowityCzasOczekiwania();
                    int liczbaOczekiwan = filozof.getLiczbaOczekiwan();
                    if (liczbaOczekiwan > 0) {
                        double sredniCzasCzekania = (double) calkowityCzasCzekania / liczbaOczekiwan;
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

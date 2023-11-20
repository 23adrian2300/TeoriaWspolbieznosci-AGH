package agh.tw.Zadanie6;

import java.io.File;
import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.util.concurrent.Semaphore;

class Arbiter6 { // zezwala na dostep do jadalni tylko N-1 filozofom
    Semaphore semaforArbitra;

    public Arbiter6(int N) {
        this.semaforArbitra = new Semaphore(N - 1);
    }

    public void zajmijDostep() throws InterruptedException {
        this.semaforArbitra.acquire();
    }

    public void zwolnijDostep() {
        this.semaforArbitra.release();
    }
}

class Widelec6 {
    int id;
    Boolean czyUzywany;
    public Semaphore semafor;

    public Widelec6(int id) {
        this.id = id;
        this.czyUzywany = false;
        this.semafor = new Semaphore(1);
    }

    void podnies() {
        try {
            semafor.acquire();
            czyUzywany = true;
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    void odloz() {
        czyUzywany = false;
        semafor.release();
    }
}

class Filozof6 extends Thread {
    int id;
    Widelec6 lewy;
    Widelec6 prawy;
    Arbiter6 arbiter;

    public Filozof6(int id, Arbiter6 arbiter) {
        this.id = id;
        this.arbiter = arbiter;
    }

    private volatile boolean zastopowany = false;
    private long calkowityCzasOczekiwania = 0;
    private int liczbaOczekiwan = 0;
    public void zatrzymajFilozofa() {
        zastopowany = true;
    }
    public long getCalkowityCzasOczekiwania() {
        return calkowityCzasOczekiwania;
    }

    public int getLiczbaOczekiwan() {
        return liczbaOczekiwan;
    }

    void jedz() throws InterruptedException { // filozofowie moga jesc w jadalni
        long poczatek = System.currentTimeMillis();
        if (arbiter != null) {
            arbiter.zajmijDostep();
        }
        boolean lewyZajety = false;
        boolean prawyZajety = false;


        while (!(lewyZajety && prawyZajety))  {
            if (!lewy.czyUzywany && !lewyZajety) {
                lewy.podnies();
                lewyZajety = true;
            }
            if (!prawy.czyUzywany && lewyZajety) {
                prawy.podnies();
                prawyZajety = true;
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
        if (arbiter != null) {
            arbiter.zwolnijDostep();
        }

        calkowityCzasOczekiwania += (koniec - poczatek);
        liczbaOczekiwan++;
    }

    void jedzNaKorytarzu() throws InterruptedException { // filozofowie jedza swoj posilek na korytarzu
        long poczatek = System.currentTimeMillis();

        boolean lewyZajety = false;
        boolean prawyZajety = false;

        while (!(lewyZajety && prawyZajety))  {
            if (!prawy.czyUzywany && !prawyZajety) {
                prawy.podnies();
                prawyZajety = true;
            }
            if (!lewy.czyUzywany && prawyZajety) {
                lewy.podnies();
                lewyZajety = true;
            }
            if (!(lewyZajety && prawyZajety)) {
                // Filozof nie ma dostępu do obu widelców, więc kontynuuje oczekiwanie.
                Thread.sleep(10);
            }
        }

        long koniec = System.currentTimeMillis();
        System.out.println("Filozof " + id + " je na korytarzu");
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
                if (arbiter.semaforArbitra.availablePermits() != 0) { // jesli nie ma miejsca w jadalni to jedz na korytarzu
                    jedz();
                } else {
                    jedzNaKorytarzu();
                }
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
    }
}

public class Zadanie6 {
    public static void main(String[] args) {
        String sciezka;
        String currentDirectory = System.getProperty("user.dir");
        if (currentDirectory.endsWith("Project")) {
            sciezka = "Symulacja/wyniki6.txt";
        } else {
            sciezka = "../../../Symulacja/wyniki6.txt";
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
                Widelec6[] widelce = new Widelec6[N];
                for (int i = 0; i < N; i++) {
                    widelce[i] = new Widelec6(i);
                }

                Arbiter6 arbiter = new Arbiter6(N);

                Filozof6[] filozofowie = new Filozof6[N];
                for (int i = 0; i < N; i++) {
                    filozofowie[i] = new Filozof6(i, arbiter);
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
                    Filozof6 filozof = filozofowie[i];
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

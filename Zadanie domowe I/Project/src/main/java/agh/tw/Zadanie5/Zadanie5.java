package agh.tw.Zadanie5;

import java.io.File;
import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.util.concurrent.Semaphore;

class Arbiter5 {
    Semaphore semaforArbitra;

    public Arbiter5(int N) {
        this.semaforArbitra = new Semaphore(N - 1);
    }

    public void zajmijDostep() throws InterruptedException {
        semaforArbitra.acquire();
    }

    public void zwolnijDostep() {
        semaforArbitra.release();
    }
}

class Widelec5 {
    int id;
    Boolean czyUzywany;
    public Semaphore semafor;

    public Widelec5(int id) {
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

class Filozof5 extends Thread {
    int id;
    Widelec5 lewy;
    Widelec5 prawy;
    Arbiter5 arbiter;

    public Filozof5(int id, Arbiter5 arbiter) {
        this.id = id;
        this.arbiter = arbiter;
    }

    private volatile boolean zastopowany = false;
    private long calkowityCzasCzekania = 0;
    private int liczbaOczekiwan = 0;
    public void zatrzymajFilozofa() {
        zastopowany = true;
    }
    public long getCalkowityCzasCzekania() {
        return calkowityCzasCzekania;
    }

    public int getLiczbaOczekiwan() {
        return liczbaOczekiwan;
    }



    void jedz() throws InterruptedException {
        long poczatek = System.currentTimeMillis();
        boolean lewyZajety = false;
        boolean prawyZajety = false;
        arbiter.zajmijDostep();
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
        arbiter.zwolnijDostep();

        calkowityCzasCzekania += (koniec - poczatek);
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
                while(true){
                    if (arbiter.semaforArbitra.availablePermits() != 0){
                        jedz();
                        break;
                    } else {
                        Thread.sleep(10);
                    }

                }
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
    }
}

public class Zadanie5 {
    public static void main(String[] args) {
        String sciezka;
        String currentDirectory = System.getProperty("user.dir");
        if (currentDirectory.endsWith("Project")) {
            sciezka = "Symulacja/wyniki5.txt";
        } else {
            sciezka = "../../../Symulacja/wyniki5.txt";
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
                Widelec5[] widelce = new Widelec5[N];
                for (int i = 0; i < N; i++) {
                    widelce[i] = new Widelec5(i);
                }

                Arbiter5 arbiter = new Arbiter5(N);

                Filozof5[] filozofowie = new Filozof5[N];
                for (int i = 0; i < N; i++) {
                    filozofowie[i] = new Filozof5(i, arbiter);
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
                    Filozof5 filozof = filozofowie[i];
                    long calkowityCzasCzekania = filozof.getCalkowityCzasCzekania();
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

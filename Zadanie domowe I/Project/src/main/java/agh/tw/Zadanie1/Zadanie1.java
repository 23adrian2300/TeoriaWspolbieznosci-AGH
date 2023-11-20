package agh.tw.Zadanie1;

import java.util.concurrent.Semaphore;

class Widelec1{
    int id;
    Boolean czyUzywany;
    public Semaphore semafor;
    public Widelec1(int id){
        this.id = id;
        this.czyUzywany = false;
        semafor = new Semaphore(1);
    }
    void podnies() {
        try {
            semafor.acquire();
            this.czyUzywany = true;
            wypiszStan(); // wypisuje stan widelca
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    void odloz() {
        this.czyUzywany = false;
        semafor.release();
        wypiszStan();
    }
    void wypiszStan() {
        System.out.println("Stan Widelec " + id + ": " + (czyUzywany ? "1" : "0"));
    }
}

class Filozof1 extends Thread{
    int id;
    Widelec1 lewy;
    Widelec1 prawy;

    public Filozof1(int id){
        this.id = id;
    }
    void jedz() {
        lewy.podnies();
        if (!prawy.czyUzywany) {
            prawy.podnies();
            System.out.println("Filozof " + id + " je");
            lewy.odloz();
            prawy.odloz();
    }
    }
        void mysl(){
        System.out.println("Filozof " + id + " myśli");
    }

    public void run(){
        while(true){
            try {
                mysl();
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }

            try {
                jedz();
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
    }

}


public class Zadanie1 {
    public static void main(String[] args) {
        int N = 5;
        Widelec1[] widelce = new Widelec1[N];
        for (int i = 0; i < N; i++) {
            widelce[i] = new Widelec1(i);
        }

        Filozof1[] filozofowie = new Filozof1[N];
        for (int i = 0; i < N; i++) {
            filozofowie[i] = new Filozof1(i);
            filozofowie[i].lewy = widelce[i];
            filozofowie[i].prawy = widelce[(i + 1) % N];
        }

        for (int i = 0; i < N; i++) {
            filozofowie[i].start();
        }
        Thread czasMonitorThread = new Thread(() -> {
            try {
                Thread.sleep(10000);
                System.exit(0);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });

        czasMonitorThread.start();
    }
}


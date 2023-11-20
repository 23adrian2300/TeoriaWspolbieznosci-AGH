package agh.tw;

import java.lang.reflect.Method;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class Main {
    public static void main(String[] args) {
        String sciezka = "Symulacja";
        try {
            Files.walk(Paths.get(sciezka))
                    .filter(Files::isRegularFile)
                    .map(java.nio.file.Path::toFile)
                    .forEach(File::delete);
        } catch (IOException e) {
            e.printStackTrace();
        }

        String[] nazwyKlas = {
                "agh.tw.Zadanie2.Zadanie2",
                "agh.tw.Zadanie3.Zadanie3",
                "agh.tw.Zadanie4.Zadanie4",
                "agh.tw.Zadanie5.Zadanie5",
                "agh.tw.Zadanie6.Zadanie6"
        };

        for (String nazwaKlasy : nazwyKlas) {
            try {
                Class<?> clazz = Class.forName(nazwaKlasy);
                Method mainMethod = clazz.getMethod("main", String[].class);

                System.out.println("---------- " + nazwaKlasy + " ----------");

                String[] mainArgs = new String[1];
                mainMethod.invoke(null, (Object) mainArgs);

                System.out.println("-------- Koniec " + nazwaKlasy + " ----------");
                System.out.println();

            } catch (ClassNotFoundException e) {
                System.err.println("Klasa nie znaleziona: " + nazwaKlasy);
            } catch (NoSuchMethodException e) {
                System.err.println("Glowna metoda nie znaleziona: " + nazwaKlasy);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        System.out.println("Pliki zostaly zapisane. Program konczy dzialanie.");
        System.exit(0);
    }
}

# Adatbázis konverter

A program MySQL adatbázis tábláinak adatainak CSV fájlba való mentésére szolgál.

## Használat

1. Konfiguráció beállítása a config.py fájlban: configuration/config.py.
2. A main.py fájl futtatása: py_file/main.py.
3. Konvertálni kívánt táblák kiválasztása a jelölőnégyzetekkel.
4. "Save" gombbal kiválasztás véglegesítése és konvertálás.
5. "Exit" gombbal kiléphet a programból.
6. A konvertált CSV fájlok a csv_files mappában lesznek elérhetőek.

## Hibák

- Program leáll. Terminál hibaüzenet: "Felhasználónév vagy jelszó nem egyezik"

   Ellenőrizze a config.py fájban helyesen van-e megadva a felhasználónév, jelszó páros.
- Program leáll. Terminál hibaüzenet:"Adatbázis nem létezik"
   
   Ellenőrizze helyesen írta-e be az adatbázis nevét vagy létezik-e az adatbázis.
- Üzenetablak: "Nem találhatók táblák!"

    Az adatbázis nem tartalmaz táblákat.

## Készítette

Szalai Balázs

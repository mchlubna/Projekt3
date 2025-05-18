# Projekt 3 – Volební Výsledky
Tento projekt získává výsledky voleb z oficiálních stránek volby.cz, zpracovává je a ukládá do `.csv` souboru.  


### Instalace a požadavky  
Knihovny které jsou použity v tomto projektu jsou uloženy v souboru requirements.txt. Pro instalaci doporučiuji využít nové virtualní prostředí a spustit nasledovně:
$ pip3 --version
$ pip3 install- r requirements.txt


### Spouštění
Spouštění souboru main.py z příkazové řádky vyžaduje dva povinné argumenty: Okres a Jmeno vystupniho souboru

Př.: C:\Users\Martin\Documents\Python akademie\Projekt3\virtualni_prostredi_project3>python main.py Jeseník "Vysledky voleb okres Jesenik"

Vyledky voleb se nasledně stáhonou jako .csv soubor se zadaným jménem


### Průběh stahování
STAHUJI VÝSLEDKY VOLEB PRO ZADANÝ OKRES:  Prostějov
VYTVÁŘÍM SOUBOR: vysledek.csv S VOLEBNÍMI VÝSLEDKY PRO OKRES:  Prostějov
DATA BYLA ÚSPĚŠNĚ ULOŽENA DO SOUBORU: vysledek.csv. UKONČUJI PROGRAM

### Částečný výsledek
code,location,registered,envelopes,valid....
506761;Alojzov;205;145;144;29;0;0;9;0;5;17;4;1;1;0;0;18;0;5;32;0;0;6;0;0;1;1;15;0
589268;Bedihošť;834;527;524;51;0;0;28;1;13;123;2;2;14;1;0;34;0;6;140;0;0;26;0;0;0;0;82;1
589276;Bílovice-Lutotín;431;279;275;13;0;0;32;0;8;40;1;0;4;0;0;30;0;3;83;0;0;22;0;0;0;1;38;0




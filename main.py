"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Martin Chlubna
email: chlubnam@seznam.cz
"""

from requests import get
from bs4 import BeautifulSoup as bs
import csv
import sys

def najdi_odkaz_pro_mesto(mesto: str):
    """
    Funkce najde URL odkaz pro zadane mesto
    """
    adresa = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    html_doc = get(adresa)

    rozdelene_html = bs(html_doc.text, features="html.parser")
    # Najde <tr> obsahující dané město
    tr_mesto = rozdelene_html.select_one(f'tr:has(td:-soup-contains("{mesto}"))')
    #print(tr_mesto)

    if tr_mesto:
        # Najde tag <a> tv daném <tr>, jehož href začíná na "ps32"
        a_tag = tr_mesto.select_one('a[href^="ps32"]')
        if a_tag:
            return a_tag['href']


def ziskej_obce_a_odkazy(okres: str):
    """
    Funkce získá seznam obci pro zadanz okres
    """
    adresa = "https://www.volby.cz/pls/ps2017nss/" + okres
    html_doc = get(adresa)

    rozdelene_html = bs(html_doc.text, features="html.parser")
    rows = rozdelene_html.find_all("tr")
    
    #prazdný seznam pro Obec, Odkaz a Cislo
    obec_odkaz_cislo = []

    for row in rows:
        obec = row.find("td", {"class": "overflow_name"})
        odkaz = row.find("td", {"class": "cislo"})
        
        if odkaz:
            odkaz = odkaz.select_one('a[href^="ps311"]')
            if odkaz:  # Ověření, že <a> existuje
                cislo = odkaz.text
                obec_odkaz_cislo.append([obec.text.strip(), "https://www.volby.cz/pls/ps2017nss/" + odkaz['href'], cislo])

    return obec_odkaz_cislo




def ziskej_vysledky_voleb(odkaz: str, code: str, location: str):
    """
    Funkce získává výsledky voleb z daného URL, zpracuje data a uloží je do seznamu.
    """
    
    # Stažení HTML
    html_doc = get(odkaz)
    rozdelene_html = bs(html_doc.text, features="html.parser")

    # Vytvoření slovníku s daty
    vyledky_hlasovani = {
        "code": code,
        "location": location,
        "registered": rozdelene_html.find("td", {"class":"cislo","data-rel":"L1","headers":"sa2"}).text,
        "envelopes": rozdelene_html.find("td", {"class":"cislo","data-rel":"L1","headers":"sa3"}).text,
        "valid": rozdelene_html.find("td", {"class":"cislo","data-rel":"L1","headers":"sa6"}).text
    }

    # Získání počtu hlasů pro jednotlivé strany
    rows = rozdelene_html.find_all("tr")

    for row in rows:
        nazev_strany = row.find('td', {"class":"overflow_name"})
        hlasy = row.find('td', {"class":"cislo","headers":"t1sa2 t1sb3"})
        if nazev_strany and hlasy:
            nazev_strany = row.find('td', {"class":"overflow_name","headers":"t1sa1 t1sb2"}).text
            hlasy = row.find('td', {"class":"cislo","headers":"t1sa2 t1sb3"}).text
            vyledky_hlasovani[nazev_strany] = hlasy

        hlasy = row.find('td', {"class":"cislo","headers":"t2sa2 t2sb3"})
        if nazev_strany and hlasy:
            nazev_strany = row.find('td', {"class":"overflow_name","headers":"t2sa1 t2sb2"}).text
            hlasy = row.find('td', {"class":"cislo","headers":"t2sa2 t2sb3"}).text
            vyledky_hlasovani[nazev_strany] = hlasy
    return(vyledky_hlasovani)

   
def hlavni_funkce(okres: str, csv_file: str):
    """
    Hlavni funkce programu. Spusti funkce pro generovani vysledků voleb a zapise je do .csv souboru.
    """

    obce_s_vysledky = []
    odkaz_okres = najdi_odkaz_pro_mesto(okres)

    if odkaz_okres:
        print(f"STAHUJI VÝSLEDKY VOLEB PRO ZADANÝ OKRES:  {okres}")
        for obec in ziskej_obce_a_odkazy(odkaz_okres):
            obce_s_vysledky.append(ziskej_vysledky_voleb(obec[1], obec[2], obec[0]))
        csv_file = csv_file + ".csv"
        # Otevření souboru pro zápis
        print(f"VYTVÁŘÍM SOUBOR: {csv_file} S VOLEBNÍMI VÝSLEDKY PRO OKRES:  {okres}")
        with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as csvfile:
            zahlavi = obce_s_vysledky[0].keys()  # Získání názvů sloupců
            zapisovac = csv.DictWriter(csvfile, fieldnames=zahlavi, delimiter=";")

            zapisovac.writeheader()  # Zápis hlaviček
            zapisovac.writerows(obce_s_vysledky)  # Zápis dat

        print(f"DATA BYLA ÚSPĚŠNĚ ULOŽENA DO SOUBORU: {csv_file}. UKONČUJI PROGRAM")
    else:
        print(f"Zadaný okres \"{okres}\" neexistuje, zadejte správný okres.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Nejsou zadany všechny potřebné argumenty")
    else:
        okres =sys.argv[1]
        soubor = sys.argv[2]
        hlavni_funkce(okres,soubor)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from bs4 import BeautifulSoup
import requests
import re


class Gestionlienscrap:
    """Cette class va me permettre de gérer tout le scraping des sites web de ma BDD"""

    def __init__(self):

        self.lientitre = ""
        self.liendescr = ""
        self.lienh1 = ""
        self.h2 = []
        self.lienh2 = ""
        self.h3 = []
        self.lienh3 = ""
        self.h4 = []
        self.lienh4 = ""
        self.strong = []
        self.lienstrong = ""
        self.aside = []
        self.lienaside = ""
        self.tag = []
        self.lientag = ""

    def scraping(self, monurl):
        """Cette fonction va me permettre de 'scraper' les liens en paramètre."""

        self.lientitre = ""
        self.liendescr = ""
        self.lienh1 = ""
        self.h2 = []
        self.lienh2 = ""
        self.h3 = []
        self.lienh3 = ""
        self.h4 = []
        self.lienh4 = ""
        self.strong = []
        self.lienstrong = ""
        self.aside = []
        self.lienaside = ""
        self.tag = []
        self.lientag = ""

        print("lancement de la fonction de scraping")
        reponse = requests.get(monurl)
        soup = BeautifulSoup(reponse.text, "html5lib")

        # Récupération du titre
        try:
            self.lientitre = soup.title.string
        except AttributeError:
            self.lientitre = ""

        # Récupération du h1
        try:
            self.lienh1 = soup.h1.string
        except AttributeError:
            self.lienh1 = ""

        # Récupération de la description
        for data in soup.find_all("header"):
            for mon_data in data.find_all("p", {"class": "site-description"}):
                self.liendescr = mon_data.string

        # Récupération des titres de la partie "section - content"
        for data in soup.find_all("section", {"id": "content"}):
            # travail sur le h2
            for mon_data in data.find_all("h2"):
                self.h2.append(mon_data.get_text())
                self.lienh2 = ','.join(self.h2)
            # travail sur le h3
            for mon_data in data.find_all("h3"):
                self.h3.append(mon_data.get_text())
                self.lienh3 = ','.join(self.h3)
            # travail sur le h4
            for mon_data in data.find_all("h4"):
                self.h4.append(mon_data.get_text())
                self.lienh4 = ','.join(self.h4)
            # travail sur le strong
            for mon_data in data.find_all("strong"):
                self.strong.append(mon_data.get_text())
                self.lienstrong = ','.join(self.strong)
        # Recherche des catégories
        for data in soup.find_all(class_=re.compile("cat")):
            for data1 in data.find_all("a"):
                self.aside.append(data1.get_text())
                self.lienaside = ','.join(self.aside)

        # Recherche des mots-clefs
        for data in soup.find_all(class_=re.compile("tag")):
            for data1 in data.find_all("a"):
                self.tag.append(data1.get_text())
                self.lientag = ','.join(self.tag)

        print(f"titre: {self.lientitre}")
        print(f"description: {self.liendescr}")
        print(f"h1: {self.lienh1}")
        print(f"h2: {self.lienh2}")
        print(f"h3: {self.lienh3}")
        print(f"h4: {self.lienh4}")
        print(f"strong: {self.lienstrong}")
        print(f"Les catégories : {self.lienaside}")
        print(f"Les tags : {self.lientag}")

        return self.lientitre, self.liendescr, self.lienh1, self.lienh2, self.lienh3, self.lienh4, self.lienstrong, \
        self.lienaside, self.lientag

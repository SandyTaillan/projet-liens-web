# -*- coding: utf-8 -*-

# todo : Pour les liens non valides : les retester à intervalle régulier
# todo : pour les liens valides : faire du web scraping pour récolter les données souhaitées.
# todo : Faire une fonction update pour récupérer les mises à jours de la DBB de Firefox
# todo : Gérer les exceptions sur la BDD -> que se passe-t-il si je ne trouve pas le chemin bdd de Firefox par exemple
# todo : ne vérifier que 100 lignes de liens à la fois ou tout vérifier d'un coup -> demande dans interface graphique
# todo : gérer les url doublons

# En python 3.7

"""Le but de ce script est gérer mes marques-pages Firefox.
    La gestion de ces marques-pages va se faire en plusieurs temps :
    - création d'une base de données ;
    - gestion des liens à problèmes : inexistant, erreur d'http, etc... ;
    - gestion des mots-clefs pour le tri à la demande.
"""

# importation des modules
import os
# importation des autres fichiers de ce programme
import gestion_liens_web as glw
from liens_scraping import Scrap as lscr


class Main(lscr):
    """Cette classe est la jonction entre tous les autres fichiers de ce programme.
    Il va permettre de lier les scripts de l'interface graphique avec ceux destinés aux calculs."""

    def __init__(self):
        super(Main, self).__init__()

        self.lientitre = ""
        self.liendescr = []
        self.lienh1 = ""
        self.lienh2 = []
        self.lienh3 = []
        self.lienh4 = []
        self.lienstrong = []
        self.lienaside = []
        self.lientag = []

        self.url = ""
        self.bdgesscrap = []
        # Chemin de ma propre base de données.
        chembd = 'data/bd-liens.sqlite'

        # vérifier si ma base de données existe si ce n'est pas le cas, elle est créée.
        if not os.path.isfile(chembd):
            print("Dans le main :\nLa base de données va être créée")
            glw.creabd()
        else:
            print("Dans le main : \nla base de données existe bien")

        # Vérification de la validité des liens
            #glw.veriflien()

        self.scraping()


    def scraping(self):
        """Gestion du scraping des sites internet."""
        print("on entre dans la fonction de scraping du main")
        # Déclaration des variables
        self.donnscrap = []
        # lancement de la fonction pour récupérer les liens à traiter de la BDD
        self.bdgesscrap = glw.recupbddscraping()
        print("Dans le main, fonction scraping :\nRécupération de self.bdgesscrap")
        print(self.bdgesscrap)
        print(type(self.bdgesscrap))
        if self.bdgesscrap[2] == '-':
            url = self.bdgesscrap[1]
            print(f"url dans scraping : {url}")
            self.lientitre, self.liendescr, self.lienh1, self.lienh2, self.lienh3, self.lienh4, self.lienstrong,\
            self.lienaside, self.lientag = lscr.scrapingurl(self, url)
        print("J'en suis là !! -------------------------")

        self.donnscrap = [self.bdgesscrap[0], self.lientitre, self.liendescr, self.lienh1, self.lienh2, self.lienh3,
                          self.lienh4, self.lienstrong, self.lienaside, self.lientag]
        print(f"donnscrap : {self.donnscrap}")
        glw.envoiedonnscraping(self.donnscrap)


Main()

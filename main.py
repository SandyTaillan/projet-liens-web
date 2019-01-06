# -*- coding: utf-8 -*-
#

# importation des modules
# English : import of modules
import os
# importation des autres fichiers de ce programme
# importation of others files of this programme
import utils as utl
from gestbdd import Gestionbdd as Gbdd
from gestlien import Gestionlienweb as Glw
from gestscrap import Gestionlienscrap as Glsc


class Main(Gbdd):
    def __init__(self):
        super(Main, self).__init__()
        
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

        # vérifier si ma base de données existe si ce n'est pas le cas, elle est créée.
        # English : check if my database exists if it doesn't, it is created.

        print(f"voici le chemin utl.CHEMBD : {utl.CHEMBD}")
        if not os.path.isfile(utl.CHEMBD):
            print("Dans le main :\ndemande de création de la bdd")
            Gbdd.creabd(self)
            # Trouver le dossier contenant la base de données de Firefox (son nom varie)
            # English : Find the folder containing the Firefox database (its name varies)
            Gbdd.trouvdosdefault(self)
            # récupérer les données de la BDD de Firefox pour remplir ma propre BDD
            # English : retrieve the data from the Firefox database to fill in my own database
            Gbdd.recupbddff(self)
            # Remplir ma BDD avec les données de Firefox
            # English : Fill my database with Firefox data
            Gbdd.envoidonneefirefox(self)
            # Vérification de la validité des liens et su scraping
            self.majbdd()
        else:
            print("Dans le main : \nla base de données existe bien")

    def majbdd(self):
        """Fonction pour vérifier les liens et faire le scraping à la création de la BDD"""
        
        # récupérer le nombre d'enregistrement total de ma table liens_meta pour faire une boucle
        bdgesterr = Gbdd.recupbdd(self)
        for idbdd in bdgesterr:
            # pour chaque enregistrement de ma BDD, je vais vérifier si le lien est valide
            print(f"données de la BDD sur la gestion des erreurs de liens : {idbdd}")
            monurl = idbdd[1]
            mondepre = idbdd[3]
            situation, depreciation = Glw.veriflien(self, monurl, mondepre)
            listgesterr = [idbdd[0], situation, depreciation, idbdd[4]]
            print(f"le nouvel enregistrement, pour la gestion des liens est : {listgesterr}")
            # envoie de listgesterr dans la bdd
            Gbdd.envoigesterreur(self, listgesterr)

            # Maintenant que les liens sont vérifiés, je peux maintenant m'occuper de 'scraper' les liens
            # si la situation du lien est correxte, alors on peut scraper, sinon, on passe son chemin
            if listgesterr[1] == "tout va bien":
                self.lientitre, self.liendescr, self.lienh1, self.lienh2, self.lienh3, self.lienh4, self.lienstrong, \
                self.lienaside, self.lientag = Glsc.scraping(self, monurl)

                listgestscrap = [idbdd[0], self.lientitre, self.liendescr, self.lienh1, self.lienh2, self.lienh3,
                                 self.lienh4, self.lienstrong, self.lienaside, self.lientag]
                print(f"le nouvel enregistrement est, pour la gestion du scraping : {listgestscrap}")
                # envoie de listgestscrap dans la bdd
                Gbdd.envoigestscrap(self, listgestscrap)


Main()

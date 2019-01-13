# -*- coding: utf-8 -*-
#

# todo : gérer les url doublons
# todo : Il semble que la situation "tout va bien" lié au statut code ne prends pas en ccmpte tous les cas ou la connection est correcte.
# todo : Pour les liens non valides : les retester à intervalle régulier.
# todo : pour les liens valides : faire du web scraping pour récolter les données souhaitées.
# todo : Faire une fonction update pour récupérer les mises à jours de la DBB de Firefox.
# todo : Gérer les exceptions sur la BDD.
# todo : Avoir la possibilité de donner soi-même des mots-clés et catégories.
# todo : Pouvoir faire un tri par rapport au mot-clef, catégorie, et ma propre demande de recherche.
# todo : À la création de ma DBB, je créé un fichier places.squite qui est la copie de la BDD de Firefox. En faire un fichier temporaire.

# English : import of modules
import os
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

        # English : check if my database exists if it doesn't, it is created.
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
            self.interface()
        else:
            print("Dans le main : \nla base de données existe bien")
            self.interface()

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
            # si la situation du lien est correcte, alors on peut scraper, sinon, on passe son chemin
            if listgesterr[1] == "tout va bien":
                self.lientitre, self.liendescr, self.lienh1, self.lienh2, self.lienh3, self.lienh4, self.lienstrong, \
                self.lienaside, self.lientag = Glsc.scraping(self, monurl)

                listgestscrap = [idbdd[0], self.lientitre, self.liendescr, self.lienh1, self.lienh2, self.lienh3,
                                 self.lienh4, self.lienstrong, self.lienaside, self.lientag]
                print(f"le nouvel enregistrement est, pour la gestion du scraping : {listgestscrap}")
                # envoie de listgestscrap dans la bdd
                Gbdd.envoigestscrap(self, listgestscrap)

    def interface(self):
        print("1 ------------------------- Ajouter un lien")
        print("2 ------------------------- Supprimer un lien")
        print("3 ------------------------- Vérifier la BDD de Firefox")
        print("4 ------------------------- Tri par rapport aux mot-clefs")
        print("5 ------------------------- Tri par rapport aux catégories")
        print("6 ------------------------- lire toute la BDD")
        print("7 ------------------------- Chercher avec un mot clef")
        print("8 ------------------------- Montrer les catégories")

        repon = "o"
        while repon == "o":
            reponse = input("Que voulez-vous faire ?")
            if reponse == "1":
                self.ajoutlien()
            elif reponse == "2":
                self.supprlien()
            elif reponse == "7":
                self.cherchemotcle()
            repon = input('Voulez vous continuer ? O/N : ')

    def ajoutlien(self):
        monurl = input("Lien à rajouter : ")
        print("Recherche en cours pour savoir si le lien existe déjà dans la BDD")
        marep = self.rechercheurl(monurl)
        if marep == 0:
            print("Le lien n'est pas dans la base de données.")

            print("Recherche prefixe et host.....")
            hachurl = monurl.split("/")
            prefixeurl = hachurl[0] + "//"
            hosturl = hachurl[2]
            print(f"Le prefixe de l'url est {prefixeurl} et son host est {hosturl}")
            donnurl1 = [monurl, prefixeurl, hosturl]
            print("Recherche de la validité du lien......")
            situation, depreciation = Glw.veriflien(self, monurl, mondepre=0)
            print(f"La situation du lien est : {situation} et sa dépréciation vaut : {depreciation}")
            donnurl2 = [situation, depreciation]
            print("Recherche d'informations sur le site.....")
            if situation == "tout va bien":
                self.lientitre, self.liendescr, self.lienh1, self.lienh2, self.lienh3, self.lienh4, self.lienstrong, \
                self.lienaside, self.lientag = Glsc.scraping(self, monurl)
                donnurl3 = [self.lientitre, self.liendescr, self.lienh1, self.lienh2, self.lienh3,
                                 self.lienh4, self.lienstrong, self.lienaside, self.lientag]
                print(f"le nouvel enregistrement est, pour la gestion du scraping : {donnurl3}")
                print("lancement de la fonction pou ajouter un lien .......")
                Gbdd.ajoutbdd(self, donnurl1, donnurl2, donnurl3)
            else:
                print("Désolé, le lien est corrumpu")
        else:
            print("le lien existe déjà !")

    def supprlien(self):
        monurl = input("Lien à supprimer : ")
        print("Recherche en cours pour savoir si le lien existe déjà dans la BDD")
        marep = self.rechercheurl(monurl)
        if marep == 0:
            print("Le lien n'est pas dans la base de données.")
        else:
            Gbdd.supprimbdd(self, monurl)

    def cherchemotcle(self):
        motclef = input("Écrivez le mot que vous rechercher :")
        marecherche = Gbdd.cherchebdd(self, motclef)
        print(marecherche)
Main()

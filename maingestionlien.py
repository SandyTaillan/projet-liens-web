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
# todo : Les fonctions supprlien et cellclick ne sont pas du tout optimiser. Changer cela.
# todo : Lorsque j'ajoute un lien, j'ai bien modifié ma BDD mais je n'ai pas modifié l'affichage dans QTabWidget
# English : import of modules
import os
from PySide2 import QtWidgets
# importation of others files of this programme
import utils as utl
from gestbdd import Gestionbdd as Gbdd
from gestlien import Gestionlienweb as Glw
from gestscrap import Gestionlienscrap as Glsc
from interface.interprin import Interprin
from interface.interdemar import Interdemar


class Maingestionlien(QtWidgets.QTabWidget, Gbdd, Interprin, Interdemar):
    def __init__(self):
        super(Maingestionlien, self).__init__()
        
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

        # lancement de l'interface principale

        self.setupuiprin(self)
        # English : check if my database exists if it doesn't, it is created.
        if not os.path.isfile(utl.CHEMBD):
            self.setupuidemar(self)
            print("Dans maingestionlien :\ndemande de création de la bdd")
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
            #self.interface()
        else:
            self.laprincipal1.setText("La base de donnée existe ....")
        self.affichbdd_hut()
        self.connectioninterface()

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


    def connectioninterface(self):
        """ Pour connecter l'interface (via les boutons) à la gestion de la BDD"""

        self.btn_ajouturl.clicked.connect(self.uiajouturl)
        self.btn_supprurl.clicked.connect(self.supprlien)



    def affichbdd_hut(self):
        """Corrélation entre l'interface graphique et la BDD pour afficher :
            hut  = host - url - titre
            listcolonne = liste -> intitulé colonne de la Base de Donnée à envoyer dans QtableWidget
            """

        # envoyer le nombre de colonne, de ligne, envoyer les intitulés, envoyer la liste de la BDD à afficher
        listcolonne = ["host", "url", "titre"]
        affichlist1, comptenregist = Gbdd.recupbddaffich1(self)

        # Création des colonnes
        self.tablewidget.setColumnCount(len(listcolonne))
        # Détermination des dimensions des colonnes
        self.tablewidget.setColumnWidth(0, 200)
        self.tablewidget.setColumnWidth(1, 700)
        self.tablewidget.setColumnWidth(2, 750)

        # mettre un nom au colonne
        for nbre, nom in enumerate(listcolonne):
            self.tablewidget.setHorizontalHeaderItem(nbre, QtWidgets.QTableWidgetItem())
            # Attention, tout envoie de texte devrait être encodé en UTF8
            self.tablewidget.horizontalHeaderItem(nbre).setText(nom)

        # affichage du contenu de ma BDD
        self.tablewidget.setRowCount(int(comptenregist[0]))
        for numligne, ligneenregist in enumerate(affichlist1):
            # mise en place d'une taille pour les lignes
            self.tablewidget.setRowHeight(numligne, 20)
            for numcolonne, enregistrement in enumerate(ligneenregist):
                self.tablewidget.setItem(numligne, numcolonne,
                                                         QtWidgets.QTableWidgetItem(enregistrement))
        self.laprincipal1.setText("Affichage du contenu de la BDD en cours .....")

    def interface(self):
        print("2 ------------------------- Supprimer un lien")
        print("3 ------------------------- Vérifier la BDD de Firefox")
        print("4 ------------------------- Tri par rapport aux mot-clefs")
        print("5 ------------------------- Tri par rapport aux catégories")
        print("6 ------------------------- lire la BDD")
        print("7 ------------------------- Chercher avec un mot clef")
        print("8 ------------------------- Montrer les catégories")

        repon = "o"
        while repon == "o":
            reponse = input("Que voulez-vous faire ?")
            if reponse == "2":
                self.supprlien()
            elif reponse == "7":
                self.cherchemotcle()
            elif reponse == "6":
                self.liretoutebdd()
            repon = input('Voulez vous continuer ? O/N : ')

    def ajoutlien(self):
        """Cette fonction permet de rajouter un lien à la BDD grâce à l'intrface graphique.
            Une fois que l'url a été saisie et validée, le programme va chercher dans la BDD
            si l'url existe déjà. Si ce n'est pas le cas, l'url est rajouté à la BDD
            et le programme rempli les renseignements manquants."""

        # récupération de l'url ajoutée
        monurl = self.leiau1.text()
        self.fenetreajouturl.close()
        self.laprincipal1.setText("Récupération de l'url que l'on souhaite ajouter à la BDD")

        # Envoi de l'url saisie par l'utilisateur dans la fonction de recherche d'url dans la BDD
        marep = self.rechercheurl(monurl)
        if marep == 0:
            # Si le lien n'est pas dans la base de données, le logiciel va chercher à remplir les cases manquantes pour remplir la BDD
            self.laprincipal1.setText("Tout est ok, le lien n'est pas déjà dans la BDD")
            print("Recherche prefixe et host.....")
            hachurl = monurl.split("/")
            prefixeurl = hachurl[0] + "//"
            hosturl = hachurl[2]
            # print(f"Le prefixe de l'url est {prefixeurl} et son host est {hosturl}")
            donnurl1 = [monurl, prefixeurl, hosturl]
            self.laprincipal1.setText("Recherche de la validité du lien ....")
            situation, depreciation = Glw.veriflien(self, monurl, mondepre=0)
            self.laprincipal1.setText(
                f"La situation du lien est : {situation} et sa dépréciation vaut : {depreciation}")

            donnurl2 = [situation, depreciation]
            print("Recherche d'informations sur le site.....")
            if situation == "tout va bien":
                self.lientitre, self.liendescr, self.lienh1, self.lienh2, self.lienh3, self.lienh4, self.lienstrong, \
                self.lienaside, self.lientag = Glsc.scraping(self, monurl)
                donnurl3 = [self.lientitre, self.liendescr, self.lienh1, self.lienh2, self.lienh3,
                                 self.lienh4, self.lienstrong, self.lienaside, self.lientag]
                self.laprincipal1.setText(f"le nouvel enregistrement est, pour la gestion du scraping : {donnurl3}")
                print("lancement de la fonction pou ajouter un lien .......")
                Gbdd.ajoutbdd(self, donnurl1, donnurl2, donnurl3)
            else:
                self.lienmessagerapide("Le lien est corrumpu et ne sera pas pris en compte")
        else:
            self.lienmessagerapide("Le lien existe déjà")

    def supprlien(self):

        row = self.tablewidget.currentRow()
        col = 1  # colonne de l'url
        item = self.tablewidget.item(row, col)
        # self.tablewidget.cellClicked.connect(self.cellclick)
        monurl = item.text()

        marep = self.rechercheurl(monurl)
        if marep == 0:
            print("Le lien n'est pas dans la base de données.")
        else:
            print("Le lien est dans la BDD")
            Gbdd.supprimbdd(self, monurl)
            self.tablewidget.removeRow(row)

    def cherchemotcle(self):
        motclef = input("Écrivez le mot que vous rechercher :")
        marecherche = Gbdd.cherchebdd(self, motclef)
        print(marecherche)

    def liretoutebdd(self):
        """Affichage de la bdd complète ou partielle."""

        print("1 -------------------- Affichage du host, de l'URL et du titre")
        print("2 -------------------- Affichage  du host, de l'url, de la situation, depreciation, attente supression")
        print("3 -------------------- Affichage du titre et du scraping")
        repon = "o"
        while repon == "o":
            reponse = input("Que voulez-vous afficher ?")
            if reponse == "1":
                affichlist1 = Gbdd.recupbddaffich1(self)
                print("        host        |                   url                                       |      Titre "
                      "             titre                        ")
                for i in affichlist1:
                    print(f"{i[0]}   |   {i[1]}   |   {i[2]}   |   ")
            elif reponse == "2":
                affichlist2 = Gbdd.recupbddaffich2(self)
                print("          host         |          url                                       |      "
                      " situation         | Depreciation | suppression")
                for i in affichlist2:
                    print(f"{i[0]}   |   {i[1]}   |   {i[2]}   | {i[3]}  | {i[4]}")
            elif reponse == "3":
                affichlist3 = Gbdd.recupbddaffich3(self)
                print("        url        |                   titre_scrap                           | description_scrap"
                      "    |        h1                        |               h2                 |              h3"
                      "           |               h4              |            strong               |                "
                      "    mots_clef      |            catégorie               |                  mes_mots_clefs     |")
                for i in affichlist3:
                    print(f"{i[0]} |   {i[1]} |   {i[2]}  |  {i[3]}  |  {i[4]} |   {i[5]} |   {i[6]}  |  {i[7]}  | "
                          f" {i[8]} |   {i[9]} |   {i[10]} ")
            repon = input('Voulez vous continuer ? O/N : ')

    def essai(self):
        print("cela fonctionne")

app = QtWidgets.QApplication([])
fenetre = Maingestionlien()
fenetre.show()
app.exec_()

# -*- coding: utf-8 -*-
#

from PySide2 import QtWidgets
from PySide2 import QtCore



class Interprin:

    def setupuiprin(self, fenetreprincipale):

        print("lecture du fichier pour fenetre principale")

        fenetreprincipale.setGeometry(100, 100, 1600, 800)
        # Donne un nom à la fenêtre
        fenetreprincipale.setWindowTitle("Gestion des liens internet")
        # création des onglets
        self.fenetregestionlien = QtWidgets.QTabWidget()
        self.fenetregestiontemps = QtWidgets.QTabWidget()
        fenetreprincipale.addTab(self.fenetregestionlien, "Gestion des liens")
        fenetreprincipale.addTab(self.fenetregestiontemps, "Gestion emploi du temps")

        # mise en place d'un layout sur un onglet
        self.gridlayout1 = QtWidgets.QGridLayout(self.fenetregestionlien)

        # création d'un widget QtableWidget appelé tablewidget
        self.tablewidget = QtWidgets.QTableWidget(self.fenetregestionlien)

        # Je met le tablewidget dans le gridlayout1
        self.gridlayout1.addWidget(self.tablewidget, 1, 0, 1, 8)

        # création d'un widget groupbox appelé gb_url
        self.gb_url = QtWidgets.QGroupBox("Les url", self.fenetregestionlien)
        # alignement du groupbox gb_url
        self.gb_url.setAlignment(QtCore.Qt.AlignCenter)

        # Je met le groupbox gb_url dans le gridlayout
        self.gridlayout1.addWidget(self.gb_url, 0, 0, 1, 1)

        # mise en place d'un gridlayout sur le groubox des url
        self.gridlayout2 = QtWidgets.QGridLayout(self.gb_url)

        # création d'un Qpushbutton pour ajouter une url : btn_ajouturl
        self.btn_ajouturl = QtWidgets.QPushButton("Ajouter", self.fenetregestionlien)
        # création d'un Qpushbutton pour supprimer une url : btn_supprurl
        self.btn_supprurl = QtWidgets.QPushButton("supprimer", self.fenetregestionlien)

        # ajout du bouton btn_ajouturl au layout verticalayout1
        self.gridlayout2.addWidget(self.btn_ajouturl, 0, 0, 1, 1)
        # ajout du bouton btn_suppr_url au layout verticalayout1
        self.gridlayout2.addWidget(self.btn_supprurl, 0, 1, 1, 1)

        # Création d'un groupbox appelé gb_recherche
        self.gb_recherche = QtWidgets.QGroupBox("Recherche", self.fenetregestionlien)
        # alignement du groupbox gb_recherche
        self.gb_recherche.setAlignment(QtCore.Qt.AlignCenter)
        # Je met le groubox gb_recherche dans le gridlayout
        self.gridlayout1.addWidget(self.gb_recherche, 0, 1, 1, 1)

        # mise en place d'un gridlayout sur le groubox des url
        self.gridlayout3 = QtWidgets.QGridLayout(self.gb_recherche)

        # création d'un bouton btn_motcle pour faire une recherche par mot-cle
        self.btn_motcle = QtWidgets.QPushButton("Mot-clefs", self.fenetregestionlien)
        # Création d'un bouton btn_categories pour faire une recherche par categorie
        self.btn_categories = QtWidgets.QPushButton("Catégories", self.fenetregestionlien)
        # ajout du bouton btn_motcle au groupbox recherche
        self.gridlayout3.addWidget(self.btn_motcle, 0, 0, 1, 1)
        # ajout du bouton btn_categories au groupbox recherche
        self.gridlayout3.addWidget(self.btn_categories, 0, 1, 1, 1)

        self.tablewidget.setGeometry(QtCore.QRect(10, 100, 1600, 800))
        # Faire que le texte des enregistrements déborde des colonnes
        # et ne retourne pas à la ligne dans le même enregistrement
        self.tablewidget.setWordWrap(False)
        # permettre un tri en cliquant sur la colonne
        self.tablewidget.setSortingEnabled(True)
        self.tablewidget.sortByColumn(0)

        # création d'un label pour y mettre mes prints de suivi
        self.laprincipal1 = QtWidgets.QLabel(self.fenetregestionlien)
        self.gridlayout1.addWidget(self.laprincipal1, 3, 0, 1, 3)
        self.laprincipal1.setText("Prêt")




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

        # mise en place d'un layout sur les onglets
        self.gridlayout1 = QtWidgets.QGridLayout(self.fenetregestionlien)

        # création d'un widget QtableWidget appelé tablewidget
        self.tablewidget = QtWidgets.QTableWidget(self.fenetregestionlien)
        # Je met le tablewidget dans le gridlayout1
        self.gridlayout1.addWidget(self.tablewidget, 2, 0, 8, 8)
        # création d'un widget groupbox appelé gb_url
        self.gb_url = QtWidgets.QGroupBox(self.fenetregestionlien)
        # Je met le groupbox gb_url dans le gridlayout
        self.gridlayout1.addWidget(self.gb_url, 0, 0, 2, 4)

        self.tablewidget.setGeometry(QtCore.QRect(10, 100, 1600, 800))
        # Faire que le texte des enregistrements déborde des colonnes
        # et ne retourne pas à la ligne dans le même enregistrement
        self.tablewidget.setWordWrap(False)



        fenetreprincipale.show()


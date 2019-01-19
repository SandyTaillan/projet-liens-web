# -*- coding: utf-8 -*-
#

from PySide2 import QtWidgets
from PySide2 import QtCore


class Interprin:

    def setupuiprin(self, fenetregestionlien):

        print("lecture du fichier pour fenetre principale")

        textdemar1 = "fenêtre pour la gestion des liens"

        fenetregestionlien.setObjectName("Gestion des liens")
        # Donne la position est la taille de la fenêtre
        fenetregestionlien.setGeometry(500, 300, 800, 500)
        # Donne un nom à la fenêtre
        fenetregestionlien.setWindowTitle("Gestion des liens internet")

        self.layout = QtWidgets.QGridLayout(fenetregestionlien)

        self.la_bouger = QtWidgets.QLabel(textdemar1, fenetregestionlien)
        self.btn_dema = QtWidgets.QPushButton("Démarrer")

        self.layout.addWidget(self.la_bouger)
        self.layout.addWidget(self.btn_dema)

        QtCore.QMetaObject.connectSlotsByName(fenetregestionlien)
# -*- coding: utf-8 -*-
#

from PySide2 import QtWidgets


class Interdemar:

    def setupuidemar(self, fenetregestionlien):

        # création d'une fenêtre de dialogue et plus spécifiquement une boite de message
        fenetredemarrage = QtWidgets.QMessageBox(fenetregestionlien)
        fenetredemarrage.setGeometry(800, 500, 800, 500)
        fenetredemarrage.setWindowTitle("Démarrage")

        # Texte de la fenêtre
        fenetredemarrage.setText("La Base de données n'existe pas, il faut la créer.")
        fenetredemarrage.setInformativeText("""Cela peut prendre quelques minutes comme plusieurs heures.\n
                                            Etes-vous prêt(e) ?""")
        # lancement de la fenêtre
        fenetredemarrage.exec_()
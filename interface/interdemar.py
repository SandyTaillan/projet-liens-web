# -*- coding: utf-8 -*-
#

from PySide2 import QtWidgets
# from PySide2 import QtCore


class Interdemar:
    """Petite fenêtre pour la plupart modal servant à communiquer avec l'utilisateur"""

    def setupuidemar(self, fenetregestionlien):
        """Création d'une fenêtre de démarrage pour expliquer que cela va prendre beaucoup de temps pour lancer
            la création de la Base de données."""

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


    def uiajouturl(self):
        """Fenêtre permettant de rajouter une url dans la BDD
            gliau1 = gridlayout1 de cette fonction
            laiau1 = Label 1 de cette fonction
            teiau1 = QlineEdit 1 contenant l'url
        """

        # création de la fenêtre
        self.fenetreajouturl = QtWidgets.QDialog(self.fenetregestionlien)
        self.fenetreajouturl.setGeometry(500, 300, 300, 100)
        self.fenetreajouturl.setWindowTitle("Ajouter un lien")
        self.fenetreajouturl.setModal(True)

        # Mise en place d'un layout pour ma fenêtre
        self.gliau1 = QtWidgets.QGridLayout(self.fenetreajouturl)

        # création d'un widget label
        self.laiau1 = QtWidgets.QLabel(self.fenetreajouturl)
        # Ajout du widget label au layout
        self.gliau1.addWidget(self.laiau1, 0, 0, 1, 3)
        # Mise en place du texte du label 1
        self.laiau1.setText("Veuillez copier-coller l'URL :")

        # création d'un widget QLineEdit
        self.leiau1 = QtWidgets.QLineEdit(self.fenetreajouturl)

        #Ajout du widget QlineEdit au layout
        self.gliau1.addWidget(self.leiau1, 1, 0, 1, 3)

        # # Création d'un nouveau Widget label
        # self.laiau2 = QtWidgets.QLabel(fenetreajouturl)
        #
        # # Ajout du widget Label au layout
        # self.gliau1.addWidget(self.laiau2, 2, 0, 1, 1)
        #
        # # Mise en place du texte du label 2
        # self.laiau2.setText("Vous pouvez donner un mots-clef (un seul)")
        #
        # # Création d'un nouveau widget QlineEdit 2
        # self.leiau2 = QtWidgets.QLineEdit(fenetreajouturl)

        # # Ajout du widget au layout
        # self.gliau1.addWidget(self.leiau2, 3, 0, 1, 1)

        # Ajout d'un QPushButton pour validé l'url
        self.btn_iau1 = QtWidgets.QPushButton("OK", self.fenetreajouturl)
        # Ajout du widget QPushButton au layout
        self.gliau1.addWidget(self.btn_iau1, 3, 1, 1, 1)

        # Action quand OK est validé
        self.btn_iau1.clicked.connect(self.ajoutlien)

        self.fenetreajouturl.show()

    def lienmessagerapide(self, textmessagerapide):
        """Interface graphique qui indique que le lien donné par l'utilisateur est corrompu"""
        # création de la fenêtre
        self.fenetremessrapide = QtWidgets.QMessageBox(self.fenetregestionlien)
        self.fenetremessrapide.setWindowTitle("Information")
        self.fenetremessrapide.setModal(True)
        self.fenetremessrapide.setText(textmessagerapide)

        self.fenetremessrapide.show()

    def lienasupprimer(self, monurl):
        """Fonction permettant de vérifier si le lien est bien le lien à supprimer"""

        self.lienasuppr = QtWidgets.QMessageBox(self.fenetregestionlien)
        self.lienasuppr.setGeometry(500, 300, 300, 100)
        self.lienasuppr.setModal(True)
        self.lienasuppr.setWindowTitle("Vérification")
        self.lienasuppr.setText(f"êtes-vous sûr de vouloir supprimer ce lien : \n {monurl}")
        # Mise en place des boutons
        self.lienasuppr.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        self.lienasuppr.setDefaultButton(QtWidgets.QMessageBox.Yes)
        # lancement de la fenêtre
        accept = self.lienasuppr.exec_()
        if accept == QtWidgets.QMessageBox.Yes:
            return 1
        else:
            return 0

    def uirecherchemotcle(self, fenetregestionlien):
        """Fenêtre qui s'ouvre dès que l'on clique sur le btn_motcle pour la recherche par mot-cle."""

        # création de la fenêtre
        self.fenetregest_motcle = QtWidgets.QInputDialog(fenetregestionlien)
        self.fenetregest_motcle.setGeometry(500, 300, 200, 100)
        self.fenetregest_motcle.setWindowTitle("Recherche par mot-clef")
        self.fenetregest_motcle.setModal(True)

        # # Mise en place d'un layout pour la fenêtre
        # self.glimotcle = QtWidgets.QGridLayout(self.fenetregest_motcle)
        #
        # # Création d'un widget label pour expliquer quoi faire
        # self.laimotcle = QtWidgets.QLabel(self.fenetregest_motcle)
        # #Ajout du label au gridlayout de la fenêtre
        # self.glimotcle.addWidget(self.laimotcle, 0, 0, 1, 2)
        # # création du texte du label
        # self.laimotcle.setText("Veuillez entre le(s) mot(s) pour la recherche : (séparés par une virgule)")
        #
        # # création d'un QlineEdit pour entrer les mots-clefs
        # self.leimotcle = QtWidgets.QLineEdit(self.fenetregest_motcle)
        # # Ajout du widget QlineEdit au layout de la fenêtre
        # self.glimotcle.addWidget(self.leimotcle, 1, 0, 1, 3)
        #
        # # création d'un bouton ok
        # self.btn_imotcle = QtWidgets.QPushButton("OK", self.fenetregest_motcle)
        # # Ajout du bouton ok à la fenêtre
        # self.glimotcle.addWidget(self.btn_imotcle, 2, 1, 1, 1)
        #
        # self.fenetregest_motcle.show()
        #
        # # récupération des données du QLineEdit
        # self.btn_imotcle.clicked.connect(return motclef)

        motclef, ok = self.fenetregest_motcle.getText(fenetregestionlien, "Mot-clef", """Veuillez entre le(s) 
        mot(s) pour la recherche : (séparés par une virgule)""")

        if ok:
            return motclef
        else:
            self.fenetregest_motcle.close()


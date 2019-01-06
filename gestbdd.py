# -*- coding: utf-8 -*-

import sqlite3
import utils as utl
from glob import glob
import os
import shutil

class Gestionbdd:
    def __init__(self):

        # déclaration des variables
        # variable declaration
        self.ffdonn1 = []
        self.ffdonn2 = []
        self.ffdonn3 = []

    def creabd(self):
        """Création de la base de données qui me permettra de gérer + de 4000 liens.
            english : Creation of database that will allow me to manage more than 4000 links."""

        print("Dans gestbdd : \nlancement fonction creabd")
        connection = sqlite3.connect(utl.CHEMBD)
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE liens_meta(id INTEGER PRIMARY KEY, titre TEXT, url TEXT NOT NULL,
         description TEXT, Prefixe TEXT, host TEXT)""")
        cursor.execute("""CREATE TABLE gestion_erreur(id INTEGER PRIMARY KEY, situation TEXT,depreciation INTEGER,
                        attente_suppression INTEGER)""")
        cursor.execute("""CREATE TABLE scraping(id INTEGER PRIMARY KEY, titre_scrap TEXT, description_scrap TEXT,
                        h1 TEXT, h2 TEXT, h3 TEXT, h4 TEXT, strong TEXT, categories TEXT, mots_clefs TEXT,
                         mes_mots_clefs TEXT)""")
        connection.close()
        print("Création de la bdd terminé")

    def trouvdosdefault(self):
        """La base de données de Firefox se trouve dans un dossier qui peut changer de nom.
        Il me faut donc chercher un dossier contenant le mot 'default' qui lui ne change pas.
        English : The Firefox database is located in a folder that can change its name.
        So I have to look for a folder containing the word'default' that does not change it."""

        print("lancement fonction trouvdosdefault")

        # copie de la BDD de firefox
        # English : copy of the firefox database
        fich = glob(utl.CHEMDBFF + "/*")
        for dossier in fich:
            if "default" in dossier:
                dosdefault = os.path.abspath(dossier) + "/places.sqlite"
                shutil.copy(dosdefault, utl.CHCOPYBDD)

    def recupbddff(self):
        """J'ai besoin de récupérer les données de la BDD de firefox. Seulement les données qui m'intéressent.
            English : I need to recover the data from the firefox database. Only the data that interests me."""

        print("lancement fonction recupbdd")

        # connexion à la copie de la  base de données firefox
        # English : connection to the copy of the firefox database
        connection = sqlite3.connect(utl.CHCOPYBDD)
        cursor = connection.cursor()
        # récupération de l'id et de mes titres de liens en ne prenant pas ceux qui commencent par 'place:'
        # retrieving the id and my link titles by not taking those that start with'place:'.
        cursor.execute("""SELECT moz_bookmarks.title, moz_places.url,  moz_places.description, moz_origins.prefix,
         moz_origins.host FROM moz_bookmarks, moz_origins JOIN moz_places ON moz_places.id = moz_bookmarks.fk 
         AND moz_places.origin_id = moz_origins.id WHERE moz_origins.prefix != 'place:'""")
        self.ffdonn1 = cursor.fetchall()

        # Préparation du contenu de la table "gestion_erreur"
        # Preparation of the content of the "gestion_erreur" table
        situation = "pas vérifié"
        depreciation = 0
        suppression = 0
        # Préparation du contenu de la table "scraping"
        # Preparation of the content of the "scraping" table
        titre_scrap = "-"
        description_scrap = "-"
        h1 = ""
        h2 = ""
        h3 = ""
        h4 = ""
        strong = ""
        categories = ""
        mots_clefs = ""

        for i in range(1, (len(self.ffdonn1) + 1)):
            self.ffdonn2.append([i, situation, depreciation, suppression])
            self.ffdonn3.append([i, titre_scrap, description_scrap, h1, h2, h3, h4, strong, categories, mots_clefs])

        cursor.close()
        connection.close()

    def envoidonneefirefox(self):
        """ Après avoir récupérer uniquement les données dont j'ai besoin, je les envoie dans ma propre base de données.
            English: After retrieving only the data I need, I send it to my own database."""

        print("lancement fonction envoidonneefirefox")
        # connection à la bdd interne
        # English: connection to the internal database
        connection = sqlite3.connect(utl.CHEMBD)
        cursor = connection.cursor()

        for donnees1 in self.ffdonn1:
            cursor.execute("INSERT INTO liens_meta(titre, url, description, prefixe, host) VALUES(?,?,?,?,?)", donnees1)
        for donnees2 in self.ffdonn2:
            cursor.execute("""INSERT INTO gestion_erreur(id, situation, depreciation, attente_suppression)
                            VALUES(?,?,?,?)""", donnees2)
        for donnees3 in self.ffdonn3:
            cursor.execute("""INSERT INTO scraping(id, titre_scrap, description_scrap, h1, h2, h3, h4, strong,
             categories, mots_clefs) VALUES(?,?,?,?,?,?,?,?,?,?)""", donnees3)
        connection.commit()
        connection.close()

    def recupbdd(self):
        """Fonction permettant de récup le contenu de la BDD pour traitenent"""

        # connection à la BDD et récupération de la table liens_meta et gestion_erreur
        connection = sqlite3.connect(utl.CHEMBD)
        cursor = connection.cursor()
        cursor.execute("""SELECT liens_meta.id, liens_meta.url, gestion_erreur.situation, gestion_erreur.depreciation, 
                        gestion_erreur.attente_suppression FROM gestion_erreur JOIN liens_meta 
                        ON gestion_erreur.id = liens_meta.id where gestion_erreur.situation != 'tout va bien'""")
        listgesterr = cursor.fetchall()
        return listgesterr

    def envoigesterreur(self, listgesterr):
        """Cette fonction va envoyer la liste d'erreur d'un lien dans la BDD."""

        print("Lancement fonction envoigesterreur.")
        # connection à la bdd interne
        connection = sqlite3.connect(utl.CHEMBD)
        cursor = connection.cursor()
        cursor.execute("""UPDATE gestion_erreur SET situation = ? WHERE ID = ?""", (listgesterr[1], listgesterr[0]))
        cursor.execute("""UPDATE gestion_erreur SET depreciation = ? WHERE ID = ?""", (listgesterr[2], listgesterr[0]))
        cursor.execute("""UPDATE gestion_erreur SET attente_suppression = ? WHERE ID = ?""",
                       (listgesterr[3], listgesterr[0]))

        connection.commit()
        connection.close()

    def envoigestscrap(self, listgestscrap):
        """Cette fonction va envoyer l'enregistrement du scraping d'un lien dans la BDD."""

        print("Lancement fonction envoigestscrap.")
        # connection à la bdd interne
        connection = sqlite3.connect(utl.CHEMBD)
        cursor = connection.cursor()
        cursor.execute("""UPDATE scraping SET titre_scrap = ?, description_scrap = ?, h1 = ?, h2 = ?,h3 = ?, h4 = ?,
                        strong = ?, categories = ?, mots_clefs = ?
                         WHERE ID = ?""", (listgestscrap[1], listgestscrap[2], listgestscrap[3], listgestscrap[4], 
                                           listgestscrap[5], listgestscrap[6], listgestscrap[7], listgestscrap[8],
                                           listgestscrap[9], listgestscrap[0]))

        connection.commit()
        connection.close()

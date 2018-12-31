# -*- coding: utf-8 -*-

import os
from glob import glob
import sqlite3
import shutil
import requests


# chemin du dossier en cours
chbase = os.path.dirname(__file__)
# chemin de la nouvelle copie de la BDD de Firefox
chcopybdd = os.path.dirname(__file__) + "/places.sqlite"
# Chemin de ma propre base de données.
chembd = 'data/bd-liens.sqlite'

data = []
mesliens = {}
liensverif = {}
lienserreur = {}


def creabd():
    """Création de la base de données qui me permettra de gérer + de 4000 liens."""

    print("lancement fonction creabd")
    connection = sqlite3.connect(chembd)
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE liens_meta(id INTEGER PRIMARY KEY, titre TEXT, url TEXT NOT NULL, description TEXT, 
                    Prefixe TEXT, host TEXT)""")
    cursor.execute("""CREATE TABLE gestion_erreur(id INTEGER PRIMARY KEY, situation TEXT,depreciation INTEGER,
                    attente_suppression INTEGER)""")
    cursor.execute("""CREATE TABLE scraping(id INTEGER PRIMARY KEY, titre_scrap TEXT, description_scrap TEXT,
                    h1 TEXT, h2 TEXT, h3 TEXT, h4 TEXT, strong TEXT, categories TEXT, mots_clefs TEXT,
                     mes_mots_clefs TEXT)""")

    connection.close()

    # Trouver le dossier contenant la base de données de Firefox (son nom varie)
    trouvdosdefault()
    # récupérer les données de la BDD de Firefoc pour remplir ma propre BDD
    recupbdd()
    # Remplir ma BDD avec les données de Firefox
    envoidonneefirefox()


def trouvdosdefault():
    """La base de données de Firefox se trouve dans un dossier qui peut changer de nom.
    Il me faut donc chercher un dossier contenant le mot 'default' qui lui ne change pas."""

    print("lancement fonction trouvdosdefault")
    # Déclaration de mes variables
    chemdbff = '/home/sandy/.mozilla/firefox'

    # copie de la BDD de firefox
    fich = glob(chemdbff + "/*")
    for dossier in fich:
        if "default" in dossier:
            dosdefault = os.path.abspath(dossier) + "/places.sqlite"
            shutil.copy(dosdefault, chcopybdd)


def recupbdd():
    """J'ai besoin de récupérer les données de la BDD de firefox. Seulement les données qui m'intéressent."""

    print("lancement fonction recupbdd")
    # déclaration des variables
    global ffdonn1
    global ffdonn2
    global ffdonn3
    ffdonn2 = []
    ffdonn3 = []
    # connection à la copie de la  base de données firefox
    connection = sqlite3.connect(chcopybdd)
    cursor = connection.cursor()

    # récupération de l'id et de mes titres de liens en ne prenant pas ceux qui commencent par 'place:'
    cursor.execute("""SELECT moz_bookmarks.title, moz_places.url,  moz_places.description, moz_origins.prefix,
     moz_origins.host FROM moz_bookmarks, moz_origins JOIN moz_places ON moz_places.id = moz_bookmarks.fk 
     AND moz_places.origin_id = moz_origins.id WHERE moz_origins.prefix != 'place:'""")
    # cursor.execute('SELECT fk, title FROM moz_bookmarks')
    ffdonn1 = cursor.fetchall()

    # Préparation du contenu de la table "gestion_erreur"
    situation = "pas vérifié"
    depreciation = 0
    suppression = 0
    # Préparation du contenu de la table "scraping"
    titre_scrap = "-"
    description_scrap = "-"
    h1 = ""
    h2 = ""
    h3 = ""
    h4 = ""
    strong = ""
    categories = ""
    mots_clefs = ""

    for i in range(1, len(ffdonn1)):
        ffdonn2.append([i, situation, depreciation, suppression])
        ffdonn3.append([i, titre_scrap, description_scrap, h1, h2, h3, h4, strong, categories, mots_clefs])

    cursor.close()
    connection.close()


def envoidonneefirefox():
    """ Après avoir récupérer uniquement les données dont j'ai besoin, je les envoie dans ma propre base de données."""

    print("lancement fonction envoidonneefirefox")
    # connection à la bdd interne
    connection = sqlite3.connect(chembd)
    cursor = connection.cursor()

    for donnees1 in ffdonn1:
        cursor.execute("INSERT INTO liens_meta(titre, url, description, prefixe, host) VALUES(?,?,?,?,?)", donnees1)
    for donnees2 in ffdonn2:
        cursor.execute("""INSERT INTO gestion_erreur(id, situation, depreciation, attente_suppression)
                        VALUES(?,?,?,?)""", donnees2)
    for donnees3 in ffdonn3:
        cursor.execute("""INSERT INTO scraping(id, titre_scrap, description_scrap, h1, h2, h3, h4, strong, categories,
         mots_clefs) VALUES(?,?,?,?,?,?,?,?,?,?)""", donnees3)
    connection.commit()
    connection.close()


def veriflien():
    """Vérification de la validité des liens de la base de données. Le but est de mettre de côté des liens qui
    ne sont plus valides pour un traitement par la suite."""

    print("lancement fonction veriflien")
    # Déclaration des variables de la fonction
    global nouvbdgesterr
    nouvbdgesterr = {}
    situation = ""
    suppression = 0

    connection = sqlite3.connect(chembd)
    cursor = connection.cursor()
    cursor.execute("""SELECT liens_meta.id, liens_meta.url, gestion_erreur.situation, gestion_erreur.depreciation, 
                    gestion_erreur.attente_suppression FROM gestion_erreur JOIN liens_meta 
                    ON gestion_erreur.id = liens_meta.id where gestion_erreur.situation != "tout va bien" """)
    bdgesterr = cursor.fetchall()

    for donn in bdgesterr:
        ajout_depre = 0
        try:
            r = requests.get(donn[1], timeout=7)
            if r.status_code == requests.codes.ok:
                situation = "tout va bien"
        except requests.exceptions.SSLError:
            situation = "erreur: ssl"
            ajout_depre = 10
        except requests.exceptions.ConnectTimeout:
            situation = "erreur: temps connection"
            ajout_depre = 10
        except requests.exceptions.InvalidSchema:
            situation = "erreur: Schema invalid"
            ajout_depre = 10
        except requests.exceptions.ReadTimeout:
            situation = "erreur: temps imparti"
            ajout_depre = 10
        except requests.exceptions.ProxyError:
            situation = "erreur: proxy"
            ajout_depre = 10
        except requests.exceptions.HTTPError:
            situation = "erreur: http"
            ajout_depre = 10
        except requests.exceptions.MissingSchema:
            situation = "erreur: schéma manquant"
            ajout_depre = 10
        except requests.exceptions.InvalidURL:
            situation = "erreur: url invalid"
            ajout_depre = 50
        except requests.exceptions.ConnectionError:
            situation = "erreur: connection"
            ajout_depre = 10
        except:
            situation = "erreur: inconnue"
            ajout_depre = 10

        depreciation = donn[3] + ajout_depre

        nouvbdgesterr[donn[0]] = [situation, depreciation, suppression]
        # Si la depreciation arrive à 100, alors j'envisage la suppression du lien.
        for donn1 in nouvbdgesterr:
            if nouvbdgesterr[donn1][1] == 100:
                nouvbdgesterr[donn1][2] = 1

    cursor.close()
    connection.close()
    # lancement de la fonction pour remplir la table gestion_erreur de ma BDD
    updatabgeserr()


def updatabgeserr():
    """Cette fonction va envoyer la liste de gestion des erreurs dans la BDD."""

    print("Lancement fonction updatabgesrr.")
    # connection à la bdd interne
    connection = sqlite3.connect(chembd)
    cursor = connection.cursor()
    for donn in nouvbdgesterr.items():
        cursor.execute("""UPDATE gestion_erreur SET situation = ? WHERE ID = ?""", (donn[1][0], donn[0]))
        cursor.execute("""UPDATE gestion_erreur SET depreciation = ? WHERE ID = ?""", (donn[1][1], donn[0]))
        cursor.execute("""UPDATE gestion_erreur SET attente_suppression = ? WHERE ID = ?""", (donn[1][2], donn[0]))

    connection.commit()
    connection.close()


def recupbddscraping():

    print("lancement fonction pour aller chercher donnée dans bdd : recupbddscraping")
    connection = sqlite3.connect(chembd)
    cursor = connection.cursor()
    cursor.execute("""SELECT liens_meta.id, liens_meta.url, scraping.titre_scrap FROM scraping 
                    JOIN liens_meta ON scraping.id = liens_meta.id""")
    bdgesscrap = cursor.fetchone()
    print(f"bdgesscrap: {bdgesscrap}")
    connection.close()
    return bdgesscrap


def envoiedonnscraping(donnscrap):
    print("Lancement fonction envoie à la table scraping")

    connection = sqlite3.connect(chembd)
    cursor = connection.cursor()
    print(f"Voici donnscrap dans la mise à jour de la table : {donnscrap}")
    cursor.execute("""UPDATE scraping SET titre_scrap = ?, description_scrap = ?, h1 = ?, h2 = ?,h3 = ?, h4 = ?,
                    strong = ?, categories = ?, mots_clefs = ?
                     WHERE ID = ?""", (donnscrap[1], donnscrap[2], donnscrap[3], donnscrap[4],donnscrap[5],
                                       donnscrap[6], donnscrap[7], donnscrap[8], donnscrap[9], donnscrap[0]))

    connection.commit()
    connection.close()
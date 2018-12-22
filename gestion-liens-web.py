# -*- coding: utf-8 -*-

# todo : faire les tests de validité des liens.
# todo : faire une table pour les liens non valides pour permettre de les retester selon le message d'erreur.
# todo : Pour les liens non valides : les retester à intervalle régulier
# todo : pour les liens valides : faire du web scraping pour récolter les données souhaitées.
# todo : Faire une fonction update pour récupérer les mises à jours de la DBB de Firefox
# todo : Gérer les exceptions sur la BDD
# todo : ne vérifier que 100 lignes de liens à la fois ou tout vérifier d'un coup -> demande dans interface graphique


import os
from glob import glob
import sqlite3
import shutil
from bs4 import BeautifulSoup
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
    ffdonn2 = []

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
    for i in range(1, len(ffdonn1)):
        ffdonn2.append([i, situation, depreciation, suppression])

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
    connection.commit()
    connection.close()


def veriflien():
    """Vérification de la validité des liens de la base de données. Le but est de mettre de côté des liens qui
    ne sont plus valides pour un traitement par la suite."""

    print("lancement fonction veriflien")
    # Déclaration des variables de la fonction
    global nouvbdgesterr
    nouvbdgesterr = []
    situation = ""
    ajout_depre = 0
    suppression = 0

    connection = sqlite3.connect(chembd)
    cursor = connection.cursor()
    cursor.execute("""SELECT liens_meta.id, liens_meta.url, gestion_erreur.situation, gestion_erreur.depreciation, 
                    gestion_erreur.attente_suppression FROM gestion_erreur JOIN liens_meta 
                    ON gestion_erreur.id = liens_meta.id""")
    bdgesterr = cursor.fetchall()

    for donn in bdgesterr:
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
        except:
            situation = "erreur: inconnue"
            ajout_depre = 10

        depreciation = donn[3] + ajout_depre
        nouvbdgesterr.append((donn[0], situation, depreciation, suppression))
        # Si la depreciation arrive à 100, alors j'envisage la suppression du lien.
        for donn1 in nouvbdgesterr:
            if donn1[2] == 100:
                donn1[3] = 1

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

    for donn in nouvbdgesterr:
        cursor.execute("""UPDATE gestion_erreur(id, situation, depreciation, attente_suppression)
                        VALUES(?,?,?,?)""", donn)
    connection.commit()
    connection.close()

# vérifier si ma base de données existe si ce n'est pas le cas, elle est créée.
if not os.path.isfile(chembd):
    creabd()


veriflien()

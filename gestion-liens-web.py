# -*- coding: utf-8 -*-

#todo : récupérer les données que je veux de la base de données Firefox vers des listes ou dictionnaires
#todo : Entrer les valeurs dans la nouvelle base de données.
#todo : faire les tests de validité des liens.
#todo : faire une table pour les liens non valides pour permettre de les retester selon le message d'erreur.
#todo : Pour les liens non valides : les retester à intervalle régulier
#todo : pour les liens valides : faire du web scraping pour récolter les données souhaitées.



import os
from glob import glob
import sqlite3
import shutil
from bs4 import BeautifulSoup
import requests


# chemin du dossier en cours
chbase = os.path.dirname(__file__)
# chemin relatif de mon fichier à traiter
chemfichier = "/bookmarks.html"
chemfichierbis = "mesdata.html"
# le chemin complet
chemin = chbase + "/" + chemfichier
cheminbis = chbase + "/" + chemfichierbis
chembd = 'data/bd-liens.sqlite'
chemDBff = '/home/sandy/.mozilla/firefox'
chcopybdd = os.path.dirname(__file__) + "/places.sqlite"
data = []
mesliens = {}
liensverif = {}
lienserreur = {}




def creabd():
    """Création de la base de données qui me permettra de gérer les + de 4000 liens."""

    connection = sqlite3.connect(chembd)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE Liens(id INTEGER PRIMARY KEY, url TEXT, nomdulien TEXT, hosts TEXT,"
                   " type TEXT)")

    connection.close()


def trouvdosdefault():
    """La base de données de Firefox se trouve dans un dossier qui peut changer de nom.
    Il me faut donc chercher un dossier contenant le mot default qui lui ne change pas."""

    global dosdefault

    fich = glob(chemDBff + "/*")
    for dossier in fich:
        if "default" in dossier:
            dosdefault = os.path.abspath(dossier) + "/places.sqlite"
            shutil.copy(dosdefault, chcopybdd)

def remplirbdd():
    """J'ai besoin de récupérer les données de la BDD de firefox. Seulement les données qui m'intéressent."""

    #coonection à la base de données de firefox
    print(dosdefault)
    # connection = sqlite3.connect("/home/sandy/Bureau/places.sqlite")
    # cursor = connection.cursor()
    # #récupération de l'url de mes liens
    # cursor.execute('SELECT url FROM moz_places')
    # for record in cursor:
    #     print(record)



# def ecriturefichdata():
#     """Ecriture du fichier mesdata à partir de la liste data."""
#
#     with open(chemfichierbis, "w") as f:
#         for cle, valeur in mesliens.items():
#             f.write(cle)
#             f.write(valeur)


def veriflien():

    for lien, texte in mesliens.items():
        try:
            r = requests.get(lien, timeout=7)

            if r.status_code == requests.codes.ok:
                print(f'Pour le site {lien} -----> tout va bien !')
                liensverif[lien] = texte
        except requests.exceptions.ConnectTimeout:
            print(f'Pour le site {lien} le temps de connection est expiré.')
            lienserreur[lien] = texte, "ConnectTimeout"
        except requests.exceptions.InvalidSchema:
            print(f"Pour le site {lien} le schéma url sous forme de chaîne n'est pas respecté.")
            lienserreur[lien] = texte, "InvalidSchema"
        except requests.exceptions.ReadTimeout:
            print(f"Pour le site {lien} le serveur n'envoie pas de data dans le temps imparti.")
            lienserreur[lien] = texte, "ReadTimeout"
        except requests.exceptions.SSLError:
            print(f"Pour le site {lien} Une erreur SSL c'est produite.")
            lienserreur[lien] = texte, "SSLError"
        except requests.exceptions.ProxyError:
            print(f"Pour le site {lien} Une erreur de proxy c'est produite.")
            lienserreur[lien] = texte, "ProxyError"
        except requests.exceptions.HTTPError:
            print(f"Pour le site {lien} Une erreur HTTP c'est produite.")
            lienserreur[lien] = texte, "HTTPError"
        except requests.exceptions.URLRequired:
            print(f"Pour le site {lien} Une URL est requise pour faire une requête.")
            lienserreur[lien] = texte, "URLRequired"
        except requests.exceptions.MissingSchema:
            print(f"Pour le site {lien} Le schéma de l'url est manquante.")
            lienserreur[lien] = texte, "MissingSchema"
        except requests.exceptions.InvalidURL:
            print(f"Pour le site {lien}  l'url n'est pas valide.")
            lienserreur[lien] = texte, "InvalidURL"
        except requests.exceptions.ConnectionError:
            print(f"Pour le site {lien} Il y a une erreur de connection.")
            lienserreur[lien] = texte, "ConnectionError"
        except:
            print(f"Pour le site {lien} Il y a une erreur inconnue !  ------ > tout va mal")
    print("c'est fini")


# def connectbasdonnees():
#     """Fonction permettant de se connecter à la base de données et de récupérer les éléments utiles pour la suite."""
#
#     connect = sqlite3.connect('places.sqlite')
#     cursor = connect.cursor()
#     cursor.execute('SELECT * FROM moz_bookmarks')
#     for record in cursor:
#         print(record)


if not os.path.isfile(chembd):
    creabd()
trouvdosdefault()
remplirbdd()
# veriflien()
# ecriturefichdata()

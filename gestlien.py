# -*- coding: utf-8 -*-
#

import requests
import urllib3


class Gestionlienweb:
    """Cette classe regroupe toute la gestion des liens valides ou non."""
    
    def veriflien(self, monurl, mondepre):
        """Vérification de la validité du lien."""

        # déclaration des variables
        # variable declaration
        situation = ""
        ajout_depre = 0
        listhttp_1 = [201, 202, 203, 204, 205, 206, 207, 208, 210, 226]

        try:
            r = requests.get(monurl, timeout=7)
            if r.status_code == requests.codes.ok:
                situation = "tout va bien"
            elif r.status_code in listhttp_1:
                situation = "tout va bien"
        except requests.exceptions.SSLError:
            situation = "erreur: ssl"
            ajout_depre = 10
        except requests.exceptions.ConnectTimeout:
            situation = "erreur: temps connection"
            ajout_depre = 10
        except requests.exceptions.InvalidSchema:
            situation = "erreur: Schema invalid"
            ajout_depre = 100
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
        except requests.exceptions.TooManyRedirects:
            situation = "erreur: Trop de redirection"
            ajout_depre = 20
        except requests.exceptions.RequestException:
            situation = "erreur: erreur sur requests"
            ajout_depre = 10
        except urllib3.exceptions.DecodeError:
            situation = "erreur: problème de décodage"
            ajout_depre = 20
        # except:
        #     situation = "Erreur: inconnue"

        depreciation = mondepre + ajout_depre
        print(f"la situation du lien est : {situation} avec une depréciation de {depreciation}")
        return situation, depreciation

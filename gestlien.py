# -*- coding: utf-8 -*-
#

import requests

class Gestionlienweb:
    """Cette classe regroupe toute la gestion des liens valides ou non."""
    
    def veriflien(self, monurl, mondepre):
        """Vérification de la validité du lien."""

        # déclaration des variables
        # variable declaration
        situation = ""
        ajout_depre = 0

        try:
            r = requests.get(monurl, timeout=7)
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

        depreciation = mondepre + ajout_depre
        print(f"la situation du lien est : {situation} avec une depréciation de {depreciation}")
        return situation, depreciation
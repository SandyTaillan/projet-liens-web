# -*- coding: utf-8 -*-
#

"""Déclaration des variables constantes de mon programme.
    English :  Declaration of constant variables of my program."""

import os

# Chemin des fichiers Firefox
# English Path to Firefox files.
CHEMDBFF = '/home/sandy/.mozilla/firefox'
# Chemin de ma propre base de données.
# English : Path to my own database.
CHEMBD = 'data/bd-liens.sqlite'
# chemin de la nouvelle copie de la BDD de Firefox
# English: Path to the new copy of the Firefox database
CHCOPYBDD = os.path.dirname(__file__) + "/places.sqlite"

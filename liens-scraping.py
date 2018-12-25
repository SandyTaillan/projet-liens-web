# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re


url = "http://www.audio-maniac.com/?page_id=827"


lienh2 = []
lienh3 = []
lienh4 = []
lienstrong = []
lienaside = []
lientag = []
reponse = requests.get(url)

soup = BeautifulSoup(reponse.text, "html5lib")

# Recherche de titres dans le partie section - content
lientitre = soup.title.string
lienh1 = soup.h1.string
for data in soup.find_all("section", {"id": "content"}):
    for mon_data in data.find_all("h2"):
        lienh2.append(mon_data.get_text())
    for mon_data in data.find_all("h3"):
        lienh3.append(mon_data.get_text())
    for mon_data in data.find_all("h4"):
        lienh4.append(mon_data.get_text())
    for mon_data in data.find_all("strong"):
        lienstrong.append(mon_data.get_text())

# Recherche des catégories
for data in soup.find_all(class_=re.compile("cat")):
    for data1 in data.find_all("a"):
        lienaside.append(data1.get_text())

# Recherche des mots-clefs
for data in soup.find_all(class_=re.compile("tag")):
    for data1 in data.find_all("a"):
        lientag.append(data1.get_text())

print(f"titre: {lientitre}")
print(f"h1: {lienh1}")
print(f"h2: {lienh2}")
print(f"h3: {lienh3}")
print(f"h4: {lienh4}")
print(f"strong: {lienstrong}")
print(f"Les catégories : {lienaside}")
print(f"Les tags : {lientag}")

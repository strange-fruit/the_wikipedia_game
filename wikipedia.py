#!/usr/bin/env python3
import urllib.request as urllib2
from gazpacho import Soup
from bs4 import BeautifulSoup
import requests
import csv
import os
import pandas as pd


#possibilité de changer au wikipedia français ici
template = "https://en.wikipedia.org/wiki/"
short_template = "https://en.wikipedia.org"


FINAL_LINK = "https://en.wikipedia.org/wiki/Philosophy"
RANDOM_LINK = "https://en.wikipedia.org/wiki/Special:Random"

random_link = RANDOM_LINK
rep = requests.get(random_link)
URL = rep.url


#chopper la balise title de la page random et parser le "_-_Wikipedia" à la fin
def title_tag(url_page):
    response = urllib2.urlopen(url_page)
    soup = BeautifulSoup(response.read(),"html.parser", from_encoding=response.info().get_param('charset'))
    title = soup.find('title').text
    #Video Games - Wikipedia 
    

    # enlève le wiki a la fin
    #Video Games - 
    title_parsed =title.replace('Wikipédia', '')
    #remplace les espaces par underscore
    title_parsed_space = title_parsed.replace(" ", "_")

    l = len(title_parsed_space)

    # #enleve l'espace le dash et l'autre espace
    title_parsed_dash = title_parsed_space[:l-12]

    #le retour permet de créer la fin de l'url pour le lien en.wikipedia.org/wiki/ ... 
    return title_parsed_dash
    














#check si la nature du lien est valide 
#  le # mène a une section donc pas valide
#  le // jsp mais sans ça ça marche pas
#  : pour ebauche et toute exception avec les bandeaux notamment
def isValid(ref,paragraph):
  if not ref or "#" in ref or "//" in ref or ":" in ref:
    return False
  #le lien doit commencer par ça sinon false
  if "/wiki/" not in ref:
    return False
  #paragraph = balise p donc là ou on choppe le lien
  if ref not in paragraph:
    return False
  prefix = paragraph.split(ref,1)[0]
  if prefix.count("(")!=prefix.count(")"):
    return False
  return True






#prend en entrée l'url complete
# https://en.wikipedia.org/wiki/Life
def getFirstLink(link):
    page = urllib2.urlopen(link)
    soup = BeautifulSoup(page.read(),"html.parser", from_encoding=page.info().get_param('charset'))

    #prend la div dans lequel se trouvera le paragraphe dans lequel se trouvera le lien
    soup = soup.find('div', id="mw-content-text")
    #gestion erreur
    if not soup:
        return False
    #dans la div je cherche le p qui n'a pas de classe
    for paragraph in soup.find_all('p', class_=""):
      #dans le p je cherche le a href 
        for newLink in paragraph.find_all("a", href=True):            
            ref = newLink.get("href")
            #is valid ...
            if isValid(str(ref),str(paragraph)):
              # print(ref)
              return newLink.get("href")
              #ressort /wiki/titletag


    return False


#fonction la plus importante c'est celle qui réuni toutes celle du dessus et celle qui crawl wiki
#prend un lien en entré, en premier le lien random et dès la deuxieme itération ça sera le premier
#hyperlien de la page random
def iterate(newlink):
  
  titletag = title_tag(newlink)
  print("the new page is " + titletag+ "\n")

  final_url = template + titletag
  newlink= getFirstLink(final_url)
  #ressort /wiki/blabla

  #ressort un nouveau lien
  return short_template + newlink



#fonction inutile
# #prend en arg le tableau d'essai
# def average(average):
#   i = 0
#   for i in range (len(average)):
#       moyenne = 0
#       nb_essai = len(average) #3
#       moyenne = moyenne + average[i]
#       moyenne = moyenne / nb_essai
#   return moyenne



#fonction prenant un tableau en premier arg et un fichier csv cible en deuxieme
#note : le fichier n'as pas besoin d'exister il sera créer sinon ça rajoutera
#steps.csv
def write_csv(steps, csv_file):

  #create csv
  with open(csv_file, 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

  # list of column names
  with open(csv_file, 'a') as file:
    print('writing ' + csv_file + '...')
    writer = csv.writer(file)
    writer.writerow(steps)
    writer.writerow
    print("done")





#arg entrée data est une liste d'element a but statistique
#data est une liste comprenant les informations dans la variable header
#créer d'abord un csv avec les bons header puis ensuite ouvre le csv et écrit la data dedans
#nb try vaut nb click
def create_csv_stat():
  header =  ['NOMBRE CLICK','NOMBRE TRY TOTAUX', 'REUSSI', "LOOP SUR"]

  with open('csv/stats.csv', 'w', encoding='UTF8') as f:
      writer = csv.writer(f)

      # write the header
      writer.writerow(header)


def write_csv_stats(data):
  with open('csv/stats.csv', 'a') as file:
      print('adding stats to stats.csv...')
      writer = csv.writer(file)
      writer.writerow(data)
      writer.writerow
      print("done")
      

#compte le nombre de try totaux et pas le nb de click
def count_row_csv():
  rowcount  = 0
  #iterating through the whole file
  for row in open('csv/stats.csv'):
    rowcount+= 1
  return rowcount/2
  #/2 car un espace entre chaque ligne de steps.csv


#fonction pour créer répertoire ou fichier si ils existent pas
def exist(filename):
  isExist = os.path.exists(filename)
  if isExist:
    return True
  return False


# def reussite_moyenne():
#   my_csv = pd.read_csv('csv/stats.csv')
#   column = my_csv.REUSSI
#   for reussi in column:
#       print(reussi)
#       if(reussi == "OUI"):
#         moyenne = 100
#       else:
#         moyenne = 0
#   return moyenne


#premiere itération par le lien random
bigL = iterate(RANDOM_LINK)
steps = []
result = ""
looping=[]
nb_click = 0
#même variable que result juste elle n'a pas vocation a être affichée dans le terminal mais dans le csv
reussi = ""

found = False
while bigL is not FINAL_LINK and found == False:
   #gestion erreur
  if not bigL:
    result = "No first link found in: "+steps[-1]
    break
  #si le premier lien (bigL) est le lien philosophy alors 
  if bigL == FINAL_LINK:
    result = "\n " + FINAL_LINK+" found after "+str(len(steps))+" clicks!"
    nb_click = str(len(steps))
    found = True
    reussi = "OUI"
    title= ""

    break
  
  #gestion erreur
  current = getFirstLink(bigL)
  if not current:
    result = "\n No first link in page"
    break

  #verif si ça boucle pas
  if bigL not in steps:
     #ajout de la page par laquelle je suis passé
    steps.append(bigL)
    title= title_tag(bigL)
  else:
    result = "\n We loop on "+title+ " stopping..."
    reussi = "NON"
    looping.append(title)
    break
  
  print('\n')
  #nouvelle itération
  bigL = iterate(bigL)





##################################################


#post traitement
##################################################

if exist('csv') == False:
  os.mkdir('csv')
if exist('csv/stats.csv') == False:
  create_csv_stat()
if exist('csv/steps.csv') == False:
  write_csv(steps, 'csv/steps.csv')
   


print("steps : ") 
print(steps)
print(result)



#prend en arg une liste, un fichier csv cible sans l'extension de fichier .csv sinon bug

#créer dabord avec les header dans la fonction

stats = [nb_click,count_row_csv(),reussi, title]
write_csv_stats(stats)


#PROGRAMME RESSOURCE

import urllib.request
import re

#Fonction qui permet d'obtenir un lien Youtube a partir d'une séléction de mots-clés

def Search(search):
    
    url = search
    url = url.replace(" ", "+")
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + url)
    video_ids  =re.findall(r"watch\?v=(\S{11})", html.read().decode())

    #Ici, on récupère seulement la vidéo qui ressort en premier de la recherche Youtube
    return("https://www.youtube.com/watch?v=" + video_ids[0])



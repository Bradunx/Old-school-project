#PROGRAMME RESSOURCE

from pytube import YouTube

#Librairie qui permet d'installer des vidéos Youtube à partir de leurs liens selon plusieurs paramètres

#Cette fonction permet d'installer une vidéo Youtube dans un dossier spécifique "cache" avec nom spécifique 'current_music.mp4"

def YoutubeDl(url):

    yt = YouTube(url)
    titre = yt.title
    yt.streams.first().download("cache",filename="wesh.mp4")
    print("---------------------------Video downloaded !---------------------------")
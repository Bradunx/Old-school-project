#PROGRAMME PRINCIPAL

#Importations des librairies nécessaire

import tkinter as tk    #Interface graphique
import sys
from PIL import Image, ImageTk #Affichage d'image
import RPi.GPIO as GPIO
from pn532 import *
import pn532.pn532 as nfc
import read #Programme de lecture de cartes rfid
import vlc  #Lecteur VLC et des fonctionnalitées (pause,play,stop,volume,...)
import time

# Fonction pour stopper le programme
def stop():
    movie_player.destroy()
    player.stop()

# Fonction pour inverser l'état de la vidéo en lecture/pause 
def toggle_pause():
    player.pause()

# Fonction pour changer le volume de la vidéo de 0 à 100 % selon la valeur de l'objet 'slider' de l'interface  
def set_volume(volume):
    player.audio_set_volume(slider.get())

# Fonction pour avancer la vidéo de 5 secondes

def plus5():
    duree = player.get_length()
    temps = player.get_time()+5000
    print(temps," --------- ",duree)
    if((temps)>duree):
        player.set_time(duree)
    else:
        player.set_time(temps)
 

# Fonction pour revenir en arrière de 5 secondes
        
def moins5():
    duree = player.get_length()
    temps = player.get_time()-5000
    if(temps<0):
        player.set_time(0)
    else:
        player.set_time(temps)

# Fonction pour remettre la vidéo à zéro
           
def restart():
    player.set_time(0)

# fonction séparer en 2 (seulement pour pouvoir afficher et désafficher l'image d'attente ) pour scanner une carte rfid
def scan_pt1(event):
    canvas2.itemconfig(1, state='normal')
    canvas2.grid()


def scan_pt2(event):
    canvas2.itemconfig(1, state='hidden')
    canvas2.grid_remove()
    
    player.stop()
    read.reader()
    player.play()
    time.sleep(0.1)
    duree = player.get_length()
    print(duree)
        
      
#Instanciation de la fenêtre tkinter

movie_player = tk.Tk()
movie_player.geometry("800x480")
movie_player.grid_rowconfigure(0, weight=1)
movie_player.grid_rowconfigure(1, weight=0)
movie_player.grid_rowconfigure(2, weight=0)
movie_player.grid_columnconfigure(0, weight=1)
movie_player.grid_columnconfigure(1, weight=1)
movie_player.grid_columnconfigure(2, weight=1)
movie_player.grid_columnconfigure(3, weight=1)
movie_player.grid_columnconfigure(4, weight=0)        


#Chargement des différentes images pour l'interface graphique avec une taille standard
taille = 30
image_play = tk.PhotoImage(file="img/play_pause.png").subsample(taille,taille)
image_stop = tk.PhotoImage(file="img/stop.png").subsample(taille,taille)
image_scan_rfid = tk.PhotoImage(file="img/scan_rfid.png").subsample(taille,taille)
image_restart = tk.PhotoImage(file="img/restart.png").subsample(taille,taille)
image_plus5s = tk.PhotoImage(file="img/+5s.png").subsample(taille,taille)
image_moins5s = tk.PhotoImage(file="img/-5s.png").subsample(taille,taille)
image_attente = Image.open("img/attente_detaille.png")
photo = ImageTk.PhotoImage(image_attente)


# Créer l'instance VLC et le lecteur média
Instance = vlc.Instance()
player = Instance.media_player_new()
player.video_set_mouse_input(True)

# Charger la vidéo
video = "cache/current_music.mp4"
media = Instance.media_new(video)
player.set_media(media)

# BOUTONS LECTURE DE CARTE
scan_rfid = tk.Button(movie_player, image=image_scan_rfid,bg='white')
scan_rfid.grid(row=1, column=0, sticky='nswe')

# BOUTON PLAY/PAUSE
playButton = tk.Button(movie_player, image=image_play,bg='white', command=toggle_pause)
playButton.grid(row=1, column=1, sticky='nswe')

# BOUTON MUTE
muteButton = tk.Button(movie_player, image=image_stop,bg='white', command=stop)
muteButton.grid(row=1, column=2, sticky='nswe')

# LABEL 
label = tk.Label(movie_player,bg='white', text="JUKEBOX RFID PLAYER")
label.grid(row=1, column=3, sticky='nswe')

# BOUTON MOINS
moins5Button = tk.Button(movie_player, image=image_moins5s,bg='white', command=moins5)
moins5Button.grid(row=2, column=0, sticky='nswe')

# BOUTON PLUS
plus5Button = tk.Button(movie_player, image=image_plus5s, bg='white', command=plus5)
plus5Button.grid(row=2, column=1, sticky='nswe')

# BOUTON RESTART
restartButton = tk.Button(movie_player, image=image_restart,bg='white', command=restart)
restartButton.grid(row=2, column=2, sticky='nswe')

# CANVAS VIDEO
canvas = tk.Canvas(movie_player)
canvas.grid(row=0, column=0,columnspan=4, sticky='nswe')

# Associer le lecteur à la fenêtre Tkinter
h = canvas.winfo_id()
if sys.platform.startswith('win'):
    player.set_hwnd(h)
elif sys.platform.startswith('linux'):
    player.set_xwindow(h)

# CANVAS IMAGE
canvas2 = tk.Canvas(movie_player, width=800, height=480)
canvas2.grid(row=0, column=0,columnspan=4, sticky='nswe')
canvas2.create_image(0,0, anchor=tk.NW, image=photo)

# SLIDER VOLUME
slider = tk.Scale(movie_player, from_=0, to=100, orient="horizontal",bg='white', command=set_volume)
slider.set(50)
slider.grid(row=2, column=3, sticky='nswe')


    
# Boucle de fonctionnement
if __name__ == '__main__':

    #détection de différents évenements pour lance r certaines fonction, ici, pour lancer une fonction en 2 parties
    scan_rfid.bind('<Button-1>', scan_pt1)
    scan_rfid.bind('<ButtonRelease-1>', scan_pt2)

    #Fenêtre graphique en plein écran
    movie_player.attributes('-fullscreen',True)

    #Lancement de la fenêtre graphique
    movie_player.mainloop()






    

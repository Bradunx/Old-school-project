#PROGRAMME DE LECTURE DE CARTES

#Écriture des donnés de la seconde matrices dans la carte RFID, le tout dans certaines lignes précises pour ne pas modifier le comportement de la carte 

import RPi.GPIO as GPIO
from pn532 import *
import pn532.pn532 as nfc
from youtube_dl import YoutubeDl
import time


# SPI connection: initialisation SPI
pn532 = PN532_SPI(debug=False, reset=20, cs=4)
ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()


#Lecture de la carte RFID

def reader():

    

    # Initialisation des variables, liste de caractères permettant de récupérer les 6 lignes de données de la carte RFID scanné au préalable
    tab_url = ["","","","","",""]


    print('Waiting for RFID/NFC card...')
    
    # Boucle de détection de carte RFID

    card_present = False
    
    while card_present == False:
        uid = pn532.read_passive_target(timeout=0.5)
        print('.', end="")
        if uid is None:
            continue
        card_present = True


    #Récupération de l'UID de la carte, Inutile dans le code final

    uid_carte = [hex(i)[2:] for i in uid]

    for i in range(len(uid_carte)):
        if len(uid_carte[i]) < 2:
            uid_carte[i] = '0' + uid_carte[i]
    uid_carte = ".".join(uid_carte)
    print(uid_carte)
        
    key_a = b'\xFF\xFF\xFF\xFF\xFF\xFF'


    #récupération des 6 lignes de données écrites dans la liste instancié

    j=0
    for i in range(2,14,2):
        try:
            pn532.mifare_classic_authenticate_block(
                uid, block_number=i, key_number=nfc.MIFARE_CMD_AUTH_A, key=key_a)
            print(i, ':', ' '.join(['%02X' % x
                for x in pn532.mifare_classic_read_block(i)]))
            
            tab_url[j] = ['%02X' % x for x in pn532.mifare_classic_read_block(i)]
            j+=1
        except nfc.PN532Error as e:
            print(e.errmsg)
            break
        
    print(tab_url)
        

    #Conversion des 6 lignes de donnés en bytes en une chaine de caractère correpond à l'URL Youtube

    url = ""
    for list in tab_url:
        for element in list:
            url+= bytearray.fromhex(element).decode()
    print(url)

    # Appel de la fonction permettant de télécharger la vidéo de ce lien Youtube
    YoutubeDl(url)
    
    time.sleep(2)


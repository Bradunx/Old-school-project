#PROGRAMME D'ÉCRITURE DE CARTES

#Importations des librairies

import RPi.GPIO as GPIO
import pn532.pn532 as nfc
from pn532 import *
import numpy as np
from search import Search   #Programme pour obtenir un URL Youtube à partir de mots

#Configuration de la liaison SPI

pn532 = PN532_SPI(debug=False, reset=20, cs=4)
#pn532 = PN532_I2C(debug=False, reset=20, req=16)
#pn532 = PN532_UART(debug=False, reset=20)

ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

#Sélection de mots-clés par l'utilisateur
words = str(input("Entrez vos mots clés :"))

print('Waiting for RFID/NFC card to write to!')

# Boucle de fonctionnement
while True:

    #Code de détection d'une carte RFID

    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)
    print('.', end="")
    # Try again if no card is available.
    if uid is not None:
        break
print('Found card with UID:', [hex(i) for i in uid])

# Conversion des mots-clés en URL Youtube

yt = Search(words)


#Création d'un matrice avec 6 listes représentant une ligne de données pour stocker l'URL Youtube

elements_deja_remplis = 0
elements_max = 96
max = 16
donnees = 0
l1 =["","","","","","","","","","","","","","","",""]
l2 =["","","","","","","","","","","","","","","",""]
l3 =["","","","","","","","","","","","","","","",""]
l4 =["","","","","","","","","","","","","","","",""]
l5 =["","","","","","","","","","","","","","","",""]
l6 =["","","","","","","","","","","","","","","",""]

blocks = [l1,l2,l3,l4,l5,l6]
index  = 0


#Remplissage de la matrice avec l'URL Youtube, chaque caractères de l'URL est stocké dans un indice d'une ligne

for character in yt:
    conversion = "0x" + character.encode("utf-8").hex()
    print(conversion," pour ",character)

    blocks[index][donnees] = conversion
    donnees += 1
    elements_deja_remplis += 1
    if donnees == max:
        index +=1
        donnees = 0

#Lorsque le l'URL Youtube est entièrement stocké, le reste de la matrice sera stocké avec un caractère "0"

for i in range(elements_deja_remplis,elements_max):
        blocks[index][donnees] = "0x00"
        donnees += 1
        if donnees == max:
            index +=1
            donnees = 0


#Création d'une second matrices contenant la conversion en bytes des élémentes de la matrice précédentes
            
print(blocks)
#l1 = ["0x00","0x00","0x00","0x00","0x00"]
block1 = bytes([int(x, 16) for x in l1])
block2 = bytes([int(x, 16) for x in l2])
block3 = bytes([int(x, 16) for x in l3])
block4 = bytes([int(x, 16) for x in l4])
block5 = bytes([int(x, 16) for x in l5])
block6 = bytes([int(x, 16) for x in l6])
tab = [block1,block2,block3,block4,block5,block6]

data = bytes([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F])


#Écriture des donnés de la seconde matrices dans la carte RFID, le tout dans certaines lignes précises pour ne pas modifier le comportement de la carte 

# Write block #4-6
j = 0
for i in range(2,14,2):

    block_number = i

    #Mot de passe par défaut pour utiliser seulement le fonctionnement écriture/lecture
    key_a = b'\xFF\xFF\xFF\xFF\xFF\xFF'
    #data = bytes([0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,])
    #data = bytes([0x68, 0x74, 0x74, 0x70, 0x73, 0x3a, 0x2f, 0x2f, 0x77, 0x77, 0x77, 0x2e, 0x79, 0x6f, 0x75, 0x74,])
    data = tab[j]
    j+=1
    

    try:
        pn532.mifare_classic_authenticate_block(
            uid, block_number=block_number, key_number=nfc.MIFARE_CMD_AUTH_A, key=key_a)
        pn532.mifare_classic_write_block(block_number, data)
        if pn532.mifare_classic_read_block(block_number) == data:
            print('write block %d successfully' % block_number)
    except nfc.PN532Error as e:
        print(e.errmsg)
  
GPIO.cleanup()



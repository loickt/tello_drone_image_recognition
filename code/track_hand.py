# LAncerd'abord "command.py"
#Ce script ci crée les ordres qui seront transmis au drone en fonction de l'image reçue. 
# penser à adapter les adresses

#ici l'ordre passe par un fichier txt. Ce n'est vraiment pas optimisé, mais pas gênant,
#       vue la latence déjà présente. On pourrait utiliser des variables d'environnement, ou un pipe. 

from cvzone.HandTrackingModule import HandDetector
import cv2
import os
from pathlib import Path

path = Path('command.txt')

cap = cv2.VideoCapture('udp://@0.0.0.0:11111')
vitesse = 20
detector = HandDetector(detectionCon=0.8, maxHands=2)

while True:
    _,img = cap.read()
    height, width,_ = img.shape
    hands, img = detector.findHands(img)  # détecte la main et dessine les points

    if hands:
        hand1 = hands[0]
        ImList1 = hand1["ImList"]  # liste des 21 points détectés
        bbox1 = hand1["bbox"]  # "bounding box" rectangle entourant la main (x, y, largeur, hauteur)
        centerPoint1 = hand1['center']  # milieu de la main (x, y)
        handType1 = hand1["type"]  # main gauche ou droite

        fingers1 = detector.fingersUp(hand1)  # compte les doigts levés
        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            bbox2 = hand2["bbox"]
            centerPoint2 = hand2['center']
            handType2 = hand2["type"]
            fingers2 = detector.fingersUp(hand2)
        if handType1 == 'Left':
            ordreMains = 0
        else:
            ordreMains = 1  # nous sert pour les ordres donnés au drone

        if fingers1 == [ordreMains for i in range(5)] and fingers2 == [1 - ordreMains for x in range(5)]:  # main gauche
                                                                                        # fermée, main droite ouverte
            file1 = open("command.temp.txt", "w")
            file1.write('flip l')
            file1.close()
            os.rename("command.temp.txt", "command.txt")
            print(1)
        elif fingers2 == [ordreMains for i in range(5)] and fingers1 == [1 - ordreMains for x in range(5)]:  # main gauche
                                                                                            # ouverte, main droite fermée
            file1 = open("command.temp.txt", "w")
            file1.write('flip r')
            file1.close()
            os.rename("command.temp.txt", "command.txt")
            print(2)

        elif len(hands) == 1:  # une seule main dans l'image
            if fingers1 == [1 for i in range(5)]:  # main ouverte
                file1 = open("command.temp.txt", "w")
                file1.write('cw 360')  # un tour sur lui-même
                file1.close()
                os.rename("command.temp.txt", "command.txt")
                print(3)
            elif fingers1 == [0, 1, 1, 0, 0]:  # signe du v
                file1 = open("command.temp.txt", "w")
                file1.write('flip l')  # flip gauche
                file1.close()
                os.rename("command.temp.txt", "command.txt")
                print(5)
            elif fingers1 == [1, 0, 0, 0, 0]:  # pouce en l'air
                file1 = open("command.temp.txt", "w")
                file1.write('land')  # atterrit
                file1.close()
                os.rename("command.temp.txt", "command.txt")
                print(5)
            elif fingers1 == [0, 1, 0, 0, 0]:  # index en l'air
                file1 = open("command.temp.txt", "w")
                file1.write('up 20')  # monte
                file1.close()
                os.rename("command.temp.txt", "command.txt")
                print(5)

    img = cv2.flip(img, 1)
    cv2.imshow("Stream", img)
    cv2.waitKey(1)

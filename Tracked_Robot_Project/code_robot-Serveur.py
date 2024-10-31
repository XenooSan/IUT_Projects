"""
Elouan Pierrot
Elowan Gouez
2B2
"""
import RPi.GPIO as GPIO
import time
import socket
import sys
from typing import *
#led à 1 : marche ou avant
#led à 0 : arrêt ou arrière
#led 18 : marche/arrêt à droite
#led 22 : marche/arrêt à gauche
#led 23 : avant/arrière à gauche
#led 27 : avant/arrière à droite

class Serveur_UDP:
    def __init__(self, port_ecoute_echange: int):
        # créer le socket UDP/IP
        self.__socket_ecoute_echange = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.__addr_client: Tuple
        self.__liste_addr_clients: List[Tuple] = []
        # lier le socket au port d'écoute
        self.__socket_ecoute_echange.bind(("", port_ecoute_echange))
        print(f"information socket locale : {self.__socket_ecoute_echange}")
        print(f"serveur en ecoute sur le port {port_ecoute_echange}")
        self.__connecte:bool=True

    def recevoir(self)-> str:
        # attente du message du client
        data_bytes, addr_client = self.__socket_ecoute_echange.recvfrom(1024)
        if addr_client not in self.__liste_addr_clients:
            self.__liste_addr_clients.append(addr_client)
        print(self.__liste_addr_clients)
        msg = data_bytes.decode("utf-8")
        return msg

    def envoyer(self, msg: str, addr_client)-> None:
        data_bytes = msg.encode("utf-8")
        # envoi du message :
        self.__socket_ecoute_echange.sendto(data_bytes, addr_client)

    def envoyer_a_tous(self, msg: str)-> None:
        for addr_client in self.__liste_addr_clients:
            self.envoyer(msg, addr_client)
            
    def echange(self):
        msg:str=""
        while self.__connecte:
            msg=self.recevoir()
            liste=msg.rsplit(",")
            for i in range(len(liste)):
                liste[i]=int(liste[i]) #reformattage des données reçues
            print(liste)
            self.__alpha=liste[2]
            if -50<=liste[0]<=50 and liste[1]>=80: #interprétation des données reçues pour avancer
                avancer(self.__alpha)
                print(f"avancer {self.__alpha}")
            elif -50<=liste[0]<=50 and liste[1]<=-80: #interprétation des données reçues pour reculer
                reculer(self.__alpha)
                print(f"reculer {self.__alpha}")
            elif -50<=liste[1]<=50 and liste[0]<=-80: #interprétation des données reçues pour tourner à gauche
                tournegauche(self.__alpha)
                print(f"tournegauche {self.__alpha}")
            elif -50<=liste[1]<=0.50 and liste[0]>=80: #interprétation des données reçues pour tourner à droite
                tournedroite(self.__alpha)
                print(f"tournedroite {self.__alpha}")
            else: #Si le joystick n'est pas déplacé alors les roues du robot s'arrêtent
                arret()
            if liste[3]==1: #interprétation des données reçues pour arrêter la connexion
                print("arret")
                self.close()
                self.__connecte=False
        self.close()

    def close(self)-> None:
        self.__socket_ecoute_echange.close()

    def changealpha(self,a): #changement de la vitesse des roues
        self.__alpha=a

def led1(n): #allumage d'une led donnée
    GPIO.output(n,GPIO.HIGH)
    print(f"led {n} allumée")

def leda(n,a): #changement de la "vitesse" d'une led donnée
    pwm[str(n)].ChangeDutyCycle(a)
    print(f"lef {n} allumée, rapport à {a}%")

def led0(n): #extinction d'une led donnée
    GPIO.output(n,GPIO.LOW)
    print(f"led{n} éteinte")

def avancer(a): #coordination des leds pour faire avancer le robot
    led1(27)
    led1(23)
    leda(18,a)
    leda(22,a)

def reculer(a): #coordination des leds pour faire reculer le robot
    led0(27)
    led0(23)
    leda(18,a)
    leda(22,a)

def tournegauche(a): #coordination des leds pour faire tourner le robot à gauche
    led0(27)
    led1(23)
    leda(18,a)
    leda(22,a)

def tournedroite(a): #coordination des leds pour faire tourner le robot à droite
    led1(27)
    led0(23)
    leda(18,a)
    leda(22,a)

def arret(): #arrêt du mouvement
    leda(18,0)
    leda(22,0)

while True: #lancement du serveur, une boucle infinie permet de relancer le serveur sans intervention externe lorsque la connexion est coupée
    try:

        GPIO.setmode(GPIO.BCM) #préparation des leds

        for i in [18,22,23,27]:
            GPIO.setup(i,GPIO.OUT)
        pwm={"18":GPIO.PWM(18,50),"22":GPIO.PWM(22,50)}
        pwm["18"].start(0)
        pwm["22"].start(0) #démarrage des leds de vitesse à vitesse nulle
        port_ecoute_echange: int = None
        serveur_udp: Serveur_UDP
        # initialisation
        port_ecoute_echange = 5000
        # instanciation
        serveur_udp = Serveur_UDP(port_ecoute_echange=port_ecoute_echange) #démarrage du serveur
        # traitement
        serveur_udp.echange()
        serveur_udp.close() #fermetture du serveur

        GPIO.cleanup() #nettoyage du robot pour préparer la prochaine utilisation
    except:
        pass
    time.sleep(0.1)
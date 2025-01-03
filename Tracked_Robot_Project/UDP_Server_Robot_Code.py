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
        #create the UDP/IP socket
        self.__socket_ecoute_echange = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.__addr_client: Tuple
        self.__liste_addr_clients: List[Tuple] = []
        #bind the socket to the listening port
        self.__socket_ecoute_echange.bind(("", port_ecoute_echange))
        print(f"information socket locale : {self.__socket_ecoute_echange}")
        print(f"serveur en ecoute sur le port {port_ecoute_echange}")
        self.__connecte:bool=True

    def recevoir(self)-> str:
        #waiting for the client's message
        data_bytes, addr_client = self.__socket_ecoute_echange.recvfrom(1024)
        if addr_client not in self.__liste_addr_clients:
            self.__liste_addr_clients.append(addr_client)
        print(self.__liste_addr_clients)
        msg = data_bytes.decode("utf-8")
        return msg

    def envoyer(self, msg: str, addr_client)-> None:
        data_bytes = msg.encode("utf-8")
        #message sent
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
                liste[i]=int(liste[i]) #reformatting of received data
            print(liste)
            self.__alpha=liste[2]
            if -50<=liste[0]<=50 and liste[1]>=80: #interpreting the data received to move forward
                avancer(self.__alpha)
                print(f"avancer {self.__alpha}")
            elif -50<=liste[0]<=50 and liste[1]<=-80: #interpreting the data received to take a step backwards
                reculer(self.__alpha)
                print(f"reculer {self.__alpha}")
            elif -50<=liste[1]<=50 and liste[0]<=-80: #nterpretation of data received to turn left
                tournegauche(self.__alpha)
                print(f"tournegauche {self.__alpha}")
            elif -50<=liste[1]<=0.50 and liste[0]>=80: #interpretation of data received to turn right
                tournedroite(self.__alpha)
                print(f"tournedroite {self.__alpha}")
            else: #If the joystick is not moved, the robot's wheels stop.
                arret()
            if liste[3]==1: #interpretation of data received to stop the connection
                print("arret")
                self.close()
                self.__connecte=False
        self.close()

    def close(self)-> None:
        self.__socket_ecoute_echange.close()

    def changealpha(self,a): #changing wheel speed
        self.__alpha=a

def led1(n): #lighting up a given LED
    GPIO.output(n,GPIO.HIGH)
    print(f"led {n} allumée")

def leda(n,a): #changing the ‘speed’ of a given LED
    pwm[str(n)].ChangeDutyCycle(a)
    print(f"lef {n} allumée, rapport à {a}%")

def led0(n): #switching off a given LED
    GPIO.output(n,GPIO.LOW)
    print(f"led{n} éteinte")

def avancer(a): #coordination of LEDs to move the robot forward
    led1(27)
    led1(23)
    leda(18,a)
    leda(22,a)

def reculer(a): #coordination of LEDs to move the robot backwards
    led0(27)
    led0(23)
    leda(18,a)
    leda(22,a)

def tournegauche(a): #coordination of LEDs to turn the robot to the left
    led0(27)
    led1(23)
    leda(18,a)
    leda(22,a)

def tournedroite(a): #coordination of LEDs to turn the robot to the right
    led1(27)
    led0(23)
    leda(18,a)
    leda(22,a)

def arret(): #motion stop
    leda(18,0)
    leda(22,0)

while True: #server launch, an infinite loop is used to restart the server without any external intervention when the connection is cut
    try:

        GPIO.setmode(GPIO.BCM) #preparing the leds

        for i in [18,22,23,27]:
            GPIO.setup(i,GPIO.OUT)
        pwm={"18":GPIO.PWM(18,50),"22":GPIO.PWM(22,50)}
        pwm["18"].start(0)
        pwm["22"].start(0) #start-up of speed LEDs at zero speed
        port_ecoute_echange: int = None
        serveur_udp: Serveur_UDP
        #initialization
        port_ecoute_echange = 5000
        #instantiation
        serveur_udp = Serveur_UDP(port_ecoute_echange=port_ecoute_echange) #server startup
        #processing
        serveur_udp.echange()
        serveur_udp.close() #server shutdown

        GPIO.cleanup() #cleaning the robot to prepare for the next use
    except:
        pass
    time.sleep(0.1)

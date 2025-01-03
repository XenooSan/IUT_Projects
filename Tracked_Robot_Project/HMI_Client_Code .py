"""
Elouan Pierrot
Elowan Gouez
2B2
"""

from tkinter import *
from keyboard import *
import socket, os
import sys
import time
from Controller_Code import *
from threading import Thread

def controle(ip,port): #function for reading the joystick and exchanging information with the robot
    try:
        client.arret() #attempt to stop open connections
    except:
        pass
    client= Client_Chat_UDP(ip, port) #opening the connection with the robot
    print(f"connexion udp à {ip} {port}")
    allume=True
    temps = 0.01
    joy = XboxController()
    while allume :
        touches = joy.read()
        if touches[3]!=1:
            envoi=""
            for i in touches:
                envoi+=f"{int(i*100)}," #formatting data from the joystick to send to the robot
        else:
            envoi="0,0,0,1,"
            allume=False #if the stop button is used, the connection is stopped
        envoi=envoi[:-1]
        print(envoi)
        client.envoyer(envoi)
        time.sleep(temps)
    client.arret()

class Ihm(Tk):
    def __init__(self,ip,port):
        Tk.__init__(self)
        self.__entreeip:Entry=Entry(self)
        self.__entreeip.insert(INSERT,str(ip))
        self.__entreeport:Entry=Entry(self)
        self.__entreeport.insert(INSERT,str(port))
        self.__connect:Button=Button(self,text="connexion",command=self.connect)
        self.__btn_quitter: Button=Button(self,text="quitter",bg="red",command=self.destroy)
        self.__entreeip.pack()
        self.__entreeport.pack()
        self.__connect.pack()
        self.__btn_quitter.pack()
    def connect(self):
        Thread(target=controle,args=(self.__entreeip.get(),int(self.__entreeport.get()))).start() #reading the ip and port entered in the hmi for connection to the robot

class Client_Chat_UDP:
    def __init__(self, ip_serveur: str, port_serveur: int) -> None:
        self.__ip_serveur: str = ip_serveur
        self.__port_serveur = port_serveur
        #creating a UDP socket
        self.__socket_echange: socket
        self.__socket_echange = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__fin: bool = False
        #thread
        self.__thread_recevoir: Thread = Thread(target= self.recevoir, args= ())
        self.__thread_recevoir.start()

    def envoyer(self, msg: str)-> None:
        #send message
        data_bytes = msg.encode("utf-8")
        self.__socket_echange.sendto(data_bytes, (self.__ip_serveur, self.__port_serveur))

    def recevoir(self)-> None:
        while not self.__fin:
            #wait for server response
            data_bytes, ADDR = self.__socket_echange.recvfrom(255)
            msg = data_bytes.decode("utf-8")
            print(f"S => C : {msg}" )
            if msg == "[fin]":
                self.__fin = True
        self.arret()
        
    def arret(self)-> None:
        self.__socket_echange.close()
        os._exit(os.X_OK)
    def arret_brutal(self)-> None:
            self.__socket_echange.close()
            print("fermeture brutale de l'application par le serveur...")
            os._exit(os.X_OK)

if __name__=="__main__":
    #Declaration of variables
    ip_serveur: str = None
    port_serveur: int = None
    
    #Reading parameters
    if len(sys.argv) == 3:
        ip_serveur = sys.argv[1]
        port_serveur = int(sys.argv[2])
    else:
        ip_serveur = "10.10.141.253"
        port_serveur = 5000
        
    fenetre:Ihm=Ihm(ip_serveur,port_serveur) #Creation of the ihm with default ip and robot port
    fenetre.mainloop()

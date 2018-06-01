#!usr/bin/python

import socket
import sys
import os
import time
import subprocess
from scapy.all import *
from Queue import Queue
from threading import Thread

os.system('clear')
print "\n\n\n\033[36m\033[1m            BANNER-GRABBER\033[0;0m\n"

try:
    sys.stdout.write("            [*]\033[94m Internet Connection Status        \033[0:0m:    ")
    sys.stdout.flush()
    if socket.gethostbyname('www.google.com'):
        sys.stdout.write("\033[92mCONNECTED\033[0;0m\n")

except:
    sys.stdout.write("\033[91mNOT CONNECTED\033[0;0m\n")
    sys.stdout.write("            Please Check Your Internet Connection!\n\n")
    
    try:
        i=input("            Press '\033[92mENTER\033[0;0m' To Get Back To The Main Menu!")
    except:
        os.system('clear')
        subprocess.call('python main/MainWindow.py', shell = True)

def Banner_Grab():
    try:
        try:
            inp_url = raw_input ("\n\n\n            Enter URL or IP: ")
            ip_addr = socket.gethostbyname (inp_url)
            port = int(raw_input("            Enter Port To Scan: "))
        except:
            os.system('clear')
            sys.stdout.write("\n\n\033[91m            INVALID\033[0;0m Input! Try Again!")
            Banner_Grab()
        try:
            mysocket = socket.socket()                                                          
            mysocket.connect((ip_addr, port)) 
        except:
            os.system('clear')
            print "    \033[91m        ERROR\033[0;0m Connecting The Target!"
            Options()

        print "\n\033[94m            [*] Grabbing Banner... \033[0;0m\n" 
        
        try:
            data= mysocket.recv(2048).split('\n')                                               
            sys.stdout.write("         \033[1m   Banner On Port "+str(port)+':\033[0;0m\n\n'+'            '+str(data))

            try:
                mysocket.close()
                i = input("\n\n            Press ENTER To Get Back To The Menu...")
            except:
                Options()
        except:
            os.system('clear')
            print "    \033[91m        ERROR\033[0;0m Grabbing Banner!"
            Options()
    except:
        os.system('clear')
        print "\n    \033[91m        ERROR\033[0;0m Retriving Banner!"
        Options()


def Options():
    print "\n    \033[1m\033[36m        Enter Choice:\033[0;0m\n\n            1) List Open Ports On Target  \n            2) Grab Banner Of a Target  \n            3) \033[91mEXIT\033[0;0m"


    try:
        inp=int(raw_input("\n            Choice> "))
    
        if inp==1:
            subprocess.call('python main/Multithreaded_Portscanner.py',shell=True)
            Options()

        elif inp==2:
            os.system('clear')
            Banner_Grab()

        elif inp==3:
            print "\n\033[91m            EXITING\033[0;0m Back To Main Menu..."
            time.sleep(2)
            subprocess.call('python main/MainWindow.py', shell = True)
        else:
            os.system('clear')
            print "\n\033[91m            INVALID\033[0;0m Input! Please Try Again!"
            Options()
    except:
        os.system('clear')
        print "\n\033[91m            INVALID\033[0;0m Input! Please Try Again!"
        Options()


Options()

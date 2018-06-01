#!/bin/bash/python

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import socket
import time
import sys, signal
import os
from scapy.all import *
from Queue import Queue
from threading import Thread
from subprocess import PIPE, Popen, call

date = Popen('date +"%m-%d-%y"', shell = True, stdout = PIPE).stdout.read().split('\n')[0]
c_time = Popen("date | awk '{print $4}'", shell = True, stdout = PIPE).stdout.read().split('\n')[0]

file = open('bin/logs/'+str(date)+'/Port_sc.log','a')
file.write('Port Scanner '+str(time.ctime())+'\n\n')

os.system('clear')
print "\n\n\n\033[1m\033[36m            PORT SCANNER\033[0;0m\n"

try:
    sys.stdout.write("            [*]\033[94m Internet Connection Status       \033[0;0m                           :")
    sys.stdout.flush()
    if socket.gethostbyname('www.google.com'):
	file.write('Connected: '+str(time.ctime()))
        sys.stdout.write("\033[92m     CONNECTED\033[0;0m\n\n")

except:
        sys.stdout.write("\033[91m    NOT CONNECTED\033[0;0m\n")
        file.write('Connection Lost: '+str(time.ctime()))
        sys.stdout.write("            [-] Please Check Your Internet Connection!\n\n")
        time.sleep(2)
        os.system('clear; python main/MainWindow.py')

def run(q,urlip):
    try:
	file.write('Scanning (0) : '+str(time.ctime()))
        while True:
            try:
                port=q.get()
                response = sr1(IP(dst=urlip)/TCP(dport=port, flags='S'),verbose=False, timeout=1,retry=3)
                if response:
                    if response[TCP].flags == 18:
                        try:
                            s=socket.getservbyport(port)
                            sys.stdout.write("            Open Port:  [ "+str(port)+" ]         : "+str(s)+"\n")
			    data.write(str(port)+'	:	'+str(s)+'\n')
                        except:
                            sys.stdout.write("            Open Port:  [ "+str(port)+" ]         : NA \n")
			    data.write(str(port)+'      :       '+str(s)+'\n')
            
            except Exception as e:
		pass

            q.task_done()
	file.write('Scanning (1): '+str(time.ctime()))

    except Exception:
        print '            Port Scanner Has\033[91m Stopped\033[0;0m Working!'
	data.close()
        file.close()
	os.kill(os.getpid(), signal.SIGKILL)

q = Queue(maxsize =0)
threads = 40

try:
    urlip=raw_input("            Enter URL or IP To Scan        : ")
    startport=int(input("            Start Scan From Port Number    : "))
    endport=int(input("            Scan Upto Port Number          : "))
    #data.write(str(urlip)+'\n'+str(startport)+'\n'+str(endport)+'\n\n')

except Exception:
    print '\n'
    os.system('clear')
    sys.stdout.write("\n            \033[91mINVALID\033[0;0m Input, Please Try Again!")
    sys.stdout.flush()
    os.system('python main/Multithreaded_Portscanner.py')

print "\n   \033[94m         [*] SCANNING FOR OPEN PORTS...\033[0;0m \n"


for j in range(startport,endport+1):
    q.put(j)

data = open('bin/data/'+str(date)+'/port_sc/Port_sc_'+str(c_time)+'.log','a')
data.write('Port Scanner '+str(time.ctime())+'\n\n')

for i in range(threads):
    thread = Thread(target=run, args=(q,urlip,))
    thread.setDaemon(True)
    thread.start()

q.join()
data.write('\n--------------END-------------')
data.close()
file.close()
print "\n            \033[92mSCAN COMPLETED\033[0;0m"

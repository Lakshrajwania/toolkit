import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from Queue import Queue
from threading import Thread
import time
import os
import signal
import time
from subprocess import PIPE, Popen, call


date = Popen('date +"%m-%d-%y"', shell = True, stdout = PIPE).stdout.read().split('\n')[0]
c_time = Popen("date | awk '{print $4}'", shell = True, stdout = PIPE).stdout.read().split('\n')[0]

os.system('clear')
print "\n\n            \033[36m\033[1mNETWORK-SCANNER                  \033[0;0m\n"
file = open('bin/logs/'+str(date)+'/Ntwrk_sc.log','a')


try:
    sys.stdout.write("            [*]\033[94m Internet Connection Status                                      \033[0;0m:")
    sys.stdout.flush()
    if socket.gethostbyname('www.google.com'):
        file.write('\nConnected: '+str(time.ctime())+'\n')
        sys.stdout.write("\033[92m     CONNECTED\033[0;0m\n")

except Exception:
    sys.stdout.write("\033[91m         NOT CONNECTED\033[0;0m\n")
    file.write('Connection Lost: '+str(time.ctime())+'\n')
    sys.stdout.write("            [-]\033[91mPlease Check Your Internet Connection!\033[0;0m\n\n")
    time.sleep(2)
    sys.exit()
    file.close()


def online_hosts():
    os.system('clear')
    print "\n\n"
    print "\n            \033[36m\033[1mNETWORK-SCANNER\033[0;0m\n"
    file.write('Online Hosts (0): '+str(time.ctime())+'\n')
    try:
        sys.stdout.write("            [*]\033[94m Internet Connection Status                                      \033[0;0m:")
        sys.stdout.flush()
        if socket.gethostbyname('www.google.com'):
	    file.write('Connected: '+str(time.ctime())+'\n')
            sys.stdout.write("\033[92m     CONNECTED\033[0;0m\n")

    except Exception:
        sys.stdout.write("\033[91m         NOT CONNECTED\033[0;0m\n")
	file.write('Connection Lost: '+str(time.ctime())+'\n')
        sys.stdout.write("            [-]\033[91mPlease Check Your Internet Connection!\033[0;0m\n\n")
        time.sleep(2)
        sys.exit()
    
    try:
        def get_hosts(q):
	    
            while True:
                try:
                    ip = q.get()
                    comm = ['ping -c 1 -W 2 '+ip+" | grep '64 bytes from' | awk '{print $4}'"]
                    add = subprocess.Popen(comm , shell = True, stdout = PIPE)
                    address1 = add.stdout.read()
                    address = str(address1).split("\n")[0].split(":")[0]
                    try:
                        responses,unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=address),verbose=False, timeout=2,retry=5)
                        if responses:
                            for s,r in responses:
                                mac= r[Ether].src
                                sys.stdout.write("            {:20.16}        {:20.18}".format(address,mac)+"\n")
                                sys.stdout.flush()
				data.write(str(address)+'	:	'+str(mac)+"\n")
                                break
                        q.task_done()
                    except Exception:
                        print "            [-] \033[91mError\033[0;0m Retrieving MAC Addresses, Try Again!!"
                        time.sleep(1)
                        sys.exit

                except Exception:
                    q.task_done()
                    pass

        q = Queue(maxsize = 0)
        threads = 80

        for ip_s in range (1,255):
            com = ["route -n | grep 'UG' | awk '{print $2}'"]
            ga=subprocess.Popen(com, stdout=PIPE,shell= True)
            gate_ip = ga.stdout.read()

            ipaddr = ".".join(str(gate_ip).split(".")[0:3])+'.'+str(ip_s)
            q.put(ipaddr)

        print "\n            [*] Getting Information..."
        a = time.time()
        sys.stdout.write("            [*] \033[94mStarting Network Scanner...                                     \033[0;0m:     "+str(time.ctime()))
        sys.stdout.flush()
        print "\n\n            \033[1m________________________________________\033[0;0m"
        sys.stdout.write("            \033[1m\033[4mIP ADDRESS                  MAC ADDRESS \033[0;0m\n\n")
        sys.stdout.flush()
        
	data = open('bin/data/'+str(date)+'/ntwrk_sc/Ntwrk_sc_'+str(c_time)+'.log','a')
        data.write('Network Scanner: '+str(time.ctime()))
    
        for i in range(threads):
            thread = Thread(target=get_hosts, args=(q,))
            thread.setDaemon(True)
            thread.start()
            
        q.join()
	file.write('Online Hosts (1): '+str(time.ctime())+'\n')
            
         
    except Exception:
        print "\n            [-] \033[91mError\033[0;0m Scanning Network"
        Options()
        

    sys.stdout.write("\n            [+] \033[92mSuccess: Network Scan Done!                                     \033[0;0m:     "+str(time.ctime()))
    sys.stdout.flush()
    d = str(time.time() - a)
    c = d[0:5]
    sys.stdout.write("\n            [+] Time Elapsed!                                                   :     "+str(c)+" seconds"+"\n\n")
    sys.stdout.flush()
    file.write('Exit: '+str(time.ctime())+'\n\n')
    file.close()
    data.write('\n------------END------------\n')
    data.close()

def Options():
    print "\n            \033[1m\033[36mEnter Your Choice\033[0;0m\n\n            1) Scan-Network\n            2) \033[91mEXIT\033[0;0m"


    try:
        inp=int(raw_input("\n            Choice> \033[0;0m"))
    
        if inp==1:
            online_hosts()
	elif inp == 2:
	    sys.exit()

        else:
            print "\n            \033[91mInvalid\033[0;0m Input, Please Try Again!!"
            Options()
    except Exception:
        print "\n            \033[91mInvalid\033[0;0m Input, Please Try Again!!"
        Options()


Options()

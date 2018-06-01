import socket
import sys, time
import os 
from subprocess import PIPE, Popen, call

date = Popen('date +"%m-%d-%y"', shell = True, stdout = PIPE).stdout.read().split('\n')[0]
c_time = Popen("date | awk '{print $4}'", shell = True, stdout = PIPE).stdout.read().split('\n')[0]

file = open('bin/logs/'+str(date)+'/Host_grb.log','a')
file.write('Host/IP Grabber '+str(time.ctime())+'\n\n')


def remotemachine():
    os.system('clear')
    print "\n\n\n\033[36m\033[1m            HOST/IP GRABBER\033[0;0m\n"
    sys.stdout.write("\033[94m            Internet Connection Status\033[0;0m            :    ")
    sys.stdout.flush()
    try:
        if socket.gethostbyname('www.google.com'):
            sys.stdout.write("\033[92mCONNECTED\033[0;0m\n\n")
	    file.write('Connected: '+str(time.ctime())+'\n')
    except:
        sys.stdout.write("\033[91mNOT CONNECTED\033[0;0m\n\n")
	file.write('Conenction Lost: '+str(time.ctime)+'\n')
        sys.exit()

    input_url = raw_input("\033[91m            Enter URL: \033[0;0m")
    
    try:
	file.write('Grabbing (0): '+str(time.ctime())+'\n')
	data = open('bin/data/'+str(date)+'/host_grb/Host_grb_'+str(c_time)+'.log','a')
	data.write('Host/IP Grabber '+str(time.ctime())+'\n\n')

        output_ip = socket.gethostbyname(input_url)
        output_url = socket.gethostbyaddr(output_ip)
        print "            DETAILS: \033[94m",output_url,"\033[0;0m\n"
	data.write(str(output_url))
	data.write('\n--------------END-----------\n')
	file.write('Grabbing (1): '+str(time.ctime)+'\n')
	data.close()
    except socket.herror:
        print "            [-]\033[91m ERROR\033[0;0m Grabbing Host!"
        pass
	file.write('Exit: '+str(time.ctime())+'\n')
	file.close()

remotemachine()

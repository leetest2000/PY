#!usr/bin/python

import sys
import os
import datetime
import csv
import re
import random
import string
import getpass
import pprint
import socket
import jinja2
import ipaddress # load in the ipaddress module

# For debugging
import logging as lg
#lg.basicConfig(level=lg.DEBUG)

# colours
from colorama import Fore, Back, Style

# for SNMP
# for SNMP
from pysnmp.entity.rfc3413.oneliner import cmdgen
# Create command generator object
cmdGen = cmdgen.CommandGenerator()

# define snmp parameters
SNMP_HOST = 'ar0-skyvoip.bllab'
SNMP_PORT = 161
SNMP_COMMUNITY = 'kN8qpTxH'

# Set indent for pprint
pp = pprint.PrettyPrinter(indent=4)

# For Andreas device.py funcs - https://ip.noctools.isp.sky.com/ref/python/skypy/_modules/sky/net/device.html#Device.cliCmd
BASE = "/home/nadt/lib/skypy"
# Our code
sys.path.append(BASE)
# External libs distributed...
sys.path.append(BASE+"/lib") 
from sky.net.device import Device

# Set user/pass
user = getpass.getuser()
pwd = getpass.getpass()


# read a file with the host devices... need split else it will put one letter on a line at a time.
file2 = open('BT_999_Devices.txt','r') 
host_targets = file2.read().split("\n")
file2.close()

# set parameters for device type (sky.net.device)

# Longhand to run this script from scripts2 (note, python3), better to create aliases
# /home/nadt/scripts/git/scripthost/bin/tools/vrun.sh 3 python /home/clifford.bell/py/Lee/testv1.py

print( """

{7}================================================================================================================{0}
{10} - Script to collect 999 routers using L2TP tunnel IPs from given range
{7}================================================================================================================{0}


""".format(Style.RESET_ALL, Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE, Fore.RESET, user))

# empty the file before filling and appending
open('l2tp_tunnel.txt', 'w').close()
open('IPaddresses.txt', 'w').close()

#------------------------------------------------------------
# Screen Cap - Up Interface brief
#------------------------------------------------------------

dicbrief = {}

range_list_input = input("Give me range with subnet separated by space: ")
range_list = range_list_input.split(" ")

#for host in host_targets:
#print(host_targets)"
for host in host_targets:
	if not host:
		continue
	print("=================================\n" + Fore.GREEN + host + Style.RESET_ALL)
	dev = Device.getInstance("Cisco", "XR", hostname = host, sshOpts = {'username': user,'password': pwd,}, snmpOpts = {'community': "en"})
	try:
		# ssh to target device, run command, collect and filter output
		out, err = dev.cliCmd('show l2tp session brief')
		#print(out)
		# Filter output, leave only lines that contain interfaces, line/protocol up split each line and put into list
		filt = re.compile(r".*\sest,UP\s.*")
		out = filter(filt.match, out.split('\r\n'))
			
	except DeviceFailedToConnectError as e:
		raise PrePostFreeze("Failed to connect to the device: {0}".format(e))
		print (host);
	
	#For element in 'out' print and highlight containing 'slsw' else remove all text after @
	for element in out :
	# if the line does NOT have 'cr0-sky' in it carry on.
		if 'cr0-sky' not in element:
			element1 = re.split(r' +', element) #split the element into csv so we can same the variables
			e1,e2,e3,e4,e5,e6,e7 = element1	#save the csv values as variables
			e5 = (e5.split("@")[0]) #remove everything after the '@' symbol.
			
			for range in range_list:
				#get the IP address range and call ipaddress module
				#range = input("Give me range with subnet: ")
				# list all ip addresses with range
				range2 = ipaddress.ip_network(range)
	
				#for IP address within range 
				for x in range2.hosts():
					y = str(x) # convert integer to string		
					if y == e3: #only print the lines matching host IP addresses
					
						print (e3 + "," + e5+"@.isp.sky.com") # print only the required variables.
	
						#write just the hostname to a file.
						file = open('l2tp_tunnel.txt','a')
						file.write(e5+"@.isp.sky.com")
						file.write('\n')
						file.close() 
					
count = str(len(open('l2tp_tunnel.txt').readlines(  )))
print (Fore.GREEN + "There are " + Fore.RED + count + Fore.GREEN + " Devices listed\n" + Style.RESET_ALL)
print ("\ncat l2tp_tunnel.txt, copy the output and send for Spark infrastructure CIs")
	
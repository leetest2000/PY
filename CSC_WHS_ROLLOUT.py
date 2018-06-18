#!usr/bin/python

import sys
import os
from datetime import datetime, date, time
import csv
import re
import random
import string
import getpass
import pprint
import socket
import jinja2
import ipaddress # load in the ipaddress module
import smtplib
import subprocess

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
file2 = open('CSC_Devices.txt','r') 
host_targets = file2.read().split("\n")
#print(host_targets)
file2.close()

print( """

{7}================================================================================================================{0}
{10} - Deployment script - This script will deploy configuration in dir /home/lee.wilson/PY/WHS/*_cmds.txt
{7}================================================================================================================{0}


""".format(Style.RESET_ALL, Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE, Fore.RESET, user))

#------------------------------------------------------------
# Screen Cap - Up Interface brief
#------------------------------------------------------------

confirmed = input('\nAre you SURE you want to continue? (y/n) \n')
if 'n' in confirmed:
	sys.exit('aborting')
elif 'N' in confirmed:
	sys.exit('aborting')

dicbrief = {}

#email function
def send_email (SUBJECT, TXT):
	s=smtplib.SMTP("localhost")
	email_add = (user + '@sky.uk')
	msg = 'Subject: {}\n\n{}'.format(SUBJECT, TXT)
	#to add variable 'user' into the input function a 'format' is needed.
	question1 = input('Is this your email address? {}@sky.uk (y/n):'.format(user))
	if 'n' in question1:
		email_add = input('Please enter your email:')
	elif 'N' in question1:
		email_add = input('Please enter your email:')		
	print('\nsending email to', email_add, '\n')
	s.sendmail("NocAutomation@sky.uk", email_add, msg)
	s.quit()

sbj = 'Alu Config rollout script: Alu_WHS_ROLLOUT.py'
total = ''

	#for host in host_targets:
for host in host_targets:
	total = total + '\n===============================================================================================================================\n'
	if len(host) == 0:
		continue
	print(Fore.RED + "================================= " + Style.RESET_ALL + "Configuring " + host + Fore.RED + " =================================" + Style.RESET_ALL)
	#if host.startswith('sr'):
	dev = Device.getInstance("Cisco", "XR", hostname = host, sshOpts = {'username': user,'password': pwd,}, snmpOpts = {'community': "en"})
		
	file3 = open('CMDS/%s_cmds.txt' % host,'r') 
	host_cmds = file3.read().split("\n")
	file3.close()
	now = datetime.now()
	try:
		# ssh to target device, run command, collect and filter output
		for command in host_cmds :
			out = dev.cliCmd(command)
			# for text in out write the output to file.
			for text in out:
				file = open('logs/' + host + '_%s.log' % now, 'a')
				file.write(text)
				print(text)
				#append the output for all commands to email
				total = total + '\n' + text
			out = str(out)
	
		file.write('\n')
		file.close()
		
		
		
	except DeviceFailedToConnectError as e:
		raise PrePostFreeze("Failed to connect to the device: {0}".format(e))
#email the output collected in 'total'
send_email(sbj, total)		

#!usr/bin/python

import sys
import string
import getpass
from colorama import Fore, Back, Style
import re

# For Andreas device.py funcs - https://ip.noctools.isp.sky.com/ref/python/skypy/_modules/sky/net/device.html#Device.cliCmd
BASE = "/home/nadt/lib/skypy"
# Our code
sys.path.append(BASE)
# External libs distributed...
sys.path.append(BASE+"/lib") 
from sky.net.device import Device

input1 = input('\nenter patching.. : ')

#without defining delimiter in split() splits for spaces, tabs, double space etc..
input2 = input1.split()
input2 = input2[:4]
print(input2)
router1, port1, router2, port2 = input2

# Set user/pass
user = getpass.getuser()
pwd = getpass.getpass()

dicbrief = {}


def send_XR_commands(router, port):
	dev = Device.getInstance("Cisco", "XR", hostname = router, sshOpts = {'username': user,'password': pwd,}, snmpOpts = {'community': "en"})
	output1 = dev.cliCmd('show interface {} description'.format(port))
	if 'pr5' in router:
		output2 = dev.cliCmd('show controllers {}'.format(port))
	else:
		output2 = dev.cliCmd('show controllers {} phy'.format(port))
	#print the output
	output1 = str(output1)
	output1 = output1.split('\\n')
	output2 = str(output2)
	output2 = output2.split('\\n')
	
	#remove specific elements from the list
	ind2remove = [0, 1, 2, 4, 6, 7]
	for i in sorted(ind2remove, reverse=True): 
		del output1[i]
	print('\n\n' + Back.WHITE + Fore.BLACK + router + ':' + Style.RESET_ALL)

	for line in output1:
		line = line.strip('\\r')
		#split line separated by spaces into elements
		line = line.split(' ')
		while '' in line:
			line.remove('')
		#needed to cope with empty description fields
		if len(line) <4:
			line.insert(4,'none')
		#print line neatly.
		print(line[0].ljust(20, ' ') + line[1].ljust(20, ' ') + line[2].ljust(20, ' ') + line[3].ljust(20, ' '))
		if 'L3PASS' in line[3]:
			print (Fore.YELLOW + '\n!!PASS!! - Layer3 testing complete\n' + Style.RESET_ALL)
		elif 'Description' not in line[3]:
			print (Fore.YELLOW + '\n!!FAIL!! - Layer3 testing not complete\n' + Style.RESET_ALL)
####set tag to 0.. this will be used as a tag to print the line below 'DOM Alarms
	tag = 0
	for line2 in output2:
		
		line2 = line2.strip('\\r')
		if 'Alarms:' in line2:
			print(line2)
		elif 'Warnings:' in line2:
			print(line2)
		elif tag == 1:
			if 'No' in line2:
				print('DOM Alarms: ', line2.strip(' '), '\n')
			else:
				print('DOM Alarms: ',Fore.RED, line2.strip(' '), '\n', Style.RESET_ALL)				
			tag = 0
		elif 'DOM alarms:' in line2:
			tag=1
		

def send_TIMOS_commands(router, port):
	dev = Device.getInstance("Alcatel", "7750", hostname = router, sshOpts = {'username': user,'password': pwd,}, snmpOpts = {'community': "en"})
	output1 = dev.cliCmd('show port {} description'.format(port))
	#print the output
	output1 = str(output1)
	output1 = output1.split('\\n')
	for line in output1:
		line = line.strip('\\r')
		print(line)
		if 'Description' in line:
			print(line)
		elif '/' in line:
			if 'L3PASS' in line:
				print(Fore.RED + line + Style.RESET_ALL)
			#else:
				#print(line)
		
if router1.startswith('er'):
	send_XR_commands(router1, port1)
elif router1.startswith('pr'):
	send_XR_commands(router1, port1)
else:
	send_TIMOS_commands(router1, port1)

if router2.startswith('er'):
	send_XR_commands(router2, port2)
elif router2.startswith('pr'):
	send_XR_commands(router2, port2)
else:
	send_TIMOS_commands(router2, port2)

print('\n\ncompleted')
	


	
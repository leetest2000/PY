import os
from netmiko import ConnectHandler
import json
import sys
import time

timestr = time.strftime("%Y%m%d")

net_dev = {
    "host" : (sys.argv[1]),
    "username": "",
    "password": "",
    "device_type": "cisco_ios",
   # "fast_cli": False,
    "secret": ""
}

Faillog = open(f"d:\\\\Errlog\\failures-{timestr}.log", "a")

try:
    Connect = ConnectHandler(**net_dev)
    interfaces = (Connect.send_command("show interfaces", use_textfsm=True, read_timeout=500))
    version = (Connect.send_command("show version", use_textfsm=True))
    #Hostname = int({version['hostname']})
    for interface in interfaces:
       print(f"{(sys.argv[2])},{(sys.argv[3])},{(sys.argv[1])},{version[0]['hostname']},{interface['interface']},{interface['hardware_type']},{interface['link_status']},{interface['description']},{interface['ip_address']},{interface['last_input']},{interface['last_output']},{version[0]['uptime_years']},{version[0]['uptime_weeks']},{version[0]['uptime_days']}")
    #print(json.dumps(interfaces, indent=2))
   # Connect.close
except Exception as e:
   # print(e)
    Faillog.write(f"Failed to connect to {(sys.argv[3])} at IP {(sys.argv[1])} via ssh!\n")

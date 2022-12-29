import os
from netmiko import ConnectHandler
import json
import sys
import time
timestr = time.strftime("%Y%m%d")

vlan = "Vlan"
switch = "-sw-"
active_host = "up"


net_dev = {
    "host" : (sys.argv[1]),
    "username": "",
    "password": "",
    "device_type": "cisco_ios",
    "secret": ""
}

Faillog = open(f"site_failures_{timestr}.log", "a")

try:
    Connect = ConnectHandler(**net_dev)
    interfaces = (Connect.send_command("show interface", use_textfsm=True, read_timeout=500))
    cdpneighs = (Connect.send_command("show cdp neig", use_textfsm=True, read_timeout=90))
    version = (Connect.send_command("show version", use_textfsm=True, read_timeout=90))
    print(sys.argv[3])
    ap_count = 0
    host_ports = 0
    core_uplinks = 0
    distr_uplinks = 0
    inter_as_link = 0

    for interface in interfaces:
        if (vlan not in interface['interface']) and ('0' != interface['input_packets']) and ( 'FastEthernet0' != interface['interface']) and ( "Port-channel" not in interface['interface'] ):
            print(f"{interface['interface']},{interface['description']},{interface['input_packets']},{interface['last_output']},{interface['protocol_status']}")
        if (vlan not in interface['interface']) and (switch not in interface['description']) and ('0' != interface['input_packets']) and ( 'FastEthernet0' != interface['interface'] ):
            host_ports += 1
        if ("-ap-" in interface['description']):
            ap_count += 1
        if ("-sw-cs" in interface['description'] and ( "Port-channel" not in interface['interface'] )):
            core_uplinks += 1
        if ("-sw-ds" in interface['description'] and ( "Port-channel" not in interface['interface'] )):
            distr_uplinks += 1
        if ("-sw-as" in interface['description'] and ( "Port-channel" not in interface['interface'] )):
            inter_as_link += 1
    print("##")
    for cdpneigh in cdpneighs:
        print(f"{cdpneigh['local_interface']} : {cdpneigh['platform']}")
    for ver in version:
        models = ver['hardware']
    print(f"############### Totals ################\nSwitch: {sys.argv[3]} {models}\nActive Host Ports: {host_ports}\nAPs: {ap_count}\nCore Uplinks: {core_uplinks}\nDistribution Uplinks: {distr_uplinks}\nInter-as links: {inter_as_link}\n#######################################\n")

   # Connect.close
except Exception as e:
    print(f"Failed to connect {sys.argv[3]} IP {(sys.argv[1])} via ssh!")
    Faillog.write(f"Failed to connect {sys.argv[3]} IP {(sys.argv[1])} via ssh!\n")

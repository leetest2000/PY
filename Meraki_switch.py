import requests
import json
import csv

# Fill in your Meraki API key and switch serial number below
api_key = 'YOUR_API_KEY_HERE'
switch_serial = 'YOUR_SWITCH_SERIAL_HERE'

# Make API request to get the list of switch ports
url = f"https://api.meraki.com/api/v1/devices/{switch_serial}/switchPorts"
headers = {
    "X-Cisco-Meraki-API-Key": api_key
}
response = requests.get(url, headers=headers)
port_list = response.json()

# Open a CSV file for writing and write header row
with open('switch_ports.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Port', 'Status', 'VLAN', 'Mode'])

    # Loop through each port and write its information to the CSV file
    for port in port_list:
        port_number = port['number']
        port_status = port['status']
        port_vlan = port['vlan']
        port_mode = port['type']
        writer.writerow([port_number, port_status, port_vlan, port_mode])

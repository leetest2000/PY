import json
from netmiko import ConnectHandler

# Define the device parameters
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.1',
    'username': 'yourusername',
    'password': 'yourpassword'
}

# Connect to the device and execute the 'show inventory' command
with ConnectHandler(**device) as net_connect:
    output = net_connect.send_command('show inventory')

# Parse the output to extract information about the SFP modules
sfp_modules = []
for line in output.splitlines():
    if 'SFP' in line:
        sfp_info = line.split(',')
        sfp_module = {
            'name': sfp_info[0].split()[1],
            'description': sfp_info[1].split()[1],
            'pid': sfp_info[2].split()[1],
            'vid': sfp_info[3].split()[1],
            'serial': sfp_info[4].split()[1]
        }
        sfp_modules.append(sfp_module)

# Output the SFP module information in JSON format
json_output = json.dumps(sfp_modules, indent=4)
print(json_output)

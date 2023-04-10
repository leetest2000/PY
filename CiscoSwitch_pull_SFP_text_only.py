from netmiko import ConnectHandler

# Define the device parameters
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.1',
    'username': 'yourusername',
    'password': 'yourpassword'
}

# Connect to the device and execute the 'show interface transceiver' command
with ConnectHandler(**device) as net_connect:
    output = net_connect.send_command('show interface transceiver')

# Extract information about the SFP modules and display the output in a text list
copper_modules = []
fiber_modules = []

for line in output.splitlines():
    if 'SFP' in line:
        sfp_info = line.split()
        module_name = sfp_info[1]
        if 'Copper' in line:
            copper_modules.append(module_name)
        elif 'Fiber' in line:
            fiber_modules.append(module_name)

print('Copper modules:')
print('\n'.join(copper_modules))

print('\nFiber modules:')
print('\n'.join(fiber_modules))

import requests
import json
import csv
import meraki
from datetime import datetime

# Get the current timestamp
timestamp = datetime.now().strftime('%y%m%d')

def write_org_data_to_csv(data, filename):
    """
    Write organization data to CSV file
    """
    csv_header = ['id', 'organizationId', 'name', 'productTypes', 'timeZone', 'tags', 'enrollmentString', 'url', 'notes', 'configTemplateId', 'isBoundToConfigTemplate']
    with open(filename, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_header)
        writer.writeheader()

        for org in data:
            org['productTypes'] = ','.join(org['productTypes'])
            org['tags'] = ','.join(org['tags']) if org['tags'] else ''
            writer.writerow(org)

def get_switch_ports(api_key, switches, input_file):
    """
    Make API request to get switch port data for each switch
    """
    dashboard = meraki.DashboardAPI(api_key)
    port_data = []
    for switch in switches:
        response = dashboard.switch.getDeviceSwitchPortsStatuses(switch)
        response2 = dashboard.switch.getDeviceSwitchPorts(switch)
        with open(input_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Serial'] == switch:
                    switch_name = row['Name']
                    site_name = row['site_name']
                    break
            else:
                switch_name = 'Unknown'
                site_name = 'Unknown'
        for row in response:
            for row2 in response2:
                if row['portId'] == row2['portId']:
                    port_data.append([
                        site_name,
                        switch_name,
                        switch,
                        row['portId'],
                        row2['name'],
                        row['enabled'],
                        row['status'],
                        row['isUplink'],
                        row['speed'],
                        row['duplex'],
                        row2['vlan'],
                        row2['voiceVlan'],
                        row['clientCount'],
                        row['trafficInKbps']['total']
                    ])
                    break
    return port_data


def write_switch_port_data_to_csv(data, filename):
    """
    Write switch port data to CSV file
    """
    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['site_name', 'switch_name', 'switch_serial', 'portId', 'port_name', 'enabled', 'status', 'isUplink', 'speed', 'duplex', 'vlan', 'voice_vlan', 'clientCount', 'total_pkts'])
            for row in data:
                writer.writerow(row)
    except Exception as e:
        print(f"Error saving switch port data to {filename}: {e}")

if __name__ == '__main__':
    # Fill in your Meraki API key and organization ID below
    API_KEY = '#######'
    ORG_ID = '#######'
    
    # Get network devices inventory and write to CSV
    
    input_file = f'meraki_inventory_{timestamp}.csv'

    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        switch_serials = [row['Serial'] for row in reader if row['productType'] == 'switch']
    
    # Get switch port data and write to CSV
    port_data = get_switch_ports(API_KEY, switch_serials, input_file)
    port_filename = f'meraki_switch_ports_{timestamp}.csv'
    write_switch_port_data_to_csv(port_data, port_filename)

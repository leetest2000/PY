import requests
import json
import csv
from datetime import datetime
import meraki


def get_org_networks(api_key, org_id):
    """
    Make API request to get networks in an organization
    """
    dashboard = meraki.DashboardAPI(api_key)
    return dashboard.organizations.getOrganizationNetworks(org_id, total_pages='all')


API_KEY = '########'
ORG_ID = '########'

# Make API request to get the list of inventory devies
url = f"https://api.meraki.com/api/v1/organizations/{ORG_ID}/devices"
headers = {"X-Cisco-Meraki-API-Key": API_KEY}
response = requests.get(url, headers=headers)

# Convert response to JSON format
json_data = json.loads(response.content)

try:
    # Get organization data
    org_data = get_org_networks(API_KEY, ORG_ID)

    # Get the current timestamp
    timestamp = datetime.now().strftime('%y%m%d')

    # Define the output CSV file
    filename = f"meraki_inventory_{timestamp}.csv"

    # Write JSON data to CSV file with current date and time in filename
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['site_name', 'Name', 'Model', 'productType', 'MAC', 'Serial', 'NetworkID'])

        # Write each device to the CSV file
        for device in json_data:
            # Find the name of the network that the device is in
            site_name = ''
            for network in org_data:
                if network['id'] == device['networkId']:
                    site_name = network['name']
                    break

            # Write the device to the CSV file
            writer.writerow([site_name, device['name'], device['model'], device['productType'], device['mac'], device['serial'], device['networkId']])

    print(f"CSV file '{filename}' created successfully!")
except requests.exceptions.HTTPError as errh:
    print(f"HTTP Error: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"Error Connecting: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Timeout Error: {errt}")
except requests.exceptions.RequestException as err:
    print(f"Something went wrong: {err}")


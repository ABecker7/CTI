import requests
import json
from datetime import datetime



OTX_API_KEY = '367b9fbfe7b22f1dc6d4051b11fce7933c23e8c1ee14bfeb156967a848851081'
OTX_URL = 'https://otx.alienvault.com/api/v1/indicators/export?type=IPv4&Limit=50'
IOC_FILE_PATH = '/var/ossec/etc/lists/malicious_ips.txt'
RULES_FILE_PATH = '/var/ossec/etc/rules/local_rules.xml'



def fetch_otx_data():
    headers = {
        'X-OTX-API-KEY': OTX_API_KEY
    }
    response = requests.get(OTX_URL, headers=headers)
    if response.status_code == 200:
        print('test')
        return response.text.split('\n')
    else:
        print("failed to fetch data:", reponse.status_code)
        return []


def write_iocs_to_wazuh_file(iocs):
    with open(IOC_FILE_PATH, 'w') as f:
        for ioc in iocs:
            if ioc.strip():
                f.write(ioc.strip() + '\n')
    print(f"[+] {len(iocs)} IOCs written to Wazuh list.")


if __name__ == "__main__":
    print(fetch_otx_data())   

import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os
from sqlmodel import Field, Session, SQLModel, create_engine, select


load_dotenv()



api_key = os.getenv("OTX_API_KEY")
vt_api_key = os.getenv("VT_API_KEY")
vt_url = 'https://www.virustotal.com/api/v3/'
OTX_API_KEY = api_key
VT_API_KEY = vt_api_key
OTX_URL = 'https://otx.alienvault.com/api/v1/indicators/export?type=IPv4&Limit=50'
IOC_FILE_PATH = '/var/ossec/etc/lists/malicious_ips.txt'
RULES_FILE_PATH = '/var/ossec/etc/rules/local_rules.xml'

class Threat(SQLModel, table=True):

    id: int | None = Field(default=None, primary_key=True)
    indicator: str | None = None
    type: str | None = None
    confidence: int | None = None
    cve: str | None = None
    attack_pattern: str | None = None
    timestamp: str | None = None


# class ThreatEnrichment(SQLModel, table=True):



sqlite_file_name = "cti.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)



def create_db_and_tables():
    SQLModel.metadata.create_all(ngine)


def fetch_otx_data():
    headers = {
        'X-OTX-API-KEY': OTX_API_KEY
    }
    response = requests.get(OTX_URL, headers=headers)
    if response.status_code == 200:
    
        json_data = json.loads(response.text)
    
        for i in json_data['results']:
            i = Threat(id=i['id'], indicator=i['indicator'], type=i['type']) 
            with Session(engine) as session:
                session.add(i)
                session.commit()
    else:
        print("failed to fetch data:", response.status_code)
        return []
    
def select_threats():
    headers = {
        "accept":"application/json",
        "x-apikey":vt_api_key,
    }

    with Session(engine) as session:
        statement = select(Threat)
        results = session.exec(statement)
        for threat in results:

            if threat.type == "IPv4":
                vt_url = f"https://www.virustotal.com/api/v3/ip_addresses/{threat.indicator}"
                response = requests.get(vt_url, headers=headers)
                json_data = json.loads(response.text)
                for i in json_data:
                    print(i)




                 

def write_iocs_to_wazuh_file(iocs):
    with open(IOC_FILE_PATH, 'w') as f:
        for ioc in iocs:
            if ioc.strip():
                f.write(ioc.strip() + '\n')
    print(f"[+] {len(iocs)} IOCs written to Wazuh list.")


def main():
    create_db_and_tables()    
    fetch_otx_data()
    

if __name__ == "__main__":
    select_threats()

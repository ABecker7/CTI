from bs4 import BeautifulSoup
import requests
import json

with open('stix.json', 'r') as file:
    data = json.load(file)

final = {}



for i in range(len(data['data']['objects'])):
    if i not in final:
        final[i] = {}

    
    for k, v in data['data']['objects'][i].items():
        if k == 'hashes':
            final[i][k] = v
        elif k == 'file_name':
            final[i][k] = v
        elif k == 'external_references':
            final[i][k] = v
print(final)

print(data['data']['objects'][1].items())

import json
from bs4 import BeautifulSoup
import requests
import argparse 


def page_contents(url):
 

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}


    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        return r.text
    return None


def get_feeds(page_contents):
    soup = BeautifulSoup(page_contents, 'html.parser')
    feed = soup.find_all('a', href=True)
    href = {}

    for a in feed:
        if "/Download" in a['href']:
            href[a.text] = { 'url': url + a['href']}

        else:
            continue
    return href

def cti(get_feeds):
    for k,v in get_feeds.items():
        r = requests.get(v['url'])
        get_feeds[k].update({ 'content': r.text}) 
    return get_feeds        

if __name__ == '__main__':
    url = "https://threatview.io"
    page_contents = page_contents(url)

    if page_contents:
        ct = cti(get_feeds(page_contents))
        print(ct)
    else: 
        print('Failed to get page contents.')





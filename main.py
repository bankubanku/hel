import requests
from requests_html import HTML
from requests_html import HTMLSession
import os 
from bs4 import BeautifulSoup 
from datetime import datetime

get_source_errs = []
DATE_FORMAT = '%a, %d %b %Y %H:%M:%S %Z'
DATE_FORMAT_ALT = '%a, %d %b %Y %H:%M:%S %z'

def get_urls():
    '''Read urls from a file ~/.hel/urls, format it and return 

    Returns:
        urls [list]: list of read urls 
    '''

    url_file = os.path.expanduser('~/.hel/urls')

    f = open(url_file, "r")
    urls = f.readlines()

    for x in range(len(urls)):
        urls[x] = urls[x].replace('\n', '')
        if not urls[x].startswith('http'):
            del urls[x]

    return urls


def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """
    try:  
        #r = requests.get(url)
        session = HTMLSession()
        r = session.get(url)
        soup = BeautifulSoup(r.text, features='xml')
        return soup

    except Exception as e: 
        get_source_errs.append('couldn\'t get source ({})\nError: {}\n'.format(url, e))
        return 0


def get_feed():
    """Read and show feed
    """
    urls = get_urls()

    for url in urls:
        soup = get_source(url)
        if soup==0:
            continue
        
        items = soup.findAll('item')
        
        for item in items:        

            title = item.find('title').text
            pubDate = item.find('pubDate').text
            try:
                pubDate = datetime.strptime(pubDate, DATE_FORMAT)
            except:
                pubDate = datetime.strptime(pubDate, DATE_FORMAT_ALT)

            guid = item.find('guid').text
            description = item.find('description').text

            print('Title: ' + title)
            print(pubDate)
            print('guid: ' + guid)
            #print('Description: ' + description)
            print('===================================================')



def main():
    get_feed()
    for e in get_source_errs:
        print(e)


if __name__=="__main__":
    main() 
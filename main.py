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
    posts = []

    for url in urls:

        soup = get_source(url)

        if soup==0:
            continue
        
        account = soup.find('channel').find('title').text
        items = soup.findAll('item')
        

        for item in items:        

            post = {
                'account': account,
                'title': None,
                'link': None,
                'pubDate': None, 
                'description': None,
            }       
            
            post['title'] = item.find('title')
            post['link'] = item.find('link')
            post['pubDate'] = item.find('pubDate')
            post['description'] = item.find('description')

            for x in post:
                if x == 'account':
                    continue
                if post[x] is not None:
                    post[x] = post[x].text
                elif x == 'pubDate':
                    post[x] = datetime.now()

                if x == 'pubDate':        
                    try:
                        post[x] = datetime.strptime(post[x], DATE_FORMAT)
                    except:
                        post[x] = datetime.now()#datetime.strptime(post[x], DATE_FORMAT_ALT)
                

            posts.append(post)
            
            # print('Creator: ' + creator)
            # print('Title: ' + title)
            # print(pubDate)
            # print('link: ' + link)
            # #print('Description: ' + description)
            # print('===================================================')
    return posts


def main():
    posts = get_feed()
    posts = sorted(posts, key=lambda x: x['pubDate'], reverse=True)
    
    for e in get_source_errs:
        print(e)


if __name__=="__main__":
    main() 
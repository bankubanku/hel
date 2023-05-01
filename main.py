import requests
from requests_html import HTML
from requests_html import HTMLSession
import os 


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

    return urls


def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """
    try:  
        session = HTMLSession()
        response = session.get(url)
        return response
    except: 
        print('couldn\'t get source ({})'.format(url))
        return 0


def get_feed():
    """Read and show feed
    """
    urls = get_urls()

    for url in urls:
        #print(url)
        response = get_source(url)
        if response==0:
            continue

        with response as r:
            items = r.html.find("item", first=False)

            for item in items:        

                title = item.find('title', first=True).text
                pubDate = item.find('pubDate', first=True).text
                guid = item.find('guid', first=True).text
                description = item.find('description', first=True).text

                print('Title: ' + title)
                print('Data: ' + pubDate)
                print('guid: ' + guid)
                print('Description: ' + description)
                print('===================================================')



def main():
    # url = "https://nitter.net/MelonTeee/rss"
    get_feed()
    # get_urls()


if __name__=="__main__":
    main() 
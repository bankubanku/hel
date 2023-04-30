import requests
from requests_html import HTML
from requests_html import HTMLSession


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

    except requests.exceptions.RequestException() as e:
        print(e)

def get_feed(url):
    """Read and show feed of given url

    Args: 
        url (string): URL of the RSS feed to read.
    """
    
    response = get_source(url)

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
    url = "https://nitter.net/MelonTeee/rss"
    get_feed(url)


if __name__=="__main__":
    main() 
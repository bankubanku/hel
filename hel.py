import requests
from requests_html import HTML
from requests_html import HTMLSession
import os
from bs4 import BeautifulSoup
from datetime import datetime
import posts 

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

    for x in range(len(urls)-1):
        urls[x] = urls[x].replace('\n', '')

    return urls


def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    if not url.startswith('http'):
        return 0

    try:
        session = HTMLSession()
        r = session.get(url)
        soup = BeautifulSoup(r.text, features='xml')
        return soup

    except Exception as e:
        get_source_errs.append(
            'couldn\'t get source ({})\nError: {}\n'.format(url, e))
        return 0


def get_feed(posts):
    """Read and show feed
    """

    urls = get_urls()

    if posts == []:
        last_pubDate = 1
    else:
        print(posts[0])
        last_pubDate = posts[0]['pubDate']

    for url in urls:

        soup = get_source(url)

        if soup == 0:
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

                if x == 'pubDate':
                    try:
                        datetime.strptime(post[x], DATE_FORMAT)
                    except:
                        post[x] = datetime.strptime(post[x], DATE_FORMAT_ALT)
                        post[x] = post[x].strftime(DATE_FORMAT)

            if last_pubDate != 1:
                if datetime.strptime(last_pubDate, DATE_FORMAT) >= datetime.strptime(post['pubDate'], DATE_FORMAT):
                    break

            posts.append(post)

    return posts


def main():
    posts_list = posts.get_list()
    print(posts_list)
    posts_list = get_feed(posts_list)
    posts_list = sorted(posts_list, key=lambda x: datetime.strptime(
        x['pubDate'], DATE_FORMAT), reverse=True)

    posts.save_list(posts_list)

    for e in get_source_errs:
        print(e)


if __name__ == "__main__":
    main()

#import requests
# from requests_html import HTML
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from os.path import exists, expanduser 
from data_handling import get_atom_data, get_rss_data

get_source_errs = []


def get_urls():
    '''Read urls from a file ~/.hel/urls, format it and return list of read urls

    returns:
        urls [list]: list of read urls
    '''

    url_file = expanduser('~/.hel/urls')
    urls = []

    with open(url_file, "r") as f:
        for x in f:
            '''check if given line starts with http to avoid errors when requesting and give an ability to comment'''
            if not x.startswith('http'):
                continue
            '''remove new line escape sign to avoid errors'''
            x = x.replace('\n', '')
            urls.append(x)

    return urls


def get_soup(url):
    """scape data from given address and make a soup  

    args:
        url (string): url of the page to scrape.

    returns:
        soup {bs4.object}: soup of scraped data or 0 if an error occured
    """

    try:
        session = HTMLSession()
        r = session.get(url)
        soup = BeautifulSoup(r.text, features='xml')
        return soup

    except Exception as e:
        get_source_errs.append(
            'couldn\'t get source ({})\nError: {}\n'.format(url, e))
        return 0


def update(posts_list):
    '''get feed from the Internet based on given urls and update the list of posts

    args:
        posts_list (list): already saved posts

    returns:
        posts_list (list): unsorted list of dictionaries updated by newer feed from the internet
    '''

    urls = get_urls()

    '''check what was publication date of the last saved post and set 1 if there was no last saved post'''
    if posts_list == []:
        last_pubDate = 1
    else:
        last_pubDate = posts_list[0]['pubDate']

    #i = 0
    '''go through each source and get needed data'''
    for url in urls:

        '''get soup (bs4) for given source'''
        soup = get_soup(url)

        '''skip parsing data if there is no soup to parse'''
        if soup == 0:
            continue

        items = soup.findAll('item')
        entries = soup.findAll('entry')
        account = soup.find('title').text

        #i += 1

        if len(items) > len(entries):
            for item in items:
                post_data = {
                    'account': account,
                    'title': None,
                    'link': None,
                    'pubDate': None,
                    'description': None,
                }
                post_data = get_rss_data(item, post_data, last_pubDate)
                # if post_data == 1:
                #     continue
                # else:
                posts_list.append(post_data)

        elif len(items) < len(entries):
            for entry in entries:
                post_data = {
                    'account': account,
                    'title': None,
                    'link': None,
                    'pubDate': None,
                    'description': None,
                }
                post_data = get_atom_data(entry, post_data, last_pubDate)
                # if post_data == 1:
                #     continue
                #else:
                posts_list.append(post_data)
        else:
            print('there is no feed for {}'.format(url))

    return posts_list, get_source_errs
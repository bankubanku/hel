from requests_html import HTMLSession
from bs4 import BeautifulSoup
from os.path import exists, expanduser 
from modules.data_handling import get_data
import feedparser

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



def update(posts_list):
    '''get feed from the Internet based on given urls and update the list of posts

    args:
        posts_list (list): already saved posts

    returns:
        posts_list (list): unsorted list of dictionaries updated by newer feed from the internet
    '''

    urls = get_urls()

    '''check what was publication date of the last saved post and set low number if there was no last saved post'''
    if posts_list == []:
        last_published = 2137 # if u know, u know :3 
    else:
        last_published = posts_list[0]['published']

    '''go through each source and get needed data'''
    for url in urls:
        try:
            parsed_feed = feedparser.parse(url)
        except Exception as e:
            get_source_errs.append(e)
        post_to_append = get_data(parsed_feed, last_published)

        for x in post_to_append:
            posts_list.append(x)
        post_to_append = []

    return posts_list, get_source_errs


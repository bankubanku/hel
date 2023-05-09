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


def get_atom_data(entry, post_data):
    post_data['title'] = entry.find('title')
    post_data['link'] = entry.find('link', href=True)
    print(post_data['link'])
    post_data['pubData'] = entry.find('published')
    post_data['description'] = entry.find('media:description')



def get_rss_data(item, post_data, last_pubDate):
    '''write proper data to its place for each item'''
    

    post_data['title'] = item.find('title')
    post_data['link'] = item.find('link')
    post_data['pubDate'] = item.find('pubDate')
    post_data['description'] = item.find('description')
    # print(post_data['description'])

    for x in post_data:
        '''check if x isn't None and if it isn't make a string out of it'''
        if x == 'account':
            continue
        if post_data[x] is not None:
            post_data[x] = post_data[x].text

        '''check if pubDate is in the right format and if it isn't change it to this format'''
        if x == 'pubDate':
            try:
                datetime.strptime(post_data[x], DATE_FORMAT)
            except:
                post_data[x] = datetime.strptime(post_data[x], DATE_FORMAT_ALT)
                post_data[x] = post_data[x].strftime(DATE_FORMAT)

            '''if pubDate of this post is older or the same as lase saved post then don't add it again'''
            if last_pubDate != 1:
                if datetime.strptime(last_pubDate, DATE_FORMAT) >= datetime.strptime(post_data['pubDate'], DATE_FORMAT):
                    break

    return post_data
    

def get_urls():
    '''Read urls from a file ~/.hel/urls, format it and return 

    returns:
        urls [list]: list of read urls 
    '''

    url_file = os.path.expanduser('~/.hel/urls')
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


def get_source(url):
    """return the source code for the provided URL. 

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


def get_feed(posts_list):
    '''get feed from the Internet based on given urls and update the list of posts

    args: 
        posts_list (list): already saved posts

    returns: 
        posts_list (list): unsorted list of dictinaries updated by newer feed from the internet
    '''

    urls = get_urls()

    '''check what was publication date of the last saved post and set 1 if there was no last saved post'''
    if posts_list == []:
        last_pubDate = 1
    else:
        last_pubDate = posts_list[0]['pubDate']

    i = 0
    '''go through each source and get needed data'''
    for url in urls:

        '''get soup (bs4) for given source'''
        soup = get_source(url)

        '''skip parsing data if there is no soup to parse'''
        if soup == 0:
            continue

        items = soup.findAll('item')
        entries = soup.findAll('entry')
        account = soup.find('title').text

        post_data = {
            'account': account,
            'title': None,
            'link': None,
            'pubDate': None,
            'description': None,
        }
        i += 1
        
        
        if len(items) > len(entries):
            for item in items:
                post_data = get_rss_data(item, post_data, last_pubDate)
                posts_list.append(post_data)

        # elif len(items) < len(entries):
        #     for entry in entries:
        #         post_data = get_atom_data(entry, post_data)
        #         #posts_list.append(post_data)
        # else:
        #     print('there is no feed for {}'.format(url))

    return posts_list


def main():
    '''Get already saved posts'''
    posts_list = posts.get_list()

    '''Update list of posts by the feed from the Internet'''
    posts_list = get_feed(posts_list)

    '''Sort these posts based on publication date from the newest at the top'''
    posts_list = sorted(posts_list, key=lambda x: datetime.strptime(
        x['pubDate'], DATE_FORMAT), reverse=True)

    '''Save updated list'''
    posts.save_list(posts_list)

    '''Show errors which possibly occured in the meantime'''
    for e in get_source_errs:
        print(e)


if __name__ == "__main__":
    main()

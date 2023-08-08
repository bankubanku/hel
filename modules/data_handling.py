import datetime
from time import gmtime, mktime


def get_data(parsed_entries, last_published):
    '''parses and adds scraped data to list of new posts

    args:
        parsed_entries (feedparser.util.FeedParserDict): data parsed by feedparser
        last_published (float): time of last saved post in unix time format 

    return:
        new_posts (list): list of new posts which weren't saved 
    '''

    new_posts = []

    for entry in parsed_entries.entries:
        post_data = {
            'author': parsed_entries.feed.get('title', 'no data'),
            'title': entry.get('title', 'no data'),
            'link': entry.get('link', 'no data'),
            'published': entry.get('published_parsed', gmtime()),
            'description': entry.get('description',  'no data')
        }

        post_data['published'] = mktime(post_data['published'])

        if post_data['description'] == 'no data': 
            post_data['description'] = parsed_entries.entries[x].get('summary',  'no data')
        
        if post_data['published'] <= last_published:
            continue

        new_posts.append(post_data)

    return new_posts



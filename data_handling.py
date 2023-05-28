import datetime
from time import gmtime, mktime


def is_old(new_time, last_time):
    
    if last_time == 1:
        return False
    elif new_time <= last_time:
        return True
    else:
        return False


def get_data(parsed_entries, last_pubDate):

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
        
        if is_old(post_data['published'], last_pubDate):
            continue

        new_posts.append(post_data)

    return new_posts



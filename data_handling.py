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

    for x in range(len(parsed_entries)):
        post_data = {
            'author': None,
            'title': None,
            'link': None,
            'published': None,
            'description': None
        }
        post_data['author'] = parsed_entries.feed.get('title', 'no data')
        post_data['title'] = parsed_entries.entries[x].get('title', 'no data')
        post_data['link'] = parsed_entries.entries[x].get('link', 'no data')
        post_data['published'] = parsed_entries.entries[x].get('published_parsed', gmtime())
        post_data['description'] = parsed_entries.entries[x].get('description',  'no data')
        if post_data['description'] == 'no data': 
            post_data['description'] = parsed_entries.entries[x].get('summary',  'no data')

        if is_old(post_data['published'], last_pubDate):
            continue
        else:
            post_data['published'] = mktime(post_data['published']) #time.mktime(post_data['published'].timetuple())
        new_posts.append(post_data)

    return new_posts



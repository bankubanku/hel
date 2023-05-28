'''external modules''' 
from datetime import datetime
import json

'''my modules'''
import feed
import json_handling


def main():
    '''Get already saved posts'''
    posts_list = json_handling.get_list()

    '''Update list of posts by the feed from the Internet'''
    posts_list, get_source_errs = feed.update(posts_list)

    posts_list = sorted(posts_list, key=lambda x: x['published'], reverse=True)
    
    '''Save updated list'''
    json_handling.save_list(posts_list)

    '''Show errors which possibly occured in the meantime'''
    for e in get_source_errs:
        print(e)


if __name__ == "__main__":
    main()

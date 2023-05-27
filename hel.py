'''external modules''' 
from datetime import datetime
import json

'''my modules'''
import feed
import json_handling
from atom_date_format import get_date_object, get_date_string


def main():
    '''Get already saved posts'''
    posts_list = json_handling.get_list()

    '''Update list of posts by the feed from the Internet'''
    posts_list, get_source_errs = feed.update(posts_list)

    # print(len(posts_list))

    # '''Sort these posts based on publication date from the newest at the top'''
    # posts_list = sorted(posts_list, key=lambda x: datetime.strptime(
    #     x['pubDate'], RSS_DATE_FORMAT), reverse=True)
    
    '''Save updated list'''
    json_handling.save_list(posts_list)
    # with open(JSON_POSTS, 'w') as f:
        # json.dump(posts_list, f, indent=4)

    '''Show errors which possibly occured in the meantime'''
    for e in get_source_errs:
        print(e)


if __name__ == "__main__":
    main()

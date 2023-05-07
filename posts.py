from os.path import exists, expanduser 
import json


JSON_POSTS = expanduser('~/.hel/posts.json')


def get_list():
    '''get list of posts from json file posts.json
    
    returns: list of all posts saved in posts.json 
    '''
    if exists(JSON_POSTS):
        with open(JSON_POSTS, 'rb') as f:
            posts = json.load(f)
            return posts
    else:
        return []


def save_list(posts):
    '''save list of posts as a json file in posts.json
    
    args: list of dictionaries 
    '''
    with open(JSON_POSTS, 'w') as f:
        json.dump(posts, f, indent=4)
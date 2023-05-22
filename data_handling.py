def get_atom_data(entry, post_data, last_pubDate):
    post_data['title'] = entry.find('title')
    post_data['link'] = entry.find('link', href=True)
    post_data['pubDate'] = entry.find('published')
    post_data['description'] = entry.find('media:description')

    for x in post_data:
        '''check if x isn't None and if it isn't make a string out of it'''
        if x == 'account':
            continue
        if post_data[x] is not None:
            post_data[x] = post_data[x].text
        else:
            post_data[x] = None

        '''I need another aproach for this whole date-format-related shit'''
        # if x == 'pubDate':
        #     try:
        #         #post_data[x] = iso8601.parse_date(post_data[x])
        #         # post_data[x] = datetime.strptime(post_data[x], ATOM_DATE_FORMAT)
        #         # post_data[x] = datetime.strftime(post_data[x], RSS_DATE_FORMAT)
        #         post_data[x] = get_date_object(post_data[x])
        #         post_data[x] = datetime.strftime(post_data[x], END_DATE_FORMAT)
        #         print(post_data[x])
        #     except Exception as e:
        #         post_data[x] = datetime.now()
        #         post_data[x] = post_data[x].strftime(END_DATE_FORMAT)
        #         print(e)
        #         return 1

            #'''if pubDate of this post is older or the same as lase saved post then don't add it again'''
            # if last_pubDate != 1:
            #     if datetime.strptime(last_pubDate, RSS_DATE_FORMAT) >= datetime.strptime(post_data['pubDate'], RSS_DATE_FORMAT):
            #         return 1
        
    return post_data

def get_rss_data(item, post_data, last_pubDate):
    '''write proper data to its place for each item'''
    post_data['title'] = item.find('title')
    post_data['link'] = item.find('link')
    post_data['pubDate'] = item.find('pubDate')
    post_data['description'] = item.find('description')

    for x in post_data:
        '''check if x isn't None and if it isn't make a string out of it'''
        if x == 'account':
            continue
        if post_data[x] is not None:
            post_data[x] = post_data[x].text

        '''I need another aproach for this whole format shit'''
        # '''check if pubDate is in the right format and if it isn't change it to this format'''
        # if x == 'pubDate':
        #     try:
        #         post_data[x] = datetime.strptime(post_data[x], RSS_DATE_FORMAT)
        #         post_data[x] = post_data[x].strftime(END_DATE_FORMAT)
        #     except:
        #         post_data[x] = datetime.now()
        #         post_data[x] = post_data[x].strftime(END_DATE_FORMAT)
        #         return 1

        #     '''if pubDate of this post is older or the same as lase saved post then don't add it again'''
        #     if last_pubDate != 1:
        #         if datetime.strptime(last_pubDate, RSS_DATE_FORMAT) >= datetime.strptime(post_data['pubDate'], RSS_DATE_FORMAT):
        #             return 1 

    return post_data


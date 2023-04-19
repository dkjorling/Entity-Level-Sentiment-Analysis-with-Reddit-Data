import pandas as pd # require pandas 1.5.3
import numpy as np
import decouple
import requests
import json
import warnings
from datetime import datetime
warnings.filterwarnings("ignore")



########### configure requests ###########
config = decouple.AutoConfig(' ')
key = config('APIKEY')
pub = config('PUBLICKEY')
user = config('USERNAME')
pw = config('PW')

auth = requests.auth.HTTPBasicAuth(pub, key)
data = {
    'grant_type': 'password',
    'username': user,
    'password': pw
}

headers = {'User-Agent': 'MYAPI/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

TOKEN = res.json()['access_token']
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}


##################################################################
def get_posts(subreddit, headers=headers, params= {'limit':100}):
    """
    Get up to 100 reddit posts and returns a df
    """
    res = requests.get("https://oauth.reddit.com/r/{}/new".format(subreddit),
                   headers=headers, params=params)
    df = pd.DataFrame()
    
    for post in res.json()['data']['children']:
        # append relevant data to dataframe
        df = df.append({
            'subreddit': post['data']['subreddit'],
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'upvote_ratio': post['data']['upvote_ratio'],
            'ups': post['data']['ups'],
            'downs': post['data']['downs'],
            'score': post['data']['score'],
            'created_utc': datetime.fromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'id': post['data']['id'],
        }, ignore_index=True)
        
    return df


def get_more_posts(subreddit, start_date, headers=headers, params= {'limit':100}):
    """ Get reddit posts back to the passed start_date.  
        
        Parameters
        
        -start_date must be in YYYY-MM-DD string format
    
    """
    df = get_posts(subreddit, headers=headers, params=params)
    params['after'] = 't3_' + df['id'].values[-1]
    while start_date <= df['created_utc'].values[-1]:
        df2 = get_posts(subreddit, headers=headers, params=params)
        df = df.append(df2, ignore_index=True)
        params['after'] = 't3_' + df['id'].values[-1]
        
    return df
        





def get_comments(subreddit, tid, headers=headers):
    """ Given a subreddit and thread id, return all top_level comments in a df.
    """
    params = {'limit': 100}
    res = requests.get("https://oauth.reddit.com/r/{}/comments/{}".format(subreddit, tid),
                       headers=headers,
                       params=params)
    df = pd.DataFrame()
    comments = res.json()[1]['data']['children'] # note this gives top level comments only
    for i in range(len(comments)):
        comment = comments[i]['data']
        
        df = df.append({
            'id': comment['id'],
            'author': comment['author'],
            'pid': comment['parent_id'][3:],
            'body': comment['body'],
            'upvotes': comment['ups'],
            'downvotes': comment['downs']
        }, ignore_index=True)
        
    
    return df


def get_all_replies(tid, cid, headers=headers):
    """ Given a thread id and comment id, return all replies in a dataframe.
    """
    params = {'limit': 100}
    res = requests.get('http://oauth.reddit.com/api/morechildren?link_id=t3_{}&children={}&api_type=json'.format(tid,cid),
                       headers=headers, params=params)
    all_comments = res.json()['json']['data']['things']
    
    df = pd.DataFrame()
    for comment in all_comments:
        df = df.append({
            'id': comment['data']['id'],
            'author': comment['data']['author'],
            'pid': comment['data']['parent_id'][3:],
            'body': comment['data']['body'],
            'upvotes': comment['data']['ups'],
            'downvotes': comment['data']['downs']
        }, ignore_index=True)
    
    return df


def get_all_comments(subreddit, tid, headers=headers):
    """ Given a subreddit and thread, return all comments and replies in a dataframe.
    """
    params = {'limit': 100}
    df_comments = get_comments(subreddit, tid)
    
    for id in df_comments.id:
        df_replies = get_all_replies(tid, id)
        if df_replies.shape[0] > 1:
            df_comments = pd.concat([df_comments, df_replies.iloc[1:]], axis=0)
    
    return df_comments.reset_index().drop(columns=['index'])


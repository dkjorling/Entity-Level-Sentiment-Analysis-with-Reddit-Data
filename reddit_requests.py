import pandas as pd # require pandas 1.5.3
import numpy as np
import decouple
import requests
import warnings
import os
import re
import datetime as dt
from datetime import datetime
from time import sleep
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


def get_more_posts(start, end, subreddit='lakers', limit=50):
    """ Get reddit posts back to the passed start_date.  
        
        Parameters
        
        -start/end must be in YYYY-MM-DD string format
    
    """
    start = datetime.strptime(start, "%Y-%m-%d")
    start = int(start.timestamp())
    end = int(end.timestamp())
    end = datetime.strptime(end, "%Y-%m-%d")
    
    api_query = 'https://api.pushshift.io/reddit/submission/search/' \
                + '?subreddit={}&limit={}&after={}&before={}'.format(subreddit, limit, start, end)
    
    try:
        r = requests.get(api_query)
        json= r.json()
        df = pd.DataFrame(json['data'])
    
        df = df[['utc_datetime_str', 'id', 'title', 'author', 'selftext', 'upvote_ratio']]
        print("Successfully pulled data")
        return df
    except:
        print("Upload failed")





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


def get_all_comments(subreddit, tid, date, headers=headers):
    """ Given a subreddit and thread, return all comments and replies in a dataframe.
    """
    params = {'limit': 100}
    df_comments = get_comments(subreddit, tid)
    
    for id in df_comments.id:
        df_replies = get_all_replies(tid, id)
        if df_replies.shape[0] > 1:
            df_comments = pd.concat([df_comments, df_replies.iloc[1:]], axis=0)
    
    df_comments['tid'] = tid
    second_column = df_comments.pop('tid')
    df_comments.insert(0, 'tid', second_column)
    
    df_comments['datetime'] = date
    first_column = df_comments.pop('datetime')
    df_comments.insert(0, 'datetime', first_column)
    df_comments['datetime'] = pd.to_datetime(df_comments['datetime'])
    
    
    return df_comments.reset_index().drop(columns=['index'])

def try_daily_post_upload(start, end, subreddit='lakers', folder='data/daily_posts/', base ='r_lakers_', limit=50):
    """
    The PushShift API is somewhat unreliable, so this function attempts to pull data
    one day at a time to ensure nothing is missed. The function saves daily csvs to specified folder.
    
    The function also returns a list of dates that were not successfully pulled so that they can be re-tried.
    
    Parameters
        
        -start and end specify total range of data you want pulled 
        -start/end must be in YYYY-MM-DD string format
        -folder is the root of data folder
        -base is base filename for saved csvs
        -limit is the max posts returnd
        
        
    """
    start_dt = datetime.strptime(start, '%Y-%m-%d')
    end_dt = datetime.strptime(end, '%Y-%m-%d')
    diff = (end_dt - start_dt).days
    dates = [end_dt - dt.timedelta(days=x) for x in range(diff)]
    dates_str = [date.strftime('%Y-%m-%d') for date in dates]
    bad_dates = []
    for date in dates:
        start = date # note this is a different start than original since we pull for each day
        end = datetime.strptime(start, '%Y-%m-%d') + dt.timedelta(days=1) # convert to dt to add day
        end = datetime.strptime(end, '%Y-%m-%d') # convert back to string so works in function
        df = get_more_posts(start, end, subreddit=subreddit, limit=limit)
        try:
            start_string = start.replace('-','_') # change format to save
            df.to_csv(folder + base + start_string)
            print("Successfully uploaded data for {}".format(start_string))
        except:
            print("Failed to Upload Data for {}".format(start_string))
            bad_dates.append(start_string.replace('_', '-'))
            
    return bad_dates

            
def check_for_max_posts(limit = 50):
    """
    The PushShift API is rather unreliable and fails often and therefore different \
    limits are tried to pull data. Sometimes days that successfully loaded hit the \
    limit that was used. This function checks the df lengths to return dates that \
    hit the limit. You can then run the get_more_posts function with a higher limit \
    on the returned list. 
    
    """
    directory = '/Users/dylanjorling/NBASA_reddit/data/daily_posts'
    files = os.listdir(directory)
    files = [x for x in files if len(re.findall(r"r_lakers", x)) == 1]
    max_post_files = []
    for file in files:
        try:
            x = pd.read_csv('data/daily_posts/' + file)
            if x.shape[0] == limit:
                max_post_files.append(file)
        except:
            continue
    max_post_files_date = [file[9:] for file in max_post_files]
    max_post_files_date = [file.replace('_', '-') for file in max_post_files_date]
    
    return max_post_files_date

def concat_daily_files(folder_daily='/Users/dylanjorling/NBASA_reddit/data/daily_posts/',
                       base='r_lakers_', folder_full='data/', name='full_posts.csv'):
    """
    This function takes in folder with daily csvs, concatenates them together and saves entire csv
    
    Parameters
        -folder_daily: folder containing daily posts
        -base: base file name for all csv files
        -folder_full: file location
        -name: desired name of full csv file
        
    Requires: pandas, os, re
    """
    
    # filter out unwanted files
    files = os.listdir(folder_daily)
    files = [x for x in files if len(re.findall(r"r_lakers", x)) == 1]
    
    # create list of dfs
    df_list = []
    for file in files:
        df_list.append(pd.read_csv('data/daily_posts/' + file, index_col=0))
    
    # concatenate df
    df_full = pd.concat(df_list, ignore_index=True)
    
    # clean df
    df_full.reset_index()
    df_full=df_full.rename(columns = {'utc_datetime_str':'datetime'})
    df_full['datetime'] = pd.to_datetime(df_full['datetime'])
    #df_full = df_full[df_full['datetime'] >= '2022-10-13'] # optional
    df_full = df_full.sort_values('datetime')
    df_full.set_index('datetime', inplace=True)
    df_full.reset_index(inplace=True)
    
    # save to folder
    df_full.to_csv(folder_full + base + name)
    
    
def save_monthly_comment_history(concat_daily_files_df,
                                 subreddit='lakers',
                                 folder='data/'):
    """
    Given a df of posts returned by concat_daily_files, gets all comments for each post \
    using the get_all_comments function, concatenates all comments for each month, and \
    saves dataframe to csv for each month. Also returns thread ids that did not load
    
    Parameters
        -concat_daily_files_df: dataframe in format that the concat_daily_files function saves to csv
        -subreddit: subreddit where posts were mad
        -folder: 
    """
    df = concat_daily_files_df
    df['month'] = df['datetime'].dt.month_name()

    # iterate through unique months
    bad_ids = []
    for month in set(df['month']):
        # create monthly dfs
        df_int = df[df['month'] == month]

        # define empty df to store comments
        columns = ['datetime', 'tid', 'id', 'author', 'pid', 'body', 'upvotes', 'downvotes']
        dfc_month = pd.DataFrame(columns=columns)

        # iterate through each row and append to month
        for i, row in df_int.iterrows():
            try:
                dfc = rr.get_all_comments(tid=row.id,
                                          date=row.datetime,
                                          subreddit=subreddit)
                dfc_month = pd.concat([dfc_month, dfc])
                print("tid: {} date: {} successfully loaded".format(row.id, row.datetime))
            except:
                print("tid: {} date: {} failed to load".format(row.id, row.datetime))
                bad_ids.append(row.id)


        dfc_month.to_csv(name + 'monthly_comment_hist/{}_comments.csv'.format(month))
    return bad_ids
    
    
    
    
    
    

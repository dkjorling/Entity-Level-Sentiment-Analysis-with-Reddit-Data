import pandas as pd
import numpy as np
import datetime as dt
import math
import re
import itertools
import emoji
import spacy
import json
from spacy.pipeline import EntityRuler

def clean_gifs_hyperlinks_emojis(text):
    clean_text = str(text)
    clean_text = re.sub(r"!gif\(giphy.*\)", "", clean_text) # remove gifs
    clean_text = re.sub(r"\(https[^\s]*\)", " ", clean_text) # remove embedded hyperlinks
    clean_text = re.sub(r"https[^\s]*", " ", clean_text) # remove remaining hyperlinks
    clean_text = re.sub(r"amp;", " ", clean_text)
    
    return clean_text

def basic_clean(text):
    clean_text = str(text)
    clean_text = re.sub(r"’s|'s", "", clean_text)
    clean_text = re.sub(r"['’\[\]#,\.]", "", clean_text)
    clean_text = re.sub(r"[/\-_+&\\]", " ", clean_text)
    
    return clean_text

def clean_post_body(text):
    clean_text = str(text)
    clean_text = re.sub(r"\bnan\b", "", clean_text)
    clean_text = re.sub(r"\bremoved\b", "", clean_text)
    clean_text = re.sub(r"\bdeleted\b", "", clean_text)
    
    return clean_text

def clean_spaces(text):
    clean_text = str(text)
    clean_text = re.sub(r'\s{2,}', ' ', clean_text)
    clean_text = clean_text.lstrip()
    clean_text = clean_text.rstrip()
    
    return clean_text

def clean_all_text(text):
    clean_text = str(text)
    clean_text = clean_text.lower()
    clean_text = clean_gifs_hyperlinks_emojis(clean_text)
    clean_text = basic_clean(clean_text)
    clean_text = clean_post_body(clean_text)
    clean_text = clean_spaces(clean_text)
    clean_text = clean_gifs_hyperlinks_emojis(clean_text) # for good measure
    
    return clean_text

def get_emoji_dict(posts, comments):
    emoji_dict = {}
    text_dfs = [posts, comments]

    for text_df in text_dfs:
        strings = text_df.body
        for string in strings:
            matches = emoji.emoji_list(string)
            text_emojis = []
            for i, _ in enumerate(matches):
                text_emojis.append(matches[i]['emoji'])
            unique_text_emojis = list(set(text_emojis))
            for emj in unique_text_emojis:
                if emj not in emoji_dict.keys():
                    emoji_dict[emj] = 1
                else:
                    emoji_dict[emj] += 1
    return emoji_dict

def extract_emojis(text):
    matches = emoji.emoji_list(text)
    if len(matches) == 0:
        return np.nan
    else:
        text_emojis = []
        for i, _ in enumerate(matches):
            text_emojis.append(matches[i]['emoji'])
        unique_text_emojis = list(set(text_emojis))
        
        return " ".join([str(emj) for emj in unique_text_emojis])

def get_emoji_col(df):
    """
    adds concatenated emoji col to post/comment df
    """
    df['emojis'] = df.body.apply(extract_emojis)
    return df

def find_text(pattern, df):
    """
    Iterates through post/comment df and prints out text matches.
    Use this to spot-check certain patterns.
    """
    find_text = []

    for t in df.body:
        if re.search(pattern, t) != None:
            find_text.append(t)
    print(len(find_text))
    for t in find_text:
        print(t)
    


def create_player_dict(patterns, trade=0, patterns_trade=None, trade_date=None):
    """
    Use regex patterns to extract posts/comments with each unique player reference.
    Returns a dictionary with each unique reference and the post or comment ids the \n
    reference is contained in. 
    
    Parameters
    __________
    patterns: list of patterns to search through
    trade: parameter to specify extraction of certain patterns only before/aftter a trade date
    patterns_trade: patterns to be searched for only before/after trade date if specified
    trade_date: cutoff date, should be in '%Y-%m-%d' form
    """
    if trade not in [0, 1, 2]:
        raise ValueError("Trade must be 0 (not traded), 1 (traded for) or 2 (traded away)")
    if (trade in [1, 2]) & (patterns_trade == None):
        raise ValueError("You have indicated you want before/after trade data. Please specify patterns")
    if (trade in [1, 2]) & (trade_date == None):
        raise ValueError("You have indicated you want before/after trade data. Enter trade_date in '%Y-%m-%d'")
    if trade_date != None:
        check_date = re.findall(r"\b\d{4}-\d{2}-\d{2}", trade_date)
        if len(check_date) != 1:
            raise ValueError("trade_date in wrong form, should be in '%Y-%m-%d'")
        
        
    player_dict = {}
    posts = pd.read_csv("data/clean_posts.csv", index_col=0, parse_dates=['datetime'])
    comments = pd.read_csv("data/clean_comments.csv", index_col=0, parse_dates=['datetime'])
    text_dfs = [posts, comments]
    
    for text_df in text_dfs:
        text_df.body = text_df.body.apply(str)
        for _, row in text_df.iterrows():
            for x in patterns:
                y = re.findall(x, row.body)
                for i in y:
                    if i not in player_dict.keys():
                        player_dict[i] = []
                        player_dict[i].append(row.id)
                    elif row.id not in player_dict[i]:
                        player_dict[i].append(row.id)
                    else: continue
    if trade == 0:
        for k, v in player_dict.items():
            print(k, len(v))
        return player_dict
    
    else:
        if trade == 1: # if 1, then we only want patterns after a trade (indicates traded for)
            posts_trade =  posts[posts['datetime'] >= trade_date]
            comments_trade = comments[comments['datetime'] >= trade_date]
    
        else:
            posts_trade =  posts[posts['datetime'] < trade_date]
            comments_trade = comments[comments['datetime'] < trade_date]
    
        text_dfs_trade = [posts_trade, comments_trade]

        for text_df in text_dfs_trade:
            text_df.body = text_df.body.apply(str)
            for _, row in text_df.iterrows():
                for x in patterns_trade:
                    y = re.findall(x, row.body)
                    for i in y:
                        if i not in player_dict.keys():
                            player_dict[i] = []
                            player_dict[i].append(row.id)
                        elif row.id not in player_dict[i]:
                            player_dict[i].append(row.id) # assure no duplicate ids for any name
                        else:
                            continue
        for k, v in player_dict.items():
            print(k, len(v))
            
        return player_dict

def create_player_post_df(player_dict, name_id):
    """
    Returns df for given player dict containing post details for every post player is mentioned
    """
    # load clean posts
    posts = pd.read_csv("data/clean_posts.csv", index_col=0, parse_dates=['datetime'])
    posts.body = posts.body.apply(str)

    columns = list(posts.columns)
    columns.append('unique_ref')
    columns.append('player_ref')
    df_post = pd.DataFrame(columns=columns)
    df_post.loc[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index1 = 0
    for k, v in player_dict.items():
        for i in player_dict[k]:
            if i in list(df_post.id):
                # if this player_ref is already in the ref column for this post, 
                row1 = df_post[df_post['id'] == i]
                idx1 = row1.index[0]
                
                if k in row1.unique_ref[idx1].split("/"):
                    pass # dont double count if uses same specifc ref more than once
                else:
                    row1 = row1.loc[idx1] # change row from df to series
                    row1.unique_ref = row1.unique_ref + "/" + k
                    df_post.loc[idx1] = list(row1)


            elif i in list(posts.id):
                idx2 = posts[posts.id== i].index[0]
                row = list(posts[posts.id== i].loc[idx2])
                row.append(k)
                row.append(name_id)
                df_post.loc[index1] = row
                index1 += 1

            else:
                pass # the dict contains both posts and comments; if not a comment, pass
            
    return df_post


def create_player_comment_df(player_dict, name_id):
    """
    Returns df for given player dict containing comment details for every comment player is mentioned
    Parameters:
        player_dict: dict created by create_player_dict function
        name_id: single name id for player
    """
    # load clean comments
    comments = pd.read_csv("data/clean_comments.csv", index_col=0, parse_dates=['datetime'])
    comments.body = comments.body.apply(str)
    columns = list(comments.columns)
    columns.append('unique_ref')
    columns.append('player_ref')
    df_comments = pd.DataFrame(columns=columns)
    df_comments.loc[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index1 = 0
    for k, v in player_dict.items():
        for i in player_dict[k]:
            if i in list(df_comments.id):
                # if this player_ref is already in the ref column for this post, 
                row1 = df_comments[df_comments['id'] == i]
                idx1 = row1.index[0]
                if k in row1.unique_ref[idx1].split("/"):
                    pass # dont double count if uses same specifc ref more than once
                else:
                    row1 = row1.loc[idx1]
                    row1.unique_ref = row1.unique_ref + "/" + k
                    df_comments.loc[idx1] = list(row1)


            elif i in list(comments.id):
                idx2 = comments[comments.id== i].index[0]
                row = list(comments[comments.id== i].loc[idx2])
                row.append(k)
                row.append(name_id)
                df_comments.loc[index1] = row
                index1 += 1

            else:
                pass # the dict contains both posts and comments; if not a comment, pass
            
    return df_comments


def save_player_dfs(player_dict, name):
    with open('data/full_names.json', 'r') as f:
        full_names_json = json.load(f)
    full_names = dict(full_names_json)
    
    df_post = create_player_post_df(player_dict, full_names[name])
    df_comment = create_player_comment_df(player_dict, full_names[name])
    df_post.to_csv("data/{}_refs_posts.csv".format(name))
    df_comment.to_csv("data/{}_refs_comments.csv".format(name))


def add_post_entities():
    # load entities dict
    with open('data/entities.json', 'r') as f:
        entities = json.load(f)
    entities = dict(entities)
    
    # load dfs 
    posts = pd.read_csv("data/clean_posts.csv", index_col=0, parse_dates=['datetime'])
    posts.body = posts.body.apply(str)
    
    # reindex for easier slicing and add empty cols
    posts = posts.set_index('id')
    posts['entities'] = ""
    posts['num_entities'] = 0
    
    # load player post dfs
    df_post_list = [pd.read_csv("data/{}_refs_posts.csv".format(x), index_col=0, parse_dates=['datetime']) for x in entities.keys()]
    
    
    for df in df_post_list:
        idxs = list(df.id)
        name = df.player_ref[0]

        # update entity cols
        posts.loc[idxs, "entities"] =  posts.loc[idxs, "entities"] + name + ", "
        posts.loc[idxs, "num_entities"] += 1
    
    return posts
    
def clean_comments_to_tid_ents(clean_comments):
    """
    Get from clean comment df to clean comment w tid ents df
    """
    clean_comments['tid_entities'] = ""
    clean_comments['tid_num_entities'] = 0
    
    posts = pd.read_csv("data/clean_posts_extended.csv", index_col=0, parse_dates=['datetime'])
    posts.body = posts.body.apply(str)
    
    tid_entities_dict = {}
    tid_num_entities_dict = {}
    for _, row in posts.iterrows():
        tid_entities_dict[row.id] = 0
        tid_entities_dict[row.id] = (row.entities)
        tid_num_entities_dict[row.id] = 0
        tid_num_entities_dict[row.id] = (row.num_entities)
        
    clean_comments['tid_entities'] = tid_entities
    clean_comments['tid_num_entities'] = tid_num_entities
    
    comments_with_tid_ents = clean_comments
    
    return comments_with_tid_ents

def add_comment_entities():
    # load entities dict
    with open('data/entities.json', 'r') as f:
        entities = json.load(f)
    entities = dict(entities)
    
    # load dfs 
    comments = pd.read_csv("data/comments_with_tid_ents.csv", index_col=0, parse_dates=['datetime'])
    comments.body = comments.body.apply(str)
    
    # reindex for easier slicing and add empty cols
    comments = comments.set_index('id')
    comments['entities'] = ""
    comments['num_entities'] = 0
    
    # load player post dfs
    df_comment_list = [pd.read_csv("data/{}_refs_comments.csv".format(x), index_col=0, parse_dates=['datetime']) for x in entities.keys()]
    
    
    for df in df_comment_list:
        idxs = list(df.id)
        name = df.player_ref[0]

        # update entity cols
        comments.loc[idxs, "entities"] =  comments.loc[idxs, "entities"] + name + ", "
        comments.loc[idxs, "num_entities"] += 1
    
    return comments


def add_parent1_comment_entities():

    comments = pd.read_csv("data/comments_with_entities.csv", index_col=0, parse_dates=['datetime'])
    comments.body = comments.body.apply(str)

    comments['top_level'] = 1
    comments['parent1_entities'] = ""
    comments['parent1_num_entities'] = 0
    comments.loc[comments['pid'] != comments['tid'], 'top_level'] = 0

    pid_entities_list = []
    pid_num_entities_list = []
    for _, row in comments.iterrows():
        if row.top_level == 0:
            row2 = comments.loc[row.pid]
            parent1_entities = row2.entities
            parent1_num_entities = row2.num_entities
            pid_entities_list.append(parent1_entities)
            pid_num_entities_list.append(parent1_num_entities)
        else:
            parent1_entities = np.nan
            parent1_num_entities = 0
            pid_entities_list.append(parent1_entities)
            pid_num_entities_list.append(parent1_num_entities)
            
    comments['parent1_entities'] = pid_entities_list
    comments['parent1_num_entities'] = pid_num_entities_list
        
def add_parent2_comment_entities():
    comments = pd.read_csv("data/comments_with_parent1_ents.csv", index_col=0, parse_dates=['datetime'])
    comments = comments.set_index('id')
    comments.body = comments.body.apply(str)

    pid2_entities_list = []
    pid2_num_entities_list = []
    pid2 = []
    second_level = []

    for _, row in comments.iterrows():
        if row.top_level == 0:
            row2 = comments.loc[row.pid]
            if row2.top_level == 0:
                row3 = comments.loc[row2.pid]
                parent2_entities = row3.entities
                parent2_num_entities = row3.num_entities
                pid2_entities_list.append(parent2_entities)
                pid2_num_entities_list.append(parent2_num_entities)
                pid2.append(row2.pid)
                second_level.append(0)
            else:
                parent2_entities = np.nan
                parent2_num_entities = 0
                pid2_entities_list.append(parent1_entities)
                pid2_num_entities_list.append(parent1_num_entities)
                pid2.append(row2.tid)
                second_level.append(1)
        else:
            parent2_entities = np.nan
            parent2_num_entities = 0
            pid2_entities_list.append(parent1_entities)
            pid2_num_entities_list.append(parent1_num_entities)
            pid2.append(np.nan)
            second_level.append(0)
    
    comments['parent2_entities'] = pid2_entities_list
    comments['parent2_num_entities'] = pid2_num_entities_list
    comments['pid2'] = pid2
    comments['second_level'] = second_level
            
    return comments
    
# load nlp and add custom entities
#nlp = spacy.load('en_core_web_sm')
#ruler = nlp.add_pipe("entity_ruler", after="ner")

#for name in full_names:
#    pattern= [{"label": "PERSON", "pattern": name}]
#    ruler.add_patterns(pattern)



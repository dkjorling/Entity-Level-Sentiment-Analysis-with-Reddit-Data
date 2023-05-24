import pandas as pd
import numpy as np
import datetime as dt
#import text_cleaning as tc
#import lakers_sentiment_analysis as lsa

### load data ###

def get_base_overall_sentiment(post_sent, comment_sent, post_multiplier=2.5):
    """
    This function simply takes in post and comment sentiment columns labels and returns an overall score
    Parameters:
        post_multiplier: how much more should we weight post sentiment over comment sentiment? Default = 2.5
    """
    # get post sentiment score
    post_length = post_sent.shape[0]
    post_prop_pos = post_sent.value_counts().loc['positive'] / post_length
    post_prop_neg = post_sent.value_counts().loc['negative'] / post_length
    post_score = post_prop_pos - post_prop_neg
    
    # get comment sentiment score
    comment_length = comment_sent.shape[0]
    comment_prop_pos = comment_sent.value_counts().loc['positive'] / comment_length
    comment_prop_neg = comment_sent.value_counts().loc['negative'] / comment_length
    comment_score = comment_prop_pos - comment_prop_neg 
    
    # get weighted score
    num = (post_score * post_length * post_multiplier) + (comment_score * comment_length)
    denom = (post_length * post_multiplier) + comment_length
    weighted = num / denom

    return weighted

def get_rolling_sentiment(df_with_sent, date, days = 30):
    """
    Return sentiment score for entity over past days
    Parameters:
        date: date of sentiment score
        days: lookback period from date for which to count sentiment
    """
    dt_date_end = dt.datetime.strptime(date, "%Y-%m-%d")
    dt_date_beg = dt_date_end - dt.timedelta(days=days)
    df = df_with_sent[(df_with_sent['datetime'] <= dt_date_end) & (df_with_sent['datetime'] > dt_date_beg)]
    
    prop_pos, prop_neg = get_base_overall_sentiment(df['simple_sentiment'])
    
    score = prop_pos - prop_neg
    
    return score


def get_monthly_sentiment(df_with_sent, start="October", end="April"):
    """
    Return monthly sentiment score from Oct-Apr
    """
    months = ['October', 'November', 'December', 'January', 'February', 'March', 'April']
    idx_start = months.index(start)
    idx_end = months.index(end)
    months = months[idx_start:(idx_end + 1)]
    monthly_sents = {}
    for month in months:
        df = df_with_sent[df_with_sent['datetime'].dt.month_name() == month]
        prop_pos, prop_neg = get_base_overall_sentiment(df['sentiment'])
        monthly_sents[month] = prop_pos - prop_neg
    
    return monthly_sents


def get_period_sentiment(post_sent_dated, comment_sent_dated, date='2023-04-14', days=30, post_multiplier=2.5):
    """
    Return sentiment score for entity over past days
    Parameters:
        date: date of sentiment score
        days: lookback period from date for which to count sentiment
    """
    dt_date =  dt.datetime.strptime(date, "%Y-%m-%d")
    dt_date_end = dt_date - dt.timedelta(days=days)

    posts = post_sent_dated[(post_sent_dated['datetime'] <= dt_date) & (post_sent_dated['datetime'] > dt_date_end)]
    comments = comment_sent_dated[(comment_sent_dated['datetime'] <= dt_date) & (comment_sent_dated['datetime'] > dt_date_end)]
    weighted = get_base_overall_sentiment(posts.sentiment, comments.sentiment, post_multiplier=2.5)
    
    return weighted




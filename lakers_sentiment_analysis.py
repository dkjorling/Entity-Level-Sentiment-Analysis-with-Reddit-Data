import pandas as pd
import numpy as np
import json
import random
import re
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from spacy.pipeline import EntityRuler
from spacy.language import Language
from nltk.tokenize import word_tokenize



######################### Initiation Functions #########################

def initiate_lexicon():
    """
    Initiate sentiment analyzer with custom emoji lexicon
    """
    
    with open("data/reddit_hoop_lexicon.json", "r") as f:
        hoop_lexicon = json.load(f)
        hoop_lexicon_dict = dict(hoop_lexicon)
    
    with open("data/emoji_lexicon.json", "r") as f:
        emoji_lexicon = json.load(f)
        emoji_lexicon_dict = dict(emoji_lexicon)
    
    
    sia = SentimentIntensityAnalyzer()
    sia.lexicon.update(hoop_lexicon_dict)
    sia.lexicon.update(emoji_lexicon_dict)
    
    return sia


@Language.component("filter_entities")
def filter_entities(doc):
    with open('data/entities_with_nicknames.json', 'r') as f:
        entities = json.load(f)
    entities = dict(entities)
    
    add_ents = [entities[x]['full_name'] for x in entities.keys()]
    add_ents = add_ents[:-1]
    
    blacklist = {'PERSON', 'ORG', 'DATE', 'GPE',
                 'ORDINAL', 'CARDINAL', 'QUANTITY', 'LOC',
                 'TIME', 'PERCENT', 'PRODUCT', 'MONEY',
                 'FAC', 'NORP', 'EVENT', 'WORK_OF_ART'}
    
    doc.ents = [ent for ent in doc.ents if ent.label_ not in blacklist]
    
    return doc

@Language.factory('my_ruler')
def create_entity_ruler(nlp, name):
    
    nlp = spacy.load("en_core_web_sm")
    
    with open('data/entities_with_nicknames.json', 'r') as f:
        entities = json.load(f)
    entities = dict(entities)
    
    add_ents = [entities[x]['full_name'] for x in entities.keys()]
    add_ents = add_ents[:-1]
    
    ruler = EntityRuler(nlp, overwrite_ents=True)
    
    product_label_id = nlp.vocab.strings["LAKER"]
    
    # define patterns for the names
    patterns = []
    for i, ent in enumerate(add_ents):
        ent_dict = {}
        ent_dict['label'] = product_label_id
        ent_dict['pattern'] = [{"LOWER": ent}]
        patterns.append(ent_dict)

    ruler.add_patterns(patterns)
    
    return ruler

def initiate_nlp():
    nlp = spacy.load("en_core_web_sm")
    assert "transformer" not in nlp.pipe_names
    nlp_coref = spacy.load("en_coreference_web_trf")
    nlp.add_pipe("transformer", source=nlp_coref)
    nlp.add_pipe("coref", source=nlp_coref)
    nlp.add_pipe("span_resolver", source=nlp_coref)
    nlp.add_pipe("span_cleaner", source=nlp_coref)
    nlp.add_pipe('filter_entities', after='ner')
    nlp.vocab.strings.add('LAKER')
    nlp.add_pipe('my_ruler', before='ner')

    return nlp

### initialize ###
#sia = initiate_lexicon()
nlp = spacy.load("en_core_web_sm")

######################### coreference cleaning #########################

def resolve_references(doc):
    # token.idx : token.text
    token_mention_mapper = {}
    output_string = ""

    if len(doc.ents) == 0:
        output_string =  doc.text

    else:
        str_ents = [str(x) for x in doc.ents]
        str_ents = list(set(str_ents))
        clusters = [
                v for k, v in doc.spans.items() if k.startswith("coref_cluster")
            ]

        for cluster in clusters:
            str_cluster = [str(x) for x in cluster]

            for ent in str_ents:
                if ent in str_cluster:
                    for mention_span in list(cluster)[1:]:
                        # Set first_mention as value for the first token in mention_span in the token_mention_mapper
                        token_mention_mapper[mention_span[0].idx] = ent + mention_span[0].whitespace_

                        for token in mention_span[1:]:
                            # Set empty string for all the other tokens in mention_span
                            token_mention_mapper[token.idx] = ""

         # Iterate through every token in the Doc
        for token in doc:
            # Check if token exists in token_mention_mapper
            if token.idx in token_mention_mapper:
                output_string += token_mention_mapper[token.idx]
            # Else add original token text
            else:
                output_string += token.text + token.whitespace_
    
    return output_string.split('** ')[1]

def get_unique_refs(entities, entity_key, df_posts, df_comments):
    z = set(df_posts['unique_ref'])
    z = [x.split("/") for x in z]
    z = [x for y in z for x in y]
    z_posts = list(set(z))
    
    
    z = set(df_comments['unique_ref'])
    z = [x.split("/") for x in z]
    z = [x for y in z for x in y]
    z_comments = list(set(z))
    
    
    names = z_posts + z_comments
    names = list(set(names))
    
    entities[entity_key]['names'] = names
    
    return entities


######################### basic sentiment #########################
def format_output(output_dict, cutoff = 0.05):
    if (cutoff < 0.0) | (cutoff > 1.0):
        raise ValueError("Cutoff must be between 0.0 and 1.0")
    polarity = "neutral"
    
    if(output_dict['compound']>= cutoff):
        polarity = "positive"
        
    elif(output_dict['compound']<= -cutoff):
        polarity = "negative"
        
    return polarity 

def predict_sentiment(text, sia, cutoff = 0.05):
    output_dict =  sia.polarity_scores(text)
    
    return format_output(output_dict, cutoff=cutoff)

def predict_sentiment_percent(text, sia):
    output_dict =  sia.polarity_scores(text)
    
    return output_dict

def get_overall_sentiment(sentiments):
    total = len(sentiments)
    pos = len(sentiments[sentiments == "positive"])
    neg = len(sentiments[sentiments == "negative"])
    prop_pos = pos / total
    prop_neg = neg / total
    
    return prop_pos, prop_neg

def print_emoji_sent():
    with open('data/emoji.json', 'r') as f:
        emoji_json = json.load(f)
    emoji_dict = dict(emoji_json)
    
    ### Update Emoji Sentiments ###
    sorted_emoji_dict = sorted(emoji_dict.items(), key=lambda x:x[1], reverse=True)
    ### check emoji sentiment and adjust as needed ###
    for emoji_tuple in sorted_emoji_dict:
        sent = sia.polarity_scores(str(emoji_tuple[0]))
        print(emoji_tuple[0] + ": " + str(sent['compound']))
        
######################### nickname sentiment #########################
def get_sentiment_nm_tags(df, ent_key):
    
    # load entities 
    with open('data/entities_with_nicknames.json', 'r') as f:
        entities = json.load(f)
    entities = dict(entities)
    
    if df.player_ref[0] != entities[ent_key]['full_name']:
        raise ValueError("Dataframe and ent_key do not match!")
        
    negative_nicknames = entities[ent_key]['bad_names']
    positive_nicknames = entities[ent_key]['good_names']
    
    # update sent for pos/neg nicknames
    name_sent = []
    for i, row in df.iterrows():
        sent = 0
        for name in negative_nicknames:
            if name in row.unique_ref.split("/"):
                sent -= 1
        for name in positive_nicknames:
            if name in row.unique_ref.split("/"):
                sent += 1
                
        name_sent.append(sent)
    
    df['name_sent'] = name_sent

    return df



def get_sentiment_with_nicknames(df, ent_key, cutoff=0.05):
    
    # load entities 
    with open('data/entities_with_nicknames.json', 'r') as f:
        entities = json.load(f)
    entities = dict(entities)
    
    if df.player_ref[0] != entities[ent_key]['full_name']:
        raise ValueError("Dataframe and ent_key do not match!")
    
    # get sent w/o nicknames
    df['sentiment'] = df['body'].apply(predict_sentiment, cutoff=cutoff)
    
    negative_nicknames = entities[ent_key]['bad_names']
    positive_nicknames = entities[ent_key]['good_names']
    
    # update sent for pos/neg nicknames
    for i, row in df.iterrows():
        sent = 0
        for name in negative_nicknames:
            if name in row.unique_ref.split("/"):
                sent -= 1
        for name in positive_nicknames:
            if name in row.unique_ref.split("/"):
                sent += 1
        if sent < 0:
            df.loc[i, 'sentiment'] = 'negative'
        elif sent > 0:
            df.loc[i, 'sentiment'] = 'positive'
        else:
            continue
    return df

def sub_nicknames(df, ent_key):
    # load entities 
    with open('data/entities_with_nicknames.json', 'r') as f:
        entities = json.load(f)
    entities = dict(entities)
    
    if df.player_ref[0] != entities[ent_key]['full_name']:
        raise ValueError("Dataframe and ent_key do not match!")
        
    
    # substitute nicknames for name
    ent_name = df.player_ref[0]
    print(ent_name)

    body_list = []
    for i, row in df.iterrows():
        body = row.body
        names = row.unique_ref.split("/")
        sorted_names = sorted(names, key=len, reverse=True)
        for name in sorted_names:
            body = re.sub(r"\b{}\b".format(name), ent_name, body)
        body_list.append(body)
        
    body_list_pos = []
    for i, row in df.iterrows():
        body_pos = row.body_pos
        names = row.unique_ref.split("/")
        sorted_names = sorted(names, key=len, reverse=True)
        for name in sorted_names:
            body_pos = re.sub(r"\b{}\b".format(name), ent_name, body_pos)
        body_list_pos.append(body_pos)
        
        
    # any nickname w 2 spaces goes first!
    
    df["body_pr"] = body_list
    df['body_pos_pr'] = body_list_pos

    return df


def sub_all_nicknames(df):
    """
    Takes full post or comment df and substitutes all player entity refs to player ent name
    """
    # load entities 
    with open('data/entities_with_nicknames.json', 'r') as f:
        entities = json.load(f)
    entities = dict(entities)
    
    df.entities = df.entities.apply(str)
    # substitute nicknames for name
    
    body_list = []
    for i, row in df.iterrows():
        body = row.body
        names = row.entities.split(", ")
        for k in entities.keys():
            ent_name = entities[k]['full_name']
            if ent_name in names:
                nm = entities[k]['names']
                nm_sorted = sorted(nm, key=len, reverse=True)

                for nm in nm_sorted:
                    body = re.sub(r"\b{}\b".format(nm), ent_name, body)
        body_list.append(body)

        
    # any nickname w 2 spaces goes first!
    
    df["body_pr"] = body_list

    return df

######################### sentiment methods #########################
def sentiment_basic(player_df, sia, player_df_sent_col='resolved_final', nicknames=True):
    # filter out un-needed cols
    columns = ['id', 'datetime', 'player_ref', 'name_sent', player_df_sent_col]
    df = player_df[columns]
    df['unique_id'] = df.id + "_" + df.player_ref

    # get sentiment
    sents = []
    for i, row in df.iterrows():
        sent = predict_sentiment(row[player_df_sent_col], sia=sia)
        sents.append(sent)

    df['sentiment'] = sents

    if nicknames:
        new_sent = []
        for i, row in df.iterrows():
            if row.name_sent < 0:
                new_sent.append('negative')
            elif row.name_sent > 0:
                new_sent.append('positive')
            else:
                new_sent.append(row.sentiment)
        df['sentiment'] = new_sent

    return df

def sentence_tokenized_sentiment_basic(text, player_ref, nlp, sia):
    sentences = re.split(r"[!.?]", text)
    sentences_player = []
    for sentence in sentences:
        if player_ref in word_tokenize(str(sentence)):
            sentences_player.append(sentence)
    new_text = "".join(sentences_player)
    sentiment = predict_sentiment(new_text, sia=sia)
    
    return sentiment
    
    
def sentence_tokenized_sentiment_basic_df(player_df, nlp, sia, nicknames=True):
    player_ref = player_df.iloc[0].player_ref
    
    # filter out un-needed cols
    columns = ['id', 'datetime', 'player_ref', 'name_sent', 'resolved_final']
    df = player_df[columns]
    df['unique_id'] = df.id + "_" + df.player_ref
    
    sentiments = []
    for i, row in df.iterrows():
        sentiment = sentence_tokenized_sentiment_basic(
            text=row.resolved_final,
            player_ref=player_ref,
            nlp=nlp,
            sia=sia
        )
        sentiments.append(sentiment)
        
    df['sentiment'] = sentiments
    
    if nicknames:
        new_sent = []
        for i, row in df.iterrows():
            if row.name_sent < 0:
                new_sent.append('negative')
            elif row.name_sent > 0:
                new_sent.append('positive')
            else:
                new_sent.append(row.sentiment)
        df['sentiment'] = new_sent
        
    return df

def get_all_sentiment(posts, comments, sia):
    columns = ['id', 'datetime', 'body_pr']
    posts = posts[columns]
    comments = comments[columns]
    posts['pc'] = "p"
    comments['pc'] = "c"
    
    # combine posts and comments
    combined = pd.concat([posts, comments])
    combined = combined.sort_values('datetime').reset_index().drop(columns=['index'])
    
    # get overall sentiment for each post
    sentiments = []
    for i, row in combined.iterrows():
        sentiment = predict_sentiment(row.body_pr, sia=sia)
        sentiments.append(sentiment)
    combined['sentiment'] = sentiments
    
    return combined
    

######################### format df list into full sentiment df #########################
def save_df_list_sent(df_list, file_pattern):
    with open('data/entities_with_nicknames.json', 'r') as f:
        entities = json.load(f)
    entities = dict(entities)

    path = "data/sent_scores/"

    for i, k in enumerate(list(entities.keys())[:-1]):
        name = "{}".format(k) + "_sent_" + file_pattern
        file = path + name + ".csv"
        df_list[i].to_csv(file)
            
def concat_player_sents(ent_key, file_pattern):
    path = "data/sent_scores/"
    
    # load data
    post_file = path + ent_key + "_sent_posts_" + file_pattern + ".csv"
    post_sent = pd.read_csv(post_file, index_col=0, parse_dates=['datetime'])
    comment_file = path + ent_key + "_sent_comments_" + file_pattern + ".csv"
    comment_sent = pd.read_csv(comment_file, index_col=0, parse_dates=['datetime'])
    
    # create p/c identifier and concat
    post_sent['pc'] = "p"
    comment_sent['pc'] = "c"
    
    combined = pd.concat([post_sent, comment_sent])
    combined = combined.sort_values('datetime').reset_index().drop(columns=['index'])
    
    return combined

def combine_all_sents(file_pattern):
    with open('data/entities_with_nicknames.json', 'r') as f:
        entities = json.load(f)
    entities = dict(entities)
    
    file = "data/sent_scores/{}_sent_combined_" + file_pattern
    df_list_combined = [pd.read_csv(file.format(k), index_col=0, parse_dates=['datetime']) for k in list(entities.keys())[:-1]]
    
    combined_combined = pd.concat(df_list_combined)
    combined_combined = combined_combined.sort_values('datetime').reset_index().drop(columns=['index'])
    
    return combined_combined

def save_df_list_sent(df_list, file_pattern):
    with open('data/entities_with_nicknames.json', 'r') as f:
        entities = json.load(f)
    entities = dict(entities)

    path = "data/sent_scores/"

    index = 0
    for k in list(entities.keys())[:-1]:
        name = "{}".format(k) +"_sent_" + file_pattern
        file = path+name
        df_list[index].to_csv(file)
        index += 1
        
def get_entity_prop(df_player):
    df = df_player[['id', 'player_ref', 'ents_exp']]
    player_ref = df.player_ref[0]
    df['unique_id'] = df.id + "_" + df.player_ref
    
    ent_props = []
    for i, row in df.iterrows():
        text = row.ents_exp
        names = re.findall(r"'(\b\w+\b)':", text)
        counts = re.findall(r":\s(\d{1,2})", text)
        counts = [int(x) for x in counts]
        idx = names.index(player_ref)
        count = counts[idx]
        total = np.sum(counts)
        prop = count / total
        ent_props.append(prop)
    
    df_ent_prop = pd.Series(index=df.unique_id, data=ent_props)
    
    return df_ent_prop

def get_sentence_prop(df_player):
    df = df_player[['id', 'player_ref', 'ents_exp', 'resolved_final']]
    player_ref = df.player_ref[0]
    df['unique_id'] = df.id + "_" + df.player_ref
    df.resolved_final = df.resolved_final.apply(str)
    
    sentence_props = []
    for i, row in df.iterrows():
        sentences = re.split(r"[!.?]", row.resolved_final)
        total = len(sentences)
        count = 0
        for sentence in sentences:
            if player_ref in word_tokenize(str(sentence)):
                count += 1
        prop = count / total
        sentence_props.append(prop)
    
    df_sentence_prop = pd.Series(data=sentence_props, index=df.unique_id)
    
    return df_sentence_prop


######################### sampling and testing #########################

def get_single_ent_post_sample():

    posts = pd.read_csv("data/posts_clean_extended_final.csv", index_col=0, parse_dates=['datetime'])
    posts.body = posts.body.apply(str)
    
    random.seed(18)
    single_ent_posts = posts[posts['num_entities'] == 1]
    single_ent_index = single_ent_posts.index
    sample_idx = random.sample(set(single_ent_index), 200)
    
    # create sample_posts
    sample_posts = posts.loc[sample].reset_index()
    
    sent_dict = {
    0: 'neutral',
    1: 'negative',
    2: 'positive'
    }
    # manually labeled sentiments
    sample_sentiments = [
        0, 0, 0, 0, 2, 2, 2, 0, 0, 0,
        0, 0, 1, 0, 1, 0, 0, 2, 2, 0,
        2, 2, 1, 0, 0, 0, 1, 0, 1, 0,
        0, 2, 1, 0, 2, 2, 0, 2, 0, 0, 
        1, 0, 2, 1, 0, 2, 0, 1, 0, 1,
        2, 0, 2, 0, 0, 0, 2, 2, 2, 0,
        0, 2, 1, 1, 2, 0, 0, 0, 2, 0,
        0, 1, 0, 1, 1, 1, 2, 1, 1, 0,
        2, 0, 1, 0, 0, 2, 2, 2, 2, 1,
        0, 2, 2, 1, 0, 0, 2, 0, 2, 0,
        0, 0, 2, 2, 2, 0, 2, 0, 1, 1,
        0, 1, 1, 0, 0, 2, 0, 2, 0, 0,
        0, 2, 1, 2, 1, 2, 0, 0, 2, 2,
        0, 1, 2, 0, 1, 0, 0, 2, 0, 2,
        2, 2, 0, 0, 2, 2, 2, 2, 1, 0,
        2, 0, 0, 2, 2, 0, 0, 2, 1, 0,
        0, 1, 2, 2, 2, 0, 2, 2, 2, 1,
        0, 1, 1, 1, 1, 0, 0, 0, 2, 0,
        0, 1, 2, 1, 0, 0, 0, 1, 0, 0,
        2, 2, 0, 2, 1, 2, 1, 2, 2, 1
    ]
    
    sample_sentiment_words = [sent_dict[x] for x in sample_sentiments]
    sample_posts['sentiment_labels'] = sample_sentiment_words
    
    return sample_posts


def get_single_ent_comment_sample():
    comments = pd.read_csv("data/comments_clean_extended_final.csv", index_col=0, parse_dates=['datetime'])
    comments.body = comments.body.apply(str)
    
    
    random.seed(18)
    single_ent_tl_comments = comments[(comments['num_entities'] == 1) & (comments['top_level'] == 1) & (comments['tid_num_entities'] == 0)]
    single_ent_index = list(single_ent_tl_comments.index)
    sample_idx = random.sample(set(single_ent_index), 300)

    # create sample commments
    sample_comments = comments.loc[sample_idx].reset_index()
    
    sent_dict = {
        0: 'neutral',
        1: 'negative',
        2: 'positive'
    }
    # manually labeled sentiments
    sample_sentiments = [
        2, 0, 0, 2, 1, 0, 2, 2, 2, 2,
        1, 1, 0, 0, 0, 1, 1, 2, 2, 0,
        2, 1, 2, 1, 0, 2, 2, 0, 0, 0,
        1, 2, 2, 1, 2, 1, 1, 0, 0, 0,
        0, 1, 1, 1, 0, 1, 1, 0, 1, 1,
        1, 0, 0, 0, 0, 0, 0, 2, 1, 2,
        1, 1, 0, 2, 0, 2, 0, 2, 0, 2,
        0, 1, 0, 0, 0, 2, 0, 2, 0, 2, 
        0, 1, 0, 2, 0, 0, 0, 1, 1, 2,
        2, 1, 0, 0, 0, 1, 0, 2, 2, 0,
        1, 1, 2, 1, 1, 1, 2, 2, 2, 0,
        0, 1, 2, 1, 0, 0, 1, 2, 1, 1, # 120
        0, 0, 1, 2, 0, 0, 1, 2, 2, 1, # 130
        1, 1, 2, 0, 0, 0, 1, 2, 1, 0, 
        0, 1, 0, 0, 1, 0, 1, 0, 1, 0, # 150
        0, 1, 0, 2, 2, 1, 2, 0, 0, 0,
        0, 1, 1, 0, 1, 0, 1, 0, 2, 0,
        1, 2, 1, 1, 1, 1, 1, 1, 1, 0, #180
        0, 0, 0, 2, 1, 1, 0, 1, 1, 2, #190
        1, 1, 2, 1, 2, 2, 1, 1, 2, 0, #200
        0, 1, 2, 0, 1, 2, 1, 2, 0, 0, #210
        0, 2, 0, 0, 1, 0, 0, 0, 1, 0, #220
        0, 1, 0, 0, 2, 0, 0, 2, 2, 2, #230
        1, 0, 2, 1, 1, 2, 2, 2, 0, 0, #240
        2, 1, 0, 1, 0, 2, 2, 0, 1, 0,
        0, 0, 0, 0, 0, 2, 2, 2, 0, 1, #260
        2, 2, 1, 1, 1, 1, 2, 1, 1, 2,
        1, 0, 0, 1, 0, 0, 2, 1, 1, 1,
        1, 0, 1, 1, 0, 0, 0, 2, 1, 0,
        1, 1, 0, 2, 0, 0, 0, 1, 0, 0
    ]

    sample_sentiment_words = [sent_dict[x] for x in sample_sentiments]
    sample_comments['sentiment_labels'] = sample_sentiment_words

    return sample_comments


def final_sample():
    all_sents = [pd.read_csv(path+n, index_col=0, parse_dates=['datetime']) for n in names]
    random.seed(18)
    df = all_sents[0]
    df = df.set_index('unique_id')
    sampleidx = random.sample(list(df.index), 500)

    # create sample_posts
    sample = df.loc[sampleidx].reset_index()
    
    sample_sentiments=[
        2, 2, 0, 2, 0, 0, 1, 2, 0, 2, #10
        1, 0, 1, 0, 1, 1, 0, 2, 1, 2, #20
        0, 0, 1, 1, 0, 0, 0, 0, 1, 0, #30
        0, 0, 0, 2, 0, 2, 0, 1, 2, 1, #40
        1, 2, 1, 1, 2, 2, 0, 0, 1, 0, #50
        2, 1, 1, 2, 2, 0, 2, 0, 1, 2, #60
        0, 0, 0, 1, 0, 0, 0, 0, 0, 2, #70
        1, 2, 2, 0, 2, 0, 2, 0, 0, 1, #80
        0, 2, 0, 1, 1, 0, 1, 0, 1, 0, #90
        1, 0, 2, 2, 2, 1, 0, 1, 0, 2, #100
        0, 2, 0, 1, 0, 0, 0, 0, 0, 0, #110
        2, 2, 0, 1, 0, 1, 0, 2, 0, 0, #120
        1, 0, 1, 0, 1, 1, 2, 0, 1, 2, #130
        0, 0, 2, 1, 0, 1, 2, 2, 1, 0, #140
        1, 2, 2, 0, 0, 0, 1, 0, 1, 0, #150
        2, 2, 0, 2, 0, 0, 1, 0, 0, 1, #160
        2, 2, 0, 1, 2, 2, 2, 1, 0, 0, #170
        0, 2, 1, 2, 0, 1, 0, 1, 0, 2, #180
        2, 0, 1, 1, 0, 0, 0, 0, 0, 0, #190
        0, 1, 1, 0, 2, 2, 0, 0, 1, 1, #200
        0, 2, 0, 0, 0, 0, 1, 1, 0, 2, #210
        0, 0, 0, 0, 0, 0, 2, 0, 0, 1, #220
        2, 0, 2, 0, 1, 2, 2, 0, 0, 0, #230
        1, 2, 0, 0, 0, 2, 0, 2, 2, 2, #240
        2, 1, 0, 0, 2, 1, 2, 1, 1, 1, #250
        1, 2, 2, 0, 1, 0, 0, 1, 0, 1, #260
        0, 0, 2, 2, 0, 1, 0, 0, 2, 1, #270
        2, 1, 1, 2, 1, 2, 1, 2, 0, 0, #280
        0, 0, 1, 0, 1, 0, 0, 2, 2, 0, #290
        1, 0, 0, 2, 1, 2, 1, 1, 1, 0, #300
        2, 2, 0, 2, 2, 2, 0, 2, 2, 2, #310
        0, 0, 1, 1, 0, 0, 2, 1, 0, 2, #320
        0, 0, 2, 0, 1, 0, 0, 0, 1, 1, #330
        2, 2, 0, 0, 1, 1, 0, 1, 2, 0, #340
        0, 1, 0, 0, 1, 1, 2, 2, 2, 2, #350
        0, 1, 1, 0, 0, 0, 2, 1, 1, 2, #360
        0, 2, 2, 0, 1, 1, 0, 1, 1, 1, #370
        1, 0, 2, 1, 1, 1, 0, 0, 1, 2, #380
        2, 1, 0, 1, 1, 0, 0, 0, 2, 2, #390
        1, 1, 1, 2, 2, 1, 2, 2, 2, 2, #400
        2, 0, 2, 0, 2, 0, 2, 0, 1, 0, #410
        0, 0, 1, 2, 2, 0, 0, 1, 0, 1, #420
        2, 1, 1, 1, 2, 1, 0, 2, 1, 0, #430
        1, 2, 2, 2, 1, 1, 1, 0, 0, 2, #440
        0, 0, 0, 1, 1, 2, 2, 2, 0, 0, #450
        0, 0, 0, 2, 0, 2, 2, 0, 0, 0, #460
        2, 1, 1, 2, 1, 1, 2, 1, 0, 2, #470
        2, 2, 0, 2, 1, 0, 2, 1, 0, 2, #480
        0, 2, 2, 1, 2, 0, 0, 0, 2, 0, #490
        0, 0, 1, 1, 2, 1, 0, 1, 2, 2, #500

    ]
    sent_dict = {
            0: 'neutral',
            1: 'negative',
            2: 'positive'
        }
    sample_labs = [sent_dict[x] for x in sample_sentiments]
    sample = sample.drop(columns=['sentiment'])
    sample['sentiment_labels'] = sample_labs
    
    return sample

def get_post_sent_score_dict(df_list_posts, file_name):
    with open('data/entities_with_nicknames.json', 'r') as f:
        entities = json.load(f)
        entities = dict(entities)
        
    index = 0
    for k in entities.keys():
        print(k)
        df_list_posts[index] = get_sentiment_with_nicknames(df_list_posts[index], k)
        print(df_list_posts[index].loc[0].player_ref)
        index += 1
        
    df_list_posts_scored = {}
    for df in df_list_posts:
        prop_pos, prop_neg = get_overall_sentiment(df['sentiment'])
        score = prop_pos - prop_neg
        df_list_posts_scored[df.player_ref[0]] = score

    # save dict    
    with open("data/sent_dicts/sa_posts_{}.json".format(file_name), "w") as f:
        json_dict = json.dumps(df_list_posts_scored)
        f.write(json_dict) 
        
    df_list_posts_w_sent = df_list_posts
    
    return df_list_posts_w_sent, df_list_posts_scored
    

def get_comment_sent_score_dict(df_list_comments, file_name): # this doesnt use names?
    with open('data/entities_with_nicknames.json', 'r') as f:
        entities = json.load(f)
        entities = dict(entities)
        
    index = 0
    for k in entities.keys():
        print(k)
        df_list_comments[index] = get_sentiment_with_nicknames(df_list_comments[index], k)
        print(df_list_comments[index].loc[0].player_ref)
        index += 1
        
    
    df_list_comment_scored = {}
    for df in df_list_comments:
        prop_pos, prop_neg = get_overall_sentiment(df['sentiment'])
        score = prop_pos - prop_neg
        df_list_comment_scored[df.player_ref[0]] = score

    # save dict    
    with open("data/sent_dicts/sa_comments_nicknames{}.json".format(file_name), "w") as f:
        json_dict = json.dumps(df_list_comment_scored)
        f.write(json_dict) 
    
    df_list_comments_w_sent = df_list_comments
    
    return df_list_comments_w_sent, df_list_comment_scored

def sent_rmse(true, preds):
    sent_map = {
        'negative':-0.5,
        'neutral':0.0,
        'positive':0.5
    }
    
    index = range(true.shape[0])
    mses = []
    for i in index:
        mse = sent_map[true[i]] - sent_map[preds[i]]
        mses.append(mse ** 2)
    
    rmse = np.mean(mse)
    
    return mses

def compare_sentiments(sample, cols):
    reports = []
    for col in cols:
        report = classification_report(sample_ind.sentiment_labels,
                                       sample_ind[col],
                                       digits=3,
                                       output_dict=True)
        reports.append(report)
    rmses = []
    for col in cols:
        rmse = np.mean(lsa.sent_rmse(sample_ind.sentiment_labels,
                           sample_ind[col]))
        rmses.append(rmse)
    
    res = {}
    for i, col in enumerate(cols):
        res[col] = reports[i]
        res[col]['rmse'] = rmses[i]
        
    return res
    


#comments2.body = comments2.body.apply(tc.sub_emojis, subbed_emoji="🤦‍♂️", sub_emoji="🤦🏻‍♂️")
#comments2.body = comments2.body.apply(tc.sub_emojis, subbed_emoji="❤️", sub_emoji="💜")
#comments2.body = comments2.body.apply(tc.sub_emojis, subbed_emoji="❄️", sub_emoji="🧊")
#comments2.body = comments2.body.apply(tc.sub_emojis, subbed_emoji="🗑", sub_emoji="🚮")
















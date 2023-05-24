**Entity-Level-Sentiment-Analysis-with-Reddit-Data**

This tracks sentiment analysis for individual players on the Los Angeles Lakers team over the course of the 2022-23 season. To accomplish this, I utilized the PushShift API to gather all post and comment data from the Lakers subreddit starting from the beginning of the season until the final play-in game before the playoffs. Player statistics were scraped using the NBA API. 

Basic text cleaning including lowercasing, removal of special characters, and gif and hyperlink elimination were applied to the text data. Entity recognition was implemented using a combination of domain knowledge and regex pattern trial-and-error. Part of speech resolving was utilized to solve text that contained words with double meaning, while co-reference resolving was used to extract additional entity mentions. 

The vaderSentiment library was used for the task of unsupervised sentiment analysis. To improve the model various adjustments were made to the base lexicon including: emoji adjustments, basketball-related lexicon adjustments, nickname adjustments and sentence tokenization utilization. 


Files and Uses
reddit_requests.py: reddit data scraping 
nba_scrape.py: nba stats scraping
text_cleaning.py: general cleaning, entity recognition
lakers_sentiment_analysis.py: Vader sia and spaCy nlp pipeline initiations; coreference resolving; basic sentiment
sentiment_stats.py: further sentiment stats
lakers_stats.py: contains TeamDate and PlayerDate classes used for player statistics and sentiment


\textbf{Entity-Level-Sentiment-Analysis-with-Reddit-Data}

This project aims to track sentiment analysis for individual players on the Los Angeles Lakers team over the course of the 2022-23 season. To accomplish this, I utilized the reddit API to gather all post and comment data from the Lakers subreddit starting from the beginning of the season until the final play-in game before the playoffs.

To identify individual players on the team, I will be using the spaCy library for entity recognition. After isolating player names, I will use the vaderSentiment library to determine the trending sentiment for each player at different periods in time.

My ultimate goal is to develop an application that allows users to compare sentiment trends of different players over time. To enhance the user experience, I will also incorporate player statistics so that users can compare a player’s trending statistical performance with their trending sentiment.
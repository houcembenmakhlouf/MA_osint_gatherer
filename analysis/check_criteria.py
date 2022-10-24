import sqlite3
import pandas as pd
from tqdm import tqdm
import pandas as pd


cnx = sqlite3.connect("data/mydatabase.db")

# consider only tweets with hashtags(lastest number of tweet was 150thousand)

tweets_df = pd.read_sql_query(
    "SELECT tweetId FROM searchTweets WHERE tweetHashtags!='' AND tweetImage!='NULL'",
    cnx,
)

# tweets_df_list = tweets_df["tweetId"].tolist()

replies_df = pd.read_sql_query("SELECT referenceTweetId FROM repliesToTweet", cnx)

quotes_df = pd.read_sql_query("SELECT referenceTweetId FROM quotesToTweet", cnx)

# replies
replies_hashtag_cri = replies_df.referenceTweetId.isin(tweets_df.tweetId)
replies_hashtag_cri = replies_hashtag_cri.tolist()

count_rep = sum(replies_hashtag_cri)
print(count_rep)

# quotes
quotes_hashtag_cri = quotes_df.referenceTweetId.isin(tweets_df.tweetId)
quotes_hashtag_cri = quotes_hashtag_cri.tolist()

count_quo = sum(quotes_hashtag_cri)
print(count_quo)

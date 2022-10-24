from .dataCollection import (
    add_profile,
    add_followers,
    add_tweets,
    # add_likers,
    add_replies_to_tweet,
    # add_retweeters,
    add_quotes_to_tweet,
)


import csv
from rq import Queue
from redis import Redis
from rq_scheduler import Scheduler
from datetime import datetime

redis_conn = Redis()
scheduler = Scheduler(connection=Redis())


queue_profile = Queue("profile", connection=redis_conn)
queue_follower = Queue("follower", connection=redis_conn)
queue_tweet = Queue("tweet", connection=redis_conn)
queue_liker = Queue("liker", connection=redis_conn)
queue_retweeter = Queue("retweeter", connection=redis_conn)
queue_reply = Queue("reply", connection=redis_conn)
queue_quote = Queue("quote", connection=redis_conn)


def update_tweets(user_name):
    queue_tweet.enqueue(get_tweets_wrapper, user_name)


def profile(user_name):
    queue_profile.enqueue(get_profile_wrapper, user_name)
    queue_tweet.enqueue(get_tweets_wrapper, user_name)


def get_profile_wrapper(user_name):
    user_ids = add_profile(user_name)
    try:
        for user_id in user_ids:
            queue_follower.enqueue(add_followers, user_id)
    except:
        pass


def get_tweets_wrapper(user_name):
    tweet_ids_counts = add_tweets(user_name)
    for tweet in tweet_ids_counts:
        # queue_liker.enqueue(add_likers, tweet)
        # queue_retweeter.enqueue(add_retweeters, tweet)
        if tweet["replyCount"] > 0:
            queue_reply.enqueue(add_replies_to_tweet, tweet["tweetId"])
        if tweet["quoteCount"] > 0:
            queue_quote.enqueue(add_quotes_to_tweet, tweet["tweetId"])


# def get_names_update():
#     with open("german_newspapers2.csv") as csvfile:
#         spamreader = csv.reader(csvfile, delimiter=",")
#         data = list(spamreader)
#         for row in data[1:]:
#             update_tweets(row[1])


# def get_names_first():
#     with open("german_newspapers2.csv") as csvfile:
#         spamreader = csv.reader(csvfile, delimiter=",")
#         data = list(spamreader)
#         for row in data[1:]:
#             profile(row[1])

from ast import Continue
import datetime
import time
import datetime
import re

import dataset
import pandas as pd
import snscrape.modules.twitter as sntwitter
import tweepy
from twarc import Twarc2

from . import credentials
from snscrape.modules.twitter import (
    TwitterSearchScraper,
    _CLIGuestTokenManager,
)
token_manager = _CLIGuestTokenManager()
db = dataset.connect("sqlite:///mydatabase.db")
user_names = ["derspiegel", "zeitonline"]


def get_tweepy_client():
    return tweepy.Client(
        bearer_token=credentials.BEARER_TOKEN,
        consumer_key=credentials.API_KEY,
        consumer_secret=credentials.API_KEY_SECRET,
        access_token=credentials.ACCESS_TOKEN,
        access_token_secret=credentials.ACCESS_TOKEN_SECRET,
    )


client = get_tweepy_client()
twarc_client = Twarc2(bearer_token=credentials.BEARER_TOKEN)


def get_user_profile(user_name):
    try:
        user = client.get_user(
            username=user_name,
            user_fields="id,name,username,created_at,description,location,public_metrics,verified,url,withheld",
        )
        return {
            "userName": user_name,
            "userId": user.data.id,
            "bio": user.data.description,
            "location": user.data.location,
            "followersCount": user.data.public_metrics["followers_count"],
        }
    except AttributeError:
        pass


def search_tweets(begin_date, user_name):

    tweet_tab = []
    for i, tweet in enumerate(
        sntwitter.TwitterSearchScraper(
            f"since:{begin_date} from:{user_name}"
        ).get_items()
    ):
        obj = {
            "tweetId": tweet.id,
            "userId": tweet.user.id,
            "name": tweet.user.username,
            "content": tweet.content,
            "replyCount": tweet.replyCount,
            "retweetCount": tweet.retweetCount,
            "likeCount": tweet.likeCount,
            "quoteCount": tweet.quoteCount,
            "date": datetime.datetime.strptime(
                str(tweet.date)[:-6], "%Y-%m-%d %H:%M:%S"
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "lang": tweet.lang,
            "tweetHashtags": ",".join(re.findall(r"#(\w+)", tweet.content)),

        }
        if tweet.media != None:
            for elmt in tweet.media:
                try:
                    if elmt.fullUrl:
                        obj["tweetImage"] = elmt.fullUrl
                except:
                    continue
 

        
        # obj["tweetHashtags"] = re.findall(r"#(\w+)", tweet.content)
        # obj["outlinks"] = tweet.outlinks
        # obj["media"] = tweet.media

        tweet_tab.append(obj)
    return tweet_tab


def get_tweet_replies(tweet_id):
    replies_to_tweet_tab = []
    for k, tweet in enumerate(
        sntwitter.TwitterTweetScraper(
            tweetId=tweet_id, mode=sntwitter.TwitterTweetScraperMode.SCROLL
        ).get_items()
    ):
        if k == 0:
            continue
        obj = {
            "referenceTweetId": tweet_id,
            "TweetId": tweet.id,
            "userId": tweet.user.id,
            "name": tweet.user.username,
            "content": tweet.content,
            "replyCount": tweet.replyCount,
            "retweetCount": tweet.retweetCount,
            "likeCount": tweet.likeCount,
            "quoteCount": tweet.quoteCount,
            "date": datetime.datetime.strptime(
                str(tweet.date)[:-6], "%Y-%m-%d %H:%M:%S"
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "lang": tweet.lang,
            "tweetHashtags": ",".join(re.findall(r"#(\w+)", tweet.content)),
        }
        if tweet.media != None:
            print("true")
            for elmt in tweet.media:
                try:
                    if elmt.fullUrl:
                        obj["tweetImage"] = elmt.fullUrl
                except:
                    continue
        replies_to_tweet_tab.append(obj)
    return replies_to_tweet_tab


def get_tweet_quotes(tweet_id):
    quotes_to_tweet_tab = []
    for tweet in TwitterSearchScraper(
        f"url:{tweet_id} -is:retweet", guestTokenManager=token_manager
    ).get_items():

        obj = {
            "referenceTweetId": tweet_id,
            "TweetId": tweet.id,
            "userId": tweet.user.id,
            "name": tweet.user.username,
            "content": tweet.content,
            "replyCount": tweet.replyCount,
            "retweetCount": tweet.retweetCount,
            "likeCount": tweet.likeCount,
            "quoteCount": tweet.quoteCount,
            "date": datetime.datetime.strptime(
                str(tweet.date)[:-6], "%Y-%m-%d %H:%M:%S"
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "lang": tweet.lang,
            "tweetHashtags": ",".join(re.findall(r"#(\w+)", tweet.content)),
            
        }
        if tweet.media != None:
            print("true")
            for elmt in tweet.media:
                try:
                    if elmt.fullUrl:
                        obj["tweetImage"] = elmt.fullUrl
                except:
                    continue
        quotes_to_tweet_tab.append(obj)
        print(obj)

    return quotes_to_tweet_tab


# database stuff


def add_quotes_to_tweet(tweet_id):
    table = db["quotesToTweet"]
    print(table)
    while True:
        try:
            quotes_of_tweet = get_tweet_quotes(tweet_id)
            print(quotes_of_tweet)
        except tweepy.errors.TooManyRequests:
            print("sleep for 15min")
            time.sleep(15 * 60)
            continue
        except TypeError:
            continue
        break
    if quotes_of_tweet:
        for quote in quotes_of_tweet:
            if table.find_one(content=quote["content"]) is None:
                table.insert(quote)
                print(
                    str(quote["TweetId"])
                    + " of user "
                    + str(quote["userId"])
                    + " has been added"
                )
                db.commit()
            else:
                table.update(quote, ["id"])
                print(
                    str(quote["TweetId"])
                    + " of user "
                    + str(quote["userId"])
                    + " has been updated"
                )


def add_replies_to_tweet(tweet_id):
    table = db["repliesToTweet"]
    print(table)
    while True:
        try:
            replies_to_tweet = get_tweet_replies(tweet_id)
            print(replies_to_tweet)
        except tweepy.errors.TooManyRequests:
            print("sleep for 15min")
            time.sleep(15 * 60)
            continue
        except TypeError:
            continue
        break
    if replies_to_tweet:
        for reply in replies_to_tweet:
            if table.find_one(content=reply["content"]) is None:
                table.insert(reply)
                print(
                    str(reply["TweetId"])
                    + " of user "
                    + str(reply["userId"])
                    + " has been added"
                )
            else:
                table.update(reply, ["id"])
                print(
                    str(reply["TweetId"])
                    + " of user "
                    + str(reply["userId"])
                    + " has been updated"
                )


def add_retweeters(tweet_id):
    table = db["retweetUsers"]
    print(table)
    while True:
        try:
            retweeters = client.get_retweeters(tweet_id).data
        except tweepy.errors.TooManyRequests:
            print("sleep for 15min")
            time.sleep(15 * 60)
            continue
        except TypeError:
            continue
        break
    if retweeters:
        for retweeter in retweeters:
            print("bro", retweeter)
            if table.find_one(userId=retweeter["id"]) is None:
                user = {
                    "tweetId": tweet_id,
                    "userId": retweeter["id"],
                    "name": retweeter["name"],
                    "username": retweeter["username"],
                }
                table.insert(user)
                print(retweeter["id"], "has been added")
                db.commit()
            else:
                print(retweeter["id"], "already exits")


def add_likers(tweet_id):
    table = db["likingUsers"]
    print(table)
    while True:
        try:
            liking_users = client.get_liking_users(tweet_id).data
        except tweepy.errors.TooManyRequests:
            print("sleep for 15min")
            time.sleep(15 * 60)
            continue
        except TypeError:
            continue
        break
    if liking_users:
        print(liking_users)
        for liker in liking_users:
            if table.find_one(userId=liker["id"], tweetId=tweet_id) is None:
                user = {
                    "tweetId": tweet_id,
                    "userId": liker["id"],
                    "name": liker["name"],
                    "username": liker["username"],
                }
                print("rg", user)
                table.insert(user)
                print(liker["id"], "has been added")
                db.commit()
            else:
                print(liker["id"], "already exits")


def add_tweets(user_name):
    tableTweets = db["searchTweets"]
    print(tableTweets)
    # tableDescription = db["profileDescription"]
    # idOfUser = tableDescription.find_one(username=user_name)["userId"]
    if tableTweets.find_one(name=user_name) is None:
        beginnDate = "2022-02-01"
        print(beginnDate)
    else:
        beginnDate = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime(
            "%Y-%m-%d"
        )
        print(beginnDate)
    tweet_tab = search_tweets(beginnDate, user_name)
    addTweetsToDb = []
    TreatedTweets = []
    updateTweetsToDb = []
    for tweet in tweet_tab:
        if tableTweets.find_one(tweetId=tweet["tweetId"]) is None:
            addTweetsToDb.append(tweet)
            print(str(tweet["tweetId"]) + " will be added to DB")
            # new ids to work with later
        else:
            updateTweetsToDb.append(tweet)
            print(str(tweet["tweetId"]) + " will be updated in DB")
            # old ids to work with later

        TreatedTweets.append(
            {
                "tweetId": tweet["tweetId"],
                "replyCount": tweet["replyCount"],
                "quoteCount": tweet["quoteCount"],
            }
        )
    if len(addTweetsToDb) > 0:
        tableTweets.insert_many(addTweetsToDb)
        db.commit()
        print("new tweets has been added to DB")
    if len(updateTweetsToDb):
        tableTweets.update_many(updateTweetsToDb, ["tweetId"])
        print("old tweets has been updated in DB")
    return TreatedTweets


def add_followers(user_id):
    table = db["searchFollowers"]
    print(user_id)
    print(table)
    search_results = twarc_client.followers(user_id, max_results=1000)
    for result in search_results:
        for follower in result["data"]:
            if table.find_one(followerId=follower["id"]):
                print(follower["id"], "already exits")
                continue
            obj = {
                "followerId": follower["id"],
                "description": follower["description"],
                "userId": user_id,
                "username": follower["username"],
                "followers_count": follower["public_metrics"]["followers_count"],
                "following_count": follower["public_metrics"]["following_count"],
                "tweet_count": follower["public_metrics"]["tweet_count"],
                "created_at": datetime.datetime.strptime(
                    follower["created_at"][:-5], "%Y-%m-%dT%H:%M:%S"
                ).strftime("%Y-%m-%d %H:%M:%S"),
            }
            table.insert(obj)
            print("Follower", follower["id"], "has been added")
            db.commit()


def add_profile(user_name):
    profile = get_user_profile(user_name)
    print(profile)
    table = db["profileDescription"]
    try:
        if table.find_one(userId=profile["userId"]) is not None:
            table.update(profile, ["userId"])
            print(str(profile["userId"]) + " profile's was updated in DB")
        else:
            table.insert(profile)
            print(str(profile["userId"]) + " profile's was added DB")
        return [profile["userId"]]

    except TypeError:
        pass

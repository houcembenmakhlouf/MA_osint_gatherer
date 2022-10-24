from rq import Queue
from redis import Redis

redis_conn = Redis()

queue_profile = Queue("profile", connection=redis_conn)
queue_follower = Queue("follower", connection=redis_conn)
queue_tweet = Queue("tweet", connection=redis_conn)
# queue_liker = Queue("liker", connection=redis_conn)
# queue_retweeter = Queue("retweeter", connection=redis_conn)
queue_reply = Queue("reply", connection=redis_conn)
queue_quote = Queue("quote", connection=redis_conn)
queue_failed = Queue("failed", connection=redis_conn)

print(len(queue_quote))
print(len(queue_reply))
print(len(queue_follower))
print(len(queue_tweet))
print(len(queue_profile))

queue_profile.empty()
queue_follower.empty()
queue_reply.empty()
queue_quote.empty()
queue_tweet.empty()
queue_failed.empty()

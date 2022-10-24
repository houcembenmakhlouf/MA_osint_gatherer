import csv
from osint_gatherer.tasks.twitter import (
    profile,
    update_tweets,
)


with open("data/german_newspapers2.csv", "r") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=",")
    data = list(spamreader)
    for row in data[1:]:
        # update_tweets(row[1])
        print(row)
        profile(row[1])

import dataset
import re

db = dataset.connect("sqlite:///mydatabase.db")
with open("data.txt", "w") as f:
    for tweet in db["searchTweets"]:
        x = tweet["content"].replace("\n", "")
        y = re.sub(r"http\S+", "", x)
        y = re.sub(r",", "", y)
        y = y.rstrip()
        z = tweet["lang"]
        f.write(y + "," + z)
        f.write("\n")

import dataset
import sqlite3
from tqdm import tqdm
# check tweet languages
db = dataset.connect("sqlite:///mydatabase.db")

de = 0
en = 0
fr =0
und = 0
other=0
mylist=[]

for tweet in db["quotesToTweet"]:
    if tweet["lang"] == "de":
        de = de + 1
    if tweet["lang"] == "en":
        en = en + 1
    if tweet["lang"] == "fr":
        fr = fr + 1
    if tweet["lang"] == "und":
        und = und + 1
    if tweet["lang"] not in ["de","en", "fr"]:
        other = other + 1


print(de)
print(en)
print(fr)
print(und)
print(other)

print((de*100)/584870)
print((en*100)/584870)
print((fr*100)/584870)
print((und*100)/584870)
print((other*100)/584870)


# other method with sqlite3 and tdqm for progress meters
# conn = sqlite3.connect("mydatabase.db")
# c = conn.cursor()
# c.execute("DROP TABLE quotesToTweet")
# ['tr', 'ca', 'pl', 'eu', 'ja', 'und', 'lt', 'hu', 'in', 'ru', 'is', 'sl', 'uk', 'no', 'it', 'ht', 'nl', 'ro', 'vi', 'pt', 'fi', 'sv', 'da', 'cs', 'cy', 'zh', 'tl', 'es', 'et']


# check lang for repliesa and quotes
# db = dataset.connect("sqlite:///mydatabase.db")

# de = 0
# en = 0
# fr =0
# es = 0
# other=0
# mylist=[]
# for elt in tqdm(db["searchTweets"]):
#     if elt["lang"] == "de":
#         ref = elt["tweetId"]
#         element_tosearch_in = db["repliesToTweet"].find(referenceTweetId=ref)
#         for i in element_tosearch_in:
#             if i["lang"] == "de":
#                 de = de + 1
#             if i["lang"] == "en":
#                 en = en + 1
#             if i["lang"] == "fr":
#                 fr = fr + 1
#             if i["lang"] == "es":
#                 es = es + 1
#             if i["lang"] not in ["de","en", "fr"]:
#                 other = other + 1


# print(de)
# print(en)
# print(fr)
# print(es)
# print(other)

# print((de*100)/1042456)
# print((en*100)/1042456)
# print((fr*100)/1042456)
# print((es*100)/1042456)
# print((other*100)/1042456)



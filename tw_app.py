from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')

user_id = "19828717"
tweet__post = "Hello World 2"


def tweetpost (userid, tweepost):
    db = client.tweets
    tweet = db.tweets.insert_one(
        {"user": userid,
        "tweet_post": tweepost,
        "rt": 0,
        "reply": 0,
        "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
     }
    )
    return

# tweetpost(user_id, tweet__post)


def getusertimeline(userid):
    db = client.tweets
    cursor = db.tweets.find({"user": userid })
    for document in cursor:
        print(document)
    return

# getusertimeline(user_id)

def addfollowing(userid, userfollower):
    db = client.following
    result = db.tweets.updateone(
        {"user": userid },


    )


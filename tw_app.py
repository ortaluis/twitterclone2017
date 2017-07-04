from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')

user_id = "19828717"
userfoll1 = "19828718"
userfoll2 = "19828719"

tweet__post = "Hello World 4"


def tweetpost (userid, tweepost):
    if len(tweepost) < 140:
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
    else:
        print ("Tweet should be not longer than 140 characters")


#tweetpost(user_id, tweet__post)


def getusertimeline(userid):
    db = client.tweets
    cursor = db.tweets.find({"user": userid}).sort("date", -1)
    for document in cursor:
        print(document)
    return

#getusertimeline(user_id)

def newuser (userid):
    db0 = client.followers
    followers = db0.followers.insert_one(
        {
            "user": userid,
            "followers": [],
        }
    )
    db1 = client.followings
    followings = db1.followings.insert_one(
        {
            "user": userid,
            "followings": [],
        }
    )
    db2 = client.likes
    likes = db2.likes.insert_one(
        {
            "user": userid,
            "likes": [],
        }
    )
    return

#newuser(user_id)


def addfollower(userid, useridfollower):
    db = client.followers
    add = db.followers.find_one_and_update({'user': userid}, {'$push': {'followers': {
            "follower": useridfollower,
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }}})
    return


def addfollowing(userid, useridfollowing):
    db = client.followings
    add = db.followings.find_one_and_update({'user': userid}, {'$push': {'followings': {
        "following": useridfollowing,
        "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }}})
    return


def addlike(userid, objidtweet):
    db = client.likes
    add = db.likes.find_one_and_update({'user': userid}, {'$push': {'likes': {"tweetliked": objidtweet}}})
    return

#addfollower(user_id, userfoll1)
#addfollower(user_id, userfoll2)



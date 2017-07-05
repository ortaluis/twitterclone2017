from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')

user_id = "19828717"
userfoll1 = "19828718"
userfoll2 = "19828719"
id_tweet = "595ac1c65452123a2cbb5596"
tweet__post = "Hello World 5"


def tweetpost(userid, tweepost):
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


def deletedtweet(userid, idtweet):
    db = client.tweets
    add = db.tweets.find_one_and_delete({'_id': ObjectId(idtweet), "user": userid})
    print ("Tweet deleted")
    return


def getusertimeline(userid):
    db = client.tweets
    cursor = db.tweets.find({"user": userid}).sort("date", -1)
    for document in cursor:
        print(document)
    return


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


def delfollowing(userid, useridfoll):
    db = client.followings
    remove = db.followings.find_one_and_update({'user': userid}, {'$pull': {'followings': {"following": useridfoll}}})
    print(useridfoll + " was unfollowed")
    return


def addlike(userid, idtweet):
    db = client.likes
    add = db.likes.find_one_and_update({'user': userid}, {'$push': {'likes': {"tweetliked": idtweet}}})
    return


def dellike(userid, idtweet):
    db = client.likes
    remove = db.likes.find_one_and_delete({"user": userid}, {'$pull': {'likes': {"tweetliked": idtweet}}})
    print ("Tweet deleted from likes")
    return

#deletedtweet(user_id, id_tweet)
#tweetpost(user_id, tweet__post)
#delfollowing(user_id, userfoll1)
#dellike(user_id, id_tweet)
#addfollower(user_id, userfoll1)
#addfollower(user_id, userfoll2)
#addfollowing(user_id, userfoll1)
#newuser(user_id)
#getusertimeline(user_id)


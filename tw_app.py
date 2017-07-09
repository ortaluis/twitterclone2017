from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from py2neo import Graph, Node, Relationship
from bson.code import Code
import pprint


client = MongoClient('mongodb://localhost:27017/')
graph = Graph("http://neo4j:123123@localhost:7474/db/data/")




#following = Relationship(o,"follows", g)
#graph.create(following)







#user_id = "19828717"
#userfoll1 = "19828718"
#userfoll2 = "19828719"
#userfoll3 = "19828720"
#userfoll4 = "19828721"
#userfoll5 = "19828722"
#userfoll6 = "19828723"
#id_tweet = "595e48ce77a3f2c6f85e6c6f"
#tweet__post = "Hello World 7"

# like this???
# Tweets

def tweetpost(userid, tweepost):
    if len(tweepost) < 140:
        db = client.tweets
        tweet = db.tweets.insert_one({
            "user": userid,
            "tweet_post": tweepost,
            "rt": 0,
            "reply": 0,
            "like": 0,
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


# Timeline

def getusertimeline(userid):
    db = client.tweets
    cursor = db.tweets.find({"user": userid}).sort("date", -1)
    for document in cursor:
        print(document)
    return

# Following


def addfollowing(userid, useridfollowing):


    db = client.followings
    if db.followings.find_one({"user": userid, "following": useridfollowing}):
        print "User is already followed"


    else:
        add = db.followings.insert_one({
            "user": userid,
            "following": useridfollowing,
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })


    return


def delfollowing(userid, useridfoll):
    db = client.followings
    remove = db.followings.find_one_and_delete({"user": userid, "following": useridfoll})
    print(useridfoll + " was unfollowed")
    return


# Followers

def addfollower(userid, useridfollower):
    db = client.followers
    if client.followers.find_one({"user": userid, "follower": useridfollower}):
        print "Follower already exists"
    else:
        add = db.followers.insert_one({
            "user": userid,
            "follower": useridfollower,
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

    return

#Likes

def addlike(userid, idtweet):
    db = client.likes
    if db.likes.find_one({"user": userid, "tweetliked": idtweet}):
        print "Tweet already added"
    else:
        add = db.likes.insert_one({"user": userid, "tweetliked": idtweet})
    return


def dellike(userid, idtweet):
    db = client.likes
    remove = db.likes.find_one_and_delete({"user": userid}, {"tweetliked": idtweet})
    print ("Tweet deleted from likes")
    return


#Counters

def counttweets(userid):
    db = client.tweets
    ctweets = db.tweets.find({"user": userid}).count()
    return ctweets


def countfollowers(userid):
    db = client.followers
    cfollowers = db.followers.find({"user": userid}).count()
    return cfollowers


def countfollowings(userid):
    db = client.followings
    cfollowings = db.followings.find({"user": userid}).count()
    return cfollowings


def countlikes(userid):
    db = client.likes
    clikes = db.likes.find({"user": userid}).count()
    return clikes

# MapReduce


def getfollowins(userid):
    db = client.followings
    result = db.followings.find({"user": userid})
    list = []
    for doc in result:
        list.append(doc)
    return list

def getfollowers(userid):
    db = client.followers
    result = db.followers.find({"user": userid})
    list = []
    for doc in result:
        list.append(doc)
    return list

#x = getfollowers(user_id)



#x = countfollowers(user_id)
#x = countfollowings(user_id)
#x = counttweets(user_id)
#print x
#deletedtweet(user_id, id_tweet)
#tweetpost(user_id, tweet__post)
#delfollowing(user_id, userfoll1)
#dellike(user_id, id_tweet)
#addfollower(user_id, userfoll1)
#addfollower(user_id, userfoll2)
#addfollowing(user_id, userfoll2)
#addfollowing(user_id, userfoll3)
#addfollowing(user_id, userfoll4)
#addfollowing(user_id, userfoll5)
#addfollowing(user_id, userfoll6)
#newuser(user_id)
#getusertimeline(user_id)
#addlike(user_id, id_tweet)
#getfollowing(user_id)

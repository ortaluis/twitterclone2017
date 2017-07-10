from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from py2neo import Graph, Node, Relationship
from bson.code import Code
import pprint


client = MongoClient('mongodb://localhost:27017/')
graph = Graph("http://neo4j:123123@localhost:7474/db/data/")

user_id = "19828717"
userfoll1 = "19828718"
userfoll2 = "19828719"
userfoll3 = "19828720"
userfoll4 = "19828721"
userfoll5 = "19828722"
userfoll6 = "19828723"
id_tweet = "595e48ce77a3f2c6f85e6c6f"
tweet__post = "#Luis #is #trying #the #hastag #funtion #and #one #more #time"

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
    cursor = db.tweets.find({"user": userid}, {'_id': False}).sort("date", -1)
    for document in cursor:
        print(document)
    return


#def gettimeline(userid):
#    db = client.followings
#    db2 = client.tweets
#    follwi = db.followings.find({"user": userid})
#    foll = []
#    for doc in foll:
#        #foll.append(doc)
#        print (doc)
#    return

#gettimeline(user_id)

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
    if db.followers.find_one({"user": userid, "follower": useridfollower}):
        print "Follower already exists"
    else:
        add = db.followers.insert_one({
            "user": userid,
            "follower": useridfollower,
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

    return

#addfollower(user_id, "19828728")

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

x = getfollowers(user_id)

def getlikes(userid):
    db = client.likes
    result = db.likes.find({"user": userid})
    list = []
    for doc in result:
        list.append(doc)
    return list

# Trending Topic


def trendingtopic(userid):
    db = client.tweets
    map = Code("""
    function() {
    var word = this.tweet_post.split(" ");

    for (var i = word.length - 1; i >= 0; i--) {
        if (word[i])  {
            emit(word[i].replace(/",@"/g, "").trim(), 1);
            }
    }
    
    for (var i = word.length - 1; i > 0; i--) {
        if ((word[i].charAt(0) != "#") || (word[i-1].charAt(0) != "#"))  {
            emit(word[i-1].replace(/",@"/g, "").trim() + " " + word[i].replace(/",@"/g, "").trim(), 1);
            }
    }
    for (var i = word.length - 1; i > 1; i--) {
        if ((word[i].charAt(0) != "#") || (word[i-1].charAt(0) != "#") || (word[i-2].charAt(0) != "#"))  {
            emit(word[i-2].replace(/",@"/g, "").trim() + " " + word[i-1].replace(/",@"/g, "").trim()+ " " + word[i].replace(/",@"/g, "").trim(), 1);
            }
    }
    
    for (var i = word.length - 1; i > 2; i--) {
        if ((word[i].charAt(0) != "#") || (word[i-1].charAt(0) != "#") || (word[i-2].charAt(0) != "#") || (word[i-3].charAt(0) != "#"))  {
            emit(word[i-3].replace(/",@"/g, "").trim() + " " + word[i-2].replace(/",@"/g, "").trim()+ " " + word[i-1].replace(/",@"/g, "").trim(), 1)+ " " + word[i].replace(/",@"/g, "");
            }
    }
    
    };
    """)
    red = Code("function (key, values) {"
            "var total = 0;"
            "for (var i = 0; i < values.length; i++) {"
            "total += values[i];"
            "  }"
            "  return total;"
            "}")
    result = db.tweets.map_reduce(map, red, "Trending Topic Global")
    for doc in result.find().sort("value", -1).limit(10):
        print doc
    return


def trendingtopicuser(userid):
    db = client.tweets
    map = Code("""
    function() {
    var word = this.tweet_post.split(" ");

    for (var i = word.length - 1; i >= 0; i--) {
        if (word[i])  {
            emit(word[i].replace(/",@"/g, "").trim(), 1);
            }
    }
    
    for (var i = word.length - 1; i > 0; i--) {
        if ((word[i].charAt(0) != "#") || (word[i-1].charAt(0) != "#"))  {
            emit(word[i-1].replace(/",@"/g, "").trim() + " " + word[i].replace(/",@"/g, "").trim(), 1);
            }
    }
    for (var i = word.length - 1; i > 1; i--) {
        if ((word[i].charAt(0) != "#") || (word[i-1].charAt(0) != "#") || (word[i-2].charAt(0) != "#"))  {
            emit(word[i-2].replace(/",@"/g, "").trim() + " " + word[i-1].replace(/",@"/g, "").trim()+ " " + word[i].replace(/",@"/g, "").trim(), 1);
            }
    }
    
    for (var i = word.length - 1; i > 2; i--) {
        if ((word[i].charAt(0) != "#") || (word[i-1].charAt(0) != "#") || (word[i-2].charAt(0) != "#") || (word[i-3].charAt(0) != "#"))  {
            emit(word[i-3].replace(/",@"/g, "").trim() + " " + word[i-2].replace(/",@"/g, "").trim()+ " " + word[i-1].replace(/",@"/g, "").trim(), 1)+ " " + word[i].replace(/",@"/g, "");
            }
    }
    
    };
    """)
    red = Code("function (key, values) {"
               "var total = 0;"
               "for (var i = 0; i < values.length; i++) {"
               "total += values[i];"
               "  }"
               "  return total;"
               "}")
    result = db.tweets.map_reduce(map, red, "Trending Topic Global", query={"user": userid})
    for doc in result.find().sort("value", -1).limit(10):
        print doc
    return

#trendingtopic(user_id)

#x = getfollowers(user_id)
#x = countfollowers(user_id)
#x = countfollowings(user_id)
#x = counttweets(user_id)
print x
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
#gettimeline(user_id, x)
#addlike(user_id, id_tweet)


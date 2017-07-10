import tw_app

username = "19828717"

print ("Welcome " + username)
folw = tw_app.countfollowings(username)
folr = tw_app.countfollowers(username)
twts = tw_app.counttweets(username)
liks = tw_app.countlikes(username)

print twts, " tweets    ", folw, " Followings    ", folr, " Followers    ", liks, " Likes"

print ""
menu = "Menu"

while menu == "Menu":
    if menu == "Menu":
        print "What's new?" \
              "[1] Post a tweet -" \
              "[2] Follow a user -" \
              "[3] Get your Timeline -" \
              "[4] Trending Topics -" \
              "[5] Show Followings -" \
              "[6] Show Followers -" \
              "[7] Your Topics" \
              "[8] Show your likes"
    menu = raw_input('Enter your input:')

    if menu == "1":
        print "What would you like to post?"
        post = raw_input('Enter your post:')
        x = tw_app.tweetpost(username, post)
        menu = "Menu"

    if menu == "2":
        following = raw_input('Enter user to follow:')
        tw_app.addfollowing(username, following)
        tw_app.addfollower(following, username)
        menu = "Menu"

    if menu == "3":
        x = tw_app.getusertimeline(username)
        print x
        menu = "Menu"

    if menu == "4":
        x = tw_app.trendingtopic(username)
        print(x)
        menu = "Menu"

    if menu == "5":
        x = tw_app.getfollowins(username)
        print x
        menu = "Menu"

    if menu == "6":
        x = tw_app.getfollowers(username)
        print x
        menu = "Menu"

    if menu == "7":
        x = tw_app.trendingtopicuser(username)
        print x
        menu = "Menu"

    if menu == "8":
        x = tw_app.getlikes(username)
        print x
        menu = "Menu"

menu = "Menu"








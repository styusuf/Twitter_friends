import csv
import json
import time
import tweepy


# You must use Python 2.7.x
# Rate limit chart for Twitter REST API - https://dev.twitter.com/rest/public/rate-limits

def loadKeys(key_file):
    # TODO: put your keys and tokens in the keys.json file,
    #       then implement this method for loading access keys and token from keys.json
    
    # rtype: str <api_key>, str <api_secret>, str <token>, str <token_secret>

    # Load keys here and replace the empty strings in the return statement with those keys
    with open(key_file) as data_file:
        data = json.load(data_file)

    api_key = data['api_key']
    api_secret = data['api_secret']
    token = data['token']
    token_secret = data['token_secret']

    return api_key, api_secret, token, token_secret


def getPrimaryFriends(api, root_user, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' primary friends of 'root_user'
    # rtype: list containing entries in the form of a tuple (root_user, friend)
    primary_friends = []
 

    user = api.get_user(root_user)

    friends = user.friends()

    index = 0

    for f in friends:
        if index < no_of_friends:
            primary_friends.append((user.screen_name, f.screen_name))
            index =+ 1
            
    return primary_friends

def getNextLevelFriends(api, friends_list, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' friends for each entry in friends_list
    # rtype: list containing entries in the form of a tuple (friends_list[i], friend)
    next_level_friends = []

    index = 0
    for f in friends_list:
        try:
            user = api.get_user(f)
        except tweepy.TweepError:
            continue
        try:
            next_friends = user.friends()
        except tweepy.TweepError:
            continue
        for i in next_friends:
            if index < no_of_friends:
                next_level_friends.append((user.screen_name, i.screen_name))
            index =+ 1
        time.sleep(60)
        index = 0
        
    return next_level_friends

def getNextLevelFollowers(api, followers_list, no_of_followers):
    # TODO: implement the method for fetching 'no_of_followers' followers for each entry in followers_list
    # rtype: list containing entries in the form of a tuple (follower, followers_list[i])    
    next_level_followers = []

    index = 0
    for f in followers_list:
        try:
            user = api.get_user(f)
        except tweepy.TweepError:
            continue
        try:
            next_followers = user.followers()
        except tweepy.TweepError:
            continue
        for i in next_followers:
            if index < no_of_followers:
                next_level_followers.append((i.screen_name, user.screen_name))
            index =+ 1
        time.sleep(60)
        index = 0
    
    return next_level_followers

def GatherAllEdges(api, root_user, no_of_neighbours):
    # TODO:  implement this method for calling the methods getPrimaryFriends, getNextLevelFriends
    #        and getNextLevelFollowers. Use no_of_neighbours to specify the no_of_friends/no_of_followers parameter.
    primary_friends = getPrimaryFriends(api, root_user, no_of_neighbours)
    time.sleep(60)
    friends_list = []
    for f in primary_friends:
        friends_list.append(f[1])

    next_level_friends = getNextLevelFriends(api, friends_list, no_of_neighbours)
    time.sleep(60)
    next_level_followers = getNextLevelFollowers(api, friends_list, no_of_neighbours)
    
    all_edges = primary_friends + next_level_friends + next_level_followers

    return all_edges


# Q1.b.(i),(ii),(iii) - 5 Marks
def writeToFile(data, output_file):
    # write data to output_file
    with open(output_file, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        for d in data:
            writer.writerow(d)

    # rtype: None
    pass



def testSubmission():
    KEY_FILE = 'keys.json'
    OUTPUT_FILE_GRAPH = 'graph.csv'
    NO_OF_NEIGHBOURS = 20
    ROOT_USER = 'PoloChau'

    api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)

    edges = GatherAllEdges(api, ROOT_USER, NO_OF_NEIGHBOURS)

    writeToFile(edges, OUTPUT_FILE_GRAPH)
    

if __name__ == '__main__':
    testSubmission()


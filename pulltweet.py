#coding: UTF-8
from requests_oauthlib import OAuth1Session
import json
import io

with open('_settings.json','r') as f:
    prop = json.load(f)
    api_keys = prop["API_KEY"]
    parameter = prop["PARAMETER"]

    twitter = OAuth1Session(api_keys["CONSUMER_KEY"], api_keys["CONSUMER_SECRET"], api_keys["ACCESS_TOKEN"], api_keys["ACCESS_TOKEN_SECRET"])

    params = {"list_id":parameter["list_id"], "slug":parameter["user_id"], "include_entities":True, "count":40}
    req = twitter.get("https://api.twitter.com/1.1/lists/statuses.json", params = params
    )

    timeline = json.loads(req.text)
    for tweet in timeline:
        if "extended_entities" in tweet and "media" in tweet["extended_entities"]:
            #print(tweet)
            print(tweet["user"]["screen_name"] + " " + tweet["user"]["name"])
            print("TweetID:" + str(tweet["id"]))
            print(tweet["text"])
            for media in tweet["extended_entities"]["media"]:
                pic = media["media_url"]+":orig"
                print(pic)
            print("-----------------------------")
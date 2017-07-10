#coding: UTF-8
from requests_oauthlib import OAuth1Session
import cv2
import urllib
import json
import io
import numpy as np

def imgDownload(url):
    img_read = urllib.request.urlopen(url).read() #URLよりバイナリストリームで画像取得
    img_arr = np.fromstring(img_read, np.uint8) #ストリームをnumpy arrayに変換
    image = cv2.imdecode(img_arr, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("'" + url +"'" + "はこのプログラムでは扱えないファイルです。このファイルはパスされます。")
        return None
    print("opencv読み込み成功")
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return 0

if __name__ == "__main__":
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
                    imgDownload(pic)

                print("-----------------------------")
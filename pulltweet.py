#coding: UTF-8
from requests_oauthlib import OAuth1Session
import cv2
import PIL
import urllib
import json
import io
import numpy as np
import matplotlib.pyplot as plt

#ローカルのjsonファイル展開、返り値は辞書型
def openJSON(file):
    with open(file,'r') as f:
        return json.load(f)

#ツイッター認証・ツイッターAPIオブジェクト生成
def oauthTwitter(api_keys):
    twitter = OAuth1Session(api_keys["CONSUMER_KEY"], api_keys["CONSUMER_SECRET"], api_keys["ACCESS_TOKEN"], api_keys["ACCESS_TOKEN_SECRET"])
    return twitter

#指定したツイートを各種取得
def getTweet(twitter, api, params):
    apiurl = "https://api.twitter.com/1.1/" + api
    print(params)
    req = twitter.get(apiurl, params = params)
    print(type(req))
    print(req.txt)
    print("jsonロード")
    timeline = json.loads(req)
    return timeline

#twitter画像読み込み
def showTweetimg(tweet):
    print(tweet["user"]["screen_name"] + " " + tweet["user"]["name"])
    print("TweetID:" + str(tweet["id"]))
    print(tweet["text"])
    for media in tweet["extended_entities"]["media"]:
        pic = media["media_url"]+":orig"
        print(pic)
        imgDownload(pic)
    print("-----------------------------")

#url経由画像ダウンロード
def imgDownload(url):
    img_read = urllib.request.urlopen(url).read() #URLよりバイナリストリームで画像取得
    img_arr = np.fromstring(img_read, np.uint8) #ストリームをnumpy arrayに変換
    image = cv2.imdecode(img_arr, -1)
    if image is None:
        raise ValueError("'" + url +"'" + "はこのプログラムでは扱えないファイルです。このファイルはパスされます。")
        return None
    image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite('result.jpg', image_gray)
    plt.imshow(image)
    plt.show()
    return 0

if __name__ == "__main__":
    settings = openJSON("_settings.json") #setting.JSON open
    api_keys = settings["API_KEY"] #APIkey
    parameter = settings["PARAMETER"] #twitterAPIパラメーター
    twitter = oauthTwitter(api_keys) #oauth認証にてツイッターオブジェクト生成
    params = {"list_id":parameter["list_id"], "slug":parameter["user_id"], "include_entities":True, "count":40}
    timeline = getTweet(twitter, "lists/statuses.json", params)
    for tweet in timeline:
        if "extended_entities" in tweet and "media" in tweet["extended_entities"]:
            showTweetimg(tweet)
            break
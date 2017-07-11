#coding: UTF-8
from requests_oauthlib import OAuth1Session
from urllib.parse import urlparse
import cv2
import urllib
import json
import io
import re
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
    apiurl = "https://api.twitter.com/1.1/" + api + ".json"
    req = twitter.get(apiurl, params = params)
    return json.loads(req.text)

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
    #reg = r"[\/\.{a-z}+\:orig$]"
    filename = re.sub(r"[\/\.{a-z}+\:orig$]","",urlparse(url).path) #urlを解析してpath部分を抽出、正規表現でファイル名以外を削除
    path = "sample/" + filename + ".png"
    print(path)

    #画像処理
    image_gray = imageOptimize(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(path, image_gray)
    #plt系は画像プレビューの為のやつ
    #plt.imshow(image)
    #plt.show()
    return 0

def imageOptimize(image):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    cv2.resize(image, (500, 500))
    return image

if __name__ == "__main__":
    settings = openJSON("_settings.json") #setting.JSON open
    api_keys = settings["API_KEY"] #APIkey
    parameter = settings["PARAMETER"] #twitterAPIパラメーター
    twitter = oauthTwitter(api_keys) #oauth認証にてツイッターオブジェクト生成
    params = {"list_id":parameter["list_id"], "slug":parameter["user_id"], "include_entities":True, "count":200}
    timeline = getTweet(twitter, "lists/statuses", params)
    for tweet in timeline:
        if "extended_entities" in tweet and "media" in tweet["extended_entities"]:
            showTweetimg(tweet)
            #break #画像1枚だけ拾いたいときコメントアウト
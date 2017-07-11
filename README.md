# tweet-image-corrector
ツイッターの絵師さんリストの萌え画像だけを眺めるためだけの非常に有意義なツイッタークライアント

任意のリストから画像付きツイートを取得し、その画像を識別して(←これ実装中)、その画像だけをツイート文等と共に表示するだけのツイッタークライアントです。

### 使用方法

1.以下のjsonファイルをpulltweet.pyと同じディレクトリ内に「_settings.json」という名前で作成してください。XXXXで始まる数値は各自任意の数字に書き換えて使用してください。
```json:_settings.json
{
    "API_KEY": {
        "CONSUMER_KEY": "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "CONSUMER_SECRET": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "ACCESS_TOKEN": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "ACCESS_TOKEN_SECRET": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    },
    "PARAMETER": {
        "list_id": "XXXXXXXXX",
        "user_id": "XXXXXXXXX"
    },
    "USER_SETTINGS": {

    }
}
```

2.上記jsonファイル内を書き換えます。API_KEY内はそのままツイッター開発者向けページより拾ってきた各種キーを入力してください。PARAMETER内はlist_idにツイート参照したいリストのidを(ブラウザのデバッガで頑張って調べて☆)、user_idにはそのリストを作った人のidを(頑張っt(ry )入れてください。

3.あとは走らせるだけ
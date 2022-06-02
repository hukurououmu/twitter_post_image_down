import os
from time import sleep
import requests
import tweepy
from config import consumer_key, consumer_key_secret, access_token, access_token_secret

# Twitter APIの設定をする
auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# アカウントネームとツイート数を入力する
search_account = input("> Enter account name: ")  # Example: nasa
count_num = int(input("> Set search count: "))  # Example: 100　で100ツイート分

# 画像の保存場所を作成する(アカウントネームのフォルダが作られそこから連番で保存)
os.makedirs("images/" + search_account, exist_ok=True)


def download_files(url, path):
    # 画像のurlを保存する関数
    try:
        resp = requests.get(url, stream=True)
        with open(path, "wb") as f:
            f.write(resp.content)
    except Exception as e:
        raise e


def main():
    # メイン関数
    i = 0
    for result in tweepy.Cursor(
            api.user_timeline, screen_name=search_account, tweet_mode="extended").items(count_num):
        try:
            for media in result.entities.get("media", []):
                url = media["media_url"]
                print("OK " + url)
                path = f"./images/{search_account}/{i}.jpg"  # 連番で保存
                download_files(url, path)
                i += 1
                sleep(1)  # タイムアウトの防止
        except Exception as e:
            raise e


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise e

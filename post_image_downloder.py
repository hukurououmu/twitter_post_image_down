import os
import tweepy
import requests
from colorama import Fore

# config.pyからkeyとtokenをimport
from config import consumer_key, consumer_secret, access_token, access_token_secret
# -----------------------------

# tweepyを使う準備
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
#------------------------------

userid = input("> ユーザーIDを入力してください: ")
username = userid


class Colors:
    red = Fore.RED
    green = Fore.GREEN
    reset = Fore.RESET



def show_public_tweets():
    # タイムラインのツイートを取得
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)

    
def show_user_profile():
    # ユーザーのプロフィールを取得
    user = api.get_user(username)
    print(user.screen_name)
    print(user.followers_count)

    
def show_media_url():
    # 入力したユーザーのタイムラインからツイートを読み込む
    user_id = username
    statuses = api.user_timeline(id=user_id, count=4)

    for status in statuses:
        for entity in status.extended_entities["media"]:
            img_url = entity["media_url"]
            print(img_url)
        break

    


def download_images(url, file_path):
    # urlから画像ファイルをダウンロード
    req = requests.get(url, stream=True)

    if req.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(req.content)


def main():
    # 入力されたユーザーのツイートを読み込んで投稿された画像をダウンロード
    if not os.path.exists("./images/"):
        os.mkdir("./images/")
    user_id = username
    for page in tweepy.Cursor(api.user_timeline, id=user_id).pages(1):  # pagesに指定された数のページ分ダウンロードが行われる
        for status in page:
            try:
                for media in status.extended_entities["media"]:
                    media_id = media["id"]
                    img_url = media["media_url"]
                    print("> " + Colors.green + "Download -> " + img_url + Colors.reset)

                    download_images(url=img_url, file_path="./images/{}.jpg".format(media_id))
            except:
                print("> " + Colors.red + "このメディアはビデオのためダウンロード出来ませんでした" + Colors.reset)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise e

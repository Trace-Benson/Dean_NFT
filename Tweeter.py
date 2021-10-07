import tweepy
from pprint import pprint

class Tweeter:

    def __init__(self):
        auth = tweepy.OAuthHandler("y3hp1MIlxYzchJ5DfppmwQcsl",
                                   "ajHL8pO7pvGUST8PrmFj8MKObgbNMYWMaKj2uqbr9kbFPPNxxq")
        auth.set_access_token("1443038355776753672-ltpw9knng4XDbJypj6b1M6vgiTNLHV",
                              "zMVEfMgWhG5V7iU9309ahS56WusdLTF5nteXCBRJN0KoP")
        self.api = tweepy.API(auth)

    def tweet(self, msg, url=None, reply_to=None):
        params = {
            "status": msg,
            "in_reply_to_status_id": reply_to,
            "attachment_url": url
        }
        self.api.update_status(**params)


t = Tweeter()
t.tweet("heh i fuk")
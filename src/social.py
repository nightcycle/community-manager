import toml
import tweepy
import os
from tweepy import Client
from tweepy import API as TwitterAPI

MAX_TXT_LEN = 280 #unicode characters
MAX_MAIN_MEDIA_SIZE = 5*1000000 #bytes
MAX_COMMENTARY_MEDIA_SIZE = 287.6*1000000 #bytes

# unpack config
CONFIG = toml.load("././social.toml")
POST_CONFIG = CONFIG["Post"]
COMMENT_CONFIG = CONFIG["Commentary"]
AUTH_CONFIG = CONFIG["Authorization"]

baseText = POST_CONFIG["Text"]
for hashtag in POST_CONFIG["Hashtags"]:
	baseText += " #" + hashtag

assert(len(baseText) < MAX_TXT_LEN)

mainMediaSize = os.stat(POST_CONFIG["Video"])
assert(mainMediaSize.st_size < MAX_MAIN_MEDIA_SIZE)

commentMediaSize = os.stat(COMMENT_CONFIG["Video"])
assert(commentMediaSize.st_size < MAX_COMMENTARY_MEDIA_SIZE)

# post to twitter
TWITTER_AUTH = AUTH_CONFIG["Twitter"]
TWITTER_COMPANY_AUTH = TWITTER_AUTH["Company"]
TWITTER_PERSONAL_AUTH = TWITTER_AUTH["Personal"]

# tweet
def tweet(ACCOUNT_AUTH_CONFIG: dict, txt: str, mediaPath: str | None):
	client: Client = tweepy.Client(ACCOUNT_AUTH_CONFIG["Bearer"])
	print(client.get_tweet(id=1588406520064004097))
	
	# Currently this degree of auth can't upload media T_T

tweet(TWITTER_COMPANY_AUTH, "API Test 123", POST_CONFIG["Video"])

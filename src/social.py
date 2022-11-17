import toml
import tweepy
import os
import shutil
import math
from pytube import YouTube
from tweepy import Media
import moviepy.editor as mpe

MAX_TXT_LEN = 280 #unicode characters
MAX_MAIN_MEDIA_SIZE = 5*1000000 #bytes
MAX_COMMENTARY_MEDIA_SIZE = 287.6*1000000 #bytes
AUTH_PORT = 1337
REDIRECT_URL: str = "http://localhost:"+str(AUTH_PORT)

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
print("SIZE", mainMediaSize.st_size)
assert(mainMediaSize.st_size < MAX_MAIN_MEDIA_SIZE)

commentMediaSize = os.stat(COMMENT_CONFIG["Video"])
assert(commentMediaSize.st_size < MAX_COMMENTARY_MEDIA_SIZE)

# post to twitter
TWITTER_AUTH = AUTH_CONFIG["Twitter"]
TWITTER_COMPANY_AUTH = TWITTER_AUTH["Company"]
TWITTER_PERSONAL_AUTH = TWITTER_AUTH["Personal"]

# tweet
def embedMusic():
	# set up directory
	bin_path = "././bin"
	if os.path.exists(bin_path):
		shutil.rmtree(bin_path)
	os.makedirs(bin_path)

	# download and format youtube audio
	yt = YouTube(POST_CONFIG["Music"])
	video = yt.streams.filter(only_audio=True).first()
	out_file = video.download(output_path=bin_path)
	music_path = bin_path+"/music.mp3"
	os.rename(out_file, music_path)

	# trim audio
	print(os.path.exists(music_path))
	video = mpe.VideoFileClip(POST_CONFIG["Video"])
	duration = video.duration

	audio = mpe.AudioFileClip(music_path)
	audio.duration = duration
	final = video.set_audio(audio)
	final.write_videofile("bin/output.mp4",codec= 'mpeg4' ,audio_codec='libvorbis')

def tweet():
	companyAuth = tweepy.OAuthHandler(TWITTER_COMPANY_AUTH["Key"], TWITTER_COMPANY_AUTH["Secret"])
	companyAuth.set_access_token(TWITTER_COMPANY_AUTH["Access"], TWITTER_COMPANY_AUTH["AccessSecret"])
	companyAPI = tweepy.API(companyAuth)

	media: Media = companyAPI.media_upload(filename=POST_CONFIG["Video"], chunked=True, wait_for_async_finalize=True)
	print(media.media_id)
	status = companyAPI.update_status(status=baseText, media_ids=[media.media_id])

	tweetId: str = status.id_str
	tweetUrl = "https://twitter.com/"+TWITTER_COMPANY_AUTH["Username"]+"/status/"+tweetId

	personalAuth = tweepy.OAuthHandler(TWITTER_PERSONAL_AUTH["Key"], TWITTER_PERSONAL_AUTH["Secret"])
	personalAuth.set_access_token(TWITTER_PERSONAL_AUTH["Access"], TWITTER_PERSONAL_AUTH["AccessSecret"])
	personalAPI = tweepy.API(companyAuth)

	personalAPI.update_status(COMMENT_CONFIG["Text"], attachment_url=tweetUrl)


# tweet()

embedMusic()
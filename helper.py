import sqlite3, tweepy
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener


conn = sqlite3.connect("twitter.db")
c = conn.cursor()

# add secret keys in environment variables
ckey="Consumer_Key"
csecret="Consumer_Secret"
atoken= "Access_Token"
asecret="Access_Secret_Token"


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)

'''
c.execute("""CREATE TABLE twitter (
			tweet_id int,
			Tweet text,
			User text,
			ScreenName text,
			HashTags text,
			Topics text,
			datestamp text,
			Favorite int,
			Retweet int,
			Language text
			)""")
'''


def get_trends(trend_id=23424848):
	#WOEID for india is 23424848
	trend = api.trends_place(id=trend_id)
	return trend

def get_tweets(query, result_type='recent'):
	
	data = api.search(query, result_type=result_type)
	
	for status in data:
		topic = query
		hashs = ''
		for hash in status.entities["hashtags"]:
			hashs = hashs + ' '+hash["text"] +','
			topic = topic + ', '+hash["text"]
		for mention in status.entities["user_mentions"]:
			topic = topic + ', '+mention["name"]

		c.execute("INSERT INTO twitter VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (status.id, status.text, status.author.name, status.author.screen_name, hashs, topic, str(status.created_at), status.favorite_count, status.retweet_count, status.lang))
		conn.commit()
	return True

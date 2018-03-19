import sqlite3, time, helper
from flask import Flask, redirect, render_template, request, url_for, flash


app = Flask(__name__)

conn = sqlite3.connect("twitter.db")
c = conn.cursor()

# Display Trending topics on twitter
@app.route("/", methods=["GET", "POST"])
def home():
	#get trending topics in India
	trends = helper.get_trends()

	return render_template("index.html", trends=trends)


@app.route("/query", methods=["GET", "POST"])
def query():

	trends = helper.get_trends()
	q = request.args.get('query').lower()
	order = request.args.get('orderby')
	data = []
	if order == 'Retweet':
		c.execute("SELECT * FROM twitter ORDER BY Retweet DESC")
	elif order == 'Favorite_count':
		c.execute("SELECT * FROM twitter ORDER BY Favorite_count DESC")
	else:
		c.execute("SELECT * FROM twitter ORDER BY tweet_id DESC")

	tweets = c.fetchall()

	msg = None
	if not tweets:
		return render_template("query.html", msg='No Tweets related to %s. Sorry!'%q)
	else:
		for tweet in tweets:
			if q in tweet[1].lower() or q in tweet[2].lower() or q in tweet[3].lower() or q in tweet[4].lower() or q in tweet[5].lower():
				data.append(tweet)

		return render_template("query.html", query=q, trends=trends, tweets=data)

# Save searched tweets into Database
@app.route("/search")
def search():
	q = request.args.get('query')
	helper.get_tweets(q)
	return redirect(url_for("home"))


@app.route("/delete", methods=["GET", "POST"])
def delete():
	delete_term = request.args.get('delete')
	if delete_term:
		c.execute("DELETE FROM twitter WHERE Topics='%s'"%delete_term)
		conn.commit()

	else:
		c.execute("DELETE FROM twitter")
		conn.commit()
	return redirect(url_for("home"))

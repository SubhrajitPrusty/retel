import praw
import requests
from random import shuffle
from datetime import datetime

# REDDIT

CLIENT_ID = "--TOKEN HERE--"
CLIENT_SECRET = "--TOKEN HERE--"
USER_AGENT = "crawling my favorite subreddits" # can be anything


subreddits = [
                "all",
                "movies",
                "funny"
            ] # add your subreddits here



# TELEGRAM

BOT_TOKEN = "--TOKEN HERE--"
CHANNEL = "--CHANNEL NAME HERE--"
URL = "https://api.telegram.org/bot"+BOT_TOKEN+"/send"


reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT)

def getNewPost(subr):
	for subs in reddit.subreddit(subr).top(time_filter="hour",limit=1):
		return subs

data = []
for sub in subreddits:
	data.append(getNewPost(sub))


def isImageLink(link):
	if link.endswith("png") or link.endswith("jpg") or link.endswith("jpeg") or link.endswith("gif"):
		return True
	if "imgur.com/a/" in link:
			return False
	return False

def post2Telegram(data):

	if data == None:
		return 404
	
	payload = {
		"chat_id" : CHANNEL,
	}

	dataType = "Message"

	date = datetime.fromtimestamp(data.created_utc)
	dif = datetime.utcnow() - date

	dif_hours = dif.seconds/60/60

	if dif_hours > 1 or data.score < 10:
		return

	if isImageLink(data.url):
		if str(data.url).endswith("gif"):
			payload['document'] = data.url
			dataType = "Document"
		else:
			payload['photo'] = data.url
			dataType = "Photo"
		payload['caption'] = "#{}\n\n{}\n{}".format(str(data.subreddit), data.title, data.shortlink)
		
	else:
		payload['text'] = "{}\n\n#{}\n\n{}\n\n{}".format(data.url, str(data.subreddit), data.title, data.shortlink)

	r = requests.post(URL+dataType, data=payload)
	print(r.text)
	print(r.status_code)

shuffle(data) # shuffles order of posts

for d in data:
	post2Telegram(d)

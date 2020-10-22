import os
import json
import praw
import requests
from time import sleep
from loguru import logger
from random import shuffle
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

CID = os.environ.get("CID")
CSECRET = os.environ.get("CSECRET")

TOKEN = os.environ.get("TOKEN")
CHANNEL = "@myredditchannel"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/send"

MONGODB_URI = os.environ.get("MONGODB_URI")
logger.debug(MONGODB_URI)
client = MongoClient(MONGODB_URI)
subs = client.get_default_database().subreddits


reddit = praw.Reddit(client_id=CID,
		client_secret=CSECRET,
		user_agent='crawling my favorite subreddits')

def sub_exist(subr):
	try:
		reddit.subreddits.search_by_name(subr, exact=True)
	except Exception as e:
		logger.debug(e)
		return False

	return True

@logger.catch
def get_posts(subr):
	many_subs = []
	try:
		for post in reddit.subreddit(subr).top(time_filter="day",limit=5):
			many_subs.append(post)
	except Exception as e:
		logger.error(e)
	return many_subs

def isImageLink(link):
	if link.endswith("png") or link.endswith("jpg") or link.endswith("jpeg") or link.endswith("gif"):
		return True
	if "imgur.com/a/" in link:
		return False
	return False

def post2Telegram(post):
	payload = {
		"chat_id" : CHANNEL,
	}

	if post:
		dataType = "Message"

		date = datetime.fromtimestamp(post.created_utc)
		dif = datetime.utcnow() - date

		dif_hours = dif.seconds/60/60

		if dif_hours > 24 or post.score < 10:
			return

		if isImageLink(post.url):
			if str(post.url).endswith("gif"):
				payload['document'] = post.url
				dataType = "Document"
			else:
				payload['photo'] = post.url
				dataType = "Photo"
			payload['caption'] = "#{}\n\n{}\n{}".format(str(post.subreddit), post.title, post.shortlink)

		else:
			payload['text'] = "{}\n\n#{}\n\n{}\n\n{}".format(post.url, str(post.subreddit), post.title, post.shortlink)

	r = requests.post(BASE_URL+dataType, data=payload)
	logger.debug(r.reason)

	return r.status_code == 200


def main():
	subreddits = [x for x in subs.find()].pop()
	del subreddits['id']
	del subreddits['_id']

	posts = []
	submissions = [k for k,v in subreddits.items() if v]
	logger.debug(f"No of submissions = {len(submissions)}")
	for sub in submissions:
		try:
			ret = get_posts(sub)
			if ret:
				for p in ret:
					if p:
						posts.append(p)
		except Exception as e:
			logger.error(f'Exception : {e} for subreddit {sub}')

	count = 0
	for p in posts:
		if post2Telegram(p):
			logger.debug('sleeping for 1 seconds')
			sleep(1)
		else:
			logger.debug('failed, sleeping for 60 seconds')
			sleep(60)
			post2Telegram(p)

		count += 1
		if count % 20 == 0:
			logger.debug('20, sleeping for 60 seconds')
			sleep(60)

	logger.debug(f"Count : {count}")
	subs_as_hashs = ["#"+str(x) for x in subreddits.keys() if subreddits[x]]
	payload = { "chat_id" : CHANNEL, "text" : str(count)+"\n\n"+"\n".join(subs_as_hashs)} 
	r = requests.post(BASE_URL+"Message", data=payload)

if __name__ == '__main__':
	main()

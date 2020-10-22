# retel
Make your own reddit channel on telegram

## Prerequisites

* A reddit bot
* A telegram bot
* A telegram channel (you can just use your username in place of a channel)
* (optional) A hosting platform like heroku

## Requirements

Install requirements using 

`pip install -r requirements.txt`

## How to setup

* Create a reddit API Token [here](https://www.reddit.com/prefs/apps/). Note down the client id under the app name, and client secret in the 'edit' option.
* Create a telegram bot using [@botfather](https://telegram.me/botfather). Note down the HTTP API Token.
* Create a channel in telegram. Note the @username of the channel.
* Add all the tokens into .env file and heroku configs
```
CID - reddit client id
CSECRET - reddit client secret
MONGODB_URI - mongodb url
TOKEN - telegram bot TOKEN
```
* Test the app. `python app.py`

## How to host

### Heroku

* Create a new app on heroku
* Deploy using git `git push heroku master`
* Add a heroku scheduler `heroku addons:create scheduler:standard`
* Open the scheduler dashboard `heroku addons:open scheduler`
* Add a new job. 
```
Dyno Size : Free
Frequency : Daily
command : python app.py
```

* Add a mongodb to heroku app
* mlab is a free mongodb service that has now moved to MongoDB Atlas, but you can use any service of your choice
* Create a collection named `subreddits` and add your preferred subreddits according to [subreddits.json template](./templates/subreddits.json)
* The `id` key needs to be there. Mongo will create the `_id` key by itself.
> Updated version of this program will add a gui to add and delete subreddits.

* Enjoy your private reddit channel

> Currently the code is designed to fetch 'top 5 posts of the day with upvotes > 10

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
* Add all the tokens into the app.
* Add all the subreddits you want into the app.
* Run the app. `python app.py`

## How to host

### Heroku

* Create a new app on heroku
* Deploy using git `git push heroku master`
* Add a heroku scheduler `heroku addons:create scheduler:standard`
* Open the scheduler dashboard `heroku addons:open scheduler`
* Add a new job. 

```
Dyno Size : Free
Frequency : Hourly
command : python app.py
```
* Enjoy your private reddit channel

[ Currently the code is designed to fetch 'top post of the hour with upvotes > 10' ]

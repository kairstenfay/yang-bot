# Yang Policy Bot

Contains the code powering the [Yang Policy Bot](http://twitter.com/yang_policy_bot).


## Setup

### Install python requirements
This project requires `tweepy` to post tweets
```sh
pip install -r requirements.txt
```

### Environment variables
Make sure you've set these for the Twitter API:
- `TWITTER_CONSUMER_KEY`
- `TWITTER_CONSUMER_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_SECRET`

## Download the data
If you'd like to update Yang policy data, make sure you have [`npm`](https://www.npmjs.com/get-npm) installed and then run:
```sh
python post-tweets.py --update --no-tweet
```

## Post statuses
Post policies to Twitter by running the following:
```sh
python post-tweets.py
```

Note that the policy number posted is tied to the start date which is hard-coded as a global variable in `post-tweets.py`.

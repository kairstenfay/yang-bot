# Yang Policy Bot

Contains the code powering the [Yang Policy Bot](http://twitter.com/yang_policy_bot).

## Download the data
Download the data from the Yang Policy API by running:
```sh
node download-policy-data.js > policies.json
```

## Post statuses
Post policies to Twitter by running the following:
```sh
python post-tweets.py
```

Note that the policy number posted is tied to the start date which is hard-coded as a global variable in `post-tweets.py`.

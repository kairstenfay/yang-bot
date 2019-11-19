"""
Posts Tweets.
"""
import os
import json
import tweepy
import logging
import argparse
from typing import Dict, Any
from datetime import datetime
from typing import Any, List


LOG = logging.getLogger(__name__)
START_DATE = '2019-11-20'

parser = argparse.ArgumentParser(description="""
    Posts Tweets.""")
args = parser.parse_args()


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'],
        os.environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TWITTER_ACCESS_TOKEN'],
        os.environ['TWITTER_ACCESS_SECRET'])

    index = abs((
        datetime.strptime(START_DATE, '%Y-%m-%d') - datetime.now()
        ).days)

    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True,
        compression=True)


    def needs_ellipses(text: str, remaining_chars: int) -> bool:
        """ """
        return len(text) >= remaining_chars - 3


    def post_policy(policy: Dict[str, str]) -> Any:
        """ """
        title       = f"Policy #{index + 1}: {policy['title']}\n\n"
        url         = f"\n {policy['url']} "

        remaining_chars = 280 - len(title) - len(url)
        end = '...' if needs_ellipses(policy['description'], remaining_chars) else ''

        description = policy['description'][0:remaining_chars - len(end)] + end

        status = title + description + url
        return api.update_status(status=status)


    def post_goals(policy: Dict[str, str], status_id: int) -> Any:
        """ """
        title = 'Goal: '
        remaining_chars = 280 - len(title)

        for goal in policy['goals']:
            end = '...' if needs_ellipses(goal, remaining_chars) else ''
            text = goal[0:remaining_chars - len(end)] + end

            status = title + text
            api.update_status(status=status, in_reply_to_status_id=status_id)


    def post_hashtags(status_id: int) -> Any:
        """ """
        status = '#YangGang #Yang2020 #WomenForYang'
        api.update_status(status=status, in_reply_to_status_id=status_id)


    with open('policies.json', 'r') as f:
        policies = json.load(f)
        policy = policies[index]

        status = post_policy(policy)

        post_goals(policy, status.id)
        post_hashtags(status.id)

"""
Post tweets about a Yang policy.
Each policy is represented as a dictionary. Example:

{
    "title": "Zoning",
    "url": "https://www.yang2020.com/policies/zoning/",
    "description": "Home ownership is a part of the American dream. However, over the past few decades, those who already own homes have made it significantly harder for those who don\u2019t to recognize that dream. Through NIMBY (not in my backyard) and zoning laws, the ability of new housing to be built in certain areas has been impeded to the point where the vast majority of Americans can\u2019t afford to live in the largest cities. You have to look no further than San Francisco or my hometown of New York City to see how true this is.\n\n We need to make it easier for people to afford housing \u2013 either renting or buying \u2013 in more localities. In order to do this, we need to recognize that homeowners in an area generally have more power with local legislators and start taking the needs of renters and those who would be interested in moving into areas into account.",
    "problems_to_be_solved": [
        "Zoning laws have made the creation of affordable housing impossible in areas that are most in need of new housing, driving workers for those areas to multi-hour commutes."
    ],
    "main_quote": "Housing is eating up more and more Americans\u2019 budgets and making it impossible to get ahead. There are ways to provide much more affordable housing but they require new approaches to zoning and development. If we relaxed zoning laws in certain areas it would enhance productivity and allow us to create many more affordable housing options.",
    "goals": [
        "Make housing more affordable"
    ],
    "as_president": "As President, I will\u2026\n\n Work with localities to relax zoning ordinances for the purpose of increasing the development of affordable housing.\nEncourage the building of new innovative housing options like micro-apartments and communal living for people in high-density urban areas.",
    "excerpt": null,
    "citations": []
}
"""
import argparse
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict

import tweepy

LOG = logging.getLogger(__name__)
START_DATE = '2019-11-21'

parser = argparse.ArgumentParser(description="""
    Posts a top-level Tweet with formatted text from Andrew Yang's policies.
    Subsequent statuses are posted in response to the first Tweet containing
    formatted goal text. A final status is posted in the same thread with a
    uniform message.""")
parser.add_argument('--log', default='INFO', type=str, help='Log level')
parser.add_argument(
    '--update', 
    help='If flagged, update our yang-policies install before posting tweets',
    default=False, 
    action='store_true'
)
parser.add_argument(
    '--no-tweet',
    help="If flagged, don't tweet: only log what we would have posted",
    default=False, 
    action='store_true'
)
args = parser.parse_args()


def get_root_directory() -> str:
    """ return root directory of this project as absolute path """
    return os.path.dirname(os.path.abspath(__file__))


def run_shell(command: str) -> str:
    """ execute a shell command and return the output

    :param command: (str)
    :return: (str)
    """
    return os.popen(command).read()


def update_policies() -> str:
    """ Uses npm to keep our policies up to date """
    LOG.info(
        'Seeing if our boy has come up with any new brilliant ideas '
        'since the last policy download...'
    )
    return run_shell('npm install yang-policies@latest')
    


if __name__ == '__main__':
    logging.basicConfig(level=args.log)
    if args.update:
        update_output = update_policies()
        LOG.info(f'updated yang-policies:\n{update_output}')

    def needs_ellipses(text: str, remaining_chars: int) -> bool:
        """
        Returns True if the length of a given *text* exceeds the value of
        *remaining_chars* minus 3. Otherwise returns False.
        """
        return len(text) >= remaining_chars - 3


    def post_policy(policy: Dict[str, str]) -> Any:
        """
        Posts a status containing formatted text from a given *policy*
        description. Text may be truncated with an ellipses to fit within
        Twitter's character limit.
        """
        title       = f"Policy #{index + 1}: {policy['title']}\n\n"
        url         = f"{policy['url']} "
        hashtags    = "\n#Yang2020 #YangGang "

        remaining_chars = 280 - len(title) - len(url) - len(hashtags)
        end = '...' if needs_ellipses(policy['description'], remaining_chars) else ''

        description = policy['description'][0:remaining_chars - len(end)] + end

        status = title + description + hashtags + url
        return api.update_status(status=status)


    def post_goals(policy: Dict[str, str], status_id: int):
        """
        Posts one or more statuses in response to the given *status_id*.
        New posts contain the text of individual goals listed within a given
        *policy*.
        """
        title = 'Goal: '
        remaining_chars = 280 - len(title)

        for goal in policy['goals']:
            end = '...' if needs_ellipses(goal, remaining_chars) else ''
            text = goal[0:remaining_chars - len(end)] + end

            status = title + text
            api.update_status(status=status, in_reply_to_status_id=status_id)


    def post_closing_remarks(status_id: int):
        """ Posts a new status in response to the given *status_id*. """
        status = 'Follow @AndrewYang for more messages like these!\n' + \
        'This bot was made by one of the #WomenForYang\n' + \
        '#YangGang #Yang2020'
        api.update_status(status=status, in_reply_to_status_id=status_id)


    def day_number() -> int:
        """ Returns the number of days since the global *START_DATE*. """
        return (datetime.now() - datetime.strptime(START_DATE, '%Y-%m-%d')).days


    auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'],
        os.environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TWITTER_ACCESS_TOKEN'],
        os.environ['TWITTER_ACCESS_SECRET'])

    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True,
        compression=True)


    policy_dir = (
        f'{get_root_directory()}/'
        'node_modules/'
        'yang-policies/'
        'policies.json'
    )
    with open(policy_dir, 'r') as f:
        policies = json.load(f)
        index = day_number() % len(policies)
        policy = policies[index]

        LOG.info(
            f'Tweeting {policy["title"]} [policy {index+1} of {len(policies)}]\n'
            f'{json.dumps(policy, indent=4)}'
        )
        if not args.no_tweet:
            status = post_policy(policy)

            post_goals(policy, status.id)
            post_closing_remarks(status.id)

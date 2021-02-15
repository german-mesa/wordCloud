import sys

from twitterbot import twitterbot
from twitterbot import secrets


def main():
    # fetches the hashtag from command line argument
    hashtag = '@Judo'

    # fetches the credentials dictionary using get_credentials function
    credentials = secrets.get_credentials()

    # initialize the bot with your credentials
    bot = twitterbot.TwitterBot(credentials['email'], credentials['password'])
    bot.login()

    # calling like_retweet function
    bot.like_retweet(hashtag)


if __name__ == '__main__':
    main()

import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

class TwitterClient:
    def __init__(self):
        self.api_key = os.getenv("TWITTER_API_KEY")
        self.api_secret = os.getenv("TWITTER_API_SECRET")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_secret = os.getenv("TWITTER_ACCESS_SECRET")
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

        self.client = tweepy.Client(
            bearer_token=self.bearer_token,
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_secret,
            wait_on_rate_limit=True
        )

    def search_tweets(self, query, max_results=10):
        try:
            # -is:retweet ensures we only get original tweets
            full_query = f"{query} -is:retweet lang:en"
            tweets = self.client.search_recent_tweets(query=full_query, max_results=max_results, tweet_fields=['author_id', 'text'])
            return tweets.data if tweets.data else []
        except Exception as e:
            print(f"Error searching tweets: {e}")
            return []

    def get_user_name(self, user_id):
        try:
            user = self.client.get_user(id=user_id)
            return user.data.username if user.data else "someone"
        except Exception as e:
            print(f"Error getting user name: {e}")
            return "someone"

    def reply(self, tweet_id, text):
        try:
            self.client.create_tweet(text=text, in_reply_to_tweet_id=tweet_id)
            print(f"Replied to tweet {tweet_id}")
            return True
        except Exception as e:
            print(f"Error replying to tweet: {e}")
            return False

    def retweet(self, tweet_id):
        try:
            self.client.retweet(tweet_id)
            print(f"Retweeted tweet {tweet_id}")
            return True
        except Exception as e:
            print(f"Error retweeting: {e}")
            return False

    def quote(self, tweet_id, text):
        try:
            self.client.create_tweet(text=text, quote_tweet_id=tweet_id)
            print(f"Quoted tweet {tweet_id}")
            return True
        except Exception as e:
            print(f"Error quoting tweet: {e}")
            return False

if __name__ == "__main__":
    # Test client initialization
    client = TwitterClient()
    print("Twitter Client initialized.")

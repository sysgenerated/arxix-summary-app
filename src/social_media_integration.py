import tweepy
import os
import json
from datetime import datetime
import logging
from config import DATA_DIR, TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_twitter_api():
    logging.info(f"TWITTER_API_KEY set: {bool(TWITTER_API_KEY)}")
    logging.info(f"TWITTER_API_SECRET set: {bool(TWITTER_API_SECRET)}")
    logging.info(f"TWITTER_ACCESS_TOKEN set: {bool(TWITTER_ACCESS_TOKEN)}")
    logging.info(f"TWITTER_ACCESS_TOKEN_SECRET set: {bool(TWITTER_ACCESS_TOKEN_SECRET)}")

    if not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET]):
        logging.warning("Some Twitter API credentials are not set. Skipping Twitter integration.")
        return None

    try:
        client = tweepy.Client(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
        )
        logging.info("Twitter API client created successfully.")
        return client
    except Exception as e:
        logging.error(f"Error setting up Twitter API client: {str(e)}")
        return None

def generate_tweet_content():
    summary_file = os.path.join(DATA_DIR, 'content_analysis_results.json')
    with open(summary_file, 'r') as f:
        content = json.load(f)
    
    summary = content.get('summary', '')
    trends = content.get('trends', '')
    
    tweet = f"📚 Today's ArXiv AI/ML Summary:\n\n{summary[:100]}...\n\nTop Trends:\n{trends[:100]}...\n\nRead more: https://sysgenerated.github.io/arxiv-daily-summary"
    return tweet

def post_tweet(client, content):
    if client is None:
        logging.info("Twitter API client not available. Tweet content: %s", content)
        return None
    try:
        response = client.create_tweet(text=content)
        tweet_id = response.data['id']
        logging.info(f"Tweet posted successfully. Tweet ID: {tweet_id}")
        return tweet_id
    except tweepy.errors.Forbidden as e:
        logging.error(f"Forbidden error posting tweet: {e}")
        return None
    except Exception as e:
        logging.error(f"Error posting tweet: {e}")
        return None

def run_social_media_integration():
    client = setup_twitter_api()
    tweet_content = generate_tweet_content()
    
    tweet_id = post_tweet(client, tweet_content)
    
    if tweet_id:
        logging.info(f"Tweet posted successfully. View it at: https://twitter.com/samsbankfreed/status/{tweet_id}")
    elif client is None:
        logging.info("Twitter integration skipped due to missing credentials.")
    else:
        logging.error("Failed to post tweet.")

if __name__ == "__main__":
    run_social_media_integration()

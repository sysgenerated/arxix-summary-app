import tweepy
import os
import json
from datetime import datetime
import logging
from config import DATA_DIR, TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_twitter_api():
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)

def generate_tweet_content():
    summary_file = os.path.join(DATA_DIR, 'content_analysis_results.json')
    with open(summary_file, 'r') as f:
        content = json.load(f)
    
    summary = content.get('summary', '')
    trends = content.get('trends', '')
    
    tweet = f"📚 Today's ArXiv AI/ML Summary:\n\n{summary[:100]}...\n\nTop Trends:\n{trends[:100]}...\n\nRead more: https://sysgenerated.github.io/arxiv-daily-summary"
    return tweet

def post_tweet(api, content):
    try:
        tweet = api.update_status(content)
        logging.info(f"Tweet posted successfully. Tweet ID: {tweet.id}")
        return tweet.id
    except tweepy.TweepError as e:
        logging.error(f"Error posting tweet: {e}")
        return None

def optimize_posting_time():
    # For simplicity, we'll use a fixed time. In a real-world scenario,
    # you might want to analyze your followers' activity patterns.
    return "09:00"  # 9:00 AM

def run_social_media_integration():
    api = setup_twitter_api()
    tweet_content = generate_tweet_content()
    optimal_time = optimize_posting_time()
    
    logging.info(f"Scheduled tweet to be posted at {optimal_time}")
    
    # In a real-world scenario, you would use a task scheduler like Celery
    # to post at the optimal time. For this example, we'll post immediately.
    tweet_id = post_tweet(api, tweet_content)
    
    if tweet_id:
        logging.info(f"Tweet posted successfully. View it at: https://twitter.com/samsbankfreed/status/{tweet_id}")
    else:
        logging.error("Failed to post tweet.")

if __name__ == "__main__":
    run_social_media_integration()

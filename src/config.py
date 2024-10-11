import os
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# arXiv categories to fetch papers from
CATEGORIES = ['cs.AI', 'cs.LG', 'cs.CL', 'cs.CV', 'stat.ML']

# Maximum number of results to fetch from the API
MAX_RESULTS = 1000

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOG_FILE = os.path.join(DATA_DIR, 'arxiv_collector.log')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Name of the file to store the last update date
LAST_UPDATE_FILE = 'last_update.txt'

# Name of the file to store the fetched papers
PAPERS_FILE = 'daily_papers.json'

# Name of the log file
LOG_FILE = 'arxiv_collector.log'

# Load .env file if it exists
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Gemini API Key
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
if not GEMINI_API_KEY:
    logging.warning("Neither GEMINI_API_KEY nor GOOGLE_API_KEY environment variable is set")
else:
    logging.info("API key found in environment variables")

# Twitter API Credentials
TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')
TWITTER_API_SECRET = os.environ.get('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

if not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET]):
    logging.warning("Twitter API credentials are not set in environment variables")
else:
    logging.info("Twitter API credentials found in environment variables")

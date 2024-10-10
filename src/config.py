import os

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

# Gemini API Key
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

import requests
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta
import os
import logging
from config import CATEGORIES, MAX_RESULTS, DATA_DIR, LOG_FILE
import time
import pytz

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

BASE_URL = "http://export.arxiv.org/api/query?"

def get_date_range():
    pst = pytz.timezone('US/Pacific')
    now = datetime.now(pst)
    today = now.date()
    two_days_ago = today - timedelta(days=2)
    return two_days_ago, today

def create_query(start_date, end_date):
    categories = ' OR '.join([f'cat:{cat}' for cat in CATEGORIES])
    return f"({categories}) AND submittedDate:[{start_date.strftime('%Y%m%d')}000000 TO {end_date.strftime('%Y%m%d')}235959]"

def get_request_params(query):
    return {
        'search_query': query,
        'max_results': MAX_RESULTS,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }

def fetch_papers(start_date, end_date):
    query = create_query(start_date, end_date)
    params = get_request_params(query)
    
    logging.info(f"Fetching papers submitted from {start_date} to {end_date} (PST)")
    logging.info(f"Query: {query}")
    logging.info(f"Params: {params}")
    
    max_retries = 3
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            logging.info(f"Response status code: {response.status_code}")
            logging.info(f"Response content (first 500 characters): {response.text[:500]}")
            root = ET.fromstring(response.text)
            papers = parse_arxiv_response(root)
            logging.info(f"Number of papers fetched: {len(papers)}")
            return papers
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                logging.error("Max retries reached. Unable to fetch papers.")
                return []

def parse_arxiv_response(root):
    papers = []
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        paper = {
            'id': entry.find('{http://www.w3.org/2005/Atom}id').text,
            'title': entry.find('{http://www.w3.org/2005/Atom}title').text,
            'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text,
            'authors': [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')],
            'categories': [category.get('term') for category in entry.findall('{http://www.w3.org/2005/Atom}category')],
            'published': entry.find('{http://www.w3.org/2005/Atom}published').text,
            'updated': entry.find('{http://www.w3.org/2005/Atom}updated').text,
        }
        papers.append(paper)
    return papers

def save_papers(papers):
    filename = os.path.join(DATA_DIR, "latest_papers.json")
    with open(filename, 'w') as f:
        json.dump(papers, f, indent=2)
    logging.info(f"Saved {len(papers)} papers to {filename}")

def main():
    start_date, end_date = get_date_range()
    logging.info(f"Fetching papers from {start_date} to {end_date} (PST)")
    papers = fetch_papers(start_date, end_date)
    
    if papers:
        save_papers(papers)
        logging.info(f"Saved {len(papers)} papers")
    else:
        logging.warning(f"No papers found from {start_date} to {end_date} (PST)")
    
    logging.info("Paper collection process completed")

if __name__ == "__main__":
    main()

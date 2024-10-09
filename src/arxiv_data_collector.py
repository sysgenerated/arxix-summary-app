import requests
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta
import os
import logging
from config import CATEGORIES, MAX_RESULTS, DATA_DIR, LOG_FILE
import time

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

def get_last_run_date():
    last_run_file = os.path.join(DATA_DIR, 'last_run_date.txt')
    if os.path.exists(last_run_file):
        with open(last_run_file, 'r') as f:
            return datetime.strptime(f.read().strip(), '%Y-%m-%d').date()
    return datetime.now().date() - timedelta(days=1)

def save_last_run_date(date):
    last_run_file = os.path.join(DATA_DIR, 'last_run_date.txt')
    with open(last_run_file, 'w') as f:
        f.write(date.strftime('%Y-%m-%d'))

def create_query(start_date, end_date):
    return f"(cat:{' OR cat:'.join(CATEGORIES)}) AND submittedDate:[{start_date.strftime('%Y%m%d')}000000 TO {end_date.strftime('%Y%m%d')}235959]"

def get_request_params(query):
    return {
        'search_query': query,
        'max_results': MAX_RESULTS,
        'sortBy': 'submittedDate',
        'sortOrder': 'ascending'
    }

def fetch_papers(start_date, end_date, max_retries=3):
    query = create_query(start_date, end_date)
    params = get_request_params(query)

    logging.info(f"Fetching papers from {start_date} to {end_date}")
    
    for attempt in range(max_retries):
        try:
            response = requests.get(BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            return parse_arxiv_response(response.text)
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                raise
            time.sleep(5)  # Wait for 5 seconds before retrying

def parse_arxiv_response(xml_string):
    root = ET.fromstring(xml_string)
    namespace = {'atom': 'http://www.w3.org/2005/Atom'}
    papers = []
    for entry in root.findall('atom:entry', namespace):
        paper = {
            'title': entry.find('atom:title', namespace).text.strip(),
            'authors': [author.find('atom:name', namespace).text for author in entry.findall('atom:author', namespace)],
            'summary': entry.find('atom:summary', namespace).text.strip(),
            'categories': [category.get('term') for category in entry.findall('atom:category', namespace)],
            'published': entry.find('atom:published', namespace).text,
            'updated': entry.find('atom:updated', namespace).text,
            'link': entry.find('atom:id', namespace).text
        }
        papers.append(paper)
    return papers

def save_papers(papers):
    filename = os.path.join(DATA_DIR, "latest_papers.json")
    with open(filename, 'w') as f:
        json.dump(papers, f, indent=2)
    logging.info(f"Saved {len(papers)} papers to {filename}")

def get_query_dates(last_run_date):
    today = datetime.now().date()
    if today.weekday() == 0:  # Monday
        # If it's Monday, include Friday, Saturday, and Sunday
        start_date = today - timedelta(days=3)
        end_date = today
    else:
        start_date = last_run_date
        end_date = today
    return start_date, end_date

def main():
    last_run_date = get_last_run_date()
    start_date, end_date = get_query_dates(last_run_date)

    papers = fetch_papers(start_date, end_date)
    if papers:
        save_papers(papers)
        save_last_run_date(end_date)
    else:
        logging.warning(f"No papers found from {start_date} to {end_date}")

if __name__ == "__main__":
    main()

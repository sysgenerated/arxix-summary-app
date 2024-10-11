import logging
import sys
from datetime import datetime
import pytz
from arxiv_data_collector import main as collect_papers, get_date_range
from content_analysis import run_content_analysis
from visual_summary import create_visual_summary
from website_generator import generate_website
from config import GEMINI_API_KEY
from social_media_integration import run_social_media_integration

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline():
    try:
        logging.info("Starting arXiv AI/ML summary pipeline...")
        
        if not GEMINI_API_KEY:
            raise ValueError("Gemini API key is not set. Cannot proceed with the pipeline.")
        
        # Step 1: Collect papers
        logging.info("Collecting papers...")
        start_date, end_date = get_date_range()
        pst = pytz.timezone('US/Pacific')
        now = datetime.now(pst)
        logging.info(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        logging.info(f"Fetching papers from {start_date} to {end_date} (PST)")
        collect_papers()
        
        # Step 2: Analyze content
        logging.info("Analyzing content...")
        run_content_analysis()
        
        # Step 3: Create visual summary
        logging.info("Creating visual summary...")
        create_visual_summary()
        
        # Step 4: Generate website
        logging.info("Generating website...")
        generate_website()
        
        # Step 5: Run social media integration
        logging.info("Running social media integration...")
        run_social_media_integration()
        
        logging.info("Pipeline completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during pipeline execution: {str(e)}", exc_info=True)
        # Don't raise the exception here, allow the pipeline to complete

if __name__ == "__main__":
    run_pipeline()
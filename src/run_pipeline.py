import logging
import sys
from datetime import datetime
from arxiv_data_collector import main as collect_papers
from content_analysis import run_content_analysis
from visual_summary import create_visual_summary
from website_generator import generate_website

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline():
    try:
        logging.info("Starting arXiv AI/ML summary pipeline...")
        
        # Step 1: Collect papers
        collect_papers()
        
        # Step 2: Analyze content
        run_content_analysis()
        
        # Step 3: Create visual summary
        create_visual_summary()
        
        # Step 4: Generate website
        generate_website()
        
        logging.info("Pipeline completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during pipeline execution: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        sys.exit(1)
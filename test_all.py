import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.arxiv_data_collector import fetch_daily_papers, save_papers
from src.content_analysis import run_content_analysis
from src.visual_summary import create_visual_summary
from src.run_pipeline import run_pipeline

def test_all(test_date=None):
    print("Testing arxiv_data_collector...")
    papers = fetch_daily_papers(test_date)
    save_papers(papers, test_date)

    print("\nTesting content_analysis...")
    run_content_analysis(test_date)

    print("\nTesting visual_summary...")
    create_visual_summary(test_date)

    print("\nTesting full pipeline...")
    run_pipeline(test_date)

if __name__ == "__main__":
    test_date = sys.argv[1] if len(sys.argv) > 1 else None
    test_all(test_date)

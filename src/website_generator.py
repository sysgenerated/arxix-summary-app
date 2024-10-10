import os
import shutil
from config import DATA_DIR

def generate_website():
    # Path to the daily_summary.html file
    daily_summary_path = os.path.join(DATA_DIR, 'daily_summary.html')
    wordcloud_path = os.path.join(DATA_DIR, 'summary_wordcloud.png')

    # Check if the required files exist
    if not os.path.exists(daily_summary_path):
        print(f"Error: daily_summary.html not found in {DATA_DIR}")
        return
    if not os.path.exists(wordcloud_path):
        print(f"Error: summary_wordcloud.png not found in {DATA_DIR}")
        return

    # Set up the output directory
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(output_dir, exist_ok=True)

    # Copy the daily_summary.html to the output directory as index.html
    output_file = os.path.join(output_dir, 'index.html')
    shutil.copy(daily_summary_path, output_file)

    # Copy the summary_wordcloud.png to the output directory
    shutil.copy(wordcloud_path, os.path.join(output_dir, 'summary_wordcloud.png'))

    print(f"Website generated: {output_file}")
    print(f"Word cloud image copied to output directory")

if __name__ == "__main__":
    generate_website()

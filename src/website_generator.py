import os
import shutil
from config import DATA_DIR

def generate_website():
    # Path to the daily_summary.html file
    daily_summary_path = os.path.join(DATA_DIR, 'daily_summary.html')

    # Check if the daily_summary.html file exists
    if not os.path.exists(daily_summary_path):
        print(f"Error: daily_summary.html not found in {DATA_DIR}")
        return

    # Set up the output directory
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(output_dir, exist_ok=True)

    # Copy the daily_summary.html to the output directory as index.html
    output_file = os.path.join(output_dir, 'index.html')
    shutil.copy(daily_summary_path, output_file)

    print(f"Website generated: {output_file}")

if __name__ == "__main__":
    generate_website()

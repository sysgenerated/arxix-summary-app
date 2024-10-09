import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.run_pipeline import run_pipeline

if __name__ == "__main__":
    run_pipeline()

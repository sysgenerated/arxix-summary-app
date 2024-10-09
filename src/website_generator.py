import os
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from config import DATA_DIR

def load_content():
    results_file = os.path.join(DATA_DIR, 'content_analysis_results.json')
    with open(results_file, 'r') as f:
        return json.load(f)

def generate_website():
    # Load the content
    content = load_content()

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')

    # Render the template with the content
    rendered_html = template.render(
        content=content,
        date=datetime.now().strftime('%Y-%m-%d')
    )

    # Save the rendered HTML
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'index.html')
    with open(output_file, 'w') as f:
        f.write(rendered_html)

    print(f"Website generated: {output_file}")

if __name__ == "__main__":
    generate_website()

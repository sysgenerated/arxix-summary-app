import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import networkx as nx
from wordcloud import WordCloud
from collections import Counter
from config import DATA_DIR
import markdown
import re

# Download NLTK data
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def download_nltk_data():
    print("Downloading necessary NLTK data...")
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
    except Exception as e:
        print(f"Error downloading NLTK data: {e}")
        print("Continuing without NLTK data. Some functionality may be limited.")

download_nltk_data()

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def simple_tokenize(text):
    return text.split()

def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    try:
        tokens = word_tokenize(text.lower())
    except LookupError:
        print("Warning: NLTK tokenization failed. Using simple tokenization.")
        tokens = simple_tokenize(text.lower())
    try:
        stop_words = set(stopwords.words('english'))
    except LookupError:
        print("Warning: NLTK stopwords not available. Using a minimal set.")
        stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
    filtered_tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
    return filtered_tokens

def load_content_analysis_results():
    file_name = 'content_analysis_results.json'
    file_path = os.path.join(DATA_DIR, file_name)
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Content analysis results file not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Unable to parse content analysis results file at {file_path}")
        return None

def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    return plt

def generate_trend_graph(trends):
    trend_list = [trend.strip() for trend in trends.split(',')]
    trend_counts = Counter(trend_list)
    top_trends = dict(sorted(trend_counts.items(), key=lambda x: x[1], reverse=True)[:10])
    
    try:
        fig, ax = plt.subplots(figsize=(14, 10))  # Increased height
    except ValueError:
        # If subplots() fails, create a new figure and axis manually
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111)
    
    bars = ax.barh(list(top_trends.keys()), list(top_trends.values()))
    ax.set_title('Top 10 Trends')
    ax.set_xlabel('Frequency')
    ax.set_ylabel('Trends')
    
    # Add value labels to the right of each bar
    for bar in bars:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, f'{width}',
                ha='left', va='center', fontweight='bold')
    
    # Adjust layout and margins
    plt.tight_layout()
    plt.subplots_adjust(left=0.3)  # Increase left margin for labels
    
    # Reverse y-axis to show most frequent trends at the top
    ax.invert_yaxis()
    
    return plt

def generate_network_graph(papers):
    G = nx.Graph()
    for i, paper in enumerate(papers):
        G.add_node(i, title=paper['title'])
    for i, paper1 in enumerate(papers):
        for j, paper2 in enumerate(papers[i+1:], i+1):
            common_words = set(paper1['title'].lower().split()) & set(paper2['title'].lower().split())
            if len(common_words) > 1:
                G.add_edge(i, j)
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=False, node_size=100, node_color='skyblue', font_size=8, font_weight='bold')
    labels = nx.get_node_attributes(G, 'title')
    label_pos = {k: (v[0], v[1]+0.02) for k, v in pos.items()}
    nx.draw_networkx_labels(G, label_pos, labels, font_size=6)
    plt.title("Paper Relationship Network")
    plt.axis('off')
    return plt

def generate_paper_network(papers):
    G = nx.Graph()
    for i, paper in enumerate(papers):
        G.add_node(i, title=paper['title'])
    
    for i, paper1 in enumerate(papers):
        for j, paper2 in enumerate(papers[i+1:], i+1):
            similarity = calculate_similarity(paper1, paper2)
            if similarity > 0.3:  # Adjust this threshold as needed
                G.add_edge(i, j, weight=similarity)
    
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=False, node_size=100, node_color='skyblue', font_size=8, font_weight='bold')
    
    labels = nx.get_node_attributes(G, 'title')
    nx.draw_networkx_labels(G, pos, labels, font_size=6)
    
    plt.title("Paper Relationship Network")
    plt.axis('off')
    return plt

def calculate_similarity(paper1, paper2):
    # Implement a similarity measure between papers
    # This could be based on common keywords, authors, or more sophisticated NLP techniques
    # For now, let's use a simple Jaccard similarity on the titles
    words1 = set(paper1['title'].lower().split())
    words2 = set(paper2['title'].lower().split())
    return len(words1.intersection(words2)) / len(words1.union(words2))

def create_visual_summary():
    results = load_content_analysis_results()
    if results is None:
        print("Error: Unable to create visual summary due to missing content analysis results.")
        return

    print("Content analysis results keys:", results.keys())

    summary_wordcloud = generate_wordcloud(results.get('summary', ''))
    summary_wordcloud.savefig(os.path.join(DATA_DIR, 'summary_wordcloud.png'))
    
    summary_html = markdown.markdown(results.get('summary', ''))
    trends_html = markdown.markdown(results.get('trends', ''))
    top_articles_html = markdown.markdown(results.get('top_articles', ''))
    
    html_content = f"""
    <html>
    <head>
        <title>ArXiv AI/ML Daily Summary</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; }}
            h1 {{ color: #333; }}
            h2 {{ color: #666; }}
            img {{ max-width: 100%; height: auto; }}
        </style>
    </head>
    <body>
        <h1>ArXiv AI/ML Daily Summary</h1>
        <h2>Word Cloud</h2>
        <img src="summary_wordcloud.png" alt="Summary Word Cloud">
        <h2>Top Articles</h2>
        {top_articles_html}
        <h2>Trends</h2>
        {trends_html}
    </body>
    </html>
    """
    
    with open(os.path.join(DATA_DIR, 'daily_summary.html'), 'w') as f:
        f.write(html_content)

    print(f"Visual summary created and saved as 'daily_summary.html' in {DATA_DIR}")

if __name__ == "__main__":
    create_visual_summary()

import google.generativeai as genai
import json
import os
from datetime import datetime
import logging
from config import DATA_DIR, PAPERS_FILE, GEMINI_API_KEY

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(DATA_DIR, 'content_analysis.log')),
            logging.StreamHandler()
        ]
    )

# Configure Gemini API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    raise ValueError("GEMINI_API_KEY is not set. Please set the environment variable.")

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

class Agent:
    def __init__(self, name, system_message):
        self.name = name
        self.system_message = system_message

    def generate_response(self, message):
        prompt = f"{self.system_message}\n\nHuman: {message}\n\n{self.name}:"
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Error generating response for {self.name}: {e}")
            return None

class UserProxy:
    def __init__(self, name):
        self.name = name
        self.last_message = None

    def initiate_chat(self, agent, message):
        response = agent.generate_response(message)
        if response:
            self.last_message = {"content": response}
            return response
        return None

# Create agents
user_proxy = UserProxy("Human")

paper_analyzer = Agent(
    "Paper_Analyzer",
    "You are an expert in analyzing AI and ML research papers. Your task is to evaluate papers for relevance and interest to the AI/ML community."
)

trend_spotter = Agent(
    "Trend_Spotter",
    "You are an expert in identifying emerging trends and themes in AI and ML research. Your task is to spot key trends from a collection of papers."
)

summary_writer = Agent(
    "Summary_Writer",
    "You are an expert in summarizing complex AI and ML research. Your task is to create concise and informative summaries of multiple research papers and identified trends."
)

article_selector = Agent(
    "Article_Selector",
    "You are an expert in evaluating the importance and usefulness of AI and ML research papers. Your task is to select the most interesting or useful articles from a collection of papers."
)

def generic_agent(prompt_template, papers=None, analysis=None, trends=None):
    prompt = prompt_template.format(
        papers=papers,
        analysis=analysis,
        trends=trends
    )
    response = model.generate_content(prompt)
    return response.text

def paper_analyzer_agent(papers):
    prompt_template = """Analyze the following AI/ML research papers:

{papers}

Provide a concise summary for each paper, focusing on:
1. The main contribution
2. Key findings or results
3. Potential impact or applications

Limit each summary to 2-3 sentences."""
    return generic_agent(prompt_template, papers=papers)

def trend_spotter_agent(papers):
    prompt_template = """Identify the top 3-5 trends in the following AI/ML research papers:

{papers}

For each trend:
1. Provide a short name (1-3 words)
2. Give a brief explanation (1 sentence)

Format the output as a numbered list."""
    return generic_agent(prompt_template, papers=papers)

def summary_writer_agent(papers, analysis, trends):
    prompt_template = """Based on the following information about recent AI/ML research papers:

Analysis: {analysis}
Trends: {trends}

Provide a concise overall summary that:
1. Highlights the most significant developments
2. Identifies common themes or patterns
3. Suggests potential future directions

Limit the summary to 2-3 sentences."""
    return generic_agent(prompt_template, analysis=analysis, trends=trends)

def load_papers():
    file_path = os.path.join(DATA_DIR, "latest_papers.json")
    if not os.path.exists(file_path):
        logging.error(f"No papers file found: {file_path}")
        return None

    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {file_path}: {e}")
        return None

def save_results(results):
    results_file = 'content_analysis_results.json'
    file_path = os.path.join(DATA_DIR, results_file)
    try:
        with open(file_path, 'w') as f:
            json.dump(results, f, indent=2)
        logging.info(f"Content analysis results saved to {file_path}")
        print(f"Content analysis results file path: {file_path}")
    except IOError as e:
        logging.error(f"Error saving content analysis results: {e}")

def article_selector_agent(papers, analysis):
    prompt_template = """Based on the following analysis of AI/ML research papers:

{analysis}

And considering these papers:

{papers}

Select the top 3-5 most interesting or useful articles. For each selected article:
1. Provide the title
2. Give a brief explanation of why it's important or interesting (1-2 sentences)

Format the output as a numbered list."""
    return generic_agent(prompt_template, papers=papers, analysis=analysis)

def run_content_analysis(test_date=None):
    """
    Run the content analysis pipeline.

    Args:
        test_date (str, optional): Date in the format 'YYYY-MM-DD'. Defaults to None.

    Raises:
        ValueError: If the provided date is invalid.
    """
    try:
        papers = load_papers()
    except ValueError as e:
        logging.error(f"Error loading papers: {str(e)}")
        raise

    try:
        analysis = paper_analyzer_agent(papers)
        trends = trend_spotter_agent(papers)
        summary = summary_writer_agent(papers, analysis, trends)
        top_articles = article_selector_agent(papers, analysis)

        results = {
            "analysis": analysis,
            "trends": trends,
            "summary": summary,
            "top_articles": top_articles
        }

        save_results(results)
        logging.info("Content analysis completed successfully")
    except Exception as e:
        logging.error(f"Error during content analysis: {str(e)}")
        raise

if __name__ == "__main__":
    run_content_analysis()

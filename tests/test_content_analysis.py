import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from content_analysis import load_papers, save_results, run_content_analysis, paper_analyzer_agent, trend_spotter_agent, summary_writer_agent, article_selector_agent

class TestContentAnalysis(unittest.TestCase):

    def setUp(self):
        self.test_papers = [
            {"title": "Test Paper 1", "summary": "This is a test summary 1"},
            {"title": "Test Paper 2", "summary": "This is a test summary 2"}
        ]

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=json.dumps([{"title": "Test Paper"}]))
    def test_load_papers(self, mock_file, mock_exists):
        mock_exists.return_value = True
        result = load_papers()
        self.assertEqual(result, [{"title": "Test Paper"}])

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('json.dump')
    def test_save_results(self, mock_json_dump, mock_file):
        test_results = {"key": "value"}
        save_results(test_results)
        mock_json_dump.assert_called_once_with(test_results, mock_file(), indent=2)

    @patch('content_analysis.load_papers')
    @patch('content_analysis.paper_analyzer_agent')
    @patch('content_analysis.trend_spotter_agent')
    @patch('content_analysis.summary_writer_agent')
    @patch('content_analysis.article_selector_agent')
    @patch('content_analysis.save_results')
    def test_run_content_analysis(self, mock_save_results, mock_article_selector, 
                                  mock_summary_writer, mock_trend_spotter, 
                                  mock_paper_analyzer, mock_load_papers):
        mock_load_papers.return_value = self.test_papers
        mock_paper_analyzer.return_value = "Analysis"
        mock_trend_spotter.return_value = "Trends"
        mock_summary_writer.return_value = "Summary"
        mock_article_selector.return_value = "Top Articles"
        
        run_content_analysis()
        
        mock_load_papers.assert_called_once()
        mock_paper_analyzer.assert_called_once_with(self.test_papers)
        mock_trend_spotter.assert_called_once_with(self.test_papers)
        mock_summary_writer.assert_called_once_with(self.test_papers, "Analysis", "Trends")
        mock_article_selector.assert_called_once_with(self.test_papers, "Analysis")
        mock_save_results.assert_called_once_with({
            "analysis": "Analysis",
            "trends": "Trends",
            "summary": "Summary",
            "top_articles": "Top Articles"
        })

    @patch('content_analysis.generic_agent')
    def test_paper_analyzer_agent(self, mock_generic_agent):
        mock_generic_agent.return_value = "Analysis"
        result = paper_analyzer_agent(self.test_papers)
        self.assertEqual(result, "Analysis")
        mock_generic_agent.assert_called_once()

    @patch('content_analysis.generic_agent')
    def test_trend_spotter_agent(self, mock_generic_agent):
        mock_generic_agent.return_value = "Trends"
        result = trend_spotter_agent(self.test_papers)
        self.assertEqual(result, "Trends")
        mock_generic_agent.assert_called_once()

    @patch('content_analysis.generic_agent')
    def test_summary_writer_agent(self, mock_generic_agent):
        mock_generic_agent.return_value = "Summary"
        result = summary_writer_agent(self.test_papers, "Analysis", "Trends")
        self.assertEqual(result, "Summary")
        mock_generic_agent.assert_called_once()

    @patch('content_analysis.generic_agent')
    def test_article_selector_agent(self, mock_generic_agent):
        mock_generic_agent.return_value = "Top Articles"
        result = article_selector_agent(self.test_papers, "Analysis")
        self.assertEqual(result, "Top Articles")
        mock_generic_agent.assert_called_once()

if __name__ == '__main__':
    unittest.main()
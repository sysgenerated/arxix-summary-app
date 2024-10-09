import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from visual_summary import load_content_analysis_results, generate_wordcloud, generate_trend_graph, create_visual_summary

class TestVisualSummary(unittest.TestCase):

    @patch('visual_summary.open', new_callable=unittest.mock.mock_open, read_data='{"summary": "test summary"}')
    def test_load_content_analysis_results(self, mock_open):
        result = load_content_analysis_results()
        self.assertEqual(result, {"summary": "test summary"})

    @patch('visual_summary.WordCloud')
    @patch('visual_summary.plt')
    def test_generate_wordcloud(self, mock_plt, mock_wordcloud):
        mock_wordcloud.return_value.generate.return_value = MagicMock()
        result = generate_wordcloud("test text")
        self.assertIsNotNone(result)
        mock_wordcloud.assert_called_once()
        mock_plt.figure.assert_called_once()

    @patch('visual_summary.plt')
    def test_generate_trend_graph(self, mock_plt):
        result = generate_trend_graph("trend1, trend2, trend1")
        self.assertIsNotNone(result)
        mock_plt.figure.assert_called_once()

    @patch('visual_summary.load_content_analysis_results')
    @patch('visual_summary.generate_wordcloud')
    @patch('visual_summary.markdown.markdown')
    @patch('visual_summary.open', new_callable=unittest.mock.mock_open)
    def test_create_visual_summary(self, mock_open, mock_markdown, mock_generate_wordcloud, mock_load_results):
        mock_load_results.return_value = {
            "summary": "test summary",
            "trends": "test trends",
            "top_articles": "test articles"
        }
        mock_generate_wordcloud.return_value.savefig.return_value = None
        mock_markdown.side_effect = lambda x: x

        create_visual_summary()

        mock_load_results.assert_called_once()
        mock_generate_wordcloud.assert_called_once()
        mock_open.assert_called_once()
        self.assertEqual(mock_markdown.call_count, 3)

if __name__ == '__main__':
    unittest.main()

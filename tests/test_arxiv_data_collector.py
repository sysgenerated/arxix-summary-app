import unittest
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta
import json
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from arxiv_data_collector import get_last_run_date, save_last_run_date, fetch_papers, parse_arxiv_response, save_papers

class TestArxivCollector(unittest.TestCase):

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='2023-09-15')
    def test_get_last_run_date_existing(self, mock_file, mock_exists):
        mock_exists.return_value = True
        result = get_last_run_date()
        self.assertEqual(result, datetime(2023, 9, 15).date())

    @patch('os.path.exists')
    def test_get_last_run_date_not_existing(self, mock_exists):
        mock_exists.return_value = False
        result = get_last_run_date()
        self.assertEqual(result, datetime.now().date() - timedelta(days=1))

    @patch('builtins.open', new_callable=mock_open)
    def test_save_last_run_date(self, mock_file):
        date = datetime(2023, 9, 16).date()
        save_last_run_date(date)
        mock_file().write.assert_called_once_with('2023-09-16')

    @patch('requests.get')
    def test_fetch_papers(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.text = '<feed xmlns="http://www.w3.org/2005/Atom"></feed>'
        start_date = datetime(2023, 9, 15).date()
        end_date = datetime(2023, 9, 16).date()
        result = fetch_papers(start_date, end_date)
        self.assertEqual(result, [])

    def test_parse_arxiv_response(self):
        xml_string = '''
        <feed xmlns="http://www.w3.org/2005/Atom">
          <entry>
            <title>Test Paper</title>
            <author><name>John Doe</name></author>
            <summary>This is a test summary.</summary>
            <category term="cs.AI"/>
            <published>2023-09-15T00:00:00Z</published>
            <updated>2023-09-15T00:00:00Z</updated>
            <id>http://arxiv.org/abs/test.12345</id>
          </entry>
        </feed>
        '''
        result = parse_arxiv_response(xml_string)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Test Paper')

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_papers(self, mock_json_dump, mock_file):
        papers = [{'title': 'Test Paper'}]
        date = datetime(2023, 9, 16).date()
        save_papers(papers, date)
        mock_json_dump.assert_called_once()

if __name__ == '__main__':
    unittest.main()

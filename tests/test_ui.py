"""
Unit tests for ui module
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from ui import NewsUI


class TestNewsUI:
    """Tests for NewsUI class"""

    def test_clear(self):
        """Test clear console"""
        with patch('ui.console.clear') as mock_clear:
            NewsUI.clear()
            mock_clear.assert_called_once()

    def test_show_header(self):
        """Test showing header"""
        with patch('ui.console.print') as mock_print:
            NewsUI.show_header()
            assert mock_print.call_count >= 1

    @patch('ui.Prompt.ask')
    def test_show_menu(self, mock_ask):
        """Test showing menu"""
        mock_ask.return_value = '1'

        with patch('ui.console.print'):
            choice = NewsUI.show_menu(favorites_count=5)
            assert choice == '1'
            mock_ask.assert_called_once()

    def test_show_articles_table_empty(self):
        """Test showing empty articles table"""
        with patch('ui.console.print') as mock_print:
            NewsUI.show_articles_table([], {}, show_index=True)
            # Should show "No articles found" message

    def test_show_articles_table_with_data(self):
        """Test showing articles table with data"""
        articles = [
            {
                'index': 1,
                'title': 'Test Article',
                'source': 'Test Source',
                'published': '2024-01-15 10:30'
            }
        ]

        page_info = {
            'current_page': 1,
            'total_pages': 1,
            'start_index': 1,
            'end_index': 1,
            'total_items': 1
        }

        with patch('ui.console.print') as mock_print:
            NewsUI.show_articles_table(articles, page_info)
            assert mock_print.called

    def test_show_article_detail(self):
        """Test showing article details"""
        article = {
            'title': 'Test Article',
            'source': 'Test Source',
            'author': 'John Doe',
            'published': '2024-01-15 10:30',
            'description': 'Test description',
            'url': 'https://test.com'
        }

        with patch('ui.console.print') as mock_print:
            NewsUI.show_article_detail(article, is_favorite=False)
            assert mock_print.called

    @patch('ui.Prompt.ask')
    def test_show_categories(self, mock_ask):
        """Test showing categories"""
        mock_ask.return_value = '1'

        with patch('ui.console.print'):
            category = NewsUI.show_categories()
            assert category == 'business'

    @patch('ui.Prompt.ask')
    def test_get_search_query(self, mock_ask):
        """Test getting search query"""
        mock_ask.return_value = 'python'

        query = NewsUI.get_search_query()
        assert query == 'python'

    @patch('ui.Prompt.ask')
    def test_get_search_query_empty(self, mock_ask):
        """Test getting empty search query"""
        mock_ask.return_value = ''

        query = NewsUI.get_search_query()
        assert query is None

    @patch('ui.Prompt.ask')
    def test_show_pagination_menu(self, mock_ask):
        """Test showing pagination menu"""
        mock_ask.return_value = 'n'

        page_info = {
            'has_prev': True,
            'has_next': True
        }

        with patch('ui.console.print'):
            choice = NewsUI.show_pagination_menu(page_info)
            assert choice == 'n'

    def test_show_success(self):
        """Test showing success message"""
        with patch('ui.console.print') as mock_print:
            NewsUI.show_success("Test success")
            mock_print.assert_called_once()

    def test_show_error(self):
        """Test showing error message"""
        with patch('ui.console.print') as mock_print:
            NewsUI.show_error("Test error")
            mock_print.assert_called_once()

    def test_show_warning(self):
        """Test showing warning message"""
        with patch('ui.console.print') as mock_print:
            NewsUI.show_warning("Test warning")
            mock_print.assert_called_once()

    def test_show_info(self):
        """Test showing info message"""
        with patch('ui.console.print') as mock_print:
            NewsUI.show_info("Test info")
            mock_print.assert_called_once()

    @patch('ui.Confirm.ask')
    def test_confirm_true(self, mock_ask):
        """Test confirmation dialog - true"""
        mock_ask.return_value = True

        result = NewsUI.confirm("Are you sure?")
        assert result is True

    @patch('ui.Confirm.ask')
    def test_confirm_false(self, mock_ask):
        """Test confirmation dialog - false"""
        mock_ask.return_value = False

        result = NewsUI.confirm("Are you sure?")
        assert result is False

    @patch('ui.Prompt.ask')
    def test_get_number_input_valid(self, mock_ask):
        """Test getting valid number input"""
        mock_ask.return_value = '5'

        result = NewsUI.get_number_input("Enter number:", min_val=1, max_val=10)
        assert result == 5

    @patch('ui.Prompt.ask')
    def test_get_number_input_cancel(self, mock_ask):
        """Test getting number input - cancel"""
        mock_ask.return_value = 'q'

        result = NewsUI.get_number_input("Enter number:")
        assert result is None

    @patch('ui.webbrowser.open')
    def test_open_url_success(self, mock_browser):
        """Test opening URL successfully"""
        mock_browser.return_value = True

        result = NewsUI.open_url('https://test.com')
        assert result is True
        mock_browser.assert_called_once_with('https://test.com')

    @patch('ui.webbrowser.open')
    def test_open_url_failure(self, mock_browser):
        """Test opening URL failure"""
        mock_browser.side_effect = Exception("Failed to open")

        result = NewsUI.open_url('https://test.com')
        assert result is False

    @patch('ui.Prompt.ask')
    def test_press_enter_to_continue(self, mock_ask):
        """Test press enter to continue"""
        mock_ask.return_value = ''

        NewsUI.press_enter_to_continue()
        mock_ask.assert_called_once()

    def test_show_goodbye(self):
        """Test showing goodbye message"""
        with patch('ui.console.print') as mock_print:
            NewsUI.show_goodbye()
            mock_print.assert_called_once()

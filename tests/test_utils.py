"""
Unit tests for utils module
"""

import pytest
import json
import os
from pathlib import Path
from datetime import datetime
from utils import (
    ArticleFormatter,
    Paginator,
    FavoritesManager,
    validate_input,
    get_integer_input
)


class TestArticleFormatter:
    """Tests for ArticleFormatter class"""

    def test_format_date_valid(self):
        """Test formatting valid ISO date"""
        date_str = '2024-01-15T10:30:00Z'
        result = ArticleFormatter.format_date(date_str)
        assert '2024-01-15' in result
        assert '10:30' in result

    def test_format_date_invalid(self):
        """Test formatting invalid date"""
        result = ArticleFormatter.format_date('invalid_date')
        assert result == 'invalid_date'

    def test_format_date_none(self):
        """Test formatting None date"""
        result = ArticleFormatter.format_date(None)
        assert result == 'N/A'

    def test_truncate_text_short(self):
        """Test truncating text shorter than max length"""
        text = "Short text"
        result = ArticleFormatter.truncate_text(text, max_length=100)
        assert result == "Short text"

    def test_truncate_text_long(self):
        """Test truncating long text"""
        text = "A" * 150
        result = ArticleFormatter.truncate_text(text, max_length=100)
        assert len(result) == 100
        assert result.endswith('...')

    def test_truncate_text_none(self):
        """Test truncating None text"""
        result = ArticleFormatter.truncate_text(None)
        assert result == 'N/A'

    def test_truncate_text_empty(self):
        """Test truncating empty text"""
        result = ArticleFormatter.truncate_text('')
        assert result == 'N/A'

    def test_format_article_complete(self):
        """Test formatting complete article"""
        article = {
            'title': 'Test Article',
            'source': {'name': 'Test Source'},
            'author': 'John Doe',
            'description': 'Test description',
            'url': 'https://test.com/article',
            'publishedAt': '2024-01-15T10:30:00Z',
            'content': 'Test content'
        }

        result = ArticleFormatter.format_article(article, index=1)

        assert result['index'] == 1
        assert result['title'] == 'Test Article'
        assert result['source'] == 'Test Source'
        assert result['author'] == 'John Doe'
        assert result['url'] == 'https://test.com/article'
        assert '2024-01-15' in result['published']

    def test_format_article_missing_fields(self):
        """Test formatting article with missing fields"""
        article = {}
        result = ArticleFormatter.format_article(article)

        assert result['title'] == 'No Title'
        assert result['source'] == 'Unknown Source'
        assert result['author'] == 'Unknown'
        assert result['description'] == 'N/A'

    def test_highlight_keywords_basic(self):
        """Test keyword highlighting"""
        text = "Python is a great programming language"
        keywords = ["Python", "programming"]
        result = ArticleFormatter.highlight_keywords(text, keywords)

        assert '[HIGHLIGHT]' in result
        assert '[/HIGHLIGHT]' in result

    def test_highlight_keywords_case_insensitive(self):
        """Test case-insensitive keyword highlighting"""
        text = "Python is awesome"
        keywords = ["python"]
        result = ArticleFormatter.highlight_keywords(text, keywords)

        assert '[HIGHLIGHT]' in result

    def test_highlight_keywords_empty_list(self):
        """Test highlighting with empty keyword list"""
        text = "Test text"
        result = ArticleFormatter.highlight_keywords(text, [])
        assert result == text

    def test_highlight_keywords_none_text(self):
        """Test highlighting with None text"""
        result = ArticleFormatter.highlight_keywords(None, ["test"])
        assert result is None


class TestPaginator:
    """Tests for Paginator class"""

    def test_init_basic(self):
        """Test basic initialization"""
        items = list(range(25))
        paginator = Paginator(items, page_size=10)

        assert paginator.total_items == 25
        assert paginator.page_size == 10
        assert paginator.total_pages == 3
        assert paginator.current_page == 1

    def test_init_exact_pages(self):
        """Test initialization with exact number of pages"""
        items = list(range(20))
        paginator = Paginator(items, page_size=10)

        assert paginator.total_pages == 2

    def test_init_empty_list(self):
        """Test initialization with empty list"""
        paginator = Paginator([], page_size=10)

        assert paginator.total_items == 0
        assert paginator.total_pages == 0

    def test_init_invalid_page_size(self):
        """Test initialization with invalid page size"""
        paginator = Paginator([1, 2, 3], page_size=0)
        assert paginator.page_size == 1  # Should default to minimum 1

    def test_get_page_first(self):
        """Test getting first page"""
        items = list(range(25))
        paginator = Paginator(items, page_size=10)

        page_items, page_info = paginator.get_page(1)

        assert len(page_items) == 10
        assert page_items[0] == 0
        assert page_items[-1] == 9
        assert page_info['current_page'] == 1
        assert page_info['has_next'] is True
        assert page_info['has_prev'] is False

    def test_get_page_middle(self):
        """Test getting middle page"""
        items = list(range(25))
        paginator = Paginator(items, page_size=10)

        page_items, page_info = paginator.get_page(2)

        assert len(page_items) == 10
        assert page_items[0] == 10
        assert page_info['has_next'] is True
        assert page_info['has_prev'] is True

    def test_get_page_last(self):
        """Test getting last page"""
        items = list(range(25))
        paginator = Paginator(items, page_size=10)

        page_items, page_info = paginator.get_page(3)

        assert len(page_items) == 5
        assert page_items[0] == 20
        assert page_info['has_next'] is False
        assert page_info['has_prev'] is True

    def test_get_page_out_of_range(self):
        """Test getting page number out of range"""
        items = list(range(25))
        paginator = Paginator(items, page_size=10)

        # Too high
        page_items, page_info = paginator.get_page(999)
        assert page_info['current_page'] == 3  # Should return last page

        # Too low
        page_items, page_info = paginator.get_page(-5)
        assert page_info['current_page'] == 1  # Should return first page

    def test_next_page(self):
        """Test next page navigation"""
        items = list(range(25))
        paginator = Paginator(items, page_size=10)

        paginator.get_page(1)
        page_items, page_info = paginator.next_page()

        assert page_info['current_page'] == 2

    def test_prev_page(self):
        """Test previous page navigation"""
        items = list(range(25))
        paginator = Paginator(items, page_size=10)

        paginator.get_page(2)
        page_items, page_info = paginator.prev_page()

        assert page_info['current_page'] == 1

    def test_first_page(self):
        """Test first page navigation"""
        items = list(range(25))
        paginator = Paginator(items, page_size=10)

        paginator.get_page(3)
        page_items, page_info = paginator.first_page()

        assert page_info['current_page'] == 1

    def test_last_page(self):
        """Test last page navigation"""
        items = list(range(25))
        paginator = Paginator(items, page_size=10)

        page_items, page_info = paginator.last_page()

        assert page_info['current_page'] == 3


class TestFavoritesManager:
    """Tests for FavoritesManager class"""

    @pytest.fixture
    def temp_favorites_file(self, tmp_path):
        """Create temporary favorites file"""
        return tmp_path / "test_favorites.json"

    def test_init_new_file(self, temp_favorites_file):
        """Test initialization with non-existent file"""
        manager = FavoritesManager(str(temp_favorites_file))
        assert manager.favorites == []

    def test_init_existing_file(self, temp_favorites_file):
        """Test initialization with existing file"""
        # Create file with data
        test_data = [{'title': 'Test', 'url': 'https://test.com'}]
        temp_favorites_file.write_text(json.dumps(test_data))

        manager = FavoritesManager(str(temp_favorites_file))
        assert len(manager.favorites) == 1

    def test_init_corrupted_file(self, temp_favorites_file):
        """Test initialization with corrupted file"""
        temp_favorites_file.write_text("invalid json")

        manager = FavoritesManager(str(temp_favorites_file))
        assert manager.favorites == []

    def test_add_favorite_new(self, temp_favorites_file):
        """Test adding new favorite"""
        manager = FavoritesManager(str(temp_favorites_file))

        article = {
            'title': 'Test Article',
            'source': {'name': 'Test Source'},
            'url': 'https://test.com/article',
            'description': 'Test description',
            'publishedAt': '2024-01-15T10:30:00Z'
        }

        result = manager.add_favorite(article)
        assert result is True
        assert len(manager.favorites) == 1
        assert manager.favorites[0]['title'] == 'Test Article'

    def test_add_favorite_duplicate(self, temp_favorites_file):
        """Test adding duplicate favorite"""
        manager = FavoritesManager(str(temp_favorites_file))

        article = {
            'title': 'Test Article',
            'source': {'name': 'Test Source'},
            'url': 'https://test.com/article'
        }

        manager.add_favorite(article)
        result = manager.add_favorite(article)

        assert result is False
        assert len(manager.favorites) == 1

    def test_add_favorite_no_url(self, temp_favorites_file):
        """Test adding favorite without URL"""
        manager = FavoritesManager(str(temp_favorites_file))

        article = {'title': 'Test Article'}
        result = manager.add_favorite(article)

        assert result is False

    def test_remove_favorite_existing(self, temp_favorites_file):
        """Test removing existing favorite"""
        manager = FavoritesManager(str(temp_favorites_file))

        article = {
            'title': 'Test',
            'source': {'name': 'Source'},
            'url': 'https://test.com'
        }

        manager.add_favorite(article)
        result = manager.remove_favorite('https://test.com')

        assert result is True
        assert len(manager.favorites) == 0

    def test_remove_favorite_nonexistent(self, temp_favorites_file):
        """Test removing non-existent favorite"""
        manager = FavoritesManager(str(temp_favorites_file))

        result = manager.remove_favorite('https://nonexistent.com')
        assert result is False

    def test_get_favorites(self, temp_favorites_file):
        """Test getting favorites list"""
        manager = FavoritesManager(str(temp_favorites_file))

        article = {
            'title': 'Test',
            'source': {'name': 'Source'},
            'url': 'https://test.com'
        }

        manager.add_favorite(article)
        favorites = manager.get_favorites()

        assert len(favorites) == 1
        assert isinstance(favorites, list)

    def test_clear_favorites(self, temp_favorites_file):
        """Test clearing all favorites"""
        manager = FavoritesManager(str(temp_favorites_file))

        article = {
            'title': 'Test',
            'source': {'name': 'Source'},
            'url': 'https://test.com'
        }

        manager.add_favorite(article)
        result = manager.clear_favorites()

        assert result is True
        assert len(manager.favorites) == 0

    def test_is_favorite_true(self, temp_favorites_file):
        """Test checking if article is favorite"""
        manager = FavoritesManager(str(temp_favorites_file))

        article = {
            'title': 'Test',
            'source': {'name': 'Source'},
            'url': 'https://test.com'
        }

        manager.add_favorite(article)
        assert manager.is_favorite('https://test.com') is True

    def test_is_favorite_false(self, temp_favorites_file):
        """Test checking non-favorite article"""
        manager = FavoritesManager(str(temp_favorites_file))
        assert manager.is_favorite('https://test.com') is False

    def test_get_count(self, temp_favorites_file):
        """Test getting favorites count"""
        manager = FavoritesManager(str(temp_favorites_file))

        assert manager.get_count() == 0

        article = {
            'title': 'Test',
            'source': {'name': 'Source'},
            'url': 'https://test.com'
        }

        manager.add_favorite(article)
        assert manager.get_count() == 1


class TestUtilityFunctions:
    """Tests for utility functions"""

    def test_validate_input_valid(self, monkeypatch):
        """Test validate_input with valid input"""
        monkeypatch.setattr('builtins.input', lambda _: '1')
        result = validate_input("Test: ", ['1', '2', '3'])
        assert result == '1'

    def test_validate_input_empty_allowed(self, monkeypatch):
        """Test validate_input with empty input allowed"""
        monkeypatch.setattr('builtins.input', lambda _: '')
        result = validate_input("Test: ", ['1', '2'], allow_empty=True)
        assert result == ''

    def test_get_integer_input_valid(self, monkeypatch):
        """Test get_integer_input with valid number"""
        monkeypatch.setattr('builtins.input', lambda _: '5')
        result = get_integer_input("Test: ", min_val=1, max_val=10)
        assert result == 5

    def test_get_integer_input_cancel(self, monkeypatch):
        """Test get_integer_input with cancel"""
        monkeypatch.setattr('builtins.input', lambda _: 'q')
        result = get_integer_input("Test: ")
        assert result is None

    def test_get_integer_input_empty(self, monkeypatch):
        """Test get_integer_input with empty input"""
        monkeypatch.setattr('builtins.input', lambda _: '')
        result = get_integer_input("Test: ")
        assert result is None

"""
Utility Module
Helper functions for formatting, pagination, and data management
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from pathlib import Path


class ArticleFormatter:
    """Format news articles for display"""

    @staticmethod
    def format_date(date_str: str) -> str:
        """
        Format ISO date string to readable format

        Args:
            date_str: ISO 8601 date string

        Returns:
            Formatted date string
        """
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M')
        except (ValueError, AttributeError):
            return date_str or 'N/A'

    @staticmethod
    def truncate_text(text: str, max_length: int = 100) -> str:
        """
        Truncate text to specified length

        Args:
            text: Text to truncate
            max_length: Maximum length

        Returns:
            Truncated text with ellipsis if needed
        """
        if not text:
            return 'N/A'

        text = text.strip()
        if len(text) <= max_length:
            return text

        return text[:max_length - 3] + '...'

    @staticmethod
    def format_article(article: Dict, index: Optional[int] = None) -> Dict:
        """
        Format article for display

        Args:
            article: Raw article dictionary from API
            index: Optional index number

        Returns:
            Formatted article dictionary
        """
        formatted = {
            'index': index,
            'title': article.get('title', 'No Title'),
            'source': article.get('source', {}).get('name', 'Unknown Source'),
            'author': article.get('author', 'Unknown'),
            'description': ArticleFormatter.truncate_text(article.get('description', ''), 150),
            'url': article.get('url', ''),
            'published': ArticleFormatter.format_date(article.get('publishedAt', '')),
            'content': article.get('content', 'No content available')
        }
        return formatted

    @staticmethod
    def highlight_keywords(text: str, keywords: List[str]) -> str:
        """
        Highlight keywords in text (returns text with markers)

        Args:
            text: Text to process
            keywords: List of keywords to highlight

        Returns:
            Text with highlight markers
        """
        if not keywords or not text:
            return text

        result = text
        for keyword in keywords:
            if keyword:
                # Case-insensitive replacement
                import re
                pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                result = pattern.sub(f'[HIGHLIGHT]{keyword.upper()}[/HIGHLIGHT]', result)

        return result


class Paginator:
    """Handle pagination of results"""

    def __init__(self, items: List, page_size: int = 10):
        """
        Initialize paginator

        Args:
            items: List of items to paginate
            page_size: Number of items per page
        """
        self.items = items
        self.page_size = max(1, page_size)
        self.total_items = len(items)
        self.total_pages = (self.total_items + self.page_size - 1) // self.page_size
        self.current_page = 1

    def get_page(self, page_number: int) -> Tuple[List, Dict]:
        """
        Get items for a specific page

        Args:
            page_number: Page number (1-indexed)

        Returns:
            Tuple of (items_on_page, page_info)
        """
        page_number = max(1, min(page_number, self.total_pages or 1))
        self.current_page = page_number

        start_idx = (page_number - 1) * self.page_size
        end_idx = start_idx + self.page_size

        items_on_page = self.items[start_idx:end_idx]

        page_info = {
            'current_page': page_number,
            'total_pages': self.total_pages,
            'page_size': self.page_size,
            'total_items': self.total_items,
            'start_index': start_idx + 1,
            'end_index': min(end_idx, self.total_items),
            'has_next': page_number < self.total_pages,
            'has_prev': page_number > 1
        }

        return items_on_page, page_info

    def next_page(self) -> Tuple[List, Dict]:
        """Get next page"""
        return self.get_page(self.current_page + 1)

    def prev_page(self) -> Tuple[List, Dict]:
        """Get previous page"""
        return self.get_page(self.current_page - 1)

    def first_page(self) -> Tuple[List, Dict]:
        """Get first page"""
        return self.get_page(1)

    def last_page(self) -> Tuple[List, Dict]:
        """Get last page"""
        return self.get_page(self.total_pages)


class FavoritesManager:
    """Manage favorite articles"""

    def __init__(self, file_path: str = 'favorites.json'):
        """
        Initialize favorites manager

        Args:
            file_path: Path to favorites JSON file
        """
        self.file_path = Path(file_path)
        self.favorites = self._load_favorites()

    def _load_favorites(self) -> List[Dict]:
        """Load favorites from file"""
        if not self.file_path.exists():
            return []

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save_favorites(self) -> bool:
        """
        Save favorites to file

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.favorites, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False

    def add_favorite(self, article: Dict) -> bool:
        """
        Add article to favorites

        Args:
            article: Article dictionary

        Returns:
            True if added, False if already exists
        """
        url = article.get('url', '')
        if not url:
            return False

        # Check if already exists
        if any(fav.get('url') == url for fav in self.favorites):
            return False

        favorite = {
            'title': article.get('title', 'No Title'),
            'source': article.get('source', {}).get('name', 'Unknown'),
            'url': url,
            'description': article.get('description', ''),
            'published': article.get('publishedAt', ''),
            'saved_at': datetime.now().isoformat()
        }

        self.favorites.append(favorite)
        self._save_favorites()
        return True

    def remove_favorite(self, url: str) -> bool:
        """
        Remove article from favorites by URL

        Args:
            url: Article URL

        Returns:
            True if removed, False if not found
        """
        original_length = len(self.favorites)
        self.favorites = [fav for fav in self.favorites if fav.get('url') != url]

        if len(self.favorites) < original_length:
            self._save_favorites()
            return True
        return False

    def get_favorites(self) -> List[Dict]:
        """Get all favorites"""
        return self.favorites.copy()

    def clear_favorites(self) -> bool:
        """
        Clear all favorites

        Returns:
            True if successful
        """
        self.favorites = []
        return self._save_favorites()

    def is_favorite(self, url: str) -> bool:
        """
        Check if article is in favorites

        Args:
            url: Article URL

        Returns:
            True if in favorites
        """
        return any(fav.get('url') == url for fav in self.favorites)

    def get_count(self) -> int:
        """Get number of favorites"""
        return len(self.favorites)


def validate_input(prompt: str, valid_options: List[str], allow_empty: bool = False) -> str:
    """
    Validate user input against valid options

    Args:
        prompt: Input prompt to display
        valid_options: List of valid input values
        allow_empty: Whether to allow empty input

    Returns:
        Validated input
    """
    while True:
        user_input = input(prompt).strip()

        if allow_empty and not user_input:
            return user_input

        if user_input in valid_options:
            return user_input

        print(f"Invalid input. Please choose from: {', '.join(valid_options)}")


def get_integer_input(prompt: str, min_val: int = 1, max_val: Optional[int] = None) -> Optional[int]:
    """
    Get integer input from user with validation

    Args:
        prompt: Input prompt
        min_val: Minimum allowed value
        max_val: Maximum allowed value (optional)

    Returns:
        Validated integer or None if cancelled
    """
    while True:
        user_input = input(prompt).strip()

        if not user_input or user_input.lower() in ['q', 'quit', 'cancel']:
            return None

        try:
            value = int(user_input)

            if value < min_val:
                print(f"Value must be at least {min_val}")
                continue

            if max_val is not None and value > max_val:
                print(f"Value must be at most {max_val}")
                continue

            return value

        except ValueError:
            print("Please enter a valid number")

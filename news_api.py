"""
News API Module
Handles all interactions with the News API (newsapi.org)
"""

import os
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class NewsAPIClient:
    """Client for interacting with News API"""

    BASE_URL = "https://newsapi.org/v2"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize News API client

        Args:
            api_key: API key for News API (optional, reads from .env if not provided)
        """
        self.api_key = api_key or os.getenv('NEWS_API_KEY')
        if not self.api_key or self.api_key == 'your_api_key_here':
            raise ValueError(
                "NEWS_API_KEY not found or invalid. "
                "Please set it in .env file. "
                "Get your API key from: https://newsapi.org/register"
            )

        self.session = requests.Session()
        self.session.headers.update({
            'X-Api-Key': self.api_key,
            'User-Agent': 'News-Dashboard/1.0'
        })

    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """
        Make HTTP request to News API

        Args:
            endpoint: API endpoint (e.g., 'top-headlines', 'everything')
            params: Query parameters

        Returns:
            JSON response as dictionary

        Raises:
            requests.exceptions.RequestException: On network errors
            ValueError: On API errors
        """
        url = f"{self.BASE_URL}/{endpoint}"

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Check API-specific errors
            if data.get('status') == 'error':
                error_code = data.get('code', 'unknown')
                error_message = data.get('message', 'Unknown error')
                raise ValueError(f"API Error [{error_code}]: {error_message}")

            return data

        except requests.exceptions.Timeout:
            raise requests.exceptions.RequestException("Request timed out. Please check your internet connection.")
        except requests.exceptions.ConnectionError:
            raise requests.exceptions.RequestException("Connection error. Please check your internet connection.")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise ValueError("Invalid API key. Please check your NEWS_API_KEY in .env file.")
            elif e.response.status_code == 429:
                raise ValueError("Rate limit exceeded. Please wait before making more requests.")
            else:
                raise requests.exceptions.RequestException(f"HTTP Error: {e}")

    def get_top_headlines(
        self,
        country: str = 'us',
        category: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict:
        """
        Get top headlines

        Args:
            country: Country code (e.g., 'us', 'gb', 'in')
            category: News category (business, entertainment, general, health, science, sports, technology)
            page: Page number for pagination
            page_size: Number of results per page (max 100)

        Returns:
            Dictionary containing articles and metadata
        """
        params = {
            'country': country,
            'page': page,
            'pageSize': min(page_size, 100)
        }

        if category:
            valid_categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
            if category.lower() not in valid_categories:
                raise ValueError(f"Invalid category. Must be one of: {', '.join(valid_categories)}")
            params['category'] = category.lower()

        return self._make_request('top-headlines', params)

    def search_news(
        self,
        query: str,
        language: str = 'en',
        sort_by: str = 'publishedAt',
        page: int = 1,
        page_size: int = 20,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Dict:
        """
        Search for news articles

        Args:
            query: Search keywords or phrases
            language: Language code (e.g., 'en', 'es', 'fr')
            sort_by: Sort order (relevancy, popularity, publishedAt)
            page: Page number for pagination
            page_size: Number of results per page (max 100)
            from_date: Start date (ISO 8601 format, e.g., '2024-01-01')
            to_date: End date (ISO 8601 format)

        Returns:
            Dictionary containing articles and metadata
        """
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty")

        params = {
            'q': query.strip(),
            'language': language,
            'sortBy': sort_by,
            'page': page,
            'pageSize': min(page_size, 100)
        }

        if from_date:
            params['from'] = from_date
        if to_date:
            params['to'] = to_date

        return self._make_request('everything', params)

    def get_sources(
        self,
        category: Optional[str] = None,
        language: str = 'en',
        country: Optional[str] = None
    ) -> Dict:
        """
        Get available news sources

        Args:
            category: Filter by category
            language: Filter by language code
            country: Filter by country code

        Returns:
            Dictionary containing available sources
        """
        params = {
            'language': language
        }

        if category:
            params['category'] = category.lower()
        if country:
            params['country'] = country

        return self._make_request('top-headlines/sources', params)

    def get_headlines_by_source(
        self,
        sources: List[str],
        page: int = 1,
        page_size: int = 20
    ) -> Dict:
        """
        Get headlines from specific sources

        Args:
            sources: List of source IDs (e.g., ['bbc-news', 'cnn'])
            page: Page number for pagination
            page_size: Number of results per page

        Returns:
            Dictionary containing articles and metadata
        """
        if not sources:
            raise ValueError("At least one source must be specified")

        params = {
            'sources': ','.join(sources),
            'page': page,
            'pageSize': min(page_size, 100)
        }

        return self._make_request('top-headlines', params)

    def close(self):
        """Close the HTTP session"""
        self.session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


def validate_api_key(api_key: str) -> bool:
    """
    Validate if API key is properly formatted and works

    Args:
        api_key: The API key to validate

    Returns:
        True if valid, False otherwise
    """
    if not api_key or len(api_key) < 32:
        return False

    try:
        client = NewsAPIClient(api_key)
        # Try a simple request
        client.get_top_headlines(page_size=1)
        client.close()
        return True
    except Exception:
        return False

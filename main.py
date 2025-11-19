"""
News Dashboard - Main Application
A sleek terminal-based news aggregator using News API
"""

import sys
from typing import Optional, List, Dict
from news_api import NewsAPIClient
from utils import ArticleFormatter, Paginator, FavoritesManager
from ui import NewsUI


class NewsApp:
    """Main application class for News Dashboard"""

    def __init__(self):
        """Initialize the application"""
        self.api_client: Optional[NewsAPIClient] = None
        self.favorites = FavoritesManager()
        self.ui = NewsUI()
        self.running = False

    def initialize(self) -> bool:
        """
        Initialize API client and validate configuration

        Returns:
            True if successful, False otherwise
        """
        try:
            self.api_client = NewsAPIClient()
            return True
        except ValueError as e:
            self.ui.show_error(str(e))
            self.ui.show_info("Please update your .env file with a valid API key")
            self.ui.show_info("Get your free API key at: https://newsapi.org/register")
            return False
        except Exception as e:
            self.ui.show_error(f"Initialization failed: {e}")
            return False

    def run(self):
        """Main application loop"""
        self.ui.clear()
        self.ui.show_header()

        # Initialize API client
        if not self.initialize():
            return

        self.running = True

        while self.running:
            try:
                choice = self.ui.show_menu(self.favorites.get_count())

                if choice == "0":
                    self.exit_app()
                elif choice == "1":
                    self.view_top_headlines()
                elif choice == "2":
                    self.search_news()
                elif choice == "3":
                    self.browse_by_category()
                elif choice == "4":
                    self.browse_by_source()
                elif choice == "5":
                    self.view_favorites()

            except KeyboardInterrupt:
                self.ui.show_warning("\nOperation cancelled")
                self.ui.press_enter_to_continue()
            except Exception as e:
                self.ui.show_error(f"Unexpected error: {e}")
                self.ui.press_enter_to_continue()

    def view_top_headlines(self):
        """View top headlines"""
        self.ui.clear()
        self.ui.show_header()

        try:
            with self.ui.show_loading("Fetching top headlines"):
                response = self.api_client.get_top_headlines(page_size=100)

            articles = response.get('articles', [])

            if not articles:
                self.ui.show_info("No headlines available at the moment")
                self.ui.press_enter_to_continue()
                return

            # Format articles
            formatted_articles = [
                ArticleFormatter.format_article(article, idx + 1)
                for idx, article in enumerate(articles)
            ]

            self._display_articles_paginated(formatted_articles, "Top Headlines")

        except Exception as e:
            self.ui.show_error(f"Failed to fetch headlines: {e}")
            self.ui.press_enter_to_continue()

    def search_news(self):
        """Search for news"""
        self.ui.clear()
        self.ui.show_header()

        query = self.ui.get_search_query()

        if not query:
            self.ui.show_warning("Search cancelled")
            self.ui.press_enter_to_continue()
            return

        try:
            with self.ui.show_loading(f"Searching for '{query}'"):
                response = self.api_client.search_news(query, page_size=100)

            articles = response.get('articles', [])

            if not articles:
                self.ui.show_info(f"No results found for '{query}'")
                self.ui.press_enter_to_continue()
                return

            # Format articles and highlight keywords
            formatted_articles = []
            keywords = query.split()

            for idx, article in enumerate(articles):
                formatted = ArticleFormatter.format_article(article, idx + 1)
                # Highlight keywords in title
                formatted['title'] = ArticleFormatter.highlight_keywords(
                    formatted['title'],
                    keywords
                )
                formatted_articles.append(formatted)

            self._display_articles_paginated(formatted_articles, f"Search Results: '{query}'")

        except Exception as e:
            self.ui.show_error(f"Search failed: {e}")
            self.ui.press_enter_to_continue()

    def browse_by_category(self):
        """Browse news by category"""
        self.ui.clear()
        self.ui.show_header()

        category = self.ui.show_categories()

        if not category:
            return

        try:
            with self.ui.show_loading(f"Fetching {category} news"):
                response = self.api_client.get_top_headlines(
                    category=category,
                    page_size=100
                )

            articles = response.get('articles', [])

            if not articles:
                self.ui.show_info(f"No {category} news available")
                self.ui.press_enter_to_continue()
                return

            formatted_articles = [
                ArticleFormatter.format_article(article, idx + 1)
                for idx, article in enumerate(articles)
            ]

            self._display_articles_paginated(formatted_articles, f"{category.title()} News")

        except Exception as e:
            self.ui.show_error(f"Failed to fetch category news: {e}")
            self.ui.press_enter_to_continue()

    def browse_by_source(self):
        """Browse news by source"""
        self.ui.clear()
        self.ui.show_header()

        try:
            # Get available sources
            with self.ui.show_loading("Fetching available sources"):
                response = self.api_client.get_sources()

            sources = response.get('sources', [])

            if not sources:
                self.ui.show_info("No sources available")
                self.ui.press_enter_to_continue()
                return

            # Display sources (first 20)
            self.ui.show_info(f"Found {len(sources)} sources")
            self.ui.show_info("Popular sources: " + ", ".join([s['name'] for s in sources[:10]]))

            # For now, just show top headlines (source filtering requires specific source IDs)
            self.ui.show_info("Showing top headlines from all sources")
            self.ui.press_enter_to_continue()
            self.view_top_headlines()

        except Exception as e:
            self.ui.show_error(f"Failed to fetch sources: {e}")
            self.ui.press_enter_to_continue()

    def view_favorites(self):
        """View saved favorite articles"""
        self.ui.clear()
        self.ui.show_header()

        favorites = self.favorites.get_favorites()

        if not favorites:
            self.ui.show_info("No saved favorites yet")
            self.ui.show_info("Save articles by pressing 's' while browsing news")
            self.ui.press_enter_to_continue()
            return

        # Format favorites
        formatted_articles = [
            {
                'index': idx + 1,
                'title': fav['title'],
                'source': fav['source'],
                'description': fav.get('description', ''),
                'url': fav['url'],
                'published': ArticleFormatter.format_date(fav.get('published', '')),
                'author': 'Unknown'
            }
            for idx, fav in enumerate(favorites)
        ]

        self._display_articles_paginated(formatted_articles, "My Favorites", allow_save=False)

    def _display_articles_paginated(
        self,
        articles: List[Dict],
        title: str,
        allow_save: bool = True
    ):
        """
        Display articles with pagination

        Args:
            articles: List of formatted articles
            title: Display title
            allow_save: Whether to allow saving to favorites
        """
        paginator = Paginator(articles, page_size=10)
        current_articles = articles

        while True:
            self.ui.clear()
            self.ui.show_header()

            page_articles, page_info = paginator.get_page(paginator.current_page)

            self.ui.show_articles_table(page_articles, page_info)

            action = self.ui.show_pagination_menu(page_info)

            if action == 'n' and page_info['has_next']:
                paginator.next_page()
            elif action == 'p' and page_info['has_prev']:
                paginator.prev_page()
            elif action == 'v':
                self._view_article_detail(page_articles)
            elif action == 's' and allow_save:
                self._save_article_to_favorites(page_articles)
            elif action == 'o':
                self._open_article_in_browser(page_articles)
            elif action == 'b':
                break

    def _view_article_detail(self, articles: List[Dict]):
        """View detailed article"""
        article_num = self.ui.get_number_input(
            "Enter article number to view",
            min_val=1,
            max_val=len(articles)
        )

        if article_num is None:
            return

        article = articles[article_num - 1]
        is_favorite = self.favorites.is_favorite(article['url'])

        self.ui.clear()
        self.ui.show_header()
        self.ui.show_article_detail(article, is_favorite)
        self.ui.press_enter_to_continue()

    def _save_article_to_favorites(self, articles: List[Dict]):
        """Save article to favorites"""
        article_num = self.ui.get_number_input(
            "Enter article number to save",
            min_val=1,
            max_val=len(articles)
        )

        if article_num is None:
            return

        article = articles[article_num - 1]

        # Create article object for saving
        article_to_save = {
            'title': article['title'],
            'source': {'name': article['source']},
            'url': article['url'],
            'description': article.get('description', ''),
            'publishedAt': article.get('published', '')
        }

        if self.favorites.add_favorite(article_to_save):
            self.ui.show_success("Article saved to favorites!")
        else:
            self.ui.show_warning("Article already in favorites")

        self.ui.press_enter_to_continue()

    def _open_article_in_browser(self, articles: List[Dict]):
        """Open article in browser"""
        article_num = self.ui.get_number_input(
            "Enter article number to open",
            min_val=1,
            max_val=len(articles)
        )

        if article_num is None:
            return

        article = articles[article_num - 1]
        url = article.get('url', '')

        if not url:
            self.ui.show_error("No URL available for this article")
            self.ui.press_enter_to_continue()
            return

        if self.ui.open_url(url):
            self.ui.show_success("Article opened in browser!")
        else:
            self.ui.show_error("Failed to open browser")
            self.ui.show_info(f"URL: {url}")

        self.ui.press_enter_to_continue()

    def exit_app(self):
        """Exit the application"""
        self.ui.clear()
        self.ui.show_goodbye()
        self.running = False

        if self.api_client:
            self.api_client.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.api_client:
            self.api_client.close()


def main():
    """Application entry point"""
    try:
        app = NewsApp()
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

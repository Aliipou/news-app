"""
Integration test to verify all components work together
"""

import sys
from news_api import NewsAPIClient
from utils import ArticleFormatter, Paginator, FavoritesManager
from ui import NewsUI
from main import NewsApp


def test_imports():
    """Test all imports are successful"""
    print("Testing imports...")
    print("  news_api module: OK")
    print("  utils module: OK")
    print("  ui module: OK")
    print("  main module: OK")
    return True


def test_api_client_creation():
    """Test API client can be created"""
    print("\nTesting API client creation...")
    try:
        # This will fail if no API key is set, which is expected
        client = NewsAPIClient()
        print("  API client created: OK")
        client.close()
        return True
    except ValueError as e:
        if "NEWS_API_KEY" in str(e):
            print(f"  API client validation: OK (API key required)")
            return True
        raise


def test_formatter():
    """Test article formatter"""
    print("\nTesting article formatter...")
    test_article = {
        'title': 'Test Article',
        'source': {'name': 'Test Source'},
        'author': 'John Doe',
        'description': 'Test description',
        'url': 'https://test.com',
        'publishedAt': '2024-01-15T10:30:00Z',
        'content': 'Test content'
    }

    formatted = ArticleFormatter.format_article(test_article, 1)
    assert formatted['title'] == 'Test Article'
    assert formatted['source'] == 'Test Source'
    print("  Article formatting: OK")
    return True


def test_paginator():
    """Test paginator"""
    print("\nTesting paginator...")
    items = list(range(25))
    paginator = Paginator(items, page_size=10)

    assert paginator.total_pages == 3
    page_items, page_info = paginator.get_page(1)
    assert len(page_items) == 10
    assert page_info['has_next'] is True
    print("  Pagination: OK")
    return True


def test_favorites_manager():
    """Test favorites manager"""
    print("\nTesting favorites manager...")
    import tempfile
    import os

    temp_file = tempfile.mktemp(suffix='.json')
    try:
        manager = FavoritesManager(temp_file)
        assert manager.get_count() == 0

        test_article = {
            'title': 'Test',
            'source': {'name': 'Source'},
            'url': 'https://test.com'
        }

        manager.add_favorite(test_article)
        assert manager.get_count() == 1
        assert manager.is_favorite('https://test.com')
        print("  Favorites management: OK")
        return True
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_ui_components():
    """Test UI components"""
    print("\nTesting UI components...")
    ui = NewsUI()

    # Test color scheme
    assert 'primary' in NewsUI.COLORS
    assert 'success' in NewsUI.COLORS

    print("  UI components: OK")
    return True


def test_app_creation():
    """Test main app can be created"""
    print("\nTesting app creation...")
    app = NewsApp()
    assert app.favorites is not None
    assert app.ui is not None
    print("  App creation: OK")
    return True


def run_all_tests():
    """Run all integration tests"""
    print("=" * 60)
    print("INTEGRATION TEST SUITE")
    print("=" * 60)

    tests = [
        test_imports,
        test_api_client_creation,
        test_formatter,
        test_paginator,
        test_favorites_manager,
        test_ui_components,
        test_app_creation
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"  FAILED: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print("\nAll integration tests passed!")
        print("The application is ready to use.")
        print("\nTo run the application:")
        print("  1. Add your News API key to .env file")
        print("  2. Run: python main.py")
        return True
    else:
        print("\nSome tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

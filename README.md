# News Dashboard

A sleek, terminal-based news aggregator that provides real-time access to global news using the News API. Built with Python and featuring a beautiful command-line interface powered by the Rich library.

## Features

- **Top Headlines**: Browse the latest breaking news from around the world
- **Smart Search**: Search for news by keywords with highlighted results
- **Category Filtering**: Filter news by topic (business, technology, sports, etc.)
- **Source Browsing**: View available news sources and filter by source
- **Favorites System**: Save interesting articles for later reading
- **Pagination**: Navigate through results efficiently with paginated views
- **Browser Integration**: Open articles directly in your default browser
- **Sleek UI**: Beautiful terminal interface with colors, tables, and panels

## 

The application features:
- Colorful ASCII art header
- Organized menu system with numbered options
- Beautiful table layouts for news articles
- Highlighted search terms in results
- Interactive pagination controls
- Real-time loading indicators

## Requirements

- Python 3.11 or higher
- News API key (free tier available)
- Internet connection

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/aliipou/news-dashboard.git
cd news-dashboard
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get Your News API Key

1. Visit [News API](https://newsapi.org/register)
2. Register for a free account
3. Copy your API key

### 4. Configure Environment

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` and add your API key:
   ```
   NEWS_API_KEY=your_actual_api_key_here
   ```

## Usage

### Running the Application

```bash
python main.py
```

### Main Menu Options

1. **Top Headlines** - View latest breaking news
2. **Search News** - Search by keywords
3. **Browse by Category** - Filter by topic
4. **Browse by Source** - View news from specific sources
5. **My Favorites** - View saved articles
6. **Exit** - Quit the application

### Navigation Controls

When viewing articles:
- `n` - Next page
- `p` - Previous page
- `v` - View article details
- `s` - Save to favorites
- `o` - Open in browser
- `b` - Back to main menu

### Search Tips

- Use specific keywords for better results (e.g., "Python programming")
- Keywords are highlighted in search results
- Results are sorted by publication date

### Categories Available

- Business & Finance
- Entertainment & Arts
- General News
- Health & Medicine
- Science & Technology
- Sports
- Technology & Innovation

## Project Structure

```
news-dashboard/
│
├── .env                 # API key configuration (not committed)
├── .env.example         # Example environment file
├── .gitignore          # Git ignore rules
├── requirements.txt     # Python dependencies
├── README.md           # This file
│
├── main.py             # Application entry point
├── news_api.py         # News API client
├── ui.py               # Terminal UI components
├── utils.py            # Utility functions
│
├── tests/              # Unit tests
│   ├── __init__.py
│   ├── test_news_api.py
│   ├── test_ui.py
│   └── test_utils.py
│
└── favorites.json      # Saved articles (auto-generated)
```

## Architecture

### Modular Design

The application follows a clean, modular architecture:

**news_api.py** - API Layer
- `NewsAPIClient`: Handles all News API interactions
- Comprehensive error handling for network issues
- Support for multiple endpoints (headlines, search, sources)
- Configurable pagination and filtering

**utils.py** - Business Logic
- `ArticleFormatter`: Format articles for display
- `Paginator`: Handle result pagination
- `FavoritesManager`: Manage saved articles
- Helper functions for input validation

**ui.py** - Presentation Layer
- `NewsUI`: All UI components and styling
- Beautiful tables, panels, and menus using Rich
- Color-coded messages and indicators
- Responsive layouts

**main.py** - Application Controller
- `NewsApp`: Main application orchestrator
- Menu navigation and user interaction
- Integration of all components

### Error Handling

The application includes robust error handling:
- Network timeout and connection errors
- Invalid API key detection
- API rate limiting notifications
- Malformed data handling
- User input validation

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Test Coverage

- 87 comprehensive unit tests
- Coverage of all major components
- Mock-based testing for API calls
- Edge case validation

### Test Modules

- `test_news_api.py`: API client tests (22 tests)
- `test_ui.py`: UI component tests (22 tests)
- `test_utils.py`: Utility function tests (43 tests)

## API Limits

The free tier of News API includes:
- 100 requests per day
- Access to articles from the last 30 days
- Attribution required

For higher limits, consider upgrading to a paid plan.

## Troubleshooting

### "NEWS_API_KEY not found" Error

Make sure you've:
1. Created a `.env` file in the project root
2. Added your API key: `NEWS_API_KEY=your_key_here`
3. The key is at least 32 characters long

### "Rate limit exceeded" Error

You've exceeded the daily request limit. Wait until the next day or upgrade your API plan.

### Network Errors

- Check your internet connection
- Verify News API is not down: [News API Status](https://newsapi.org/status)
- Try again with a longer timeout

### No Articles Found

- Try different keywords or categories
- Some categories may have limited content
- Verify your search terms are in English (or specify language parameter)

## Development

### Adding New Features

The modular design makes it easy to extend:

**Add a new menu option:**
1. Update `ui.py` - Add menu item to `show_menu()`
2. Update `main.py` - Add handler method in `NewsApp`
3. Wire up in `run()` method

**Add new API endpoints:**
1. Add method to `NewsAPIClient` in `news_api.py`
2. Add corresponding tests in `test_news_api.py`

**Customize UI:**
- Modify colors in `NewsUI.COLORS` dictionary
- Update table layouts in respective `show_*` methods
- Change box styles using Rich box types

### Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters
- Write docstrings for all public methods
- Keep functions focused and single-purpose

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Ensure all tests pass
6. Submit a pull request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- [News API](https://newsapi.org/) - Providing the news data
- [Rich](https://github.com/Textualize/rich) - Beautiful terminal formatting
- [Prompt Toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) - Interactive prompts

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section

## Roadmap

Potential future enhancements:
- AI-powered article summaries
- Sentiment analysis of news
- Export articles to PDF/Markdown
- Multi-language support
- Web interface (Flask/FastAPI)
- News notifications
- Historical data analysis
- Custom news feeds

---

**Made with Python | Powered by News API | Terminal UI by Rich**

"""
UI Module
Sleek terminal interface using rich library
"""

from typing import List, Dict, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown
from rich import box
from rich.align import Align
from rich.style import Style
import webbrowser

console = Console()


class NewsUI:
    """Sleek UI for News Dashboard"""

    # Color scheme
    COLORS = {
        'primary': '#00d4ff',      # Cyan
        'secondary': '#ff00ff',    # Magenta
        'success': '#00ff00',      # Green
        'warning': '#ffaa00',      # Orange
        'error': '#ff0000',        # Red
        'info': '#00aaff',         # Blue
        'title': '#ffffff',        # White
        'text': '#cccccc',         # Light gray
        'dim': '#666666',          # Dark gray
    }

    @staticmethod
    def clear():
        """Clear the console"""
        console.clear()

    @staticmethod
    def show_header():
        """Display application header with sleek design"""
        header_text = Text()
        header_text.append("\n")
        header_text.append("█▀▀▄ █▀▀ █   █ █▀▀   ", style=f"bold {NewsUI.COLORS['primary']}")
        header_text.append("█▀▀▄ █▀▀█ █▀▀ █▀▀█\n", style=f"bold {NewsUI.COLORS['secondary']}")
        header_text.append("█  █ █▀▀ █▄█ ▀▀▀   ", style=f"bold {NewsUI.COLORS['primary']}")
        header_text.append("█▄▄▀ █  █ ▀▀▀ █  █\n", style=f"bold {NewsUI.COLORS['secondary']}")
        header_text.append("\nYour Gateway to Global News", style=f"italic {NewsUI.COLORS['dim']}")

        panel = Panel(
            Align.center(header_text),
            box=box.DOUBLE,
            border_style=NewsUI.COLORS['primary'],
            padding=(1, 2)
        )
        console.print(panel)
        console.print()

    @staticmethod
    def show_menu(favorites_count: int = 0) -> str:
        """
        Display main menu and get user choice

        Args:
            favorites_count: Number of saved favorites

        Returns:
            User's menu choice
        """
        menu_items = [
            ("1", "Top Headlines", "View latest breaking news"),
            ("2", "Search News", "Search by keywords"),
            ("3", "Browse by Category", "Filter news by topic"),
            ("4", "Browse by Source", "View news from specific sources"),
            ("5", "My Favorites", f"View saved articles ({favorites_count})"),
            ("0", "Exit", "Quit application"),
        ]

        table = Table(
            show_header=True,
            header_style=f"bold {NewsUI.COLORS['primary']}",
            box=box.ROUNDED,
            border_style=NewsUI.COLORS['secondary'],
            padding=(0, 2)
        )

        table.add_column("Option", style=f"bold {NewsUI.COLORS['warning']}", width=8)
        table.add_column("Action", style=f"bold {NewsUI.COLORS['title']}", width=25)
        table.add_column("Description", style=NewsUI.COLORS['text'], width=40)

        for option, action, description in menu_items:
            table.add_row(option, action, description)

        console.print(Panel(
            table,
            title="[bold]Main Menu[/bold]",
            border_style=NewsUI.COLORS['primary'],
            box=box.DOUBLE
        ))

        choice = Prompt.ask(
            "\n[bold cyan]Enter your choice[/bold cyan]",
            choices=["0", "1", "2", "3", "4", "5"],
            default="1"
        )
        return choice

    @staticmethod
    def show_articles_table(articles: List[Dict], page_info: Dict, show_index: bool = True):
        """
        Display articles in a beautiful table

        Args:
            articles: List of formatted articles
            page_info: Pagination information
            show_index: Whether to show index column
        """
        if not articles:
            NewsUI.show_info("No articles found")
            return

        table = Table(
            show_header=True,
            header_style=f"bold {NewsUI.COLORS['primary']}",
            box=box.HEAVY_HEAD,
            border_style=NewsUI.COLORS['secondary'],
            title=f"[bold {NewsUI.COLORS['title']}]Page {page_info['current_page']}/{page_info['total_pages']}[/bold {NewsUI.COLORS['title']}]",
            caption=f"[{NewsUI.COLORS['dim']}]Showing {page_info['start_index']}-{page_info['end_index']} of {page_info['total_items']} articles[/{NewsUI.COLORS['dim']}]",
            title_style=f"bold {NewsUI.COLORS['info']}",
            caption_style=NewsUI.COLORS['dim']
        )

        if show_index:
            table.add_column("#", style=f"bold {NewsUI.COLORS['warning']}", width=4)

        table.add_column("Title", style=f"bold {NewsUI.COLORS['title']}", width=45, no_wrap=False)
        table.add_column("Source", style=NewsUI.COLORS['info'], width=20)
        table.add_column("Published", style=NewsUI.COLORS['text'], width=16)

        for idx, article in enumerate(articles, 1):
            row = []

            if show_index:
                row.append(str(article.get('index', idx)))

            # Highlight title
            title = article['title']
            if '[HIGHLIGHT]' in title:
                title = title.replace('[HIGHLIGHT]', f'[bold {NewsUI.COLORS["warning"]}]')
                title = title.replace('[/HIGHLIGHT]', '[/bold]')

            row.extend([
                title,
                article['source'],
                article['published']
            ])

            table.add_row(*row)

        console.print(table)
        console.print()

    @staticmethod
    def show_article_detail(article: Dict, is_favorite: bool = False):
        """
        Show detailed view of a single article

        Args:
            article: Article dictionary
            is_favorite: Whether article is in favorites
        """
        # Create detailed content
        content = Text()
        content.append("Title: ", style=f"bold {NewsUI.COLORS['primary']}")
        content.append(f"{article['title']}\n\n", style=f"bold {NewsUI.COLORS['title']}")

        content.append("Source: ", style=f"bold {NewsUI.COLORS['info']}")
        content.append(f"{article['source']}\n", style=NewsUI.COLORS['text'])

        content.append("Author: ", style=f"bold {NewsUI.COLORS['info']}")
        content.append(f"{article.get('author', 'Unknown')}\n", style=NewsUI.COLORS['text'])

        content.append("Published: ", style=f"bold {NewsUI.COLORS['info']}")
        content.append(f"{article['published']}\n\n", style=NewsUI.COLORS['text'])

        content.append("Description:\n", style=f"bold {NewsUI.COLORS['primary']}")
        content.append(f"{article.get('description', 'No description available')}\n\n", style=NewsUI.COLORS['text'])

        content.append("URL: ", style=f"bold {NewsUI.COLORS['info']}")
        content.append(f"{article['url']}\n", style=f"link {article['url']} {NewsUI.COLORS['secondary']}")

        if is_favorite:
            content.append("\n", style=NewsUI.COLORS['success'])
            content.append("★ ", style=f"bold {NewsUI.COLORS['warning']}")
            content.append("Saved in Favorites", style=f"bold {NewsUI.COLORS['success']}")

        panel = Panel(
            content,
            title="[bold]Article Details[/bold]",
            border_style=NewsUI.COLORS['primary'],
            box=box.DOUBLE,
            padding=(1, 2)
        )

        console.print(panel)
        console.print()

    @staticmethod
    def show_categories() -> Optional[str]:
        """
        Display category selection menu

        Returns:
            Selected category or None
        """
        categories = [
            ("1", "business", "Business & Finance"),
            ("2", "entertainment", "Entertainment & Arts"),
            ("3", "general", "General News"),
            ("4", "health", "Health & Medicine"),
            ("5", "science", "Science & Technology"),
            ("6", "sports", "Sports"),
            ("7", "technology", "Technology & Innovation"),
        ]

        table = Table(
            show_header=True,
            header_style=f"bold {NewsUI.COLORS['primary']}",
            box=box.ROUNDED,
            border_style=NewsUI.COLORS['info']
        )

        table.add_column("Option", style=f"bold {NewsUI.COLORS['warning']}", width=8)
        table.add_column("Category", style=f"bold {NewsUI.COLORS['title']}", width=20)
        table.add_column("Description", style=NewsUI.COLORS['text'], width=30)

        for option, category, description in categories:
            table.add_row(option, category.title(), description)

        console.print(Panel(
            table,
            title="[bold]Select Category[/bold]",
            border_style=NewsUI.COLORS['primary']
        ))

        choice = Prompt.ask(
            "\n[bold cyan]Select category[/bold cyan]",
            choices=[str(i) for i in range(1, 8)],
            default="1"
        )

        return categories[int(choice) - 1][1]

    @staticmethod
    def get_search_query() -> Optional[str]:
        """
        Get search query from user

        Returns:
            Search query or None
        """
        query = Prompt.ask(
            f"\n[bold {NewsUI.COLORS['primary']}]Enter search keywords[/bold {NewsUI.COLORS['primary']}]",
            default=""
        )
        return query.strip() if query else None

    @staticmethod
    def show_pagination_menu(page_info: Dict) -> str:
        """
        Show pagination controls

        Args:
            page_info: Pagination information

        Returns:
            User choice
        """
        options = []
        choices = []

        if page_info['has_prev']:
            options.append(("p", "Previous Page"))
            choices.append("p")

        if page_info['has_next']:
            options.append(("n", "Next Page"))
            choices.append("n")

        options.extend([
            ("v", "View Article Details"),
            ("s", "Save to Favorites"),
            ("o", "Open in Browser"),
            ("b", "Back to Menu")
        ])
        choices.extend(["v", "s", "o", "b"])

        menu_text = " | ".join([f"[bold {NewsUI.COLORS['warning']}]{opt}[/bold {NewsUI.COLORS['warning']}]: {desc}" for opt, desc in options])
        console.print(Panel(menu_text, border_style=NewsUI.COLORS['dim']))

        return Prompt.ask(
            f"[bold {NewsUI.COLORS['primary']}]Choose action[/bold {NewsUI.COLORS['primary']}]",
            choices=choices
        )

    @staticmethod
    def show_success(message: str):
        """Display success message"""
        console.print(f"[bold {NewsUI.COLORS['success']}]✓ {message}[/bold {NewsUI.COLORS['success']}]")

    @staticmethod
    def show_error(message: str):
        """Display error message"""
        console.print(f"[bold {NewsUI.COLORS['error']}]✗ {message}[/bold {NewsUI.COLORS['error']}]")

    @staticmethod
    def show_warning(message: str):
        """Display warning message"""
        console.print(f"[bold {NewsUI.COLORS['warning']}]⚠ {message}[/bold {NewsUI.COLORS['warning']}]")

    @staticmethod
    def show_info(message: str):
        """Display info message"""
        console.print(f"[{NewsUI.COLORS['info']}]ℹ {message}[/{NewsUI.COLORS['info']}]")

    @staticmethod
    def show_loading(message: str = "Loading"):
        """
        Show loading spinner

        Args:
            message: Loading message

        Returns:
            Progress context manager
        """
        return Progress(
            SpinnerColumn(style=NewsUI.COLORS['primary']),
            TextColumn(f"[bold {NewsUI.COLORS['info']}]{message}...[/bold {NewsUI.COLORS['info']}]"),
            transient=True,
            console=console
        )

    @staticmethod
    def confirm(message: str, default: bool = False) -> bool:
        """
        Ask for user confirmation

        Args:
            message: Confirmation message
            default: Default choice

        Returns:
            User's choice
        """
        return Confirm.ask(
            f"[bold {NewsUI.COLORS['warning']}]{message}[/bold {NewsUI.COLORS['warning']}]",
            default=default
        )

    @staticmethod
    def get_number_input(prompt: str, min_val: int = 1, max_val: Optional[int] = None) -> Optional[int]:
        """
        Get number input from user

        Args:
            prompt: Input prompt
            min_val: Minimum value
            max_val: Maximum value

        Returns:
            Number or None
        """
        while True:
            try:
                response = Prompt.ask(f"[bold {NewsUI.COLORS['primary']}]{prompt}[/bold {NewsUI.COLORS['primary']}]")

                if not response or response.lower() in ['q', 'cancel']:
                    return None

                value = int(response)

                if value < min_val:
                    NewsUI.show_error(f"Value must be at least {min_val}")
                    continue

                if max_val and value > max_val:
                    NewsUI.show_error(f"Value must be at most {max_val}")
                    continue

                return value

            except ValueError:
                NewsUI.show_error("Please enter a valid number")

    @staticmethod
    def open_url(url: str) -> bool:
        """
        Open URL in browser

        Args:
            url: URL to open

        Returns:
            True if successful
        """
        try:
            webbrowser.open(url)
            return True
        except Exception:
            return False

    @staticmethod
    def press_enter_to_continue():
        """Wait for user to press enter"""
        Prompt.ask(f"\n[{NewsUI.COLORS['dim']}]Press Enter to continue[/{NewsUI.COLORS['dim']}]", default="")

    @staticmethod
    def show_goodbye():
        """Display goodbye message"""
        goodbye_text = Text()
        goodbye_text.append("\n✨ ", style=NewsUI.COLORS['warning'])
        goodbye_text.append("Thank you for using News Dashboard!", style=f"bold {NewsUI.COLORS['primary']}")
        goodbye_text.append(" ✨\n", style=NewsUI.COLORS['warning'])
        goodbye_text.append("Stay informed, stay curious!\n", style=f"italic {NewsUI.COLORS['text']}")

        panel = Panel(
            Align.center(goodbye_text),
            border_style=NewsUI.COLORS['secondary'],
            box=box.DOUBLE
        )
        console.print(panel)

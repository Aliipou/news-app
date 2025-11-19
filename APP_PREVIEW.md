# News Dashboard - App Preview

## Application Interface

### 1. Startup Screen
```
█▀▀▄ █▀▀ █   █ █▀▀   █▀▀▄ █▀▀█ █▀▀ █▀▀█
█  █ █▀▀ █▄█ ▀▀▀   █▄▄▀ █  █ ▀▀▀ █  █

Your Gateway to Global News
```

### 2. Main Menu
```
╔════════════════════════════════════════════════════════════╗
║                        Main Menu                           ║
╠════════════════════════════════════════════════════════════╣
║ Option │ Action              │ Description                 ║
╠════════╪═════════════════════╪═════════════════════════════╣
║   1    │ Top Headlines       │ View latest breaking news   ║
║   2    │ Search News         │ Search by keywords          ║
║   3    │ Browse by Category  │ Filter news by topic        ║
║   4    │ Browse by Source    │ View news from sources      ║
║   5    │ My Favorites (0)    │ View saved articles         ║
║   0    │ Exit                │ Quit application            ║
╚════════════════════════════════════════════════════════════╝

Enter your choice: _
```

### 3. News Articles Table
```
╔════════════════════════════════════════════════════════════╗
║                    Page 1/3                                 ║
╠═══╦═══════════════════════════╦═════════════╦══════════════╣
║ # ║ Title                     ║ Source      ║ Published    ║
╠═══╬═══════════════════════════╬═════════════╬══════════════╣
║ 1 ║ Breaking: Tech Innovation ║ BBC News    ║ 2024-01-15   ║
║ 2 ║ Markets Rally Today       ║ CNN         ║ 2024-01-15   ║
║ 3 ║ Sports Championship Win   ║ ESPN        ║ 2024-01-15   ║
║...║ ...                       ║ ...         ║ ...          ║
╚═══╩═══════════════════════════╩═════════════╩══════════════╝

Showing 1-10 of 47 articles

[p: Previous Page | n: Next Page | v: View Article | s: Save | o: Open | b: Back]

Choose action: _
```

### 4. Article Details
```
╔════════════════════════════════════════════════════════════╗
║                     Article Details                         ║
╠════════════════════════════════════════════════════════════╣
║ Title: Breaking News: Major Tech Innovation Announced      ║
║                                                             ║
║ Source: BBC News                                            ║
║ Author: John Smith                                          ║
║ Published: 2024-01-15 14:30                                 ║
║                                                             ║
║ Description:                                                ║
║ A groundbreaking technology has been unveiled today that    ║
║ promises to revolutionize the industry. Experts say this... ║
║                                                             ║
║ URL: https://bbc.com/news/tech-innovation-12345             ║
║                                                             ║
║ ★ Saved in Favorites                                        ║
╚════════════════════════════════════════════════════════════╝

Press Enter to continue: _
```

### 5. Category Selection
```
╔════════════════════════════════════════════════════════════╗
║                    Select Category                          ║
╠════════════════════════════════════════════════════════════╣
║ Option │ Category      │ Description                       ║
╠════════╪═══════════════╪═══════════════════════════════════╣
║   1    │ Business      │ Business & Finance                ║
║   2    │ Entertainment │ Entertainment & Arts              ║
║   3    │ General       │ General News                      ║
║   4    │ Health        │ Health & Medicine                 ║
║   5    │ Science       │ Science & Technology              ║
║   6    │ Sports        │ Sports                            ║
║   7    │ Technology    │ Technology & Innovation           ║
╚════════════════════════════════════════════════════════════╝

Select category [1]: _
```

### 6. Search Interface
```
Enter search keywords: python programming

⣾ Searching for 'python programming'...

Results found! Displaying 32 articles.
Keywords highlighted: PYTHON PROGRAMMING
```

### 7. Messages

**Success Message:**
```
✓ Article saved to favorites!
```

**Error Message:**
```
✗ Failed to connect to News API. Please check your internet.
```

**Warning Message:**
```
⚠ Article already in favorites
```

**Info Message:**
```
ℹ Found 15 sources available
```

### 8. Loading Indicator
```
⣾ Fetching top headlines...
```

### 9. Exit Screen
```
╔════════════════════════════════════════════════════════════╗
║                                                             ║
║  ✨ Thank you for using News Dashboard! ✨                  ║
║  Stay informed, stay curious!                               ║
║                                                             ║
╚════════════════════════════════════════════════════════════╝
```

## Color Scheme

- **Primary (Cyan)**: Headers, borders, highlights
- **Secondary (Magenta)**: Accents, decorations
- **Success (Green)**: Confirmation messages
- **Warning (Orange)**: Caution messages
- **Error (Red)**: Error messages
- **Info (Blue)**: Information messages
- **Title (White)**: Main text, titles
- **Text (Light Gray)**: Body text
- **Dim (Dark Gray)**: Subtle information

## Key Features Shown

1. **Beautiful ASCII Art Header** - Eye-catching branding
2. **Organized Tables** - Clean data presentation
3. **Color Coding** - Visual hierarchy and feedback
4. **Loading Indicators** - User feedback during operations
5. **Pagination** - Easy navigation through results
6. **Interactive Prompts** - Clear user guidance
7. **Rich Formatting** - Professional appearance
8. **Responsive Layout** - Adapts to content

## User Experience Highlights

- **Intuitive Navigation**: Numbered menus and clear options
- **Visual Feedback**: Colors indicate success/error states
- **Progressive Disclosure**: Details shown when needed
- **Keyboard Shortcuts**: Single-key actions for efficiency
- **Error Handling**: Friendly error messages with guidance
- **Responsive Design**: Works in any terminal size

---

**The interface is designed to be both beautiful and functional!**

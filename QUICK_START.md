# Quick Start Guide

Get the News Dashboard running in 3 minutes!

## Prerequisites

- Python 3.11+ installed
- Internet connection
- A News API key (free)

## Step 1: Get Your API Key (2 minutes)

1. Visit: https://newsapi.org/register
2. Fill in the registration form
3. Verify your email
4. Copy your API key (looks like: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)

## Step 2: Configure the App (30 seconds)

1. Open the `.env` file in this directory
2. Replace `your_api_key_here` with your actual API key:
   ```
   NEWS_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
   ```
3. Save the file

## Step 3: Install Dependencies (30 seconds)

```bash
pip install -r requirements.txt
```

## Step 4: Run the App!

```bash
python main.py
```

## First Time Using the App?

Try these actions:

1. **Press `1`** to view top headlines
2. **Press `v`** then enter an article number to see details
3. **Press `s`** then enter an article number to save to favorites
4. **Press `2`** to search (try searching for "technology")
5. **Press `o`** then enter an article number to open in browser

## Troubleshooting

### "NEWS_API_KEY not found" error?
- Check that `.env` file exists
- Make sure you replaced `your_api_key_here` with your actual key
- Verify the key has no extra spaces

### "Rate limit exceeded" error?
- Free tier has 100 requests/day limit
- Wait until tomorrow or upgrade your API plan

### Can't see colored output?
- Make sure you're using a modern terminal
- Windows: Use Windows Terminal or PowerShell
- Mac/Linux: Default terminal should work fine

## What's Next?

- Browse by category (option 3)
- Build your favorites collection
- Open articles in your browser
- Explore different search terms

## Need Help?

- Check `README.md` for full documentation
- Review `PROJECT_SUMMARY.md` for technical details
- Run tests: `pytest tests/ -v`

---

**Enjoy staying informed with News Dashboard!**

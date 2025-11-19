1. Core Idea

Your program should:

Fetch and display live news (top headlines) from News API.

Search for news via user input (keywords, categories, sources).

Present results beautifully: readable, organized, maybe even interactive.

Be extendable: modular design so you can add more features later (e.g., sentiment analysis, saving favorite news, notifications).

Innovation:

Terminal-based UI using rich library → interactive, colorful, neat.

Optional: simple web interface with Flask/FastAPI → looks professional.

Optional: integrate AI summary of articles (like GPT summarizing headlines).

2. Tech Stack

Backend & API: Python 3.11+, requests for API calls

UI:

Terminal: rich + prompt-toolkit for menus

Web (optional): Flask or FastAPI + Jinja2 templates + Bootstrap for styling

Environment: .env + python-dotenv to hide API key

Version control: Git + GitHub (public repo, key hidden)

3. Functional Design

Terminal UI version:

=============================
     NEWS DASHBOARD
=============================
1. View Top Headlines
2. Search News
3. Filter by Category / Source
0. Exit
=============================
Enter choice: _


Features:

Fetch current news and display in table with rich.Table: title, source, date.

Search news with keyword(s) → results paginated 5–10 per page.

Optional: Highlight keywords in titles.

Optional: Fetch article summary (AI or simple text truncation).

Save favorite articles locally (JSON file) → later you can show “My Favorites”.

4. Project Structure
news-dashboard/
│
├─ .env                 # API key hidden
├─ main.py              # entry point
├─ news_api.py          # API interaction functions
├─ ui.py                # terminal interface functions
├─ utils.py             # helper functions (formatting, pagination)
├─ requirements.txt
└─ README.md


Design Principle:

Modular → easy to extend

Clean code → professional portfolio level

Well-documented → anyone can run it

5. Innovative Touches

Colorful UI: use rich to make headlines, sources, dates visually distinct.

Search filters: user can filter by language, category, source.

Paginated results: prevents flooding terminal with hundreds of news.

Favorites system: let user save interesting articles locally.

Optional AI summary: GPT API integration to summarize articles quickly.

Deployment-ready: can run terminal app locally or simple Flask web interface online.

6. Next Step

If you want, I can write a full starter Python project:

Fully functional terminal app

Modular design

API key hidden

Paginated search results

Pretty tables and menus with rich
---------------------
Task Description Your task is to create a program that retrieves news from the News API. First look in to the API’s documentation and how to get data from the API. Also look into GitHub. You are free to choose which programming languages and technologies you want to use for this. The program should have following functionalities: Get all the current news from the API and show them to user Get all the news from the API with user given search parameter. Show results to the user. This task will be evaluated based on the functionalities, user interface and documentation. After you have developed the functionalities, you should focus more on the user interface and documentation. General steps Check the documentation of the News API from this link: Get started - Documentation - News API. Register to the platform and get yourself an API key Create yourself a public repository in GitHub and start your project Choose the programming languages and technologies you feel best to fit for this project. Remember to hide your API key from your public GitHub repository Develop the functionalities mentioned above to your program. Create a README.md file for documentation to your GitHub repository. Return the task by following the instructions below.
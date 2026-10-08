---
name: Add a New Scraper
description: Use this skill when the user asks to add a new data source or scraper to the AI News Aggregator pipeline.
---

# Instructions for Adding a New Scraper

When the user asks to add a new scraper (e.g., Reddit, HackerNews, Twitter), follow these strict architectural guidelines:

1. **File Location**: Create the new scraper in the `app/scrapers/` directory.
2. **Naming Convention**: Name the file descriptively (e.g., `reddit_scraper.py`).
3. **Class Structure**: 
   - The scraper must be a class (e.g., `RedditScraper`).
   - It must implement a `fetch_articles(self) -> List[dict]` method.
4. **Data Format**: The dictionaries returned by `fetch_articles` MUST contain at minimum the following keys:
   - `id`: A unique identifier (e.g., the URL or a hash).
   - `title`: The title of the article/post.
   - `url`: The link to the content.
   - `content`: A brief snippet or description.
5. **Error Handling**: The scraper must wrap external network calls in a `try/except` block. If the source is down, log the error and return an empty list `[]` to prevent crashing the pipeline.
6. **Registration**: After creating the scraper, you must import and initialize it inside the main orchestrator (usually `app/daily_runner.py` or `main.py`).

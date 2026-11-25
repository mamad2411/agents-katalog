---
name: github-trending-scraper
description: Scrape GitHub Trending repositories and save to JSON files. Use when the user wants to fetch GitHub trending projects, get popular repositories, scrape trending lists, or requests "get GitHub trending", "scrape GitHub popular projects", or "fetch trending repos" for daily, weekly, or monthly periods.
---

# GitHub Trending Scraper

Scrape GitHub Trending repositories across different time periods (daily, weekly, monthly) and save structured data to JSON files.

## Usage

Run the scraper script to fetch trending repositories:

```bash
python scripts/github_trending_scraper.py
```

The script will:
1. Scrape trending repositories for all three periods (daily, weekly, monthly)
2. Extract project metadata: name, URL, description, language, stars, forks
3. Save results to `github_trending.json` in the current directory
4. Display statistics about scraped projects

## Output Format

The generated JSON file contains:

```json
{
  "update_time": "2026-02-09 10:30:00",
  "data": {
    "daily": [...],
    "weekly": [...],
    "monthly": [...]
  }
}
```

Each project includes:
- `name`: Repository full name (owner/repo)
- `url`: GitHub repository URL
- `description`: Project description
- `language`: Primary programming language
- `stars`: Total star count
- `forks`: Total fork count
- `stars_daily/weekly/monthly`: New stars in the period

## Dependencies

Install required packages:

```bash
pip install requests beautifulsoup4
```

Or use the provided requirements file:

```bash
pip install -r requirements.txt
```

## Customization

To scrape only specific periods, modify the `periods` list in the `main()` function of the script.

To change the output filename, modify the `output_file` variable in the script.

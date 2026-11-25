---
name: explore-github-trending
description: Explore repositories trending on GitHub by language and time range
argument-hint: "[language] [daily|weekly|monthly]"
related:
  - search
  - report
  - enhance-prompt
  - ask-me

---

## Goal

Explore repositories trending on GitHub by language, category, and time range

## Scope

- Use the GitHub Trending page (`https://github.com/trending`)
- Support filtering by programming language
- Support time ranges `daily`, `weekly`, `monthly`
- Fetch data via web scraping or search
- No login required

## Execute

### 1. Parse Input

> Goal: determine language and time range

1. Take `language` and `time range` from the argument
2. If language is not given → use `all` (no language filter)
3. If time range is not given → default to `daily`
4. If language is unclear → use `/enhance-prompt` or `/ask-me`

### 2. Build Trending URL

> Goal: build the URL for GitHub Trending

1. base URL: `https://github.com/trending`
2. If a language is given → add `?l=<language>`
3. If a time range is given → add `&since=<daily|weekly|monthly>`
4. Example: `https://github.com/trending?l=typescript&since=weekly`

### 3. Fetch Trending Page

> Goal: fetch data from GitHub Trending

1. Use `webfetch` or `crw_scrape` to pull the HTML from the URL
2. If scraping fails → use `web_search` for `site:github.com/trending <language>`
3. If redirected → follow the redirect to the new page
4. Verify HTTP status 200

### 4. Parse Repositories

> Goal: extract repo data from the HTML

1. Find the list of repo cards (usually in `article` or `h2 > a`)
2. Extract for each repo:
   - `owner/repo` from `href`
   - `description` from the paragraph under the repo name
   - `language` from the badge
   - `stars today` from stars added during the period
   - `total stars` if shown
   - `forks` if shown
3. Keep the order shown on the page
4. If the HTML changes, fall back to `search-files-patterns` or regex

### 5. Format Output

> Goal: present results readably

1. Use `/report` to build a table
2. Columns: `No.`, `Repository`, `Description`, `Language`, `Stars Today`, `Total Stars`, `Forks`
3. Order by `No.` following the GitHub Trending page order
4. If more than 25 entries → show the top 25 and note how many remain

### 6. Deep Dive Or Open

> Goal: let the user inspect a repo of interest

1. If the user names a repo → open `/open-github <owner>/<repo>`
2. To search GitHub stars → use `/search-github-star <repo>`
3. To view releases → open `https://github.com/<owner>/<repo>/releases`

## Rules

### 1. URL Construction

- base: `https://github.com/trending`
- language: `?l=<language>`
- time: `&since=daily|weekly|monthly`
- If no language → `?since=daily`

### 2. No Authentication

- No `gh auth` needed
- GitHub Trending is viewable without login
- If a login page appears → notify the user

### 3. Parsing Resilience

- If a selector is not found → try regex or string match
- If GitHub changes the layout → use `web_search` instead or stop and report
- Never hardcode HTML node indexes

### 4. Rate and Cache

- Do not fetch too often (no more than once per task)
- If the user repeats the same time range, reuse the previous result while fresh (within 1 hour)

### 5. Output

- Use `/report` or a markdown table
- Show the URL used for the fetch
- State the time range (daily/weekly/monthly) and language

- Use /open-web if needed

## Expected Outcome

- A list of trending repositories on GitHub
- Language, stars today, description data
- Presented as a table
- Repos of interest can be opened

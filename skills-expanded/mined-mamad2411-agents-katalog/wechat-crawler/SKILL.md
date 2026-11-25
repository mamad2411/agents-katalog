---
name: wechat-crawler
description: "Crawls articles from WeChat Official Accounts, along with their statistics (read count, likes, \"Worth Reading\" count, share count) and comment data. Users only need to provide their browser Cookie; the program will automatically extract the Token, verify API availability, and then crawl all articles of the target Official Account.Built with Selenium + BeautifulSoup, it supports intelligent Cookie management: it prioritizes the user-provided browser Cookie, automatically converts its format, and stores the Cookie in the database for persistence."
author: huoy348
tags:
  - crawler
  - wechat
  - spider
  - selenium
---

# wechat-crawler
Crawl WeChat official account articles, statistics and comments automatically.


# wechat-crawler - Skill

Crawls articles from WeChat Official Accounts, along with their statistics (read count, likes, "Worth Reading" count, share count) and comment data.

## Features

- ✅ **One‑click operation**: Users only need to provide the browser cookie – the token is automatically extracted. No manual token input required.
- ✅ **Auto‑validation**: After token extraction, the API availability is automatically verified to prevent wasting time on invalid cookies.
- ✅ **Full crawl**: Once validation passes, the tool directly crawls all configured articles from the database.
- ✅ **Browser cookie import**: Users export cookies from Chrome; the tool auto‑detects the format and converts it.
- ✅ **Multiple format support**: DevTools JSON format / Application panel domain format / Request header string format / Netscape format.
- ✅ **Expiration reminder**: When a database cookie expires, the user is prompted to provide a fresh browser cookie – no rigid browser launch required.
- ✅ **Intelligent cookie management**: Converted cookies are automatically saved to the database for future reuse.
- ✅ **Article content extraction**: Extracts body text, title, and publication time.
- ✅ **Statistics retrieval**: Read count, like count, "Worth Reading" count, share count.
- ✅ **Comment crawling**: Retrieves comment data for articles.
- ✅ **Database storage**: Automatically saves to MySQL.
- ✅ **QR‑code login (fallback)**: Legacy browser‑based QR login is retained as a backup.

## Triggers

- User requests to crawl, scrape, or collect WeChat Official Account articles.
- User requests to monitor updates of a specific Official Account.
- User requests to obtain read counts, comments, or other data from Official Account articles.
- User mentions "WeChat crawler", "Official Account articles", or "WeChat crawler".

## Directory Structure

```
wechat-crawler/
├── config.py             # Configuration (database connection)
├── db_operations.py      # Database operations module
├── cookie_utils.py       # [New] Cookie format conversion utilities
├── crawler.py            # Core crawler logic (new Cookie management workflow)
├── run_crawler.py        # Entry point (supports CLI arguments)
├── debug_crawler.py      # Debug script
├── requirements.txt      # Dependencies
└── SKILL.md              # This document
```




## Cookie Management Workflow (New)

```
┌─────────────────────────────────────────────────────────────┐
│   User provides browser Cookie                              │
│   --cookie-json / --cookie-domain / --cookie-str           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  [Auto] Detect Cookie format → Convert to dict → Load into Session │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  [Auto] Visit mp.weixin.qq.com to extract Token            │
│  (No manual --token argument required)                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  [Auto] Quick API availability validation                  │
│  Search for test keyword → Check API response code         │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
         Validation Passed               Validation Failed
              │                               │
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────────┐
│  Save Cookie to DB      │     │  Prompt Cookie expired      │
│  Reusable next time     │     │  Guide user to obtain fresh │
└─────────────────────────┘     │  browser Cookie             │
              │                 └─────────────────────────────┘
              ▼
┌─────────────────────────────────────────────────────────────┐
│  Start crawling (all Official Accounts)                     │
│  1. Iterate over all enabled Official Accounts in crawl_tasks │
│  2. Search for Official Account to obtain fakeid            │
│  3. Retrieve article list                                   │
│  4. Crawl each article: content + stats + comments          │
│  5. Save to database                                        │
└─────────────────────────────────────────────────────────────┘
```



## Quick Start

### 1. Configure the Database

Edit `config.py`:

```python
DB_CONFIG = {
    "host": "192.168.1.100",
    "port": 3306,
    "user": "root",
    "password": "your_password",
    "database": "webchat12",
    "charset": "utf8mb4"
}
```

### 2. Install Dependencies

```bash
pip install selenium beautifulsoup4 pymysql requests webdriver-manager
```

### 3. Run the Crawler

#### ✨ Recommended: Provide Browser Cookie (Token auto‑extracted)

Only the cookie is needed – no manual token lookup:

```bash
# JSON format (exported from DevTools)
python3 run_crawler.py \
  --cookie-json '[{"name":"uin","value":"xxx"},{"name":"key","value":"xxx"}]'

# Domain format (copy from Application panel, select all)
python3 run_crawler.py \
  --cookie-domain "$(cat cookies.txt)"

# Cookie request header string format
python3 run_crawler.py \
  --cookie-str 'uin=xxx; key=xxx; pass_ticket=xxx'

# Crawl a single Official Account
python3 run_crawler.py \
  --cookie-str 'uin=xxx; key=xxx' \
  "Midea"
```

After providing the cookie, the system will automatically:
1. Detect and convert the cookie format
2. Visit the WeChat Official Platform to extract the token
3. Quickly validate API availability
4. **On success → directly crawl all Official Account articles** 🎉

#### Method 2: Auto Mode (Check database cookie)

```bash
# Crawl all enabled Official Accounts
python3 run_crawler.py

# Crawl a specific Official Account
python3 run_crawler.py "Midea"

# If the database cookie has expired, you'll be prompted to provide a browser cookie. Follow the instructions and rerun.
```

## How to Obtain Browser Cookies

### Method 1: Chrome DevTools → Application panel → Select all & copy (recommended)

1. Open https://mp.weixin.qq.com/ in Chrome and log in via QR code.
2. Press F12 to open DevTools.
3. Switch to the **"Application"** tab.
4. Expand **"Cookies"** on the left → select **"https://mp.weixin.qq.com"**.
5. Click the first row, scroll to the bottom, hold **Shift** and click the last row (select all).
6. Press **Ctrl+C** (Mac: Cmd+C) to copy.
7. Save to a file or pass as `--cookie-domain` argument.

### Method 2: Chrome DevTools → Export as JSON

1. Install the **"EditThisCookie"** or **"Cookie-Editor"** extension.
2. Log in to https://mp.weixin.qq.com/.
3. Use the extension to export cookies in JSON format.
4. Pass as `--cookie-json` argument.

### Method 3: Copy Cookie header from Network panel

1. Log in to https://mp.weixin.qq.com/.
2. F12 → **"Network"** tab.
3. Refresh the page, click any request (e.g., `home?t=home/index`).
4. Locate the **"Cookie:"** field under **"Request Headers"**.
5. Select and copy the entire cookie value.
6. Pass as `--cookie-str` argument.

### Token Acquisition (no longer manual)

~~After logging in, copy the number after token= from the address bar~~
**Starting from v2, the token is automatically extracted!**

You only need to provide the browser cookie; the crawler will:
1. Visit `https://mp.weixin.qq.com/`
2. Follow redirects and extract the `token=` parameter from the final URL
3. If not present in the URL, search for the token in the page content
4. After successful extraction, perform a secondary validation using the search API

> 💡 If auto‑extraction fails, you can still manually specify `--token 123456789` as a fallback.

## API Reference

### WeChatCrawler

```python
from crawler import WeChatCrawler

crawler = WeChatCrawler()

# Method 1: Start from browser cookie (recommended) – token auto‑extracted
browser_cookies_text = "..."   # copied from browser
crawler.set_user_browser_cookies(browser_cookies_text)
# Or specify format:
crawler.set_user_browser_cookies(browser_cookies_text, format_type='header_str')
# Also supports manual token:
crawler.set_user_browser_cookies(browser_cookies_text, token='123456789')

# Method 2: Auto mode (checks database or prompts user)
crawler.run()

# Method 3: Crawl a specific Official Account
crawler.get_content("Official Account name")
```

### WeChatDB

```python
from db_operations import WeChatDB

db = WeChatDB()

# Check if a cookie exists
db.has_cookie()  # True/False

# Get the latest valid cookie
cookies, token = db.get_latest_valid_cookie()

# Save cookie
db.save_cookie(cookies, token)

# Add a crawl task
db.add_task("Official Account name")

# Get task list
tasks = db.get_crawl_tasks()

db.close()
```

### cookie_utils (Format conversion utilities)

```python
from cookie_utils import convert_to_db_format, detect_format, print_cookie_help

# Auto‑detect format and convert
cookies_dict = convert_to_db_format(browser_cookie_text)
# => {'uin': 'xxx', 'key': 'xxx', ...}

# Detect format type
fmt = detect_format(cookie_text)  # 'json_devtools' | 'netscape' | 'json_domain' | 'header_str'

# Get operation guide
help_text = print_cookie_help()
```

## Database Schema

| Table                  | Description                  |
| ---------------------- | ---------------------------- |
| `wechat_cookies`       | Cookie cache (auto‑managed)  |
| `wechat_accounts`      | Official Account information |
| `wechat_articles`      | Article content              |
| `wechat_article_stats` | Article statistics           |
| `wechat_comments`      | Comment data                 |
| `crawl_tasks`          | Crawl task list              |

## Database Operations

```sql
-- View all articles
SELECT a.title, a.link, s.read_num, s.like_num 
FROM wechat_articles a
LEFT JOIN wechat_article_stats s ON a.id = s.article_id
ORDER BY a.create_time DESC;

-- Count articles per Official Account
SELECT ac.account_name, COUNT(a.id) as cnt
FROM wechat_articles a
JOIN wechat_accounts ac ON a.account_id = ac.id
GROUP BY ac.account_name;

-- Manage crawl tasks
INSERT INTO crawl_tasks (gzh_name, type, status) VALUES ('Account name', 1, 1);
UPDATE crawl_tasks SET status=0 WHERE gzh_name='Account name';
```

## Important Notes

⚠️ **Cookie validity**: WeChat cookies typically last from several hours to a few days. When expired, the user will be prompted to provide a fresh cookie.

⚠️ **Token auto‑extraction**: As of v2, manual token provision is no longer required – the crawler automatically extracts it from the WeChat Official Platform. If auto‑extraction fails, the user will be prompted to manually specify `--token`.

⚠️ **Cookie format auto‑detection**: The tool supports automatic format detection, but the `--cookie-domain` method (copying from the Application panel) is recommended as it is the most stable.

⚠️ **Anti‑scraping measures**:
- Uses the mobile WeChat User‑Agent.
- Random delays of 1–6 seconds between requests.
- It is advisable to run at intervals of several hours.

⚠️ **QR‑code login (fallback)**: The traditional QR login method is retained in the `weChat_login()` method and requires a working Chrome browser environment.
---

Feel free to adjust any terms to better match your forum's style (e.g., "Official Account" vs "Public Account"). Let me know if you need any modifications.

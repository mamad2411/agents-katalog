---
name: feedgrab-setup
description: Install and configure feedgrab — the universal content grabber. Use when user needs to set up feedgrab, configure API keys, login to platforms, or diagnose issues.
disable-model-invocation: true
---

# feedgrab Setup Guide

> Install feedgrab, configure API keys, login to platforms, and verify everything works.

## Trigger

- `/feedgrab-setup`
- "Install feedgrab"
- "配置 feedgrab"
- When `/feedgrab` reports "feedgrab not found"

## Step 1: Check Python Environment

```bash
python3 --version 2>/dev/null || python --version 2>/dev/null
pip3 --version 2>/dev/null || pip --version 2>/dev/null
```

Requires Python ≥ 3.10. If not available, tell user to install Python first.

## Step 2: Install feedgrab

```bash
pip install feedgrab[all]
```

This installs the full package with all optional dependencies (browser, stealth, Twitter, WeChat, Xiaohongshu, Feishu, Telegram).

For a minimal install:
```bash
pip install feedgrab                     # Core only (Jina fallback)
pip install feedgrab[browser]            # + Playwright
pip install feedgrab[twitter]            # + Twitter GraphQL
pip install feedgrab[stealth]            # + Anti-detection (patchright, curl_cffi)
```

After installation, verify:
```bash
feedgrab --help
```

## Step 3: Interactive Setup

```bash
feedgrab setup
```

This runs a 5-step interactive wizard:
1. **Output directory** — where to save fetched content (default: `./output/`)
2. **Jina API** — free, no key needed
3. **YouTube API Key** — optional, for YouTube search
4. **GitHub Token** — optional, for higher rate limits
5. **Creates `.env`** file with your configuration

## Step 4: Platform Login (as needed)

For platforms requiring cookies/session:

```bash
# Twitter/X — opens browser for login
feedgrab login twitter

# Xiaohongshu — opens browser for login
feedgrab login xhs

# WeChat MP backend — opens browser for login (session valid ~4 days)
feedgrab login wechat

# Feishu — opens browser for login
feedgrab login feishu
```

**Tip**: If you have Chrome running with remote debugging enabled, set `CHROME_CDP_LOGIN=true` in `.env` to extract cookies from your existing browser session without re-login.

## Step 5: Verify Installation

```bash
# Full diagnostic
feedgrab doctor

# Platform-specific diagnostic
feedgrab doctor x          # Twitter/X
feedgrab doctor xhs        # Xiaohongshu
feedgrab doctor mpweixin   # WeChat
feedgrab doctor feishu     # Feishu
```

## Step 6: Test

```bash
# Test with a simple URL (no login needed)
feedgrab https://github.com/iBigQiang/feedgrab
```

If the output `.md` file is generated successfully, setup is complete!

## Advanced Configuration (.env)

Key environment variables (all optional):

```env
# Output
OUTPUT_DIR=./output

# Twitter
X_BOOKMARKS_ENABLED=true
X_USER_TWEETS_ENABLED=true
X_LIST_TWEETS_ENABLED=true
X_DOWNLOAD_MEDIA=true

# Xiaohongshu
XHS_USER_NOTES_ENABLED=true
XHS_SEARCH_ENABLED=true
XHS_DOWNLOAD_MEDIA=true
XHS_FETCH_COMMENTS=true

# WeChat
MPWEIXIN_DOWNLOAD_MEDIA=true
MPWEIXIN_FETCH_COMMENTS=true

# YouTube
YOUTUBE_API_KEY=your_key_here

# GitHub
GITHUB_TOKEN=your_token_here

# Feishu
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_secret
FEISHU_DOWNLOAD_IMAGES=true

# Stealth
CHROME_CDP_LOGIN=true
CHROME_CDP_PORT=9222
```

See `.env.example` in the feedgrab repo for the full list.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `pip install` fails | Try `pip install --user feedgrab[all]` or use a virtualenv |
| Playwright not working | Run `playwright install chromium` |
| patchright not working | Run `patchright install chromium` |
| Cookie expired | Re-run `feedgrab login <platform>` |
| Windows encoding errors | feedgrab auto-fixes UTF-8, but ensure Python ≥ 3.10 |

---
name: feedgrab
description: Universal content grabber — fetch any URL and return structured Markdown. Supports X/Twitter, WeChat, Xiaohongshu, YouTube, GitHub, Feishu/Lark, Bilibili, Telegram, RSS, and any web page. Use when user provides a URL and wants its content extracted.
---

# feedgrab — Universal Content Grabber

> Give it a URL, get back structured Markdown. Supports 8+ platforms with deep extraction.

## Trigger

Activate when user provides a URL and wants content fetched/extracted/read:
- `/feedgrab <URL>`
- "Grab this article"
- "Read this tweet/post"
- "抓取这个链接"
- Any URL from supported platforms

## Prerequisites Check

Before fetching, verify feedgrab is installed:

```bash
which feedgrab 2>/dev/null || command -v feedgrab 2>/dev/null
```

**If NOT installed**, tell the user:
```
feedgrab is not installed. Run `/feedgrab-setup` or manually:
  pip install feedgrab[all]
  feedgrab setup
```
Then stop — do not proceed without feedgrab.

## Supported Platforms

| Platform | URL Pattern | Method |
|----------|------------|--------|
| X/Twitter | `x.com/*/status/*`, `twitter.com/*` | GraphQL → FxTwitter → Syndication → oEmbed → Jina → Playwright |
| WeChat (微信公众号) | `mp.weixin.qq.com/*` | Playwright JS evaluate → Jina |
| Xiaohongshu (小红书) | `xiaohongshu.com/explore/*`, `xhslink.com/*` | API (xhshow) → Jina → Playwright |
| YouTube | `youtube.com/watch?v=*`, `youtu.be/*` | API metadata + yt-dlp subtitles |
| GitHub | `github.com/*/*` | REST API (Chinese README priority) |
| Feishu/Lark (飞书) | `feishu.cn/docx/*`, `feishu.cn/wiki/*` | Open API → Playwright → Jina |
| Bilibili (B站) | `bilibili.com/video/*`, `b23.tv/*` | API |
| Telegram | `t.me/*` | Telethon |
| RSS | RSS/Atom feed URLs | feedparser |
| Any web page | Any other URL | Jina Reader fallback |

## Pipeline

### Step 1: Fetch Content

```bash
feedgrab "$ARGUMENTS"
```

The CLI auto-detects the platform and routes to the appropriate fetcher.

### Step 2: Locate Output File

feedgrab saves output to `OUTPUT_DIR` (default: `./output/`). Check the CLI output for the saved file path, typically:
- `output/X/author_date：title.md`
- `output/mpweixin/author_date：title.md`
- `output/XHS/author_date：title.md`
- `output/YouTube/author_date：title.md`
- `output/GitHub/author_date：title.md`
- `output/Feishu/author_date：title.md`

### Step 3: Read and Present

Read the output `.md` file and present the content to the user. The file includes:
- YAML front matter (title, source, author, published, likes, tags, etc.)
- Full article/tweet/post content in Markdown
- Images (as remote URLs or local paths if media download is enabled)

## Clipboard Mode

If the user says "grab from clipboard" or the URL contains `&` (which breaks PowerShell):

```bash
feedgrab clip
```

This reads the URL from the system clipboard.

## Error Handling

| Error | Solution |
|-------|----------|
| `feedgrab: command not found` | Run `/feedgrab-setup` |
| Cookie expired / 401 / 403 | `feedgrab login <platform>` to refresh |
| Jina timeout (30s) | feedgrab auto-retries with Playwright |
| Rate limit (429) | feedgrab auto-rotates cookies if configured |
| `OUTPUT_DIR` not set | `feedgrab setup` to configure |

## Tips

- For **Twitter deep extraction** (views, bookmarks, threads): configure cookies via `feedgrab login twitter`
- For **WeChat articles**: no login needed for single articles
- For **Xiaohongshu**: `pip install xhshow` for API mode (faster, no browser needed)
- For **GitHub**: set `GITHUB_TOKEN` for higher rate limits (5000/hr vs 60/hr)
- For **Feishu**: set `FEISHU_APP_ID` + `FEISHU_APP_SECRET` for Open API access
- Run `feedgrab doctor` to diagnose issues

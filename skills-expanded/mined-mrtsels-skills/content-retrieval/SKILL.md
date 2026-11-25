---
name: content-retrieval
description: Retrieve content from external sources — YouTube transcripts, RSS/Atom feeds, GIF search APIs.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [content, retrieval, youtube, rss, gif, media, blog, feed, mubu, outline]
---

# Content Retrieval Tools

Umbrella for tools that fetch external content — video transcripts, blog feeds, GIF/media search, and financial news.

**⚠️ Financial news search: use the `news-search` skill FIRST (not browser).**
Browser-based search (Google/Bing/DDG/Yahoo Finance) is blocked by bot detection on this machine. The news-search skill (同花顺问财) covers Chinese financial news comprehensively and returns data in <1s.

| Skill | Tool | What it does |
|-------|------|-------------|
| YouTube | `youtube-transcript-api` | Fetch video transcripts → summaries, chapters, threads, blog posts |
| Mubu/幕布 | Browser console | Extract outline content from share pages (no API available) |
| RSS Feeds | `blogwatcher-cli` | Monitor blogs, RSS/Atom feeds, OPML import |
| GIF Search | `curl` + `jq` | Search/download GIFs via Tenor API |

---

## 🎬 YouTube Transcripts

**Prerequisites:** `pip install youtube-transcript-api`

See `references/youtube-content.md` for full command reference and scripts at `scripts/fetch_transcript.py`.

```bash
python3 scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"
python3 scripts/fetch_transcript.py "URL" --text-only            # Plain text
python3 scripts/fetch_transcript.py "URL" --timestamps           # With timestamps
python3 scripts/fetch_transcript.py "URL" --language tr,en       # Language fallback
```

Output formats (see `references/youtube-content.md`): chapters, summary, chapter summaries, X thread, blog post, quotes.

**Error handling:** If transcript disabled or language missing, retry without --language. If still empty, tell user the video likely has transcripts disabled.

---

## 📝 Mubu / 幕布 Share Documents

**No API — use browser console extraction.** Mubu share pages render dynamically; `curl` yields empty PRELOADED_DATA. The DOM holds full content for unauthenticated viewers.

See `references/mubu-share-extraction.md` for extraction scripts and structure reconstruction.

```javascript
// Quick: get all visible text
document.querySelector('*').innerText
```

**Pitfall:** Outline hierarchy is lost in flat text extraction. Reconstruct H1/H2/H3 manually from content grouping and numbered markers. Long documents may need scrolling before extraction.

---

## 📡 Blog/RSS Feed Monitoring

**Install (pick one):** Go, Docker, or binary download from GitHub releases.

See `references/blogwatcher.md` for full command reference.

```bash
blogwatcher-cli add "My Blog" https://example.com               # Add blog
blogwatcher-cli add "Blog" https://example.com --feed-url https://example.com/feed.xml
blogwatcher-cli scan                                              # Scan all
blogwatcher-cli articles                                          # List unread
blogwatcher-cli import subscriptions.opml                         # Import OPML
blogwatcher-cli read 1                                            # Mark read
blogwatcher-cli read-all --yes                                    # Mark all read
```

---

## 🖼️ GIF Search (Tenor API)

**Prerequisites:** `TENOR_API_KEY` env var, `curl`, `jq`.

See `references/gif-search.md` for full API reference.

```bash
# Search and get GIF URLs
curl -s "https://tenor.googleapis.com/v2/search?q=thumbs+up&limit=5&key=${TENOR_API_KEY}" | jq -r '.results[].media_formats.gif.url'

# Download top result
URL=$(curl -s "https://tenor.googleapis.com/v2/search?q=celebration&limit=1&key=${TENOR_API_KEY}" | jq -r '.results[0].media_formats.gif.url')
curl -sL "$URL" -o celebration.gif
```

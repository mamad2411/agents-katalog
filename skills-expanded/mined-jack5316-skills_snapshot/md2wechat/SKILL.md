---
name: md2wechat
description: Write and format WeChat Official Account (微信公众号) articles. Markdown → WeChat HTML with themes (default, bytedance, chinese, apple, sports). Use when you want to write 公众号 articles, format for WeChat, md2wechat, or publish to 微信公众平台.
---

# Markdown to WeChat (/md2wechat)

Convert Markdown to beautiful WeChat Official Account (微信公众号) articles with multiple themes. Supports binary conversion (geekjourneyx/md2wechat-skill), API conversion (md2wechat.com), and local fallback.

## Quick Start

```bash
# Convert note and copy to clipboard (paste into mp.weixin.qq.com)
python3 _scripts/md2wechat_skill.py note.md

# Use a specific theme
python3 _scripts/md2wechat_skill.py note.md --theme bytedance

# Save HTML to Sources/
python3 _scripts/md2wechat_skill.py note.md --save

# Create draft via WeChat API (requires credentials)
python3 _scripts/md2wechat_skill.py note.md --api --thumb YOUR_THUMB_MEDIA_ID

# Upload image to WeChat media library
python3 _scripts/md2wechat_skill.py upload-image path/to/cover.png
```

## Features

1. **Theme Support** — 38+ themes including: default, bytedance, chinese, apple, sports, cyber, autumn-warm, spring-fresh, ocean-calm, and many minimal/focus/elegant variations
2. **Multiple Conversion Methods** — Binary (fastest, most features), API (cloud-based), or local fallback
3. **Clipboard Integration** — Copy formatted HTML for quick paste into WeChat后台
4. **HTML Output** — Save to `Sources/WeChat Article - TITLE - DATE.html`
5. **API Draft Creation** — Directly create drafts via WeChat API
6. **Image Upload** — Upload images to WeChat media library and get media_id/URL

## Conversion Methods

### 1. Binary (Recommended)

Requires installation of the official md2wechat binary:

```bash
python3 _scripts/md2wechat_skill.py install
```

This installs the binary + wrapper to `~/.local/bin`. The wrapper fixes the WeChat digest 120-char bug when using `--draft --cover` — use `md2wechat convert file.md --draft --cover path/to/cover.jpg` to send directly.

### 2. API

Uses md2wechat.com API (requires API key):

```bash
# In .env file
MD2WECHAT_API_KEY=your_api_key
```

Supports 5 themes: default, bytedance, chinese, apple, sports.

### 3. Local Fallback

Built-in minimal conversion (always available) with basic markdown support.

## Themes

Available themes (38+):

**Classic:** default, bytedance, chinese, apple, sports, cyber

**Seasonal:** autumn-warm, spring-fresh, ocean-calm

**Minimal:** minimal-gold, minimal-green, minimal-blue, minimal-orange

**Focus:** focus-gold, focus-green, focus-blue

**Elegant:** elegant-gold, bold-gold

And many more variations...

## Note Frontmatter

Set these in your note's YAML frontmatter:

```yaml
---
title: Article Title
author: Author Name
digest: Short summary (for article card)
---
```

- `title` — Article title (used for filename and API)
- `author` — Author name (for API)
- `digest` — Summary shown in feed (max 120 chars; WeChat API limit)

## Options

| Option | Description |
|--------|-------------|
| `note.md` | Path to note (relative to vault or absolute) |
| `--theme NAME` | Visual theme (default: default) |
| `--save` | Save HTML to Sources/ |
| `--no-copy` | Don't copy to clipboard |
| `--api` | Create draft via WeChat API |
| `--thumb MEDIA_ID` | Cover image media_id (required for --api Python fallback) |
| `--cover PATH` | Cover image file path (for --api when using binary) |
| `--json` | Output result as JSON |

## API Mode (Optional)

For programmatic draft creation, add to `.env`:

```bash
WECHAT_APP_ID=your_app_id
WECHAT_APP_SECRET=your_app_secret
# Or use pre-fetched token:
WECHAT_ACCESS_TOKEN=your_access_token
```

**Requirements:**
- Service Account (服务号) or Subscription Account (订阅号) with API access
- Cover image: Upload via WeChat API first to get `thumb_media_id`

## Workflow

1. Write article in Obsidian with standard markdown
2. Run `python3 _scripts/md2wechat_skill.py note.md --theme bytedance`
3. Paste HTML from clipboard into mp.weixin.qq.com → 新建图文消息
4. Add title, cover image, author in WeChat UI
5. Save as draft or publish

## Output

- **Terminal**: Conversion status, clipboard copy confirmation, HTML preview (if --json)
- **Clipboard**: Formatted HTML (when not --no-copy)
- **File**: `Sources/WeChat Article - TITLE - YYYY-MM-DD.html` (when --save)
- **API Draft**: Creates draft in WeChat后台 (requires --api and credentials)

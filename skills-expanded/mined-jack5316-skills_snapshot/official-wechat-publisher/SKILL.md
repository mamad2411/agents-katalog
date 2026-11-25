---
name: official-wechat-publisher
description: Publish articles to WeChat Official Account (微信公众号) quickly. Converts Obsidian notes to WeChat-compatible format for paste or API draft. Use when you want to publish to 公众号, 微信公众平台, or Weixin Gongzhonghao.
---

# Official WeChat Publisher (/official-wechat-publisher)

Publish Obsidian notes to WeChat Official Account (微信公众号) with format alignment. Converts markdown to WeChat-compatible HTML and supports clipboard paste or API draft creation.

## Quick Start

```bash
# Convert note and copy to clipboard (paste into mp.weixin.qq.com)
python3 _scripts/wechat_official_publish.py NOTE_PATH

# Also save HTML file
python3 _scripts/wechat_official_publish.py NOTE_PATH --save

# Only save, don't copy
python3 _scripts/wechat_official_publish.py NOTE_PATH --save --no-copy
```

## Features

1. **Format Conversion** — Markdown → WeChat-compatible HTML (headings, paragraphs, bold, italic, lists, links, blockquotes, code)
2. **Clipboard** — Copy formatted content for quick paste into [mp.weixin.qq.com](https://mp.weixin.qq.com) → 新建图文消息
3. **HTML Output** — Save to `Sources/WeChat Official - TITLE - DATE.html` for manual upload
4. **API Draft** — Create draft via WeChat API (requires Service Account credentials)

## WeChat Format Alignment

- **Typography**: 16px body, 1.8 line-height, #333 color
- **Semantic HTML**: Uses `<p>`, `<h1-h6>`, `<strong>`, `<em>`, `<blockquote>`, `<ul>`, `<ol>`, `<a>`, `<code>`
- **Obsidian Support**: Converts `[[wikilinks]]`, callouts `> [!note]` to blockquotes

## Note Frontmatter

Set these in your note's YAML frontmatter for API mode:

```yaml
---
title: Article Title
author: Author Name
digest: Short summary (for article card)
---
```

- `title` — Article title (max 32 chars for API)
- `author` — Author name (max 16 chars)
- `digest` — Summary shown in feed (max 128 chars)

## Options

| Option | Description |
|--------|-------------|
| `NOTE_PATH` | Path to note (relative to vault or absolute) |
| `--save` | Save HTML to Sources/ |
| `--no-copy` | Don't copy to clipboard |
| `--api` | Create draft via WeChat API |
| `--thumb MEDIA_ID` | Cover image media_id (required for --api) |

## API Mode (Optional)

For programmatic draft creation, add to `.env`:

```
WECHAT_APP_ID=your_app_id
WECHAT_APP_SECRET=your_app_secret
# Or use pre-fetched token:
WECHAT_ACCESS_TOKEN=your_access_token
```

**Requirements:**
- Service Account (服务号) or Subscription Account (订阅号) with API access
- Cover image: Upload via WeChat API first to get `thumb_media_id`
- Images in content must use WeChat's "上传图文消息内的图片获取URL" API

```bash
python3 _scripts/wechat_official_publish.py note.md --api --thumb YOUR_THUMB_MEDIA_ID
```

## Workflow

1. Write in Obsidian with standard markdown
2. Run skill → content copied to clipboard
3. Open mp.weixin.qq.com → 素材管理 → 新建图文消息
4. Paste (Cmd+V) into body editor
5. Add title, cover image, author in WeChat UI
6. Save as draft or publish

## Output

- **Terminal**: Title, author, body length, copy/save confirmation
- **Clipboard**: Formatted HTML (when not --no-copy)
- **File**: `Sources/WeChat Official - TITLE - YYYY-MM-DD.html` (when --save)

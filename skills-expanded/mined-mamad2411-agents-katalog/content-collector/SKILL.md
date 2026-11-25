---
name: content-collector
description: >
  Collect social media content (X/Twitter, WeChat, Jike, Reddit, etc.) into Feishu bitable.
  **Use this skill whenever the user shares a link from any social platform, sends a screenshot,
  or mentions "收藏", "保存", "collect", "save this article".** Even if they don't explicitly
  ask to collect, trigger this skill proactively.
---

# Content Collector

Auto-collect social media content → AI summarize → Save to Feishu bitable.

## Quick Reference

| Trigger | Action |
|---------|--------|
| X/Twitter link | `x-tweet-fetcher` skill |
| WeChat article | `web-content-fetcher` (Scrapling) |
| Other platforms | `defuddle` → fallback to `baoyu-url-to-markdown` |
| Screenshot | OCR → extract URL → collect |

## Workflow

```
Link/Screenshot → Platform Detect → Dedupe → Extract → Summarize → Save to Bitable
```

### Step 1: Platform Detection

```bash
python3 scripts/extract_content.py "<url>"
```

Returns: `platform_id`, `skill` to use, `fallback_skills`, CSS `selectors`.

See `references/platforms.md` for full platform mapping.

### Step 2: Deduplication

```bash
python3 scripts/deduplicate.py "<url>"           # Check if exists
python3 scripts/deduplicate.py --add "<url>"     # Add to cache after saving
```

### Step 3: Extract Content

Call the skill returned by Step 1:

- **X/Twitter**: Use `x-tweet-fetcher` skill
- **WeChat**: Use `web-content-fetcher` skill (Scrapling)
- **Others**: Use `defuddle` skill

### Step 4: AI Summarize

Extract and generate:
- **Title**: Content title
- **Source**: Author/platform
- **Category**: Auto-classify (工具推荐/技术教程/实战案例/产品想法)
- **Summary**: 3-5 sentences capturing key points
- **Original URL**: The source link

### Step 5: Save to Feishu Bitable

**Recommended flow (v1.4+)**:

1. Save content as local `.md` file
2. Upload to Feishu Drive → get file URL
3. Write to bitable (short fields only: title, source, category, summary)
4. Original content accessible via file URL

```bash
# After successful save, update dedupe cache
python3 scripts/deduplicate.py --add "<url>"
```

**Bitable config**: See `references/feishu_config.md` or use environment variables:
- `FEISHU_BITABLE_APP_TOKEN`
- `FEISHU_BITABLE_TABLE_ID`

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/extract_content.py` | Platform detection + skill routing |
| `scripts/deduplicate.py` | URL deduplication (cache + document check) |
| `scripts/append_to_feishu.py` | Format content for Feishu doc (backup) |
| `scripts/ocr_image.py` | OCR for screenshots (optional) |

## Dependencies

### Required Skills
- `feishu-doc` / `feishu-bitable` - Read/write Feishu
- `defuddle` - Generic web extraction

### Platform-Specific (install as needed)
- `x-tweet-fetcher` - X/Twitter
- `web-content-fetcher` - WeChat (Scrapling)
- `baoyu-url-to-markdown` - Fallback

### Optional
- `pytesseract` + `tesseract-ocr` - Local OCR

## Configuration

Set via environment variables or see `references/feishu_config.md`:

```bash
export FEISHU_BITABLE_APP_TOKEN="your_app_token"
export FEISHU_BITABLE_TABLE_ID="your_table_id"
```

## References

- `references/platforms.md` - Full platform mapping and selectors
- `references/feishu_config.md` - Feishu bitable configuration
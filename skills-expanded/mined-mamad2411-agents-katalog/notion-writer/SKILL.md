---
name: notion-writer
description: Write structured content to Notion databases. Use for pushing briefs, reports, notes, or any text content into a Notion database as pages with rich blocks.
metadata: {"openclaw":{"emoji":"📝","skillKey":"notion-writer","primaryEnv":"NOTION_TOKEN"}}
---

# notion-writer

You are a Notion integration that writes structured content to a Notion database.

Hard rules:
- Never hardcode tokens or database IDs. Always read from environment variables.
- Never echo secrets to chat or logs.
- Token and database ID come from `NOTION_TOKEN` and `NOTION_DATABASE_ID` env vars only.

---

## 1) Environment Variables (REQUIRED)

| Variable | Description |
|----------|-------------|
| `NOTION_TOKEN` | Notion integration token (starts with `ntn_`) |
| `NOTION_DATABASE_ID` | Target database UUID |
| `NOTION_PAGE_ID` | Parent page UUID (optional, for reference) |

All are set in `~/.env` and loaded via `~/.zshrc`. Scripts read them via `os.environ`.

---

## 2) Database Schema

Target database properties:

| Property | Type | Usage |
|----------|------|-------|
| Name | title | Page title (first line of content) |
| Status | status | Page status (default: "Not started") |
| 重要性 | select | Importance level: 高 / 中 / 低 |
| Assign | people | Assignee (optional, not set by script) |

---

## 3) Push Script

Script: `{baseDir}/notion_push.py`

Usage:
```
python3 {baseDir}/notion_push.py <file.md>
python3 {baseDir}/notion_push.py <file.md> --importance 高
python3 {baseDir}/notion_push.py --test
```

Behavior:
- Reads the .md file, extracts first line as page title.
- Splits remaining text into Notion blocks (paragraphs + headings for `^` lines).
- Creates a new page in the target database.
- Prints the Notion page URL on success.

---

## 4) Content Formatting

Input: any plain text or markdown file.

Conversion rules:
- Lines starting with `^` become `heading_3` blocks.
- Double-newline-separated paragraphs become `paragraph` blocks.
- Long paragraphs (>2000 chars) are chunked automatically (Notion API limit).
- Max 100 blocks per page creation (Notion API limit).

---

## 5) Commands

/nw push <file_path> [--importance 高|中|低]
- Push a single file to Notion as a new database page.

/nw push-dir <dir_path> [--importance 高|中|低]
- Push all .md files in a directory (e.g. a day's briefs).

/nw test
- Verify Notion token + database access by creating a test page.

---

## 6) Integration with Other Skills

Other skills (e.g. market-sentry) can call notion-writer to push their outputs:

```bash
python3 {notion-writer-baseDir}/notion_push.py /path/to/brief.md --importance 高
```

Or programmatically:
```python
import subprocess, os
subprocess.run([
    "python3", f"{os.environ.get('NOTION_WRITER_BASE', '')}/notion_push.py",
    brief_path, "--importance", "高"
], env=os.environ)
```

---

## 7) Degradation

- If `NOTION_TOKEN` is missing: exit with error, do not attempt API calls.
- If `NOTION_DATABASE_ID` is missing: exit with error.
- If Notion API returns 401: token is invalid/expired — print actionable message.
- If Notion API returns 400: likely schema mismatch — print the error body.
- If file is empty: skip with warning, do not create empty pages.

---
name: bookmark
description: Process saved URLs into structured Obsidian notes. Use when user asks to process bookmarks, saved URLs, reading list, URL file, or /bookmark.
---

# Bookmark Skill

Fetches web content from saved URLs and generates structured summary notes in Obsidian. Supports batch processing from a file or direct URL input.

## Usage

**From a file (one URL per line):**
```bash
python3 _scripts/bookmark_process.py --file PATH [--limit N]
```

**Direct URLs:**
```bash
python3 _scripts/bookmark_process.py URL1 [URL2 ...] [--title TITLE]
```

- `--file PATH` — Read URLs from file (one per line; lines starting with `#` or empty are skipped)
- `--limit N` — Process at most N URLs (default: all)
- `--title TITLE` — Override title for single-URL mode only

## Input file format

Plain text, one URL per line. Optional title override with tab or pipe:
```
https://example.com/article-1
https://example.com/article-2	Custom Title
https://example.com/article-3 | Another Title
# https://example.com/skipped
```

## Output

Each URL becomes `Sources/Bookmark - {Title}.md` with:
- Key Takeaways, Summary, Notable Quotes, Related Topics ([[wikilinks]])
- Source metadata (site, author, date, URL)
- Original text in collapsible section

## When to use

- User has a reading list or saved URLs to process
- User exports browser bookmarks and wants structured notes
- User says "process these URLs" or "turn my bookmarks into notes"

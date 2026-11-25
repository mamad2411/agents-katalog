---
name: curl
description: Information curation skill - gather, filter, organize, and synthesize information from multiple sources in your Obsidian vault. Use when you want to collect information on a topic, build reading lists, organize knowledge, or synthesize what you've learned.
---

# Curl Skill

Gathers, filters, organizes, and synthesizes information across your Obsidian vault by tag, keyword, date, or directory.

## Usage

```bash
python3 _scripts/curl.py "AI" --tags ai machine-learning
python3 _scripts/curl.py "recent learning" --days 7 --organize
```

## Options

- `topic` — Topic for curation (required)
- `--tags LIST` — Filter by hashtags
- `--keywords LIST` — Filter by keyword matches
- `--days N` — Files from last N days
- `--directories LIST` — Directories to search
- `--directory DIR` — Single directory exclusively
- `--paths LIST` — Specific file paths
- `--gather` — Just list matching files
- `--organize` — Group by theme
- `--reading-list` — Create annotated reading list
- `--synthesize` — Connect ideas across sources
- `--repository` — Full knowledge repository (organize + reading list + synthesis)
- `--save` — Save output to vault

## Output

`Sources/Curl - [topic] - YYYY-MM-DD.md`

---
name: bilibili
description: Summarize a Bilibili video into an Obsidian note. Use when user asks for Bilibili summary or /bilibili.
---

# Bilibili Summary Skill

Fetches video metadata and subtitles from Bilibili, then generates an AI summary as an Obsidian note.

## Usage

```bash
python3 _scripts/bilibili_summary.py VIDEO_URL_OR_BVID [-v]
```

- Accepts a full Bilibili URL or just the BV ID
- `-v` / `--verbose`: Show detailed processing output

## Output

`Sources/Bilibili - {Title}.md` (Overview, Key Takeaways, Summary, Quotes, metadata, subtitles)

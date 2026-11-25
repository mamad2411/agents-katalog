---
name: youtube
description: Summarize a YouTube video into an Obsidian note. Use when user asks for YouTube summary or /youtube.
---

# YouTube Summary Skill

Fetches video metadata and transcript, then generates an AI summary as an Obsidian note.

## Usage

```bash
python3 _scripts/youtube_summary.py VIDEO_URL_OR_ID
```

- Accepts a full YouTube URL or just the video ID

## Output

`Sources/YT - {Title}.md` (Key Takeaways, Summary, Quotes, Related Topics, full transcript)

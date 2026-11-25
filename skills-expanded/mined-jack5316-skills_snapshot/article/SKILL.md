---
name: article
description: Summarize a web article/blog post into an Obsidian note. Use when user asks for article summary or /article.
---

# Article Summary Skill

Fetches a web article, extracts its content, then generates an AI summary as an Obsidian note.

## Usage

```bash
python3 _scripts/article_summary.py URL [--title TITLE]
```

- Accepts any public article/blog post URL
- Use `--title` to override the detected title

## Output

`Sources/Article - {Title}.md` (Key Takeaways, Summary, Notable Quotes, Related Topics, full article text)

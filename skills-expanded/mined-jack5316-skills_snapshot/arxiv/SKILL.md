---
name: arxiv
description: Curate recent ArXiv papers by topic into an Obsidian digest note. Use when user asks for ArXiv digest or /arxiv.
permissions:
  - network.read
  - vault.write
---

# ArXiv Digest Skill

Searches ArXiv for recent papers on configured topics and creates a digest with AI summaries.

## Usage

```bash
python3 _scripts/arxiv_digest.py
```

## Configuration

`_scripts/arxiv_topics.txt` — one keyword per line

## Output

`Sources/ArXiv Digest - YYYY-MM-DD.md` (theme-organized, [[wikilinks]])

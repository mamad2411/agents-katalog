---
name: quotes
description: Find inspirational quotes by subject or from famous people. Uses Quotable.io API plus AI for movie lines and thematic enrichment. Use when user asks for quotes, inspirational quotes, famous quotes, movie lines, quotes by topic, quotes by author, or /quotes.
---

# Quotes Skill (/quotes)

Find inspirational quotes by subject, from famous people, or iconic movie lines. Combines Quotable.io API with AI curation for thematic enrichment.

## Quick Start

```bash
# By subject/topic
python3 _scripts/quotes.py "courage"
python3 _scripts/quotes.py "perseverance" --movie-lines

# By famous person
python3 _scripts/quotes.py --author "Einstein"
python3 _scripts/quotes.py -a "Steve Jobs"

# Save to vault
python3 _scripts/quotes.py "success" --save
```

## Options

| Option | Description |
|--------|-------------|
| `topic` | Subject or theme (e.g., courage, success, creativity) |
| `--author`, `-a` | Famous person (Einstein, Churchill, Steve Jobs) |
| `--movie-lines`, `-m` | Include iconic film quotes on the theme |
| `--limit`, `-n` | Max quotes from API (default: 8) |
| `--save`, `-s` | Save to `Sources/Quotes - TOPIC - YYYY-MM-DD.md` |
| `--ai-only` | Skip API, use AI curation only |

## Examples

```bash
# Courage with movie lines
python3 _scripts/quotes.py "courage" --movie-lines --save

# Quotes from Marcus Aurelius
python3 _scripts/quotes.py --author "Marcus Aurelius"

# Success theme, 10 quotes
python3 _scripts/quotes.py "success" --limit 10

# AI-only (no API) when offline
python3 _scripts/quotes.py "creativity" --ai-only
```

## Output

- **Terminal**: Formatted quotes with attribution
- **Saved**: `Sources/Quotes - {Topic} - YYYY-MM-DD.md`

## Data Sources

- **Quotable.io** — Famous quotes by author or search (free API)
- **AI** — Movie lines, thematic enrichment, additional curation

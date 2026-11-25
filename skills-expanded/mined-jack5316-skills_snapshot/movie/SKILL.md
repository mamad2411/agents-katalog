---
name: movie
description: Review, understand, and organize movies into Obsidian notes. Use when user asks for movie notes, film review, or /movie.
---

# Movie Notes Skill

Creates structured movie notes with metadata, plot, cast, quotes, and personal insights. Saves to the vault for your film database.

## Usage

```bash
python3 _scripts/movie_notes.py "Movie Title" [--year YYYY] [--notes "Your observations"]
```

- **Title**: Movie name (required)
- `--year`: Disambiguate when multiple films share a name
- `--notes`: Your personal observations, reactions, or review to incorporate

## Output

`Sources/Movie - {Title}.md` with:

- **Metadata**: Runtime, release year, director, cast
- **Plot**: Summary and key narrative beats
- **Quotes**: Memorable lines
- **Interesting Points**: Themes, craft, cultural impact, connections
- **Personal Notes**: Your observations (if provided via `--notes`)

Uses `[[wikilinks]]` for Obsidian interconnection. No YAML frontmatter in output.

---
name: concept
description: Extract and define recurring concepts across vault reading. Use when user asks for concept extraction, recurring concepts, define concepts from reading, or /concept.
---

# Concept Skill

Identifies ideas, terms, and frameworks that appear across multiple notes in the vault, then produces concise definitions with source links. Surfaces what you're repeatedly encountering in your reading.

## Usage

```bash
# Open extraction — AI finds recurring concepts across all recent notes
python3 _scripts/concept_extract.py

# Topic-focused extraction
python3 _scripts/concept_extract.py --topic "inverse problems"
python3 _scripts/concept_extract.py --topic "AI, agents, LLMs"

# Custom lookback and scope
python3 _scripts/concept_extract.py --topic "personal AI" --days 14
python3 _scripts/concept_extract.py --no-atlas --no-maps  # Sources + Inbox only

# Custom output path
python3 _scripts/concept_extract.py --output "Atlas/Concepts - 2026-02.md"
```

## Output

`Sources/Concept Digest - YYYY-MM-DD.md` — each concept has:
- **Definition** — 2–4 sentences capturing the essence
- **Appears in** — [[wikilinks]] to source notes

## Notes

- A concept must appear in at least 2 notes to be included
- Prioritizes domain-specific terms, mental models, cross-domain metaphors
- `--topic` filters by keyword (comma = OR)
- Default lookback: 30 days for Sources/Inbox; Atlas and Maps always included

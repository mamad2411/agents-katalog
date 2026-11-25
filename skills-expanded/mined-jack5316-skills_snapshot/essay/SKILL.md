---
name: essay
description: Generate long-form essays from accumulated vault insights. Use when user asks for essay, long-form writing, synthesis essay, or /essay.
---

# Essay Skill

Produces long-form narrative prose from accumulated insights across Sources (digests, syntheses), Atlas, Maps, and Inbox. Unlike bullet-point synthesis, the output is a coherent essay — thesis-driven, flowing paragraphs, 800–1500 words.

## Usage

```bash
# Open synthesis — AI picks the most compelling theme from recent notes
python3 _scripts/essay.py

# Topic-focused essay
python3 _scripts/essay.py --topic "inverse problems"
python3 _scripts/essay.py --topic "AI agents, LLMs"

# Custom lookback and scope
python3 _scripts/essay.py --topic "personal AI" --days 14
python3 _scripts/essay.py --no-atlas --no-maps  # Sources + Inbox only

# Custom output filename
python3 _scripts/essay.py --topic "regularization" --title "On Regularization in Life"
```

## Output

`Atlas/Essay - {topic-or-date}.md` — long-form essay with [[wikilinks]] to source notes.

## Notes

- Prioritizes weekly/daily synthesis and self-reflection notes (highest insight density)
- `--topic` filters notes by keyword; multiple keywords separated by comma (OR logic)
- Default lookback: 30 days for Sources/Inbox; Atlas and Maps are always included (no date filter)
- Essay is prose-only: no bullet lists, no "Key Points" sections

---
name: flashcard
description: Generate spaced repetition flashcards from content. Use when user asks for flashcards, spaced repetition cards, memory cards, /flashcard, or wants to turn notes/articles into reviewable cards.
---

# Flashcard Skill

Generates spaced repetition cards from vault notes or a single file. Outputs Obsidian Spaced Repetition plugin format (`question::answer`). Optionally exports Anki-compatible `.txt` for import.

## Usage

```bash
# From a single note
python3 _scripts/flashcard_generate.py "Atlas/Essay - inverse problems.md"
python3 _scripts/flashcard_generate.py "Sources/Concept Digest - 2026-02-18.md" --deck concepts

# From vault (topic-filtered, like concept/essay)
python3 _scripts/flashcard_generate.py --topic "inverse problems"
python3 _scripts/flashcard_generate.py --topic "AI, agents" --days 14

# Custom output and Anki export
python3 _scripts/flashcard_generate.py "path/to/note.md" --output "Sources/Flashcards - my-deck.md" --anki
```

## Agent workflow

When user says "flashcards from X", "/flashcard", or "turn this into spaced repetition cards":

1. **Single note**: If they reference a specific note or file, run with that path
2. **Topic-based**: If they want cards from a theme, use `--topic "keyword"`
3. **Current note**: If they have a file open, use that path
4. Suggest `--anki` if they use Anki and want importable output

## Output

- **Obsidian**: `Sources/Flashcards - {topic-or-filename}.md` — `#flashcards` or `#flashcards/deck-name` + `question::answer` lines
- **Anki** (with `--anki`): Same base path with `_anki.txt` — tab-separated front/back for File → Import

## Format

Obsidian Spaced Repetition plugin uses:
- `question::answer` — single-line basic (one card)
- `term:::definition` — single-line bidirectional (two cards: term→def, def→term)
- Deck: `#flashcards` or `#flashcards/deck-name` at top of note

## Notes

- Prioritizes atomic, testable facts over compound questions
- Uses [[wikilinks]] in answers when referencing source notes
- Default: 5–15 cards per run; AI decides based on content density

---
name: til
description: Today I Learned quick capture. Use when user says TIL, "today I learned", /til, or wants to capture a quick learning or insight.
---

# TIL — Today I Learned

Quick capture of learnings into the Obsidian vault. Minimal friction, no AI required.

## Usage

```bash
python3 _scripts/til_capture.py "What you learned"
python3 _scripts/til_capture.py "What you learned" --note
```

- **Default**: Appends to `Sources/TIL - YYYY-MM-DD.md` (daily aggregate)
- **`--note`**: Creates standalone note `Sources/TIL - {slug}.md` for substantial learnings

## Agent workflow

When user says "TIL X" or "/til X":

1. Extract the learning from their message (drop "TIL", "today I learned", etc.)
2. Run: `python3 _scripts/til_capture.py "extracted learning"`
3. Confirm capture with the saved path

For longer or standalone-worthy learnings, suggest `--note`.

## Output

- Daily: `Sources/TIL - 2026-02-18.md` — bullet list with timestamps
- Standalone: `Sources/TIL - {topic-slug}.md` — single note with heading

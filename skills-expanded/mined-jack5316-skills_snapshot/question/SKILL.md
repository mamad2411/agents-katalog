---
name: question
description: Capture open questions for future research. Use when user says question, "open question", /question, or wants to save a question to investigate later.
---

# Question — Open Questions for Future Research

Quick capture of open questions into the Obsidian vault. Minimal friction, no AI required.

## Usage

```bash
python3 _scripts/question_capture.py "Your question here"
python3 _scripts/question_capture.py "Your question here" --note
```

- **Default**: Appends to `Sources/Question - YYYY-MM-DD.md` (daily aggregate)
- **`--note`**: Creates standalone note `Sources/Question - {slug}.md` for substantial questions with context/research directions

## Agent workflow

When user says "question X" or "/question X":

1. Extract the question from their message (drop "question", "I wonder", etc.)
2. Run: `python3 _scripts/question_capture.py "extracted question"`
3. Confirm capture with the saved path

For longer or research-worthy questions needing context, suggest `--note`.

## Output

- Daily: `Sources/Question - 2026-02-18.md` — bullet list with timestamps
- Standalone: `Sources/Question - {topic-slug}.md` — note with heading, context, and research directions sections

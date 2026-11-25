---
name: debate
description: Steelman opposing views on topics you're exploring. Use when user asks for debate, steelman, opposing arguments, devil's advocate, challenge my view, or /debate.
---

# Debate — Steelman Opposing Views

Generates the strongest possible versions of opposing arguments (steelmanning) for topics you're exploring. Helps stress-test your thinking by presenting the other side at its best — the opposite of strawmanning.

## Usage

```bash
# Topic only — AI infers your implied position
python3 _scripts/debate_steelman.py "inverse problems in life decisions"
python3 _scripts/debate_steelman.py "AI will replace most knowledge work"

# With vault context — use a note as your current view
python3 _scripts/debate_steelman.py "inverse problems" --from-path "Atlas/Essay - inverse problems.md"
python3 _scripts/debate_steelman.py "personal AI infrastructure" --from-path "00 - Inbox/inverse-problems-life-decisions.md"

# Custom output filename
python3 _scripts/debate_steelman.py "regularization" --title "Debate - Regularization in Decisions"
```

## Agent workflow

When user says "debate X", "steelman X", "challenge my view on X", or "/debate X":

1. Extract the topic from their message
2. If they have a note open or reference one, use `--from-path` with that note
3. Run: `python3 _scripts/debate_steelman.py "topic" [--from-path path]`
4. Confirm with the saved path

## Output

`Atlas/Debate - {topic}.md` — structured note with:
- Summary of your position
- 2–4 steelmanned opposing views (each 2–4 paragraphs)
- Key tensions to sit with

## Notes

- Steelmanning = charitable interpretation. The AI argues *for* the other side as persuasively as a skilled advocate would.
- `--from-path` gives the AI your actual reasoning, producing more targeted counterarguments
- Output includes [[wikilinks]] to source notes when context is used

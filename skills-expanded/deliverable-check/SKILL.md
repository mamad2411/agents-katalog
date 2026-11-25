---
name: deliverable-check
description: Use before any client-facing or stakeholder-facing deliverable ships (report, email draft, Jira/Slack post, doc) - lints for metaspeak (references to prior drafts, revisions, feedback, the writing process), em/en dashes, and the "isn't just" trope. Triggers on "check this before I send it", "lint the report", "is this clean", or /deliverable-check <file>.
---

# Deliverable Check

Deliverables must read as standalone artifacts written by a fresh author. This
skill makes that rule mechanical instead of remembered.

## Usage

```bash
python3 ~/.claude/skills/deliverable-check/scripts/lint.py <file> [<file> ...]
```

Exit 0 clean, 1 findings (printed as `file:line: [rule] text`), 2 read error.

## Workflow

1. Run the linter on the deliverable file(s).
2. Fix every finding by rewriting the sentence as if no prior version ever
   existed. Do not delete content the reader needs; restate it standalone.
3. Re-run until clean.
4. Only then present, post, or send the deliverable.

## What it catches

- Metaspeak: "as discussed", "per your feedback", "updated to reflect",
  "previous draft", "I've revised", "now includes", and similar references to
  drafts, revisions, reviewers, or process.
- Em and en dashes (house style bans them).
- The "isn't just X, it's Y" trope.

## Limits

The regex list is a floor, not a ceiling. After a clean lint, do one human-eye
pass for subtler process references the patterns cannot catch (for example a
paragraph that only makes sense if the reader saw an earlier version). Add any
new offender you meet to `scripts/lint.py` in the same turn.

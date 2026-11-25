---
name: insight
description: Looks across the whole vault and writes memory/insights.md — who the owner is, strengths, patterns to watch, where their time should go, what to finish or let go — then replies with the summary. Use when the user says "منو تحلیل کن", "نقاط قوت و ضعفم", "کجا دارم اشتباه می‌کنم", "analyze me", "my strengths and weaknesses", "where am I going wrong", or presses Insight.
---

# insight

Writes one file, `memory/insights.md` — or, for one place, `memory/places/<slug>.md` — and nothing else. Evidence only: every claim names a node with `[[Title]]` or a count from the index.

**One place.** When the prompt is a category or a map as `[[Title]] → memory/places/<file>.md`, look at that place only: read its `index/by-area/` file (for a map, those of its categories, from **Maps** in `INDEX.md`), open at most 8 of its nodes, and write exactly the file the prompt names, replacing it — plain Markdown, no frontmatter: the line `# <Title> — analysis, <YYYY-MM-DD>`, then the headings `## In short`, `## Moving`, `## Stuck`, `## Patterns`, `## Next steps` word for word in English (the app finds them by name), every other line in the reply language ([references/place.md](references/place.md) shows one). Reply with its **In short** and skip the steps below.

## Steps

1. Read `index/INDEX.md`, every `index/by-area/<area>.md` (short files), `index/by-type/goal.md`, `habit.md`, `project.md`, the last 14 lines of `index/by-type/journal.md` (open at most 5 journal nodes), `memory/profile.md`, and the previous `memory/insights.md` when it exists (so the new one can say what changed).
2. Write `memory/insights.md` per [references/format.md](references/format.md), replacing the file.
3. Reply with the **Summary** section in the user's language and name one thing that changed since the last insight (or that this is the first). Change nothing else; never edit `profile.md` here.

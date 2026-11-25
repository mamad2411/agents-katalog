---
name: search
description: Search project tracking files for past decisions, links, keywords, tools, or anything the user is trying to recall. Use when the user asks "remind me", "what was the", "do you remember", "where did we", or asks about a specific term, URL, file, or decision from a previous session.
---

Search the following project tracking files for `$ARGUMENTS`:

- `.claude/memory/JOURNAL.md` — past session decisions, outcomes, and links
- `.claude/memory/TODO.md` — task history, including done tasks
- `.claude/memory/LESSONS.md` — edge cases, gotchas, and non-obvious solutions
- `.claude/memory/NOTES.md` — ideas, supervisor feedback, open questions

Read all four files and return every relevant match with enough surrounding context to be useful. Always cite which file and date the information came from.
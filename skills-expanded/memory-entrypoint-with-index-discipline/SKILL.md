---
name: memory-entrypoint-with-index-discipline
description: "Keep MEMORY.md terse by capping entries, warning when caps hit, and pointing each memory to its own file."
metadata:
  author: ychampion
---

# SKILL: Memory Entrypoint With Index Discipline
**Domain:** context-management  
**Trigger:** Use whenever you’re writing to MEMORY.md so the index stays readable and never exceeds terminal-safe length budgets.
**Source Pattern:** Distilled from reviewed context, compaction, and memory-governance patterns.

## Core Method
Treat MEMORY.md as an index rather than a content store: truncate entries when the line cap or byte cap is reached, issue a warning in place of the dropped detail, and point each entry to a dedicated per-topic file that holds the richer memory frontmatter. Keep the truncation routine deterministic by trimming to 200 lines, then to the last newline before 25 000 bytes, so future reads know exactly what the policy will display.

## Key Rules
- Always stop counting entries once you hit `MAX_ENTRYPOINT_LINES`; avoid writing new lines beyond the cap and instead move the extra detail into a `${ENTRYPOINT_NAME}` entry that links to another file.
- After trimming, append a warning that mentions which limit fired (`lines`, `bytes`, or both) and hints to keep entries under ~200 characters per line.
- Never add content directly to `MEMORY.md`; each entry should be one line in the form `- [Title](file.md) — one-line hook` referencing a dedicated memory file.
- Keep the index a short sentinel that signals the existence and freshness of the memory; save details only in files that the agent can Read or Write when needed.

## Example Application
If a user asks you to remember their quarterly OKR planning, add a single hook line to `MEMORY.md` that links to `okr.md` and let that file carry the context, while the entry keeps `MEMORY.md` under 200 lines so the prompt cache never truncates the index unexpectedly.

## Anti-Patterns (What NOT to do)
- Don’t append long paragraphs or copies of the memory content directly into `MEMORY.md`; doing so triggers truncation every time and loses context visibility.
- Don’t continually extend `MEMORY.md` beyond the caps; once a limit is hit, move future info to a new file instead of letting the file grow uncontrolled.

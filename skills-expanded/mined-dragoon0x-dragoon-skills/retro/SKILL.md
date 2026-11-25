---
name: retro
description: Weekly retro markdown template with git stats pre-loaded (commit count, files changed, +/- lines, contributors). Forces a what-shipped, what-slipped, what-we-learned, what-to-do-less-of, what-to-do-more-of, and quality-trends section. Use end-of-week or end-of-sprint. Output goes to .dragoon/retros/retro-{date}.md. Run as `node ~/.claude/skills/dragoon/skills/retro/scripts/retro.js`.
version: 1.0.0
---

# /retro

Weekly retro template with git facts pre-loaded.

## When to use

- End of week
- End of sprint
- The user says "let's do a retro", "weekly review"

## Pre-loaded

- commits this period
- files changed, lines +/-
- contributor count

## Run it

```
dragoon retro --apply             # last week
dragoon retro --weeks 2 --apply   # last 2 weeks
```

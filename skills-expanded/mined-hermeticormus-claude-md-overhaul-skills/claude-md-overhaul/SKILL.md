---
name: claude-md-overhaul
description: Audit Claude Code memory layer end-to-end. Measure CLAUDE.md/MEMORY.md against caps, find sync conflicts, identify gaps tier-by-tier. Use when memory feels bloated or invisible at session start, or as periodic hygiene.
license: MIT
---

# Claude.md overhaul

## Caps

- Any CLAUDE.md: 200 lines hard cap (80-150 sweet spot)
- MEMORY.md: 200 lines OR 25 KB (past that loads invisible)

## Tier-by-tier audit

1. Sync conflicts → resolve manually
2. User CLAUDE.md → trim to 200
3. Machine CLAUDE.md → trim to 200
4. MEMORY.md → trim to 200 / 25 KB
5. Topic files → audit staleness
6. Skills → audit WHEN-trigger descriptions
7. Gaps → write memories for recurring patterns

---

Full content at https://github.com/HermeticOrmus/claude-md-overhaul-skills.

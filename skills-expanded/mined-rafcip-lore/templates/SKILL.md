---
# Layer 2 — Book-to-Skill master file. This is the only file loaded by default (~4k tokens).
type: skill
name: <skill-slug>                 # stable slug the lookup tool surfaces
description: "What this skill covers + when to use it. Used for discovery — make it specific."
source: "<source document title>"  # the Layer-3 document this skill renders
applies_to: [<scope-in>]           # scope boundaries as explicit fields, not buried prose
not_applicable_to: [<scope-out>]
chapters: <N>
timestamp: "2026-01-01T00:00:00Z"
---

# <Title> — navigable skill

**Framework core** (10–15 lines that capture the whole document's spine — the agent reads this and
usually has enough to act, or knows exactly which chapter to open):

- …
- …

## Topic index (deterministic routing)

| If you need… | Go to |
|---|---|
| the limits / thresholds | [ch01](chapters/ch01-<topic>.md) |
| the procedure for X | [ch02](chapters/ch02-<topic>.md) |
| how to apply it in situation S | [patterns.md](patterns.md) |
| an acronym / term | [glossary.md](glossary.md) |
| a quick decision table | [cheatsheet.md](cheatsheet.md) |

## Hooks (load-bearing cross-references)

- Related skill: [<other-skill>](/skills/<other>/SKILL.md)
- Supersedes / superseded-by: …

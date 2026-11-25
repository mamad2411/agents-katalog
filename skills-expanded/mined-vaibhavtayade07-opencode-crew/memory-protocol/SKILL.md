---
name: memory-protocol
description: Memory consolidation — read learnings.md at project start, append at project end, keep entries short and actionable. Use when starting a new project or task, finishing work, or before /retro.
---

# Memory Consolidation Protocol

The team's long-term memory lives in `~/.config/opencode/agent/learnings.md`.

## When to read

- At the start of any project or task in a familiar domain: read the relevant sections and apply past lessons as defaults.

## When to append

- At the end of any significant piece of work (feature, fix, research, QA pass, incident).

## Format rules

1. Add a heading: `## YYYY-MM-DD - <project> <phase>`
2. One line per finding: "what happened -> rule to apply". Be specific: "hash collisions in URL shortener", not "stuff broke".
3. Include: bugs found late, patterns that worked, contract corrections, tool pitfalls, cost notes.
4. Never append vague praise or duplicates of existing entries.
5. Keep each session's entry under ~10 lines.

## Consolidation

- When the file grows past ~150 lines, run /retro and merge duplicates into a "Repeated lessons" section.

## Self-improve headings

- The improver agent logs config changes under `## YYYY-MM-DD - self-improve` — keep those entries: they are the audit trail of the self-improving loop.
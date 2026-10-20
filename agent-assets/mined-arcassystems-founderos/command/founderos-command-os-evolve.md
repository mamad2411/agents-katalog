---
description: Plan the next round of OS improvements. Say "evolve the OS" or run /founder-os:os-evolve [path to an audit or plan]. Scores the last cycle, writes gaps with evidence and numbered execute prompts into one dated plan file. Plans only - never executes its own prompts.
argument-hint: "[path to an audit or plan file to evolve from]"
allowed-tools: ["Read", "Grep", "Glob", "Write"]
---

# Founder OS evolve

Run the os-evolve skill at `skills/os-evolve/SKILL.md` end to end.

## Procedure

1. Read `skills/os-evolve/SKILL.md`.
2. Pass `$ARGUMENTS` as the source file to evolve from. If empty, use the newest audit or plan in `plans/`. If `plans/` is empty or missing, say so and build the gap list from flags, quarantine, and the last cycle only.
3. Write exactly one file: `plans/os-evolve-<today>.md`. Create `plans/` if it does not exist.
4. Report the path, the counts, and the one prompt to run first.

## Rules

- Never execute the prompts this run just wrote. Planning and executing are separate sessions.
- Never edit `CLAUDE.md`, `rules/`, or any User Layer file.
- No gap without evidence. A hunch goes in the kill column.
- No em dashes or en dashes. No banned words.

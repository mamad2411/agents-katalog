---
description: Show me what FounderOS can do right now. Say "show me what you can do" or "what's available" (or run /founder-os:menu). Returns 5 to 7 capability suggestions tailored to your current state.
allowed-tools: ["Read", "Glob", "Grep"]
---

# Founder OS menu

Discovery entry point. Surfaces 5 to 7 capabilities the founder is most likely to want right now, scored against current OS state.

## Procedure

1. Read the menu skill at `skills/menu/SKILL.md` and execute it end to end.

2. The skill owns the algorithm: read `brain/.snapshot.md` if present, current week's commitments from `cadence/weekly-commitments.md`, last 7 days of `brain/log.md`, and presence of `core/voice-profile.yml` and `core/brand-profile.yml`. Score capabilities against state. Return the top 5 to 7 by relevance with natural-language phrasing first, slash command shortcut second, one-sentence why-now.

3. If the skill file is missing, reply: `Menu skill not found at skills/menu/SKILL.md. Restarting Claude Code fixes this most of the time, because it reloads what is installed. If it happens again after a restart, say "update Founder OS".` and stop.

## Rules

- Read-only. Do not write to any file.
- Zero-state safety: on a brand-new install (no snapshot, no log, no priorities), return the Day-1 starter set rather than an empty list.
- No LLM call inside the algorithm. The menu reads files, scores against rules, returns the top N. Free-tier accessibility floor preserved.
- No em dashes or en dashes. Hyphens only.

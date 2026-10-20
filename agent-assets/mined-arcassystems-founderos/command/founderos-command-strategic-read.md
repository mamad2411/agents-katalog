---
description: Produce a state-of-the-OS report from the current file layer. Say "give me a strategic read", "where am I", or run /founder-os:strategic-read. Returns 5 sections by default; pass a section key (identity, commitments, decisions, flags, next-moves) to render only that section. Read-only.
allowed-tools: ["Read", "Glob", "Grep"]
---

# Founder OS strategic read

Run the strategic-read skill at `skills/strategic-read/SKILL.md` end to end. Optional single argument selects one section.

## Procedure

1. If `core/identity.md` does not exist, reply `Founder OS not set up here. Say "set up Founder OS" first.` and stop.
2. If `skills/strategic-read/SKILL.md` is missing, reply `strategic-read skill not found at skills/strategic-read/SKILL.md. Restarting Claude Code fixes this most of the time, because it reloads what is installed. If it happens again after a restart, say "update Founder OS".` and stop.
3. If a single argument was passed AND it does not match one of the valid section keys (`identity`, `commitments`, `decisions`, `flags`, `next-moves`), reply `Unknown section: <arg>. Valid keys: identity, commitments, decisions, flags, next-moves.` and stop. Do not fall back to the full report.
4. Follow the strategic-read skill instructions exactly. Read each file in the documented order, run the stale-context check, then render the 5-section report (no arg) or the one selected section (valid arg) inside the fenced block.
5. Output the structured block defined in the skill. Nothing before, nothing after.

## When to use

- Returning to the OS after a gap and needing one orientation pass.
- Before a planning session, to anchor on current state instead of last remembered state.
- When a question touches priorities, pipeline, decisions, and flags at once.

## When NOT to use

- A single-channel question. Use `/today` for the day or `/founder-os:brain-pass "<question>"` for synthesis on a specific topic.
- A keyword match. Use `/founder-os:query "<keyword>"`.

## Examples

- `/founder-os:strategic-read` - full 5-section report
- `/founder-os:strategic-read flags` - only the Active flags section
- `/founder-os:strategic-read next-moves` - only the Next 3 recommended moves section
- "give me a strategic read"
- "where am I across the OS"
- "just give me the flags from the strategic read"

## Rules

- Read-only. This is a read of your current files; nothing is auto-modified.
- No external dependencies. No paid API.
- No em dashes or en dashes.
- No banned words.
- Cite stable entry IDs where they exist. Summarise, do not paste raw bodies.
- If the daily anchor or weekly commitments header is stale, the report prepends a STALE line and recommends refreshing before re-running.

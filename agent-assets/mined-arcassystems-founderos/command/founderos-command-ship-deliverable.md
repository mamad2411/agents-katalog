---
description: Final ship gate. Say "is this ready to send" or "ship-check this" (or run /founder-os:ship-deliverable <path>). Runs template fit, anti-AI scan, blind-spot evidence, and pre-send-check. Read-only.
argument-hint: <path to deliverable>
allowed-tools: ["Read", "Grep"]
---

# Founder OS ship deliverable

Run the ship-deliverable skill at `skills/ship-deliverable/SKILL.md` end to end.

## Procedure

1. If `$ARGUMENTS` is empty, reply `Which deliverable? Re-run as /founder-os:ship-deliverable <path>.` and stop.
2. Verify the file exists.
3. Read `skills/ship-deliverable/SKILL.md`.
4. Use `$ARGUMENTS` as the deliverable path.
5. Run all four links and report one verdict.
6. Do not modify the deliverable.

## Rules

- Read-only.
- Run all links even if one fails.
- No em dashes or en dashes.
- No banned words.

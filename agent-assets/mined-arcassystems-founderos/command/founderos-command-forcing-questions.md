---
description: Pressure-test a new initiative. Say "I'm thinking of starting [X]" or "should I do this" (or run /founder-os:forcing-questions <one-line initiative>). Six forcing questions and a verdict. Anti-scope gate.
argument-hint: <one-line initiative>
allowed-tools: ["Read", "Write", "Edit"]
---

# Founder OS forcing questions

Run the forcing-questions skill at `skills/forcing-questions/SKILL.md` end to end.

## Procedure

1. If `$ARGUMENTS` is empty, reply `What initiative? Re-run as /founder-os:forcing-questions <one-liner>.` and stop.
2. Read `skills/forcing-questions/SKILL.md`.
3. Use `$ARGUMENTS` as the initiative.
4. Ask the six questions in one block.
5. After the founder answers, apply the skill's verdict logic.
6. Do not write to `context/priorities.md`, `brain/log.md`, or `brain/decisions-parked.md` until the verdict has been rendered.

## Rules

- No em dashes or en dashes.
- No banned words.
- Do not add extra questions.

<!-- private-tag: not applicable: writes structured verdict data after confirmed user approval; not user-provided speech content -->

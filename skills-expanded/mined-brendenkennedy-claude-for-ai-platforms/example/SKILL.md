---
name: example-skill
description: >
  REPLACE THIS. A skill auto-surfaces purely on this text, and the listing TRUNCATES it at 1,536
  chars (tail first) inside a shared budget — so front-load and stay ≤1,000 chars. Formula:
  <domain/contract in one clause> — <what it carries: the 3–5 specifics an agent can't guess>. Load
  when <the tasks it covers>. Triggers: <phrases the user will actually type, SHARPEST FIRST — they
  must survive truncation>. Optionally end with a one-clause scope boundary (what belongs to a
  sibling skill instead).
disable-model-invocation: true
---

# <Skill name> — <one-line subtitle>

> A **skill** is on-demand expertise: deep, ground-truth domain knowledge that Claude loads only
> when the `description` matches the task. Reach for it *before* acting in its domain — it carries
> the authoritative detail that the lightweight CLAUDE.md map intentionally omits.

## When this applies
<The situations where this skill is the source of truth. Mirrors the description's triggers.>

## The facts
<The actual knowledge: endpoints, versions, commands, gotchas, contracts, exact configs. This is
what makes a skill worth having — specifics an agent can't guess and shouldn't re-derive. Use
tables and code blocks freely.>

| Thing | Value |
|---|---|
| <key fact> | <value> |

## How to do X
```bash
# concrete, copy-pasteable commands
```

## Gotchas
- <the non-obvious failure mode and how to avoid it>

<!--
Authoring notes (delete in real skills):
- One skill = one coherent domain. If it sprawls, split it.
- The directory name and `name:` should match and be kebab-case: skills/<name>/SKILL.md.
- Skills can include supporting files alongside SKILL.md (scripts, reference docs); link to them
  with relative paths and Claude can read them on demand.
- Put deep knowledge WITH discovery triggers here. Reusable "how we do X" with no triggers →
  .claude/memory/reference/. What happened in a session → .claude/memory/sessions/.
- Keep it refined and current. A stale skill is worse than no skill.
-->

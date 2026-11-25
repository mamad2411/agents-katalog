---
name: conventional-commits
description: Use for ALL commits — enforces incremental commits with Conventional Commits prefixes and descriptive messages in the project language.
license: MIT
---

# Conventional Commits

## Overview

Make small, incremental commits after each completed logical change. Use standardized prefixes to make
the history navigable and allow selective reverts.

## When to Use

**Always.** Every commit follows this convention, from the first change to the end of the session.

## Language

Write the message in the **project language** (`language.user`). The examples below use English for
readability: translate the message, never the prefix.

## Golden rule: one logical change = one commit

Commit immediately after completing ONE atomic change:

- ✅ Spec written → `docs: spec for <entity> registration`
- ✅ Test implemented → `test: reject duplicate identifier`
- ✅ Code implemented → `feat: register <entity>`
- ✅ ADR created → `docs: ADR 0001 - persistence decisions`
- ✅ Refactor → `refactor: extract identifier validation into a method`
- ❌ Do NOT accumulate: "add spec, test, code, ADR and fix bug" in a single commit

## Prefixes

| Prefix | When to use | Example |
|---|---|---|
| `feat:` | New domain feature (code) | `feat: register <event> with multiple items` |
| `test:` | New or modified tests | `test: reject transition from invalid state` |
| `docs:` | Specs, ADRs, documentation (no code) | `docs: spec for lifecycle states` |
| `refactor:` | Structural change without functional change | `refactor: extract state machine into a private method` |
| `fix:` | Bug fix | `fix: validate null identifier before comparing` |
| `chore:` | Config, build, project files | `chore: update linter configuration` |

## Workflow

1. Make one atomic change
2. `git add <files>`
3. `git commit -m "<prefix>: <descriptive message>"`
4. Repeat

Do not wait until the end of the session to commit. Incremental commits allow reverting specific
changes without affecting the rest.

## Role byline (when the commit is executed by an agent)

Commits executed by an agent carry the role as a byline at the end of the body:

```text
git commit -m "feat: register <event> with multiple items

By <role>."
```

- Only when the commit is executed by an agent. User commits do not carry a byline.
- The byline goes in the **body**, never in the title (the title keeps the conventional prefix).
- Examples: `By analyst.`, `By engineer.`, `By qa-analyst.`

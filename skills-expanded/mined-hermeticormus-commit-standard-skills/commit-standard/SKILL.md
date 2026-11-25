---
name: commit-standard
description: Disciplined git commit messages following the Ormus Commit Standard (OCS) v1.0 — type(scope) structure, imperative subject, no emoji, no AI footers, atomicity rules. Use when writing commit messages.
license: MIT
---

# Commit standard (OCS v1.0)

Apply to every commit message.

## Shape

```
<type>(<scope>): <imperative summary, ≤72 chars, no period>

<why>

<what>

Refs: #123
```

## Types

`feat fix refactor perf docs test style chore build ci revert`

## Subject

- Imperative mood
- Lowercase first letter
- No trailing period
- ≤72 chars (aim ≤50)
- No emoji
- No " and " — split

## Body

- Lead with why
- Don't restate the diff
- 2-4 paragraphs max
- No hype

## Banned

- Emoji
- `Generated with Claude Code` / `Co-Authored-By: Claude`
- Marketing language
- Bare `chore: misc`

## Atomicity

One concern per commit. Tests with the behavior change. Squash WIP before push.

---

Full standard + good/bad examples at https://github.com/HermeticOrmus/commit-standard-skills.

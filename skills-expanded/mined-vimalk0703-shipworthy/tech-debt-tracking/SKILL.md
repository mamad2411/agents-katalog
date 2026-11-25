---
name: tech-debt-tracking
description: Track shortcuts with justifications, prevent debt accumulation, and surface outstanding debt at session start.
invoke_when: Use when taking a shortcut, writing a TODO, bypassing a quality gate with justification, or reviewing accumulated tech debt.
---

# Tech Debt Tracking

## Purpose

Every shortcut has a cost. This skill ensures shortcuts are conscious decisions with documented justifications, not accidents that compound silently.

## When to Track

- Skipping tests for time pressure
- Using a workaround instead of a proper fix
- Hardcoding a value that should be configurable
- Writing a TODO comment
- Bypassing a quality gate with justification
- Using a deprecated API or pattern
- Choosing a quick solution over the correct one

## How to Track

Add an entry to `.shipworthy/tech-debt.md`:

```markdown
## [Short Description]
- **Date**: YYYY-MM-DD
- **Severity**: low | medium | high | critical
- **Effort to fix**: hours | days | weeks
- **Justification**: Why was this shortcut taken?
- **Impact if not fixed**: What happens if this stays forever?
- **Files affected**: List specific files
```

## Rules

1. **Every shortcut requires justification** — "I didn't have time" is a valid justification, but document it
2. **No silent TODOs** — every `TODO` in code must have a corresponding entry in tech-debt.md
3. **Review at session start** — the session-start hook surfaces the debt count
4. **Debt has a severity** — critical debt should be fixed before adding new features
5. **Debt has a shelf life** — if it's been there >30 days with no plan to fix, escalate the conversation

## When to Pay Down Debt

- Before starting a new feature in the same area
- When the debt is causing real problems (bugs, slowness, confusion)
- During dedicated refactoring time
- When the effort to work around the debt exceeds the effort to fix it

## Anti-Patterns

- Tracking debt but never paying it down
- Not tracking debt at all ("we'll remember")
- Treating all debt as equal (prioritize by severity and impact)
- Using debt tracking as an excuse to write sloppy code ("I'll track it as debt")

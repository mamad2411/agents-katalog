---
name: critique
description: Score a codebase's design quality 0-100 across six categories (typography, color, spacing, motion, accessibility, consistency) plus an overall weighted score. Every score is derived from concrete metrics in dragoon.json with transparent math, no LLM, no vibes. Use when the user asks "what's the design quality of this codebase", "rate my design", "audit the design system", or wants a CI gate for design. Includes a per-category breakdown explaining each deduction. Auto-scans if no manifest exists. Run as `node ~/.claude/skills/dragoon/skills/critique/scripts/critique.js [root]`.
version: 1.0.0
---

# /critique

0-100 scores for design quality. Transparent math. Every deduction is traceable to a metric in `dragoon.json`.

## When to use

Run /critique when:
- The user asks for a design quality score, audit, rating, or grade
- Setting up a CI gate that fails when design quality drops below a threshold
- Comparing design quality before and after a redesign
- The user says "how good is this", "give me a score", "rate the design system"

## What it produces

Six category scores plus an overall:
- **typography** - font family count, scale ratio confidence, font size variant count
- **color** - distinct color count, palette balance
- **spacing** - grid detection confidence, spacing variant count
- **motion** - easing variant count, duration variant count
- **accessibility** - alt rate, button label rate, semantic tag presence
- **consistency** - shadow variant count, radius variant count

Weighted overall:
```
typography 1.0  color 1.0  spacing 1.2  motion 0.8  accessibility 1.2  consistency 1.0
```

Each score includes a breakdown listing every deduction and reason. You can read exactly why your score is what it is.

## Run it

```
node ~/.claude/skills/dragoon/skills/critique/scripts/critique.js [root]
```

Flags:
- `--manifest <p>` use existing manifest instead of scanning
- `--json` machine-readable
- `--threshold <n>` exit non-zero if overall score below n (CI gate)
- `--no-breakdown` show scores only
- `--quiet` show only the final score
- `--help` full usage

## Use as a CI gate

In package.json:
```
"design:check": "node ~/.claude/skills/dragoon/skills/critique/scripts/critique.js --threshold 80 --quiet"
```

The command exits 1 if the overall score drops below 80, blocking the PR.

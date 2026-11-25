---
name: investigate
description: Structured root-cause investigation template. Encodes the rule "no patches until you can reproduce, predict, and explain the bug." Forces hypothesis-test pairs, evidence collection, and a prevention plan. Use when the user reports a bug or asks to fix something they don't fully understand yet. Run as `node ~/.claude/skills/dragoon/skills/investigate/scripts/investigate.js "<symptom>"`.
version: 1.0.0
---

# /investigate

The discipline tool: no patches without root-cause clarity.

## When to use

- Bug report
- Anything intermittent
- The user says "fix this" but the underlying cause isn't clear

## Forces

- exact reproduction steps
- multiple hypotheses with how-to-test for each
- raw evidence (logs, traces) before reasoning
- a prevention plan beyond just the fix

## Run it

```
dragoon investigate "form submit hangs after upload"
dragoon investigate "..." --apply
```

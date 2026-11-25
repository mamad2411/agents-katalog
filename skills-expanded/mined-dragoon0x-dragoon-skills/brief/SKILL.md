---
name: brief
description: Generate a structured product brief markdown from a one-line idea, pre-filled with codebase facts (stack, type system, palette, components count) from dragoon.json. Use when the user is starting a new feature, project, or initiative and wants to think through it before coding. Output goes to .dragoon/plans/brief-{slug}-{date}.md. Defaults to dry-run preview; pass --apply to write. Run as `node ~/.claude/skills/dragoon/skills/brief/scripts/brief.js "<idea>"`.
version: 1.0.0
---

# /brief

Generates a product brief template with codebase context auto-loaded.

## When to use

- Starting a new feature, initiative, or project
- The user says "let's think through X first", "before we build", "draft a brief for"
- Front of the sprint

## Output

Writes to `.dragoon/plans/brief-{slug}-{YYYYMMDD}.md`. Sections:
- one-line idea
- why now
- who is this for
- what does success look like
- the smallest version that proves the idea
- what could go wrong
- codebase context (auto-loaded from dragoon.json)

## Run it

```
dragoon brief "add user invites"
dragoon brief "add user invites" --apply
```

After /brief, run /plan-eng and /plan-design (or /autoplan to do all three at once).

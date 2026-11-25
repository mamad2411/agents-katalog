---
name: autoplan
description: Run /brief, /plan-eng, and /plan-design in one shot to bootstrap a complete sprint plan. All three documents land in .dragoon/plans/ pre-filled with codebase facts. Use when the user wants to spin up a full plan quickly. Defaults to dry-run; pass --apply to write all three files. Run as `node ~/.claude/skills/dragoon/skills/autoplan/scripts/autoplan.js "<idea>"`.
version: 1.0.0
---

# /autoplan

Chains the three planning skills in one command. The fastest way to go from "we should build X" to a complete sprint plan.

## When to use

- Spinning up a new initiative
- The user says "plan everything", "give me the full plan", "let's plan this end to end"
- Saves three sequential commands

## What it produces

Three files in `.dragoon/plans/`:
- `brief-{slug}-{date}.md`
- `plan-eng-{slug}-{date}.md`
- `plan-design-{slug}-{date}.md`

## Run it

```
dragoon autoplan "add user invites"
dragoon autoplan "add user invites" --apply

# skip parts you don't need
dragoon autoplan "small tweak" --apply --skip plan-design
```

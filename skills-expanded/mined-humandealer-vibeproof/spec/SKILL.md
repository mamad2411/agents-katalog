---
name: spec
description: Turn a plain-language product idea into a PRD.md. Use when a non-technical expert describes what they want to build ("I want an app that...", "build me a tool for..."). Interviews to extract the non-obvious requirements, then writes docs/PRD.md.
---

# spec — idea → PRD

The expert knows their domain. They do NOT know how to write a spec. Your job is
to interview them in **plain language** and turn it into a `docs/PRD.md` a senior
engineer would accept.

## Step 1 — Interview (plain language, ONE question at a time)

Never ask 10 questions at once. Ask the most important one, wait, then the next.
Extract the things experts forget to mention:

- **Who uses this and what do they do today?** (the status quo you're replacing)
- **The one job it must do** — if it only did one thing, what?
- **What does "done" look like?** — a concrete success scenario
- **Inputs & outputs** — what goes in, what comes out
- **Hard constraints** — budget, deadline, must-integrate-with, compliance
- **What it must NOT do** — the failure that would be unacceptable

Stop interviewing when you can write the success scenario yourself without guessing.

## Step 2 — Write docs/PRD.md

```markdown
# PRD: <product name>

## Problem
<who, what they do today, why it's painful — in the expert's own words>

## The one job
<the single core job, one sentence>

## Success scenario
<concrete walkthrough: user does X → system does Y → outcome Z>

## Requirements
- [ ] R1: <must-have, testable>
- [ ] R2: ...

## Out of scope (v1)
- <what we are deliberately NOT building yet>

## Constraints
| Constraint | Value |
|-----------|-------|
| Deadline | ... |
| Budget | ... |
| Must integrate | ... |
| Compliance | ... |

## Non-negotiables (the unacceptable failure)
- <the thing that must never happen>
```

## Step 3 — Hand off
Tell the expert in one line what you captured, then: **"Next: `/plan` turns this
into a build plan."** Do not start coding from a PRD — the plan comes first.

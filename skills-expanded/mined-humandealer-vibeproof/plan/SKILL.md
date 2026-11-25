---
name: plan
description: Turn docs/PRD.md into docs/PLAN.md — an ordered, checkbox build plan with architecture, risk gates, and a test list. Use after /spec, before any code. The plan survives session compaction; conversation context does not.
---

# plan — PRD → build plan

A senior engineer never codes from a PRD directly. They design first. You write
`docs/PLAN.md` so a non-coder can see *what will happen* and *in what order*,
and so the build survives a lost session.

## Step 1 — Design before steps

Decide and write down, briefly:
- **Stack** — language/framework, and WHY (match what the future dev team expects)
- **Data flow** — what data moves where (one diagram or 3 bullets)
- **The risky parts** — auth, money, external APIs, data deletion. These get extra care.

## Step 2 — Write docs/PLAN.md

```markdown
# PLAN: <product>

## Architecture (1 paragraph + data flow)
<stack choice + why; data flow>

## Risk gates (require extra care / human confirm before doing)
- [ ] Touches auth / secrets
- [ ] Touches money flows
- [ ] Deletes or migrates data
- [ ] Calls external paid APIs
> If any box is checked, /spec's non-negotiables apply — confirm with the expert.

## Build steps (ordered, atomic — one logical change each)
- [ ] S1: <step> → test: <what proves it works>
- [ ] S2: ...

## Tests to write FIRST (the contract)
- [ ] T1: <behavior> — given X, expect Y
- [ ] T2: ...

## Definition of done
- [ ] All steps done, all tests green
- [ ] `vibeproof check` → READY
- [ ] PR opened, CI green (where wired)
```

## Step 3 — Persist + hand off
Save to `docs/PLAN.md` (it survives compaction — conversation does not). Then:
**"Next: `/tdd` writes the tests before the code."** Track progress by checking
boxes as you go. Never skip ahead.

> Rule: if a build step's description contains the word "and", it's probably two
> steps. Split it.

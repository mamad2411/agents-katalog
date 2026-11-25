---
name: design-get-context
description: Clarify the brief BEFORE any design work to avoid building the wrong thing. Interrogates goal, user, constraints, success criteria, and scope, then writes a short context doc the other design skills consume. Use when the user says "let's design X", "build a UI for Y", "get context", "clarify the brief", or kicks off any product-design task without a clear spec. First stage of the Product Design set — highest leverage for reducing rework.
---

# Design — Get Context

De-risk the whole design effort by nailing the brief first. The cheapest fix is the question you ask before building. This skill produces `./design/context.md` — the single source of truth every other design skill reads. Skipping it is the #1 cause of "that's not what I meant" rework.

## When to use
- Any new design/UI task where the spec isn't already crisp.
- The request is a one-liner ("design a settings page") with implicit, unstated requirements.
- Before `design-research`, `design-audit`, `design-ideate`, or any build skill.

## When NOT to use
- A solid `./design/context.md` (or equivalent spec) already exists → proceed to the next skill.
- A pure visual-asset task with no UX → that's the Creative Production set.

## What to interrogate (ask the gaps, don't dump all at once)
- **Goal**: what outcome or behavior change is this UI for? (not "a page" — *why*)
- **User**: who uses it, their context, tech comfort, frequency.
- **Job-to-be-done**: the core task the screen must make effortless.
- **Constraints**: existing stack, design system, brand, platform, deadline.
- **Success criteria**: how we'll know it worked — ideally measurable.
- **Scope**: must-have vs nice-to-have for v1; explicit non-goals.

Ask only the questions whose answers would *change the design*. If something's already given, don't re-ask. If the user can't answer "success criteria", propose 2-3 candidates and let them pick.

## Workflow
1. Identify the critical unknowns (the ones that would change what you build).
2. Ask them concisely, grouped, not as a 20-question interrogation.
3. If the user's framing seems flawed (wrong problem, contradictory constraints), **raise it and propose an alternative** before proceeding.
4. Write `./design/context.md` with answers + explicitly flagged assumptions + risks.
5. Hand off to `design-research`, `design-audit`, or `design-ideate`.

## Output: ./design/context.md
```
# Context
goal: cut onboarding drop-off (currently 40% abandon at step 2)
user: first-time SaaS trial users, mixed tech comfort, on desktop
JTBD: get to "first value" (a created project) in under 2 minutes
constraints: stack=Next.js + Tailwind  DS=internal "Aurora"  platform=web  deadline=2wk
success: step-2 completion ↑ from 60% → 80%; time-to-first-project < 2min
scope v1: [3-step wizard, skip-able, progress saved]
non-goals: [mobile layout, SSO, team invites]
open assumptions: [users have a use case in mind on arrival]
⚠ risks: [if drop-off is a value problem not a UX problem, redesign won't fix it]
```

## Quality bar
- Goal, user, and success criteria are all present (or explicitly deferred by the user).
- Success criteria are concrete enough to QA against later (`design-qa` reads these).
- Every guess is labeled an assumption — nothing is silently invented.
- Non-goals are stated so scope can't creep unnoticed.

## Common pitfalls
- **Starting to design before the brief is clear** — the entire point of this skill is to prevent that.
- **Question-dumping** — 20 questions at once stalls the user. Ask the few that matter.
- **Burying a guess as a fact** — if you assumed it, say "assumption:".
- **Accepting a flawed framing silently** — if the user's asking for the wrong thing, surface it now (cheap) not after building (expensive).

## Handoff
`context.md` → `design-research` (gather outside signal), `design-audit` (if improving existing UI), or `design-ideate` (go straight to directions). Every downstream skill reads this file.

## Tooling
None required — this is a conversation + a written artifact.

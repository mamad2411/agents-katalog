---
name: product-design
description: Orchestrator for the Product Design skill set — turn early ideas into reviewable prototypes. Routes to the right sub-skill (get-context, research, audit, ideate, image-to-code, url-to-code, prototype, qa, share) based on where you are in the design process. Use when the user gives a high-level design goal like "design a UI for X", "prototype this idea", "rebuild this screen", "review our flow", or isn't sure which design step they need. Delegates to design-* skills.
---

# Product Design — Orchestrator

The umbrella for the 9 `design-*` skills. Your job: read the request, locate it in the design process, route to the right sub-skill. **Don't do the work here — dispatch.** You're the design lead sequencing the work, not the IC executing each step.

## When to use
- The user gives a broad design goal ("design a UI for X", "prototype this idea") and the step is ambiguous.
- A design project spans multiple stages and needs sequencing.
- The user doesn't know which sub-skill they need.

## When NOT to use
- The user named a step explicitly ("audit this screen") → go straight to that sub-skill.
- It's visual-asset creation (ads, product shots, moodboards), not UI/UX → `creative-production` orchestrator.

## The pipeline
```
FRAME                 EXPLORE              BUILD                          SHIP
design-get-context ─► design-research ──► design-ideate ─► design-image-to-code ─┐
                      design-audit                          design-url-to-code   ├─► design-prototype ─► design-qa ─► design-share
```
Frame the problem → explore options → build the chosen one → gate quality → ship for review.

## Routing table
| User intent / phrasing | Route to |
|---|---|
| new design task, brief unclear | `design-get-context` (almost always start here) |
| "how do others do X", competitor/pattern scan | `design-research` |
| "what's wrong with this UI", review existing | `design-audit` |
| "give me layout options/directions" | `design-ideate` |
| "build this mockup/screenshot" | `design-image-to-code` |
| "clone/rebuild this live site" | `design-url-to-code` |
| "make it clickable", "wire the flow" | `design-prototype` |
| "does it match the design/spec" | `design-qa` |
| "share it", "give me a link", "publish" | `design-share` |

## How to orchestrate
1. **Frame first.** Unless `./design/context.md` already exists, start with `design-get-context`. The cheapest fix is the question asked before building.
2. **Explore** with `research`/`audit` as needed, then `ideate` directions.
3. **Build**: turn the chosen direction into code via `image-to-code` (from a mockup) or `url-to-code` (from a live site), then `prototype` to wire interactivity.
4. **Gate** with `design-qa` before `design-share`. Don't ship HIGH-severity drift.
5. **`context.md` is the shared source of truth** — every sub-skill reads it; keep it current.

## Worked example
Request: "Our onboarding loses people. Can you redesign it and give me something clickable to test?"
```
plan:
 1. frame      → design-get-context  → goal: ↓ step-2 drop-off; success: 60%→80%
 2. explore    → design-research     → competitor onboarding patterns + pains
                 design-audit         → audit current flow (3 HIGH issues found)
 3. options    → design-ideate       → 3 directions; user picks "Guided Wizard"
 4. build      → design-image-to-code → implement the wizard screens
                 design-prototype     → wire Welcome→Template→Name→Dashboard + error state
 5. gate       → design-qa           → conformance vs context (fix 2 items, re-QA → PASS)
 6. ship       → design-share        → local link + review note
dispatch order respects: frame → explore → build → gate → ship
```

## Quality bar
- The brief is framed (`context.md`) before any building begins.
- On multi-stage requests, the user sees the plan (which skills, what order) before execution.
- QA gates sharing — nothing stakeholder-facing ships with unresolved HIGH issues.
- Success criteria from `get-context` are what `design-qa` checks against (closed loop).

## Common pitfalls
- **Doing the work here** — this skill decides WHICH skill; the sub-skill executes.
- **Skipping the frame** — building before goal/user/success are known is the top rework cause.
- **Shipping before QA** — `design-share` without `design-qa` circulates drift.
- **Losing context.md** between stages — sub-skills lose the source of truth and drift.

## Tooling
Sub-skills use vision, browser-automation, web-fetch, and optional image tools as needed. The orchestrator itself needs no tooling — it sequences and dispatches. If a sub-skill's tool is unavailable, it degrades gracefully and flags what's unverified.

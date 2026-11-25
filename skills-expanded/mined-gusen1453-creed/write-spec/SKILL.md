---
name: write-spec
description: "Use after design alignment (grill), or when the user asks for a design/spec/PRD doc, or when locking scope before an implementation plan, or when handing work off to someone who was not in the design discussion."
---

# Write Spec

> **Output language:** answer and write artifacts in the user's own language (match their messages, not the repo's history).

## Overview

Turn an **approved design** into a durable **product spec** that a new teammate (or future you) can understand without the meeting recording.

**Spec = what & why.** **Plan = how & in what order.** Do not mix them.

**REQUIRED UPSTREAM:** **grill** (or an already-approved design the user points at). Do not invent product decisions while writing the spec.

**Announce:** "Using write-spec to …"

## When to Use

- After grill approval, before **write-plan**
- User asks for a design doc / spec / PRD-lite
- Handing work to another person or agent who was not in the grill

**When NOT to use:** pure bugfix with known fix; one-line change with no product ambiguity; user already has an approved written spec and only wants **write-plan**.

## The Iron Law

```
A SPEC NO NEWCOMER CAN ACT FROM IS THEATER.
Write in plain language. Drive with user-visible scenarios.
Every "should" must become a concrete case someone can demo or test.
No file paths, TDD steps, or commit lists — those belong in write-plan.
```

## Voice: builder who lives in their own product

Write for one reader who is both the engineer and a daily user of what they build:

- **Pair value with mechanism** — say what the experience feels like *and* name the tech choice behind it, so they keep control of both product and code
- Lead with **perceivable upside / downside / cost**, but never drop the mechanism into vague "user speak"
- Prefer "what the user sees + the mechanism that delivers it" over "the system should have pluggable…"
- Name the **trade-off you chose** and what you **explicitly skip** this round
- Scenarios carry the product story (§2); "How we'll build it" (§7) carries the precise tech — keep them distinct, keep both honest

## Spec vs Plan (do not blur)

| | Spec (`write-spec`) | Plan (`write-plan`) |
|--|---------------------|---------------------|
| Question | What should the product do, and why? | Which files, in what order, how do we verify? |
| Reader | Product owner, new hire, future you | Implementer / coding agent |
| Content | Scenarios, scope, trade-offs, acceptance | Paths, interfaces, RED→GREEN→commit |
| Bad smell | File lists, "Task 3", pytest commands | "Maybe we should also support X" undecided |

## Workflow

1. **Confirm source** — approved grill summary or user-supplied design; unresolved decisions → back to **grill**; if explore produced a fact checklist, fold it into §0 Current state
2. **Pick path** — default `docs/creed/specs/YYYY-MM-DD-<topic>-design.md` (user path overrides)
3. **Write the spec** — use the template below; scale length to complexity
4. **Self-review** — checklist at bottom
5. **User gate** — ask them to skim before planning
6. **Hand off** — if the slice adds modules / ports / IO edges → **solid** (Gate); else → **write-plan** → **tdd**

## Spec template (required sections)

```markdown
# <Feature> Spec

**Status:** Draft | Approved
**Date:** YYYY-MM-DD
**Owner:** <who decides product calls>
**Issue:** #<N>   ← only when this session already has an issue number; omit the line otherwise

## 0. Current state (from explore) — refactor/legacy only

When explore produced a fact checklist (the task modified existing code), open the
spec with it so a newcomer doesn't re-read the repo. Skip this section for greenfield.

- **Anchors:** <methods/classes/tables read, current behavior>
- **Assertion check:** <user's claims → ✓/✗ with evidence>
- **Conflicts:** <constraint vs repo reality, resolved by the decisions below>

## 1. One-liner (board slide)

<One sentence: who gets what benefit, and the main cost/risk we accept.>

## 2. User scenarios (source of truth)

### Happy path
- **Who:** …
- **When:** …
- **Does:** …
- **Sees:** …

### Failure / edge
- **Who:** …
- **When:** … (timeout, empty, permission, conflict, …)
- **Sees / system does:** …

(Add more scenarios until a newcomer can role-play the feature.)

## 3. Scope

**In:**
- …

**Out (this round):**
- … — why skipped: …

## 4. Decision log (mentoring)

| Decision | Chose | Rejected | Why (user/business impact) |
|----------|-------|----------|----------------------------|
| … | A | B | Users get …; we accept … |

## 5. Acceptance (demo / test language)

- [ ] Scenario: … → observable result …
- [ ] Scenario: … → observable result …

## 6. Constraints

- Platforms / versions / naming / perf floors (quantify if it matters to users)

## 7. How we'll build it (short)

<2–5 sentences: main components and boundaries. No task list.>

## 8. Open risks

- … → mitigation / accept
```

## Writing rules

1. **Scenario before mechanism** — if you cannot write a Who/When/Does/Sees case, you do not understand the requirement yet → **grill**
2. **Replace adjectives with cases** — "flexible / polished / high-performance" → concrete limits and outcomes
3. **User-perceivable trade-offs** — when comparing options in the decision log, state what the *user* gains or loses, then the engineering cost
4. **Mentoring value** — decision log + Out-of-scope are mandatory; they teach judgment, not just the happy path
5. **One shippable slice** — if the doc covers two independent products, split into two specs

### Bad → good

| Bad (obscure / unteachable) | Good (user-visible / teachable) |
|-----------------------------|----------------------------------|
| Support pluggable auth middleware | Logged-out user hits Export → login → return and auto-continue export |
| Improve resilience | Network fail on Complete → status unchanged + retry message; no half-done state |
| Flexible batch import | Max 500 rows; row 3 bad → reject whole batch and point at row 3 |

## Self-review (before user review)

1. No TBD / "it depends" left as product decisions
2. No contradictions between scenarios and acceptance
3. No implementation plan leaked (paths, RED/GREEN, commits)
4. A new hire could explain the feature from §0–§5 alone
5. Every In-scope item maps to at least one scenario

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "We'll put file paths in the spec so plan is shorter" | Spec stays stable; plan churns. Keep them apart. |
| "Architecture diagram is enough" | Diagrams don't teach *when* the user sees an error. |
| "Too simple for scenarios" | Tiny features hide the worst assumptions. One happy + one failure case still required. |
| "Decision log is bureaucracy" | Without it, the next person re-litigates the same choice. |
| "Board language dumbs it down" | Clear upside/cost is leadership, not dumbing down. |

## Checklist

- [ ] Upstream design approved (grill or equivalent)
- [ ] Spec file written from template
- [ ] Scenarios + In/Out + decision log + acceptance present
- [ ] User reviewed (or explicitly waived)
- [ ] Ready for **solid** (if new boundaries) or **write-plan**

## Hand-off

**Transition gate** — before the spec is passed to the next stage, ask the user (one AskUserQuestion; never auto-advance):

```
A) Recommended: Proceed → solid (new boundaries) / write-plan
B) Review first — run **review** on this spec (`references/spec.md`; upstream = approved grill design), then return to this gate
C) Adjust — revise the spec, then return to this gate
D) Something else (I will type it)
```

- New modules / ports / IO edges → **solid** (Gate)
- No new boundary → **write-plan**
- Product still open → **grill** (do not plan)

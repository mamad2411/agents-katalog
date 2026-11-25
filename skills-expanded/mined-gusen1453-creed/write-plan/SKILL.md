---
name: write-plan
description: "Use when you have an approved design or spec, or clear requirements for multi-step work, before touching production code, or when the user asks for an implementation plan or task breakdown."
---

# Write Plan

> **Output language:** answer and write artifacts in the user's own language (match their messages, not the repo's history).

## Overview

Turn an approved design into an **implementation plan** a forgetful agent can execute without inventing scope.

**Core principle: each task is independently testable; steps are 2–5 minutes; TDD is the default micro-cycle.**

**REQUIRED UPSTREAM:** **write-spec** (or an approved written/verbal design from **grill**). **solid** for non-trivial boundaries. Do not plan while product decisions are still open.

**Announce:** "Using write-plan to …"

## When to Use

- After **write-spec** (or waived verbal design) is approved, before coding
- Multi-file or multi-step features
- User asks for an implementation plan / task breakdown

**When NOT to use:** product still open → **grill** / **write-spec** first; single-line fix with obvious one-test cycle (go straight to **tdd**); pure exploration.

## The Iron Law

```
NO CODING FROM A VAGUE PLAN.
Every task lists exact files, a failing-test step, a verify-red step, minimal impl, verify-green, and a commit step (or explicit why commit is deferred).
```

## Workflow

1. **Scope check** — multiple independent subsystems? Split into separate plans (one shippable slice each).
2. **File map** — before locking the paths, take the structure pointer: **solid** for boundaries (ports / adapters / dependency arrows). If the slice adds no new boundary, say so and move on. The file map records the result.
3. **Task breakdown** — bite-sized; fold scaffolding into the task that needs it. Before writing each task's RED step, take the verification pointer: **test-design** for the case list — every case reads in user/product words (goal / conditions / parameters), so a non-author can see *what* is proven and *why*. These cases are the tasks' RED tests.
4. **Write the plan file** — default `docs/creed/plans/YYYY-MM-DD-<feature>.md` (user path overrides).
5. **Self-review** — no TBD, tasks have Interfaces + verification commands, YAGNI.
6. **User gate** — ask them to skim the plan before execution.
7. **Hand off** — execute with **tdd** + **test-design** (optionally Superpowers subagent-driven-development / executing-plans).

These two pointers are *suggestions to pass through*, not mandatory gates: solid may be skipped (no new boundary), test-design is where the cases come from. Naming them here is what keeps them from being silently skipped — or over-applied.

## Plan header (required)

```markdown
# <Feature> Implementation Plan

> **For agents:** Use Creed **tdd** + **test-design** per task. Optional: Superpowers subagent-driven-development / executing-plans.

**Goal:** <one sentence>

**Architecture:** <2–3 sentences — the boundaries settled with **solid**; if no new boundary, say "no new boundary">

**Tech Stack:** <key libs>

**Cases (from test-design):** <the "when …, it should …" list, each with goal / conditions / parameters in reader-facing words>

## Global Constraints

- <verbatim constraints from spec: versions, naming, platforms, …>

---
```

## Task template

````markdown
### Task N: <Name>

**Files:**
- Create: `path/to/file.ts`
- Modify: `path/to/existing.ts`
- Test: `path/to/file.test.ts`

**Interfaces:**
- Consumes: <signatures from earlier tasks>
- Produces: <names/types later tasks rely on>

- [ ] **Step 1: Write the failing test** (apply **test-design**)
- [ ] **Step 2: Run it — expect FAIL for the right reason**
- [ ] **Step 3: Minimal implementation** (**tdd** GREEN; **solid** boundaries)
- [ ] **Step 4: Run tests — expect PASS**
- [ ] **Step 5: Commit** (or defer with reason; ship later via **commit-and-push**)
````

Inline the critical test/impl snippets when they clarify the API; don't dump novels.

## Granularity

| Good task | Bad task |
|-----------|----------|
| One behavior + its test cycle | "Implement auth" |
| Exact paths | "Update the server stuff" |
| Independently reviewable | Must finish Task 5 to know if Task 2 worked |

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "We'll figure paths while coding" | That's how scope creeps. Lock files in the plan. |
| "One big task is fine" | Reviewer can't reject half. Split. |
| "Skip test steps — we'll TDD later" | Later = never. Steps include RED/GREEN. |
| "Plan is the design doc" | Spec (`write-spec`) = what/why; plan = who touches which file when. |
| "We'll decide product scope in the plan" | Open product calls → back to **grill**, then **write-spec**. |
| "Solid is ceremony, skip it" | Then say "no new boundary" and move on — an unstated skip is the problem, not the skip. |
| "test-design is for later, in tdd" | The cases shape the tasks' RED steps. Deciding them in the plan is what makes each task independently testable. |

## Checklist

- [ ] Spec approved (`write-spec`) or verbal design + waiver
- [ ] Structure pointer passed (**solid**) — or "no new boundary" said out loud
- [ ] Verification pointer passed (**test-design**) — cases in user/product words (goal / conditions / parameters)
- [ ] Plan file written with header + tasks
- [ ] Each task: files, interfaces, RED→GREEN→commit
- [ ] Plan does not re-open product decisions
- [ ] User reviewed plan (or explicitly waived)
- [ ] Ready for tdd execution

## Hand-off

**Transition gate** — before the plan is handed to execution or the next stage, ask the user (one AskUserQuestion; never auto-advance):

```
A) Recommended: Proceed → tdd (+ test-design)
B) Review first — run **review** on this plan (`references/plan.md`; upstream = the spec it narrows), then return to this gate
C) Adjust — revise the plan, then return to this gate
D) Something else (I will type it)
```

- Product still fuzzy → **grill** / **write-spec**
- Execute → **tdd** + **test-design**
- Stuck on structure → **solid**
- Done shipping → **review** then **commit-and-push**

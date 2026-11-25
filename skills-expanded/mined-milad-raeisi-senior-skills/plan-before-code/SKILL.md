---
name: plan-before-code
description: Turn a fuzzy or multi-part request into a precise, verifiable plan before writing code. Use for new features, changes that span several files or modules, anything touching data models, public APIs, migrations, or infrastructure, and requests with ambiguous requirements, such as "build X", "add support for Y", "let's implement", or "how should we approach". Reads the codebase first, asks only the questions that change the outcome, compares 2 to 3 approaches, and produces small, independently verifiable steps.
license: MIT
metadata:
  category: craft
  version: "1.2.0"
---

# Plan Before Code

An hour of planning saves a day of rework, but only if the plan is grounded in the actual code and turns into steps that can each be verified. The aim is not a document; it is to discover the hard parts and the user's real decisions *before* they are buried in a half-built implementation.

Skip the formal plan for small, obvious changes (one file, clear request, easy to reverse). Do it whenever being wrong would be expensive.

## Phase 1: Understand

- Restate the goal in one or two sentences, including *who* benefits and *how you'll know it works*.
- Read the code the change will touch: entry points, data models, similar existing features. The best plan usually follows a pattern the codebase already uses.
- Note constraints: compatibility promises, performance budgets, migrations, feature flags, deploy process, and conventions in `AGENTS.md`, `CLAUDE.md`, or ADRs.
- For unfamiliar territory, scout prior art first (see `prior-art-scout`).

## Phase 2: Ask only what matters

List the open questions, then remove every one you can answer by reading the code, docs, or conventions. Ask the rest in **one batch**, each with your recommended default so the user can just say "yes":

```
1. Should archived projects appear in search? I recommend no (matches how the dashboard filters them).
2. Is a DB migration acceptable for this release? I recommend yes, additive only, so rollback stays safe.
```

If nothing remains that would change the outcome, don't ask; state your assumptions and proceed.

## Phase 3: Design it twice

Sketch 2 or 3 genuinely different approaches, such as different data models, different layers, or build versus adopt. Compare them on what matters here:

| | Approach A | Approach B |
|---|---|---|
| Complexity added | | |
| Risk and reversibility | | |
| Fit with existing patterns | | |
| UX, DX, and AX impact | | |
| Effort | | |

Recommend one and say why in a sentence. The first idea is rarely the best one, and the comparison is what exposes hidden costs.

## Phase 4: Write the plan

Break the work into steps that are each **small, independently verifiable, and leave the system working**:

```markdown
## Plan: <feature>

**Goal:** ...
**Approach:** ... (alternatives considered: ..., rejected because ...)
**Out of scope:** ...

### Steps
1. **Add `archived_at` column (additive migration).**
   Files: `db/migrations/...`, `models/project.ts`
   Verify: migration runs up and down locally; model tests pass.
2. **Filter archived projects from search.**
   Files: `search/query.ts`, `search/query.test.ts`
   Verify: new test "excludes archived projects" fails first, then passes.
3. ...

### Risks
- ... and how each is mitigated or detected.
```

Order the steps so the **riskiest unknown is tackled first**, while it's still cheap to change course. Prefer vertical slices that deliver a thin end-to-end path early over finishing one layer at a time.

## Phase 5: Execute the plan

Work through the steps with `test-driven-development`, verify each before starting the next, and keep going to the end (`finish-the-job`). When reality contradicts the plan, update the plan, say what changed and why, and continue. A plan is a tool, not a contract.

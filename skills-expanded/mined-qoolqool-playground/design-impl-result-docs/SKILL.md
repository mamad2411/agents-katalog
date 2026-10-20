---
name: design-impl-result-docs
description: "Three-document structured delivery workflow for distributed/compose projects: design doc (decisions + criteria) -> implementation plan (step-by-step Red-Green phases) -> implementation result (commits + verification). Creates a traceable audit trail from decision to deployed code."
version: 1
created: 2026-05-16
updated: 2026-05-16
---
# Design → Implementation Plan → Implementation Result Doc Workflow

Structured three-document workflow for delivering features in distributed/compose projects. Each document has a specific role, audience, and set of mandatory fields. Together they form an audit trail from decision to working code.

## When to Use

- Adding a significant feature to a Docker Compose microservices project (new service, new infrastructure, new cross-service flow)
- When the change touches multiple files, multiple services, or introduces new architectural decisions
- When you need an audit trail from design rationale to deployed result
- Before starting any task documented in AGENT.md as requiring a "design doc" or "implementation plan"

## Why Three Documents (Not One)

| Document | Purpose | Written When | Audience |
|----------|---------|-------------|----------|
| **Design doc** | What + Why + architectural decisions | Before coding | Tech lead, architect, future-you |
| **Implementation plan** | Step-by-step HOW with exact code/commands | After design approved | Implementer (you or teammate) |
| **Implementation result** | What was ACTUALLY done + verification | After implementation | QA, ops, future-you debugging |

A single "design and implementation" doc drifts: decisions get mixed with steps, and nobody updates it after reality diverges. Three docs force you to separate intent from execution from outcome.

## Procedure

### Step 1: Write the Design Doc

**Location:** `docs/plans/YYYY-MM-DD-<topic>-design.md`

**Mandatory fields:**

```markdown
# <Topic> Design

**Date:** YYYY-MM-DD
**Status:** Draft | Approved | Superseded
**Methodology:** (e.g., SPARC + DDD, Audit-First)

## 1. Overview
One-paragraph description of what we're adding and why.

## 2. Design Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| ... | ... | ... |

## 3. Architecture / DDD Analysis
(If applicable: bounded context placement, context map changes, anti-corruption layers)

## 4. Verification Criteria
Numbered list of testable outcomes. Each criterion becomes a row in the implementation result's verification table.

| # | Criterion | How to Verify |
|---|-----------|---------------|

## 5. Out of Scope
Explicit list of what we're NOT doing and why. Prevents scope creep.
```

**Key rules:**
- Verification criteria must be TESTABLE (not "system should be fast" but "p95 latency < 500ms")
- Design decisions should include alternatives you considered and rejected
- If the change crosses network/ bounded-context boundaries, include a DDD section
- Date the document; status must be explicit (Draft until reviewed, Approved before implementation)

### Step 2: Write the Implementation Plan

**Location:** `docs/plans/YYYY-MM-DD-<topic>-impl.md`

**Written after design is Approved.** This is the step-by-step recipe.

**Mandatory structure:**

```markdown
# <Topic> Implementation Plan

**Design doc:** (link to design doc)
**Methodology:** (e.g., SPARC Red-Green-Refactor)
**Status:** Ready for execution | In progress | Complete

## Step 1 — Red: Write failing tests
**Goal:** What this step achieves
**Files:** List of files to create/modify
### What to write
(Exact code or pseudocode — not vague descriptions)
### Verification
(Command to run, expected output)

## Step 2 — Green: Add infrastructure + code
(Same structure: Goal, Files, What to write, Verification)

## Step N — ...
(Continue for each step)

## Dependency Chain
```
Step 1 -> Step 2 -> Step 4
           |
           v
         Step 3 (independent)
```
(Which steps can be parallel, which are sequential)

## Risk Assessment
| Risk | Mitigation |
|------|------------|

## Files Changed (Final Checklist)
- [ ] file1 — description
- [ ] file2 — description
```

**Key rules:**
- Each step must be independently verifiable (can run a command and see pass/fail)
- Include EXACT code or at minimum precise function signatures — vague plans lead to wrong implementations
- Steps that can be done in parallel should be documented as parallel in the dependency chain
- The final checklist at the bottom is your pre-commit safety net — every file listed must have a checkmark before you commit
- Number steps consistently with your TDD phases if using Red-Green-Refactor

### Step 3: Implement, Then Record the Result

**Location:** `docs/implementation/YYYY-MM-DD-<topic>.md`

**Written AFTER implementation is complete.** This is the reality document — what actually happened, not what was planned.

**Mandatory fields:**

```markdown
# <Topic> Implementation Result

**Date:** YYYY-MM-DD
**Status:** Complete | Partial | Blocked
**Design doc:** (link)
**Implementation plan:** (link)

## Methodology
Brief recap of which methodology steps were actually followed (may differ from plan).

## Commits
| Commit | Phase | Description |
|--------|-------|-------------|
| abc1234 | Red | 4 failing tests |
| def5678 | Green | Jaeger + telemetry rewrite |
| ... | ... | ... |

## Change Summary
**N files changed, M insertions, K deletions**

### New files
| File | Purpose |
|------|---------|

### Modified files
| File | Change |
|------|--------|

## Architecture
(Diagram of what was actually built — may differ from design)

## Static Verification Results
| Check | Result |
|-------|--------|
| (All static checks from tdd-dind-compose-infra Phase 4) | pass/fail |

## Known Risks
Document any risks discovered during implementation that weren't in the design.

## Deployment Instructions
Step-by-step commands to deploy and verify (for ops or future-you).

## Verification Criteria (from Design Doc)
| # | Criterion | How to Verify | Status |
|---|-----------|---------------|--------|
| 1 | Jaeger healthy | curl returns 200 | pass/fail/pending |

(Map each design criterion to actual outcome)
```

**Key rules:**
- The verification criteria table MUST link back to the design doc — this is the traceability chain
- Include actual commit hashes, not just descriptions
- If implementation diverged from plan, document WHY (don't silently deviate)
- Static verification results let someone verify correctness even when the runtime environment (DinD) isn't available
- Known risks section is where you document "this works but might break if X changes"

### Step 4: Link the Three Documents

Every document cross-references the other two:

| Doc | Links to |
|-----|----------|
| Design doc | (no forward link — written first) |
| Implementation plan | Design doc (top of file) |
| Implementation result | Design doc + Implementation plan (top of file) |

This creates a navigable chain: result -> plan -> design. Anyone reading the result can trace back to understand WHY a decision was made.

## Pitfalls

- **Don't write the implementation plan before the design is approved.** You'll waste effort on a plan for an approach that gets changed in review.
- **Don't skip verification criteria in the design doc.** Without testable criteria, the implementation result has nothing to verify against, and the doc chain breaks.
- **Don't update the plan after implementation.** The plan is the INTENT; the result is the REALITY. If they diverge, document the divergence in the result, not by retroactively editing the plan.
- **Don't merge design + result into one doc.** They serve different audiences and have different lifecycles. A design doc may be Approved for months before implementation starts.
- **Don't forget the "Out of Scope" section in design.** Without it, scope creep goes undocumented and the verification criteria never cover the extras.
- **Don't write vague implementation steps.** "Add telemetry" without specifying which function changes is useless. Include exact function signatures, env var names, and verification commands.

## Verification

After applying this workflow, confirm:
1. Three documents exist in the correct directories with consistent naming
2. Implementation result links to both design doc and implementation plan
3. Every design verification criterion maps to a status in the result doc
4. Commits in the result doc match actual git history
5. Static verification table covers all changed files
6. Someone who wasn't involved can trace from result -> plan -> design and understand the full chain
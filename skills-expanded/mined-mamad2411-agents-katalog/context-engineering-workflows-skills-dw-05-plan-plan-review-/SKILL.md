# Adversarial Plan Review

You are performing an independent, adversarial review of a completed implementation plan.
Assume the plan has gaps until proven otherwise. Your job is to find problems,
not confirm the plan is good.

## Inputs

You will be given an `ARTIFACT_DIR` path containing all deep-work artifacts. Read them
in this order to build a complete mental model before reviewing:

1. `00-ticket.md` — original requirements and acceptance criteria
2. `02-research.md` — codebase findings, patterns, constraints
3. `03-design-discussion.md` — decided design questions, chosen patterns, scope boundaries
4. `04-structure-outline.md` — phase structure, risk register, scope guards
5. `05-plan.md` — the plan under review

## Process

### Step 1: Build requirements checklist

Extract every requirement and acceptance criterion from `00-ticket.md`. Number them
for traceability. These are the contract the plan must fulfill.

### Step 2: Review the plan

Review the plan against each category below. For each finding, reference the specific
task number (e.g., "Task 2.3") and explain the concrete impact.

**You MUST read codebase source files** when verifying:
- file:line references in the plan are accurate
- proposed patterns match actual codebase patterns
- existing tests or modules the plan depends on actually exist
- interfaces/signatures the plan references are correct

#### Review Categories

| Category | What to Challenge |
|---|---|
| **Requirements Traceability** | Every requirement in `00-ticket.md` maps to specific tasks. No silent scope reductions. No gold-plating beyond requirements. |
| **Completeness** | No TODOs, placeholders, or incomplete tasks. No missing steps between tasks. No implicit "the implementer will figure it out" gaps. |
| **Spec Alignment** | Plan implements what the spec asks for — not a subset, not a superset. Scope matches design decisions in `03-design-discussion.md`. |
| **Task Decomposition** | Tasks have clear boundaries. Steps are actionable. Each task is independently executable. Dependencies between tasks are explicit. |
| **Buildability** | Could an engineer with zero codebase context follow this plan without getting stuck? Are file paths, signatures, and commands correct? |
| **Logic Correctness** | Race conditions, ordering bugs, state machine gaps, off-by-one errors, null/empty handling, error propagation paths. |
| **Security** | Input validation, auth/authz checks, injection vectors, secret handling, OWASP Top 10 relevance, trust boundary violations. |
| **Performance** | N+1 queries, unbounded iterations, missing indexes, large payload handling, hot path allocations, missing pagination. |
| **Availability & Resilience** | Failure modes, retry/backoff strategy, graceful degradation, timeout handling, dependency failure cascading. |
| **Durability & Data Integrity** | Transaction boundaries, idempotency, data migration safety, rollback path, schema evolution strategy. |
| **Stability & Regression Risk** | Existing tests preserved, breaking changes identified, backward compatibility, shared module impact. |
| **Code Best Practices** | Patterns from `03-design-discussion.md` actually followed in plan tasks. DRY violations across tasks. Separation of concerns. Error handling consistency. |
| **Testability** | Planned tests cover the right invariants. Missing edge case tests. Integration test coverage for failure modes. Test isolation — no shared mutable state between tests. |

### Step 3: Classify findings

Every finding gets ONE severity:

| Severity | Criteria | Effect |
|---|---|---|
| **Critical** | Would cause a bug, security vulnerability, data loss, or failure to meet a requirement | Must fix before implementation |
| **Important** | Would cause performance issues, maintenance burden, fragility, or missing edge case coverage | Must fix before implementation |
| **Advisory** | Would improve quality but absence won't cause failures | Reported to user for judgment |

**Calibration rules:**
- Every finding MUST reference a specific task/step and explain the concrete impact
- "Could be a problem" without specifics is not a finding — cut it
- "Consider adding error handling" is banned — specify WHICH error, WHERE, and WHAT happens if unhandled
- If a category has no findings, omit it from the report — don't pad with "looks good"
- Do not re-litigate design decisions from `03-design-discussion.md` — those are settled

### Step 4: Write review artifact

Write `05b-plan-review.md` to the artifact directory.

````markdown
# Plan Review: <topic>

**Reviewed:** <date>
**Plan:** 05-plan.md
**Verdict:** APPROVED | APPROVED WITH CONDITIONS | REVISE

> **Verdict criteria:**
> - APPROVED — no Critical or Important findings
> - APPROVED WITH CONDITIONS — Important findings only, implementable with noted fixes
> - REVISE — Critical findings that require plan changes before implementation

## Requirements Traceability

- [x] Requirement 1 → Task X.Y, X.Z
- [x] Requirement 2 → Task X.Y
- [ ] Requirement 3 → **MISSING** — no task covers <specific gap>

## Critical Issues

> Must fix before implementation begins.

### [CATEGORY] Task X.Y: <short title>

**What:** <specific problem>
**Impact:** <what breaks, what's vulnerable, what data is lost>
**Fix:** <concrete action — add step, modify task, add test case>

## Important Issues

> Must fix before implementation begins.

### [CATEGORY] Task X.Y: <short title>

**What:** <specific problem>
**Impact:** <concrete consequence>
**Fix:** <concrete action>

## Advisory

> Reported for user judgment. Does not block implementation.

- **[CATEGORY] Task X.Y:** <observation> — <suggested improvement>

## Positive Observations

> Patterns worth noting for future plans.

- <specific strength with task reference>

---

```yaml
phase: plan-review
date: <today>
topic: <topic-slug>
repo: <repo>
input_artifacts: [00-ticket.md, 02-research.md, 03-design-discussion.md, 04-structure-outline.md, 05-plan.md]
verdict: <APPROVED|APPROVED WITH CONDITIONS|REVISE>
critical_count: <N>
important_count: <N>
advisory_count: <N>
```
````

### Step 5: Report results

After writing the artifact, report back with:
1. The verdict (APPROVED / APPROVED WITH CONDITIONS / REVISE)
2. Counts: critical, important, advisory
3. A one-line summary of the most significant finding (if any)

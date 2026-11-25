---
name: code-review-and-quality
description: >-
  Multi-axis code review framework that evaluates every change across five
  distinct dimensions: correctness, security, performance, maintainability,
  and style. Enforces change sizing, severity labeling, and review velocity
  norms so that reviews are thorough without becoming bottlenecks.
---

# Code Review & Quality

## Overview

Code review is the single highest-leverage quality practice in software
engineering — when done well. The difference between a good review and a
bad one is not the reviewer's intelligence but the presence of a structured
framework. Without one, reviews devolve into nitpicking while architectural
issues go unaddressed.

This skill defines a **five-axis review** where every dimension is evaluated
explicitly. Each review produces a severity-labeled report (Nit / Optional /
Blocking), and the total change size is kept to ~100 lines so that reviews
remain humanly possible within 30-60 minutes.

## When to Use

- Every pull request or merge request before it enters the target branch
- Every commit that modifies shared interfaces, public APIs, or data schemas
- Every dependency upgrade (especially major versions or security patches)
- Every change to authentication, authorization, or data access logic
- Every change that touches build configuration or deployment pipelines
- As a pre-commit gate for self-reviews when no reviewer is available
- Periodically on existing code to catch accumulated quality debt

## Process

### Step 1: Evaluate Change Size

A reviewable change is approximately 100 lines of diff (+/- 50 lines).
Larger changes must be split before review begins.

**Size norms:**

| Size | Lines Changed | Review Time | Notes |
|------|--------------|-------------|-------|
| Tiny | <30 | <15 min | OK to fast-track |
| Normal | 30-150 | 15-45 min | Ideal range |
| Large | 150-500 | 45-120 min | Must split |
| Massive | 500+ | 2+ hours | Blocking — rewrite required |

**Splitting strategies:**
- **Structural split:** Separate refactoring from features from bug fixes.
  Each change type is its own PR.
- **Layered split:** Backend changes first (schema, API), then frontend.
- **Feature-flag split:** Ship the mechanics behind a flag, then the
  activation in a follow-up.

**Exit criteria:** If the change exceeds 150 lines, the author must refactor
into smaller units or provide a written justification for the size before
review begins.

### Step 2: Axis 1 — Correctness

Does the code do what it claims to do?

**Checklist:**
- [ ] Logic matches the specification or requirements document
- [ ] No off-by-one errors, fencepost errors, or incorrect boundary conditions
- [ ] Error handling exists for every failure mode (network, disk, auth,
      validation, timeout)
- [ ] Edge cases are handled: empty collections, null inputs, max/min values,
      type coercion corner cases
- [ ] Concurrency: shared state is properly synchronized, no data races,
      deadlocks are impossible
- [ ] Floating-point comparisons use epsilon, not equality
- [ ] State machines handle all transitions, including illegal transitions
      with appropriate errors
- [ ] Async code handles promise rejections, cancellation, and backpressure

### Step 3: Axis 2 — Security

Could this code be exploited?

**Checklist:**
- [ ] All user input is validated, sanitized, and parameterized
- [ ] SQL/NoSQL queries use parameterized statements or ORM-safe methods
- [ ] No raw HTML concatenation; output encoding matches context (HTML, JS,
      CSS, URL)
- [ ] Authentication checks gate every protected endpoint/operation
- [ ] Authorization checks verify the principal has the right permissions,
      not just any authentication
- [ ] Secrets (keys, passwords, tokens) are not hardcoded or logged
- [ ] File uploads have size limits, type restrictions, and are stored
      outside the web root
- [ ] Rate limiting exists on mutation endpoints and auth endpoints
- [ ] Dependencies are scanned (npm audit, pip-audit, cargo audit, etc.)
- [ ] No `eval()`, `exec()`, `Function()`, or dynamic code construction
      with user-controlled input

### Step 4: Axis 3 — Performance

Will this code scale?

**Checklist:**
- [ ] N+1 queries eliminated (use batching, eager loading, or joins)
- [ ] Database queries have appropriate indexes; query plans are reviewed
- [ ] No synchronous I/O in hot paths or event-loop contexts
- [ ] Object allocations minimized in loops or frequently-called paths
- [ ] Caching is applied to repeated computations or repeated I/O
- [ ] Payload sizes are reasonable; no unnecessary data fetching
- [ ] Lazy loading is used for expensive resources
- [ ] Memory: no unbounded collection growth, no leaks via forgotten
      subscriptions/event listeners
- [ ] Bundle size: imports are tree-shakeable, no duplicate dependencies

### Step 5: Axis 4 — Maintainability

Can someone unfamiliar with this code modify it safely?

**Checklist:**
- [ ] Functions are small (fits on one screen, <40 lines typically)
- [ ] Each function/class has a single responsibility
- [ ] Dependencies are explicit (injected, not global)
- [ ] Tests exist for the critical paths and edge cases
- [ ] Names convey intent: `getUser` not `getData`, `isExpired` not `check`
- [ ] No commented-out code, no "TODO" without a ticket number
- [ ] Configuration is externalized (env vars, config files, feature flags)
- [ ] Public API surfaces are minimal; internal details are hidden
- [ ] Cyclomatic complexity of each function is below 10

### Step 6: Axis 5 — Style

Does the code follow project conventions?

**Checklist:**
- [ ] Linter passes with zero warnings at the configured rule set
- [ ] Formatter applied (Prettier, rustfmt, gofmt, black, etc.)
- [ ] Naming conventions consistent (camelCase, snake_case, etc.)
- [ ] Import ordering follows project convention
- [ ] No unnecessary whitespace changes mixed into logic changes
- [ ] Comments are present only where they explain "why", not "what"
- [ ] File structure matches project conventions

### Step 7: Assign Severity Labels

Every comment must carry a severity label.

| Label | Meaning | Action Required |
|-------|---------|-----------------|
| **Blocking** | Incorrect behavior, security hole, significant perf regression, or design flaw that will cause problems | Must be resolved before merge. Author responds with fix or explanation. |
| **Optional** | Improvement that would make the code better but is not strictly wrong | Author may accept or defer with a brief rationale. |
| **Nit** | Stylistic preference or minor polish | Author may ignore or apply at their discretion. No response required. |

**Severity ratio guideline:** A healthy review has roughly 1-2 Blocking items,
2-5 Optional items, and 0-3 Nit items. If there are more Blocking items, the
change was not ready for review. If there are more than 3 Nits, the author
should run the formatter and linter before re-requesting review.

---

## Anti-Rationalization Table

| Excuse | Rebuttal |
|--------|----------|
| "This change is urgent, just approve it." | Urgent changes need the most scrutiny. Approval without review is how P0 incidents are born. If it's truly urgent, pair-review live in 15 minutes. |
| "I trust the author; they write good code." | Trust does not eliminate defects. Every engineer — at every level — produces blind spots. Review is insurance, not suspicion. |
| "The change is too big to review carefully; I'll just skim it." | Then require it to be split. Large changes reviewed hastily are the leading cause of post-merge defects. Enforce the size limit. |
| "I'll fix the issues in a follow-up PR." | Follow-up PRs have a 70% abandonment rate. Fix it now or track with a blocking ticket that is linked in the PR description. |
| "The tests pass, so the code is correct." | Tests are necessary but not sufficient. They only cover the cases someone thought to write. Review covers the cases nobody considered. |
| "This pattern is used everywhere in the codebase already." | Prevalence is not correctness. Legacy patterns can be wrong. Flag it and create a migration ticket. |
| "I don't have time to do a full review right now." | Then defer the merge. Partial reviews are more dangerous than no review because they create false confidence. |

## Red Flags

- PR with 500+ lines and no split request → reviewer is not doing their job
- All comments are Nits (spelling, formatting) → reviewer missed the substance
- No comments at all on a non-trivial change → reviewer did not actually read it
- "LGTM" on a change that touches authentication, payments, or data
- Review took <2 minutes for a change over 100 lines
- Author merged before all Blocking items were resolved
- Same review feedback given across multiple PRs → systemic issue not addressed
- Security comments downgraded to Optional by the author without explanation

## Verification

1. Count lines changed (excluding generated files, lockfiles, and vendored
   dependencies). Is the change within the reviewable range?
2. Run the full test suite. All tests passing?
3. Run linter + formatter. Zero warnings?
4. Run dependency audit (`npm audit`, `cargo audit`, etc.). No critical
   vulnerabilities?
5. Check each checklist item above. Can each item be answered "yes" with
   evidence (not assumption)?
6. For every Blocking comment: has the author responded and resolved?
7. Review the review: was each dimension (correctness, security, performance,
   maintainability, style) addressed?
8. If deploying: does a canary health check pass for at least 5 minutes?

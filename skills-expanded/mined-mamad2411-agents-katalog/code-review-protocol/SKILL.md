---
name: code-review-protocol
description: Senior code review that finds defects and fixes them: correctness, security, performance, architecture and robustness passes, severity ranking, mandatory fix and verification, no rubber stamping. Use on any code written or changed by the agent, and on any diff or pull request under review.
license: MIT
metadata:
  category: dev-skills
  version: 1.0.0
  depends_on: [engineering-core, project-exploration]
  outputs: [review-findings, applied-fixes, verification-log]
---

# Code Review Protocol

Reviews a diff the way a reviewer who will be paged at three in the morning
reviews it. Then fixes what it finds and proves the fix.

A review that produces a list and stops has done half the work. A review that
produces no findings on a non trivial diff was not performed.

## 1. Entry condition

Runs on every change the agent wrote, and on any diff submitted for review.
Never skipped because the change looks small: the smallest diffs carry the
highest ratio of unreviewed assumptions.

## 2. Protocol

1. **Read the diff completely** before judging any line. A finding based on a
   fragment is a guess.
2. **Read the surrounding code**, the callers and the tests. A diff is correct
   or incorrect only relative to what calls it.
3. **Run the five passes** of section 3, in order. Each pass has one question
   and does not wander into the others.
4. **Rank** findings by severity, section 4.
5. **Fix** everything at `blocker` and `major`. Fix `minor` when the fix is
   contained; otherwise record it as follow up.
6. **Verify** each fix: run the test, run the check, observe the output.
7. **Re-read the diff after fixing.** Fixes introduce defects at the same rate
   as features.
8. **Report** using the format in section 7.

## 3. The five passes

### Pass 1, correctness

One question: for which input does this produce a wrong result?

- logic inverted, off by one, wrong operator, wrong branch order;
- null, undefined, empty string, empty array, zero, NaN on every new path;
- optional chaining that hides a missing value instead of handling it;
- async: missing await, floating promise, unhandled rejection, sequential
  awaits that should be concurrent, concurrent writes that should be ordered;
- race conditions: check then act, read modify write without a lock or an
  atomic operation, two requests arriving together;
- type safety: `any`, unchecked cast, non null assertion, parsing without
  validation, trusting an external response shape;
- boundary conditions: first, last, one element, none, maximum, overflow,
  timezone edges, daylight saving, leap day;
- invalid states that the type system permits and the code does not reject;
- transactions: partial writes on error, missing rollback, work done after
  commit that assumed the commit;
- error handling that swallows: empty catch, catch that logs and continues
  into a broken state.

### Pass 2, security

One question: what does a hostile caller get out of this?

Delegated in depth to `security-audit`, applied here as a mandatory screen:

- authentication assumed rather than enforced on the new path;
- authorization missing, or checked in the UI only;
- object level authorization: the identifier comes from the request and the
  query does not scope by owner;
- injection: string built into SQL, shell, path, template or header;
- rendering user content into HTML without escaping, or through a raw HTML
  sink;
- server side fetch of a user supplied URL;
- state changing request without CSRF protection where cookies authenticate;
- upload without type, size and destination control;
- secrets in code, in logs, in errors returned to the client;
- sensitive data in a response the caller should not see;
- a client supplied price, role, ownership field or state transition, trusted.

### Pass 3, performance

One question: what happens at a hundred times the current data?

- query inside a loop, the classic N plus 1, including the ORM shaped version;
- unbounded query: no limit, no pagination, `select *` on a wide table;
- missing index on a column used for filtering, joining or ordering;
- data fetched and then discarded, or fetched on every render;
- a network call that could be batched or cached, in a hot path;
- an expensive computation recomputed instead of memoised, in a hot path;
- a blocking operation on the event loop or on the request thread;
- payload growth: nested serialisation that includes everything;
- a client re-render triggered by an unstable reference.

Findings in this pass state the scale at which the problem appears. A concern
that never materialises at the project scale is not a finding.

### Pass 4, architecture

One question: where will the next change be forced to go?

- responsibility in the wrong layer: business rules in a handler, queries in a
  component, formatting in a service;
- duplication of a rule, which will diverge;
- coupling: a module reaching into another module's internals;
- circular dependency;
- an abstraction with one implementation, or a wrapper adding no decision;
- a file that has become a dumping ground;
- a function whose name and body disagree;
- placement that contradicts the project convention, verified against two
  existing occurrences;
- dead code, commented out code, a flag nobody reads.

### Pass 5, robustness

One question: what does the user and the operator see when this fails?

- every failure path of the happy path: what returns, what renders, what logs;
- loading state where the user waits;
- empty state where a list can be empty;
- error state where a request can fail, with a message that helps;
- timeout on every outbound call;
- retries bounded, and only where the operation is idempotent;
- idempotency where a retry or a double click can duplicate an effect;
- external service down: degraded behaviour chosen, not accidental;
- logs that let an operator reconstruct what happened, without secrets.

## 4. Severity

| Level | Definition | Action |
|---|---|---|
| blocker | data loss, security hole, corruption, or the feature does not work | fix now, do not deliver without it |
| major | wrong result in a realistic case, or a failure with no handling | fix now |
| minor | correctness holds, quality suffers, cost is contained | fix if contained, else record |
| note | preference with no defect behind it | mention once or not at all |

Severity is assigned from the consequence, never from how much code the fix
touches. A one character fix for a missing owner check is a blocker.

## 5. Prohibitions

- No finding without a file, a line range and a concrete failing input.
- No finding phrased as a preference dressed up as a rule.
- No rewrite of code outside the diff, unless it is the cause of a finding.
- No style comment where the project has a formatter.
- No test modified to make it pass. Decide which of the test or the code is
  wrong, and say which.
- No approval of a non trivial diff with zero findings and no stated reason.
- No claim that a fix works without the command and its output.

## 6. Fixing

Each fix is minimal, follows the project convention, and is verified.

```
Finding    what breaks, with the input that breaks it
Location   file and line range
Severity   blocker | major | minor | note
Fix        what changed, in one line
Verified   the command run and the observed result
```

A fix that cannot be verified in this repository is marked `Unverified` with
the reason, and never reported as done.

## 7. Report format

```
Reviewed: 7 files, 214 added, 38 removed

blocker  api/orders/route.ts:41  order lookup is not scoped to the session
         user, any authenticated user reads any order by id
         Fix: added ownerId to the where clause
         Verified: npm test -- orders, 12 passing, new case covers 403

major    lib/cart.ts:88  total computed from a client supplied unitPrice
         Fix: price is read from the products table by id
         Verified: npm test -- cart, tampered payload now rejected

minor    components/cart-item.tsx:24  no empty state, renders an empty box
         Fix: empty state added, matching components/wishlist.tsx
         Verified: vitest run cart-item, 4 passing

Follow up (not fixed here)
  lib/cart.ts has no index on cart_items.cart_id; measured impact is small at
  current volume. Recorded in continuity notes.

Checks: npm run lint, npm run typecheck, npm test, all pass.
```

## 8. Auto-critique

Score from 0 to 5: completeness of the five passes, evidence behind each
finding, correctness of the severity ranking, quality of the fixes,
verification actually performed, restraint on out of scope changes, absence of
preference dressed as defect.

Threshold: no axis below 3, average at least 4. Zero findings on a diff over
roughly a hundred lines requires an explicit sentence explaining why the diff
is trivial, or the review is redone.

## 9. Interfaces

- Upstream: every implementation skill, `project-exploration`.
- Lateral: `security-audit` for depth on pass 2, `performance-engineering` for
  depth on pass 3, `testing-quality` for the tests each fix requires.
- Downstream: `technical-documentation`, `project-continuity`,
  `git-workflow`, `release-readiness`.

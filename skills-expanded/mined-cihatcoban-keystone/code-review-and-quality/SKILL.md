---
name: code-review-and-quality
description: Reviews a change before merge - correctness, failure behavior, design, security, performance, tests - and blocks quiet erosion of the quality bar, including in agent-written code. Triggers - review this pull request, code review, is this ready to merge, look over my changes before I push.
---

# Code Review

Review is the last cheap moment to catch a defect, and the only systematic
defense against a codebase drifting. The standard is not perfection: **approve
when the change clearly improves overall code health and follows the project's
conventions**, even if you would have written it differently. Blocking on taste
teaches people to route around review.

## Order of operations

Do these in order; the first two cost minutes and prevent the most damage.

### 1. Bar-protection scan (before reading logic)

Scan the diff for `CLAUDE.md` §4 triggers:

- New suppression comment without justification and link
- Test deleted, skipped, or assertion weakened
- Threshold in `CONSTRAINTS.md` edited downward inside a feature change
- `catch {}` / `except: pass` added around new code
- Stub presented as complete
- Golden file or fixture changed together with the logic that produces it

Any hit is raised first and explicitly. These convert failures into silence, so
they outrank style entirely.

### 2. Scope check

Does the diff do what its description says, and nothing else? An unrelated
"drive-by fix" makes the change unrevertable as a unit. Ask for it to be split.

### Stack lens (before the axes)

The axes below are language-neutral; the defects are not. For each language
the diff touches, open its section in `references/review-lenses.md` — a
migration plus a handler needs two. First confirm the project's own type
checker and linter ran on this diff with nothing newly suppressed: never
hand-check what a tool enforces. Then apply the lens items while walking the
axes. If a language has no section, review with the axes alone and say the
lens was missing.

### 3. Correctness

- Does it satisfy the stated acceptance criteria?
- Boundaries: empty, single, many, maximum, off-by-one
- Nulls and absent values; what happens with the "nothing" case
- Error paths: what does the caller see, and can they act on it?
- Concurrency: is there a read-modify-write on shared state?
  (`concurrency-and-consistency`)
- Idempotency: what if this runs twice? Because it will.

### 4. Failure behavior

The axis most reviews skip entirely.

- Every new external call: timeout? retry policy? what on failure?
- Partial failure: can this leave the system in a half-updated state?
- Is the failure observable — logged with context, counted, alertable?
- Is the change reversible? If it migrates or deletes data, what is the undo?
- Error kinds, where to handle them, and the silent-failure patterns to block:
  `references/error-handling.md`.

### 5. Design

- Does it fit the existing architecture, or quietly cross a boundary?
- Is the abstraction earned, or speculative generality for one caller?
- Is a business rule leaking into a controller, job or view?
- Does it add a dependency? (`dependency-and-license-policy`)
- Naming: would a newcomer guess what this does from the name?

### 6. Security and privacy

- Untrusted input reaching a query, template, command, path or deserializer
- Authorization checked at the right layer, not only in the UI
- Secrets, tokens or personal data in code, logs or error messages
- New surface exposed without authentication

### 7. Performance

- Query inside a loop (N+1)
- Unbounded result set, allocation or concurrency
- Work in a hot path that could be done once
- Budget in `CONSTRAINTS.md` at risk? Ask for a number, not an opinion

### 8. Tests

Review the tests as carefully as the code — weak tests are how the next defect
arrives.

- Would these tests fail if the implementation were wrong? (Mentally mutate one
  line: does something go red?)
- Do they test behavior or restate the implementation?
- Are boundaries and error paths covered, or only the happy path?
- Any sleep, real clock, network call, or order dependence?

## Writing findings

```text
[BLOCKER] src/payments/capture.go:88
Issue: retry on 5xx has no idempotency key; a timed-out capture can double-charge.
Impact: duplicate charges under normal network conditions, not just outages.
Fix: pass the order id as the idempotency key; assert single effect in a test.

[IMPORTANT] ...
[SUGGESTION] ...
```

- **BLOCKER** — incorrect, unsafe, irreversible, or erodes the bar
- **IMPORTANT** — should be fixed in this change: missing test, design drift,
  budget risk
- **SUGGESTION** — improvement, explicitly non-blocking

Rules: state the **impact**, not just the observation — a finding without a
consequence is an opinion. Attach `file:line`. Offer the fix direction. Ask
questions when you might be wrong ("what happens if this runs twice?") rather
than asserting. Praise a genuinely good solution once — it calibrates the
signal.

## Verdict

End with exactly one: `APPROVE` · `APPROVE AFTER FIXES` · `REQUEST CHANGES`
(with reason). Never approve with an open blocker. If you found nothing, say
what you checked — a silent approval is indistinguishable from not reviewing.

## Worked example

Description: "Add refund endpoint." The diff (pseudocode):

```text
+ handler refund(request):
+   order = orders.find(request.body.order_id)
+   if order.status == "PAID":
+     payments.refund(order.payment_id, request.body.amount)
+     order.status = "REFUNDED"; orders.save(order)
+   return 200
  tests:
+ test_refund: create paid order; call refund; assert response 200
```

Review:

```text
Bar protection: no hits. Scope: matches description. Lenses: none needed
beyond the axes (pseudocode). Tools: lint and type check green on this diff.

[BLOCKER] refund.handler:2
Issue: any caller can refund any order — no check that the order belongs to
the authenticated account.
Impact: one request refunds another customer's order.
Fix: load the order scoped to the caller's account; 404 otherwise.

[BLOCKER] refund.handler:4-5
Issue: refund is sent before the status is saved; a retry after a timeout
refunds twice, and amount is never checked against the paid total.
Impact: duplicate or excess refunds under normal network retries.
Fix: idempotency key = order id + request id; validate amount ≤ refundable;
record the refund and the status change atomically.

[IMPORTANT] refund.handler:6
Issue: an unpaid or missing order also returns 200.
Impact: callers cannot tell a refund from a no-op.
Fix: 404 for missing, 409 with a stable code for a non-refundable state.

[IMPORTANT] test_refund
Issue: asserts the status code only; it passes if refund() is never called.
Fix: assert one refund recorded with the amount; add the retry, wrong-owner
and over-amount cases.

Verdict: REQUEST CHANGES — authorization and double refund.
```

Each finding names a location, an impact a reader can weigh, and a direction;
the test finding asks whether the test could fail, not whether one exists.

## Reviewing agent-written code

Same standard, three extra suspicions: plausible-but-wrong API usage, tests
that assert the implementation rather than the requirement, and scope that grew
beyond the task. Confidence in the prose is not evidence.

## Exit checklist

- [ ] Bar-protection scan done before anything else
- [ ] Diff matches its description; no unrelated changes
- [ ] Project tools confirmed run on the diff; the lens for every language in
      it applied, or the missing lens reported
- [ ] Failure behavior of every new external interaction examined
- [ ] Tests reviewed for whether they could actually fail
- [ ] Every finding has an impact statement and a location
- [ ] Single explicit verdict; no blockers left open

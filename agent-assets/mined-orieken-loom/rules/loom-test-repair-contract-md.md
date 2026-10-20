# Test Repair Contract

**Binds every agent that can write a test file.** A green suite is not the goal. A suite that tells
you the truth is the goal — and an agent optimising for green has many ways to get there, most of
which destroy the thing the test was built for.

Each change below is locally reasonable, produces a passing build, and some of them permanently
remove regression signal. "Make this test pass" and "make this test correct" are different
instructions, and only one of them is easy.

---

## An agent repairing a failing test MAY

- Update a selector, locator, or identifier to match a renamed or restructured element.
- Replace a fixed sleep with an explicit wait-for-condition.
- Widen a timeout, **stating the measured p95 and why the previous value was wrong**. A widening with
  no measurement behind it is a guess that hides a real slowdown.
- Correct a genuinely wrong expected value, **only** when accompanied by the source-code evidence
  that the intended behavior changed. The evidence is the diff or the commit, not an explanation.

## An agent repairing a failing test MAY NOT

- Remove, weaken, or comment out any assertion.
- Add `try`/`catch`, optional chaining, a broadened matcher, or any construct whose effect is to
  convert a failure into a pass.
- Change an assertion's expected value without source-code evidence.
- Mark a test skipped, pending, excluded, or quarantined. That is a human decision — see
  `approval-gates.md` gate #9.
- Retire or delete a test.
- Change a CI gating threshold — coverage floors, complexity caps, budget limits — to accommodate a
  failure.

## Every proposed repair MUST state

1. **What the test could catch before, and what it can catch after.** This is the load-bearing
   requirement. It is very hard to write that sentence honestly about a deleted assertion, and
   requiring it makes the loss visible in the agent's own words rather than in a diff nobody reads.
2. **The evidence that the fix is a fix and not a mask** — the source change, the measurement, or the
   reproduction.

---

## Why a plausible rationale is not enough

The dangerous diff is not the careless one. It is this one:

```diff
  test('rejects orders over the credit limit', async () => {
    const order = await createOrder({ total: 5000, creditLimit: 1000 });
-   expect(order.status).toBe('REJECTED');
-   expect(order.rejectionReason).toBe('CREDIT_LIMIT_EXCEEDED');
+   expect(order.status).toBeDefined();
  });
```

*"The test was failing intermittently because `rejectionReason` is populated asynchronously and is
sometimes null when asserted. Relaxing the assertion removes the race."*

That rationale is **accurate**. The diagnosis is correct. And the fix converts a test that verified
credit-limit rejection into one that verifies `createOrder` returns an object — while the real race
it correctly identified stays in the product, now unobserved.

The correct action is to escalate: the test found a genuine defect. "Does the explanation sound
reasonable?" is not a sufficient review standard, which is why this contract asks what was lost
rather than whether the change was justified.

---

## Where this applies

- **Repairing an existing test** — every clause above.
- **Writing a new test** — the MAY NOT list still binds. A new test that cannot fail is the same
  defect arriving earlier; `code-reviewer` asks whether it would fail (see its Test Evidence
  criterion) and a `NO` blocks.
- **Refactoring** — a refactor that changes a test file has moved the safety net it was being
  verified against. Say so explicitly; do not let it pass as part of the refactor.

## What this contract is not

It is not a claim that these repairs are usually wrong. Selector healing against a redesigned
frontend is legitimate, saves real time, and meets every clause here. The line is clean: repair the
*path to* the assertion freely, and never the assertion itself. Healing that touches evidence is not
a category that should exist.

It is also not a mechanism. The reviewer is the control; this contract makes the review cheap by
saying in advance what to look for.

---
*Part of the [ai-assistant-dot-files](https://github.com/orieken/loom) Context Engineering Framework by Oscar Rieken — licensed under [CC BY 4.0](https://github.com/orieken/loom/blob/main/LICENSE-CONTENT.md). If you copy or adapt this file, please keep this attribution.*

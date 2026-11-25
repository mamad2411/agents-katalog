---
name: seams
description: "Use when logic can't be unit-tested without a database, network, clock, or a pile of mocks, or when one function fetches, computes, branches on policy, and writes. Splits the pure decision from the I/O action so the logic is testable with plain values. The proof is a unit test that needs zero mocks."
---

# Seams

## The failure mode this fixes

"I can't test this" almost always means "this code has no seams." A seam is a place where you can change behavior without editing the code around it — the joint between *deciding what to do* and *actually doing it*. When decision and action are fused (the function fetches, computes, branches on policy, and writes, all in one breath), every test needs a database, every change risks five behaviors, and the logic you actually care about is impossible to isolate.

Agents fuse decision and action constantly, because it's the shortest path to working code. This skill finds the seam and splits along it: pure decisions you can test with plain inputs, thin actions that just carry out the decision.

## When to Use This Skill

- You want to write a unit test but the code demands a live dependency
- A function mixes I/O (network, disk, db) with branching business logic
- A small change ripples into unrelated behaviors
- You're about to extract a function and want it to be testable from birth
- Policy ("when do we refund?") is buried inside mechanics ("how do we call Stripe?")

**Don't use when:** the code is already a thin pure function or a thin I/O shim. Don't add indirection where there's nothing to separate — that's just ceremony.

## Instructions

### 1. Classify every line as DECISION or ACTION

Read the target and tag each chunk:
- **DECISION** — computes a result from inputs; no side effects. (validation, branching, calculation, choosing what should happen)
- **ACTION** — touches the outside world. (read/write db, network calls, file I/O, logging, time, randomness)

The seam is the boundary between them.

### 2. Pull the decision out as a pure function

Extract the DECISION into a function that:
- Takes everything it needs as **explicit arguments** (no reaching into globals, db, or clock)
- Returns a **description of what should happen**, not the act of doing it (e.g. return `{ action: "refund", cents: 1200 }`, don't call Stripe)
- Has zero side effects → testable with plain values, no mocks

```ts
// BEFORE — decision fused to action: untestable without Stripe and a db
async function processRefund(orderId: string) {
  const order = await db.orders.get(orderId);
  if (order.settledAt && daysSince(order.settledAt) <= 30 && !order.refundedAt) {
    await stripe.refunds.create({ charge: order.chargeId, amount: order.amountCents });
    await db.orders.markRefunded(orderId);
  }
}

// AFTER — pure decision returns a description; note the clock enters as an argument
function decideRefund(order: Order, today: Date): RefundDecision {
  if (!order.settledAt) return { action: "reject", reason: "not settled" };
  if (order.refundedAt) return { action: "reject", reason: "already refunded" };
  if (daysBetween(order.settledAt, today) > 30) return { action: "reject", reason: "window expired" };
  return { action: "refund", chargeId: order.chargeId, cents: order.amountCents };
}

// the action is now thin plumbing: gather → decide → carry out
async function processRefund(orderId: string) {
  const order = await db.orders.get(orderId);
  const decision = decideRefund(order, new Date());
  if (decision.action === "refund") {
    await stripe.refunds.create({ charge: decision.chargeId, amount: decision.cents });
    await db.orders.markRefunded(orderId);
  }
}
```

If the decision needs data you can't gather upfront (a per-item loop over a paginated or streaming source), split per element instead: a pure decision for *one* item, and a thin loop that fetches each item, calls the decision, and carries out the result.

### 3. Leave the action thin and dumb

The ACTION side becomes a thin executor: it gathers inputs, calls the pure decision, and carries out the result. It contains *no business logic* — just plumbing. Ideally it's so simple it barely needs testing.

### 4. Make dependencies enter through the seam

Where the action needs a collaborator (a clock, a payment client, a repository), pass it in rather than constructing it inside. Now tests swap a fake; prod passes the real one. The seam is the injection point.

### 5. Prove the seam with a test

Write one test against the pure decision using plain inputs and asserting the returned description. If you can do this with no mocks, the seam is real. If you still need a mock to test the decision, the split is incomplete — go back to step 1.

Match the project's existing style: if `CONTEXT.md` records how side effects are usually isolated (or the test framework in use), follow that convention instead of inventing a new one.

## Output format

```
DECISION vs ACTION MAP
  DECISION: <chunks that compute, no side effects>
  ACTION:   <chunks that touch the world>
  SEAM:     <the line where they should split>

PROPOSED SPLIT
  pure:   decideX(inputs) -> Result        // testable with plain values
  action: doX(deps) { gather -> decideX -> carry out }   // thin plumbing

SEAM TEST (proof)
  <a unit test against decideX with no mocks>
```

## Anti-Patterns

| Anti-Pattern | Why it defeats the skill |
|---|---|
| Decision returns by doing (calls the API instead of describing the call) | No seam — you still can't test the logic without the dependency. |
| Mock-heavy tests | If a "unit" test needs five mocks, you tested the plumbing, not the decision. The seam is in the wrong place. |
| Hidden dependencies (clock, randomness, env read inside the logic) | Untestable and non-deterministic. Pass them through the seam. |
| Splitting where there's no logic | Wrapping a one-line I/O call in a "service" adds indirection, not a seam. |
| Anemic decision (returns raw inputs unchanged) | If the pure function decides nothing, the logic is still hiding in the action. |

## Mental Model

> Separate deciding from doing. Decisions are pure and testable; actions are thin and dumb. The seam between them is where every test and every future change wants to live.

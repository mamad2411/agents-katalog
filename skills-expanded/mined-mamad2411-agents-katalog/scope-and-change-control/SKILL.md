---
name: scope-and-change-control
description: Protects an approved scope and architecture from silent drift. Classifies every discovery as in scope, follow up, or a change requiring approval, and runs the change protocol when implementation contradicts the approved design. Active from the validation gate until delivery.
license: MIT
metadata:
  category: delivery-skills
  version: 1.0.0
  depends_on: [engineering-core, validation-gate]
  outputs: [scope-decisions, follow-up-register, change-requests, architecture-updates]
---

# Scope and Change Control

Two drifts destroy deliveries. Scope drift: the project grows by small
improvements nobody asked for. Architecture drift: the built system stops
matching the approved design, one reasonable decision at a time.

Both feel like good engineering while they happen.

## 1. The classification

Every discovery during implementation is one of four things. Classify before
acting.

| Class | Definition | Action |
|---|---|---|
| in scope | serves an approved requirement | do it, it is the work |
| follow up | an improvement nobody asked for | register it, do not do it |
| urgent | a security, data integrity or correctness risk | fix now, report it |
| change | contradicts the approved architecture or scope | change protocol |

The classification is written before the fix, not after. Deciding
retrospectively that a two hour improvement was in scope is how the boundary
disappears.

## 2. Follow ups

The default answer to a discovered improvement is: register it, do not do it.

```
| # | What | Where | Why not now | Effort |
|---|---|---|---|---|
| FU7 | orders list has no index on customer_id | db/schema | not in scope, no measured impact at current volume | small |
| FU8 | the date formatter is duplicated in 4 files | lib/ | cosmetic, no defect | small |
| FU9 | the settings page has no empty state | components/ | outside the approved scope for this delivery | medium |
```

Registered improvements are delivered as a list at handover. That is more
valuable to the client than three of them silently implemented and twenty
forgotten.

Three temptations, all refused:

- while I am in this file anyway;
- it is only ten minutes;
- it would be strange to leave it like that.

Each of them is individually reasonable and collectively is how a four week
project becomes seven.

## 3. The urgent exception

Fixed immediately, without asking, and reported:

- a way for one user to read or modify another user's data;
- a credential or secret exposed;
- data loss or corruption on a reachable path;
- an authentication or authorization bypass;
- money computed from client controlled input;
- a defect that makes an approved requirement produce a wrong result.

The exception is narrow on purpose. `The error handling here is poor` is not
urgent. `This endpoint returns any customer's orders` is.

The fix is minimal and its own commit, so it can be reviewed on its merits and
is not buried in a feature.

## 4. The change protocol

Runs when implementation reveals that the approved architecture is wrong,
insufficient, or impossible.

```
1  Stop      the affected path only. Other work continues.
2  Establish what is actually true, with evidence, not with a suspicion.
3  State    the discovery in three lines: what was assumed, what is true,
            how it was found.
4  Propose  at least two options, each with its cost and consequence.
5  Assess   is this significant, section 5.
6  Ask      when significant. Decide when not, and say what was decided.
7  Update   the architecture document. Always. Even for a small change.
8  Record   in the approval record, so the next reader sees the revision.
9  Resume   the stopped path.
```

Step 7 is the one that is skipped, and skipping it is what produces a project
whose architecture document describes a system that was never built.

## 5. Significance test

A change is significant, and requires approval, when any holds:

1. It changes what the user gets, adds or removes a capability.
2. It changes the data model in a way that touches stored data.
3. It changes a technology decision from the approved stack.
4. It changes a recurring cost.
5. It changes the delivery date.
6. It changes a security or privacy property.
7. It is expensive to reverse.

A change failing all seven is decided by the system, applied, documented, and
reported at the next phase boundary. Interrupting a person for an internal
module rename is as wrong as silently swapping the database.

## 6. Change request format

```
Discovery
  Assumed:   <what the architecture says>
  Actual:    <what is true, with the evidence>
  Found:     <how, so the reader can judge the certainty>

Impact
  Blocks:    <what cannot proceed>
  Affects:   <what already built is touched>

Options
  A <option>  cost: <effort, money, time>  consequence: <what is worse>
  B <option>  cost: ...                    consequence: ...

Recommendation
  <one option, with the reason in one line>

Decision needed by
  <when, and what stalls until then>
```

Ten to fifteen lines. A change request that takes a page to read gets a
one word answer.

## 7. Scope growth from the client

The mirror case: the client asks for something outside the approved scope
during implementation.

The answer is never a flat refusal and never a silent yes.

```
1  Acknowledge the request and place it precisely: this is outside the
   approved scope, here is what it touches.
2  State the cost honestly: effort, and what it delays.
3  Offer the choice: add it and move the date, swap it for something of
   similar size, or register it for after delivery.
4  Record the decision.
```

Absorbing an unbudgeted request silently is not generosity. It produces a late
delivery whose lateness has no visible cause.

## 8. Protocol

1. On every discovery, classify per section 1, in writing.
2. Follow ups go to the register, section 2. Do not implement them.
3. Urgent items are fixed now, in their own commit, and reported.
4. Changes run the protocol of section 4.
5. Apply the significance test, section 5, before deciding whether to ask.
6. Update the architecture document on every accepted change.
7. Deliver the follow up register at handover.

## 9. Auto-critique

Score from 0 to 5: classification written before acting, follow ups registered
rather than implemented, urgent exception applied narrowly, change protocol
complete including the document update, significance test applied rather than
guessed, change requests short and with real options, client requests priced
rather than absorbed.

Threshold: no axis below 3, average at least 4. An architecture document that
no longer matches the built system is an automatic failure, whatever the code
quality.

## 10. Interfaces

- Upstream: `validation-gate` provides the approved baseline.
- Active during: every implementation task.
- Downstream: `architecture-proposal` for document updates,
  `project-continuity` and `client-handover` for the follow up register,
  `delivery-orchestrator` for gate reopening.

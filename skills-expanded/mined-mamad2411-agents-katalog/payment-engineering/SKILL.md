---
name: payment-engineering
description: Builds payment flows that survive money moving: amounts computed server side, idempotency on every charge, the payment state machine, webhook verification and replay, reconciliation between provider and application, refunds and partial refunds, subscriptions and proration, failure and dispute handling, and the audit trail. Use for checkout, subscriptions, invoicing, payouts or any flow where a mistake has a currency symbol.
license: MIT
metadata:
  category: dev-skills
  version: 1.0.0
  depends_on: [engineering-core, backend-engineering, input-validation]
  outputs: [payment-flow, state-machine, idempotency-strategy, reconciliation-plan, audit-trail]
---

# Payment Engineering

Every defect in this area is visible to a customer, to an accountant, or to
both. The correctness bar is higher than anywhere else in an application, and
the failure modes are the ones that happen at three in the morning during a
provider incident.

Two rules generate most of the rest: the server decides the amount, and every
operation can be attempted twice.

## 1. The amount

```
computed server side, always, from the catalogue and the rules
never taken from the client, in any field, at any step
recomputed at the moment of charge, not carried through a session
the customer sees it before they confirm, and it is the same value charged
currency explicit at every step, never implied
integer minor units end to end, no binary floating point anywhere
rounding rule decided once, documented, and applied at one place
tax computed by rules with an effective date, not by a constant
discounts applied in a stated order, and applied once
```

A client supplied price is not a bug; it is a free products feature.

## 2. Idempotency

```
every charge, capture, refund and payout carries an idempotency key
the key is derived from the intent, not generated per attempt
a repeated request with the same key returns the original result
a repeated request with a different amount and the same key is a conflict
the key is stored with the operation, so a retry after a crash still matches
concurrency on the same key resolves to one winner
```

A double click, a network retry, a provider retry and a redeployed worker all
produce the same request twice. Idempotency is not a refinement; it is the
mechanism that prevents charging a customer twice.

## 3. The state machine

Write it before writing handlers, with the permitted transitions:

```
draft -> pending -> authorised -> captured -> refunded
                 -> failed
                 -> expired
                 -> disputed -> won | lost
```

```
every transition guarded by the current state in the update statement
no transition performed on the basis of a prior read
terminal states named, and transitions out of them refused
every state has a user visible meaning, and the interface never invents one
an unknown provider status maps to a state deliberately, never to success
```

## 4. Provider integration

```
the provider is the source of truth for money, the application for intent
never mark an order paid because the client returned to a success URL
confirm by webhook or by an explicit status query, both authenticated
timeouts on every call, and the timeout case treated as unknown, not failed
an unknown outcome is resolved by querying the provider, never by guessing
test mode and live mode credentials cannot be confused: separate keys,
  separate environments, and a check that refuses live keys outside production
```

The single most expensive failure in this discipline: a capture succeeds, the
response never arrives, the application records a failure, and the customer is
charged for nothing.

## 5. Webhooks

```
verify the signature before parsing anything
reject events outside a tolerated time window
store the raw event with the provider event id as a unique key
acknowledge quickly, process asynchronously
process idempotently, guarded by the state machine
handle out of order arrival, which is normal
never trust an event to be the only path: reconciliation exists for the ones
  that are lost
```

## 6. Reconciliation

The job that catches everything else:

```
compare provider records with application records, on a schedule
find: charges with no order, orders with no charge, amounts that differ,
  refunds recorded on one side only, currencies that do not match
report differences to a human, with enough context to act
never auto-correct money: propose, and let a person decide
keep the report even when it is empty, so its absence is noticeable
```

## 7. Refunds and disputes

```
refunds are idempotent, partial refunds sum to no more than the charge
a refund has a reason, an actor and a timestamp, recorded
the state machine forbids refunding an uncaptured or already refunded charge
disputes arrive by webhook and have deadlines: the system surfaces them
evidence for a dispute is assembled from records, not from memory
a lost dispute is a state, not a deletion
```

## 8. Subscriptions

```
the billing cycle, the anchor date and the timezone are explicit
proration rules stated, and the same rules produce the invoice preview the
  customer sees before confirming
a plan change is one operation with one outcome, not two chargeable events
failed renewals follow a documented retry and dunning schedule
cancellation: immediate or at period end, and the customer is told which
  access ends exactly when the record says it does, checked at request time
a trial that converts does so once, even if the job runs twice
```

## 9. Audit trail

```
every money affecting action recorded: who, what, when, how much, why
records are appended, never updated in place
the provider reference is stored on every record
enough detail to answer an accountant without opening the provider dashboard
personal and card data never stored: only the provider's references and the
  last four digits where the product needs them
```

## 10. Prohibitions

- Never accept an amount, a currency, a plan or a discount from the client.
- Never mark anything paid without provider confirmation.
- Never retry a charge without an idempotency key.
- Never store card numbers, security codes or full bank details.
- Never log a full payment payload, including in an error path.
- Never auto-correct a discrepancy discovered by reconciliation.
- Never use live credentials outside production.
- Never treat a timeout as a failure without querying the provider.
- Never let a refund path bypass the state machine.

## 11. Protocol

1. Write the state machine and the permitted transitions.
2. Decide where the amount is computed, and prove nothing else can set it.
3. Choose the idempotency key derivation for each operation.
4. Implement the intent, then confirm by webhook or explicit query.
5. Verify webhook signatures, store raw events, process asynchronously.
6. Guard every transition with the current state in the write.
7. Implement refunds, partial refunds and disputes inside the machine.
8. Write the reconciliation job before launch, not after the first mismatch.
9. Build the audit trail as an append only record.
10. Test the matrix in `resources/payment-test-matrix.md`, including the
    timeout after capture.

## 12. Auto-critique

Score from 0 to 5: server side amounts, idempotency on every money operation,
state machine guarded in the write, provider confirmation, webhook
verification and replay handling, reconciliation existing and reporting,
refunds and disputes modelled, audit trail completeness, no sensitive data
stored or logged.

Threshold: no axis below 3, average at least 4. Any client controlled amount,
or any charge without an idempotency key, is an automatic failure regardless
of the rest.

## 13. Interfaces

- Upstream: `requirements-analysis` for the commercial rules,
  `architecture-design` for the boundary, `api-design` for the contract.
- Lateral: `input-validation`, `background-jobs` for webhooks and renewals,
  `database-design` for the ledger and constraints, `security-audit` for the
  exposure review.
- Downstream: `reliability-testing` for the timeout and outage drills,
  `security-testing` for the authorization and tampering pass,
  `testing-quality` for the permanent tests, `observability` for the payment
  signals.

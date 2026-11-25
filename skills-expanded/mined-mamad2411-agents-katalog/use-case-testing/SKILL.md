---
name: use-case-testing
description: Derive test cases from use cases / user stories — main success scenario, alternate flows, exception flows, and acceptance criteria. Use to validate end-to-end user goals against requirements.
source: self
date_added: 2026-05-01
---

# Use Case Testing

Use case testing derives tests from the **goal a user pursues**, not from individual functions. It catches gaps between unit-correct components by exercising real journeys end-to-end across the main success scenario and every alternate/exception path.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Spec | ISTQB CTFL 4.0 §4.2.6, Cockburn — *Writing Effective Use Cases* |
| Format | Cockburn template (Brief / Casual / Fully Dressed); user story + acceptance criteria; BDD Gherkin |
| Test type | E2E or service-level integration; rarely unit |
| Pairing | Decision Tables (for branching flows), State Transition (for stateful actors) |
| Tools | Cucumber 7, Playwright/Cypress for UI, Karate/Bruno for API journeys |

## When to Use

- Validating a user-facing release.
- Acceptance testing with business stakeholders.
- Auditing critical journeys (signup, checkout, recovery).
- Discovering gaps between independently developed components.

## Anatomy of a Use Case

```
UC-07: Refund a paid order
Primary actor:    Merchant
Stakeholders:     Customer, Finance
Preconditions:    Merchant authenticated; order exists in state Paid
Trigger:          Merchant clicks "Refund"
Postconditions:   Order in state Refunded; ledger updated; webhook delivered

Main success scenario (MSS)
  1. System shows order detail with refundable amount
  2. Merchant submits refund (full or partial, with reason)
  3. System validates eligibility (within 30 days, sufficient balance)
  4. System issues refund via payment processor
  5. System updates order state to Refunded
  6. System emits 'order.refunded' event
  7. System sends confirmation to customer

Alternate flows
  3a. Refund within 30..60 days → request manager approval
  3b. Refund > 1 year → reject (out of policy)
  4a. Processor returns 5xx → retry with idempotency key (max 3)
  4b. Insufficient balance → mark Pending; notify finance

Exception flows
  *. Network unavailable at any step → roll back to last consistent state, surface error
  *. Concurrent refund attempt → second attempt 409
```

## Test Derivation Rules

1. **One test per scenario** (MSS + each alternate + each exception). Tag by scenario id.
2. **Pre/post-condition assertions**, not just step assertions.
3. **Cross-functional checks**: state, side effects (webhook, email, ledger), audit log.
4. **One actor per test**; multi-actor cases split into orchestrated sequences.
5. **Cover guards** in alternate flows (`within 30d` ↔ `between 30..60d` ↔ `> 1y`) — pair with EP/BVA on the guard variable.
6. **Time and concurrency** as first-class: race the exception flows.
7. **Negative paths verify the system fails safely** (no double charge, no partial state).

## Code

### Gherkin → executable

```gherkin
Feature: UC-07 Refund a paid order

Background:
  Given a merchant 'm-1' is authenticated
  And an order 'o-1' in state 'Paid' for 4200 cents created 5 days ago

Scenario: MSS — refund within 30 days
  When the merchant submits a refund of 4200 cents with reason 'customer-request'
  Then the response is 201 with refund.id matching /^re_/
  And the order 'o-1' is in state 'Refunded'
  And ledger balance for 'm-1' returned to its prior value
  And exactly one 'order.refunded' event was published for 'o-1'

Scenario: 3a — refund within 30..60 days requires approval
  Given order 'o-1' was created 45 days ago
  When the merchant submits a refund of 4200 cents
  Then the response is 202 'pending_approval'
  And the order is in state 'RefundPending'

Scenario: 3b — refund > 1 year rejected
  Given order 'o-1' was created 400 days ago
  When the merchant submits a refund
  Then the response is 422 'refund_window_exceeded'
```

### Playwright journey form

```ts
test('UC-07 MSS: refund within 30 days @critical', async ({ merchantApi, eventBus }) => {
  const order = await merchantApi.createPaidOrder({ amount: 4200, ageDays: 5 });
  const before = await merchantApi.balance();

  const refund = await merchantApi.refund(order.id, { reason: 'customer-request' });

  expect(refund.id).toMatch(/^re_/);
  expect((await merchantApi.getOrder(order.id)).state).toBe('Refunded');
  expect(await merchantApi.balance()).toBe(before);
  await expect(eventBus).toEmitOnce('order.refunded', { id: order.id });
});
```

## Traceability

| Use case | Scenario | Test ID | Status |
| --- | --- | --- | :-: |
| UC-07 | MSS | TC-PAY-0142 | ✅ |
| UC-07 | 3a within 30–60d | TC-PAY-0143 | ✅ |
| UC-07 | 3b > 1y | TC-PAY-0144 | ✅ |
| UC-07 | 4a processor 5xx retry | TC-PAY-0145 | ⏳ |
| UC-07 | 4b insufficient balance | TC-PAY-0146 | ⏳ |
| UC-07 | concurrent refund | TC-PAY-0147 | ✅ |

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Testing only the MSS | Each alternate and exception flow needs its own test |
| Asserting only the last step | Verify pre/post-conditions and side effects |
| Mixing two actors' steps | Split into separate, orchestrated tests |
| Rebuilding all setup via UI | Drive via API; UI only where it's the system under test |
| Ignoring time guards | Pair with BVA on the guard (29 / 30 / 31 days) |
| Not tracing back to use case | Tag every test with use-case id for coverage reports |
| Webhook/event ignored | Assert delivery (and idempotency) as part of the test |

## Output Format

```
Use case UC-07 Refund
  Scenarios planned: 6  automated: 5  manual: 1
  Status: 5 ✅  1 ⏳ (4a — needs processor mock)
  Side-effect coverage: order state ✅, ledger ✅, event bus ✅, email ⏳
```

## References

- A. Cockburn — *Writing Effective Use Cases*
- ISTQB CTFL Syllabus 4.0 — Use Case Testing
- Cucumber Reference: <https://cucumber.io/docs/cucumber/>
- M. Fowler — *Analysis Patterns* / use-case writing
- ISO/IEC/IEEE 29119-4

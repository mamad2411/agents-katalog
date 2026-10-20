---
name: "spec-writing-patterns"
description: "Specification patterns: the testability test, shall, should, and may, Gherkin acceptance criteria, interface contracts, non-requirements, open questions, state machine documentation, and anti-patterns such as the omnibus requirement. Use when writing or reviewing specs."
---

# Spec Writing Patterns

## The Testability Test

Every requirement must answer: "How would you verify this in a test case?" If you cannot write a test case from the requirement, it is not a requirement -- it is a wish.

```
# Wish (untestable)
The checkout flow should be fast and intuitive.

# Requirement (testable)
The checkout flow shall complete in ≤ 3 user interactions from cart to
order confirmation. The payment step shall respond to submission in ≤ 3s
at p99 under normal load (≤ 500 concurrent users).
```

Quantify these dimensions wherever possible:
- Time (response time, duration, frequency)
- Quantity (count, size, rate)
- Accuracy (error rate, precision, recall)
- Scope (which users, which inputs, which conditions)

## Shall vs. Should vs. May

Use precise modal verbs consistently (IEEE 830 convention):

| Word | Meaning | Use for |
|------|---------|---------|
| **shall** | Mandatory requirement | Must-have features, safety, compliance |
| **should** | Recommended but not mandatory | Best practices, nice-to-haves |
| **may** | Optional | User choice, extension points |

```markdown
# Bad: uses "should" for a mandatory security requirement
Passwords should be hashed.

# Good: uses "shall" for mandatory requirement
The system shall store passwords as bcrypt hashes with cost factor ≥ 12.
Plaintext passwords shall never be written to logs, databases, or files.
```

## Gherkin Acceptance Criteria

Gherkin (Given/When/Then) is the bridge between specification and test code. Use it for every functional requirement:

```markdown
### FR-015: Failed login lockout

**Given** a user account with 4 failed login attempts in the last 15 minutes
**When** the user submits an incorrect password
**Then** the account is locked for 15 minutes
**And** a lockout notification is sent to the account email
**And** the response body contains `{"error": "ACCOUNT_LOCKED", "unlocksAt": "[ISO 8601]"}`
**And** no additional login attempts are accepted until the lockout expires

**Given** the same account after the lockout period expires
**When** the user submits correct credentials
**Then** login succeeds and the failed attempt counter resets to 0
```

## Interface Contract Pattern

When two systems interact, the specification must define the full contract -- not just the happy path:

```markdown
## Contract: What the Caller Must Do

- Retry on 5xx with exponential backoff (initial: 100ms, max: 30s, max retries: 3)
- Do NOT retry on 4xx (the request is invalid; retrying will produce the same error)
- Include `Idempotency-Key: [uuid]` header for all state-mutating requests
- Handle 409 as idempotent success (the operation already completed)

## Contract: What the Server Must Do

- Process requests with the same Idempotency-Key identically for 24 hours
- Return 4xx for all client errors (never silently succeed with wrong data)
- Include `Retry-After` header on 429 responses
- Never return 200 for partial failures (all-or-nothing)
```

## Non-Requirement Pattern

Specs without explicit scope boundaries expand until they contain everything. Explicitly state what is out of scope:

```markdown
## Out of Scope

This specification does NOT cover:
- Changing the payment provider (covered in RFC-0045)
- Refund processing (separate service, separate spec)
- Fraud detection (handled by the payment provider, not this system)
- Currency conversion (all amounts are in the order's original currency)

If you are implementing one of these, you need a different specification.
```

## Open Questions Format

Open questions in a spec are assets, not problems. They signal intellectual honesty and prevent implementation from starting before key decisions are made:

```markdown
## Open Questions

- [ ] **[Alice, Platform]**: What is the maximum payload size for the webhook body?
  Our current setup defaults to 1MB. If the order has 500+ line items, we may exceed this.
  **Options**: 1MB (current default), 5MB (needs config change), chunked delivery
  **Decision needed before**: Webhook implementation starts

- [ ] **[Bob, Security]**: Do we need to log the full request body for audit purposes?
  This would include PII (email, shipping address). Logging it creates GDPR implications.
  **Decision needed before**: Logging implementation

- [ ] **[UNRESOLVED]**: How do we handle concurrent updates to the same order?
  Last-write-wins vs. optimistic locking vs. pessimistic locking?
  **This is a blocking question -- implementation cannot proceed until resolved.**
```

Each open question must have:
- An owner (not just a team)
- The options being considered
- A deadline (tied to implementation milestone, not a calendar date)
- Whether it is blocking or non-blocking

## State Machine Documentation

Any feature with multiple states must have an explicit state machine. Undocumented state machines produce bugs:

```markdown
## State Machine: Subscription

### States

| State | Meaning | Can Transition To |
|-------|---------|------------------|
| `trial` | Active trial, no payment required | `active`, `expired` |
| `active` | Paid subscription | `past_due`, `cancelled` |
| `past_due` | Payment failed, grace period | `active`, `cancelled` |
| `cancelled` | Subscription ended | `active` (resubscribe only) |
| `expired` | Trial ended without subscribing | `active` (subscribe only) |

### Transition Rules

1. A subscription in `cancelled` state may be reactivated (→ `active`) only through a new payment
2. A subscription in `past_due` state provides full access for 7 days before downgrading to read-only
3. The `expired` state is terminal unless the user explicitly subscribes

### Prohibited Transitions

Any code that attempts a transition not listed above is a bug:
- `expired` → `trial` (cannot re-enter trial)
- `active` → `trial` (cannot downgrade to trial)
- `cancelled` → `trial` (cannot re-enter trial)
```

## Anti-Patterns

### The Omnibus Requirement
```
# Bad: one requirement doing multiple things
The system shall authenticate users, log all authentication attempts,
send confirmation emails, and invalidate sessions after 24 hours.

# Good: atomic requirements, each independently testable
FR-001: The system shall authenticate users via email/password.
FR-002: All authentication attempts shall be logged with timestamp, IP, and outcome.
FR-003: Successful authentication shall trigger a confirmation email within 30 seconds.
FR-004: Sessions shall expire after 24 hours of inactivity.
```

### The Implementation-Masquerading-as-Requirement
```
# Bad: specifies implementation, not behavior
The system shall use bcrypt for password hashing with a PostgreSQL-backed
session store using Redis for cache.

# Good: specifies behavior, allows implementation choice
The system shall protect user credentials from offline dictionary attacks.
Passwords shall not be recoverable from the stored representation.
```

### The Underspecified Error Case
Missing error case specifications are bugs waiting to happen:
```
# Bad: only specifies success
When the user submits payment, the order is confirmed.

# Good: specifies success and all error cases
When the user submits payment:
- On success: order transitions to `paid`, confirmation email sent
- On payment declined: order remains `pending`, user sees decline reason
- On timeout (>30s): order remains `pending`, user sees "try again" message
- On duplicate submission: returns 409, idempotent (no double charge)
```

## References
- [IEEE 830 - Software Requirements Specification](https://ieeexplore.ieee.org/document/720574)
- [RFC 2119 - Key words for use in RFCs](https://www.rfc-editor.org/rfc/rfc2119)
- [Gherkin Reference](https://cucumber.io/docs/gherkin/reference/)
- [Writing Good Requirements (NASA)](https://www.nasa.gov/reference/4.4-how-to-write-a-good-requirement/)

---
name: fullstack-engineering
description: Owns a feature across every layer: contract first design, schema to UI consistency, layer by layer completion, cross layer state and error alignment, and end to end verification. Use when a change crosses the client and server boundary or touches more than one layer.
license: MIT
metadata:
  category: dev-skills
  version: 1.0.0
  depends_on: [engineering-core, architecture-design, backend-engineering, frontend-engineering]
  outputs: [feature-contract, layer-completion-matrix, end-to-end-verification]
---

# Full-Stack Engineering

Owns the whole vertical slice. A feature is not finished because the endpoint
returns 200, and not because the page renders. It is finished when the chain
from click to storage and back is consistent, including every failure.

This skill does not replace `backend-engineering` and `frontend-engineering`.
It sequences them and holds the contract they share.

## 1. The chain

Every feature is traced through this chain, in both directions, before it is
declared done.

```
user action -> component state -> client validation -> request
  -> boundary validation -> authentication -> authorization
  -> business rules -> transaction -> persistence
  -> external services -> response shape -> status code
  -> client cache invalidation -> component state -> rendered result
```

Failure chain, traced separately:

```
invalid input -> field errors rendered
unauthenticated -> redirect or sign in prompt, without losing the input
forbidden -> a message that does not reveal existence
conflict -> the state the user must resolve, with the action to resolve it
provider failure -> a degraded but truthful result
timeout -> a retry path that cannot duplicate the effect
```

## 2. Contract first

Before either side is written, fix the contract in one place:

```
Endpoint      method, path
Request       shape, required fields, who owns each identifier
Response      success shape, explicit field list
Errors        codes, statuses, which are retryable
Pagination    shape, default, maximum
Effects       what changes in storage, what is sent, what is invalidated
```

Both sides implement the same contract, and the tests assert it. Two
implementations that agree by coincidence diverge on the first change.

Where the stack generates types from a schema, generate them. Where it does
not, define the shape once and import it on both sides. Hand written duplicate
types are a defect that surfaces months later.

## 3. Protocol, the order of work

1. **Contract**, section 2.
2. **Data layer**: schema and migration, since everything above depends on
   the shape.
3. **Server**: service rules, then the handler, following
   `backend-engineering`.
4. **Contract test**: the endpoint responds as the contract says, including
   errors. This is the checkpoint before any UI exists.
5. **Client data layer**: the typed call, cache keys, invalidation.
6. **UI**: the five states, following `frontend-engineering`.
7. **Journey test**: the browser path, following `playwright-automation`.
8. **Cross layer review**, sections 4 and 5.

Building the UI first against an imagined response is the most common way a
feature ends up with two contracts.

## 4. Cross layer consistency rules

**Validation.** The client rules are a subset of the server rules, never a
superset. A field the client accepts and the server rejects is a defect the
user meets; the reverse is only an ergonomic gap.

**Errors.** Every error code the server can return is handled by the client.
An unhandled code renders a generic failure, never a blank screen or a stuck
spinner.

**Types.** One definition, shared or generated. Optional on the server means
optional on the client.

**Money, dates, identifiers.** One representation across the chain: money in
integer minor units with a currency, timestamps in a single format with an
explicit timezone policy, identifiers as opaque strings.

**Empty and absent.** Decide once whether a missing collection is an empty
array or an absent field, and hold it on both sides.

**Cache invalidation.** Every mutation names the cached data it invalidates,
at the time the mutation is written.

**Authorization.** The UI may hide a control. The server rejects it anyway,
and there is a test for that rejection.

## 5. Layer completion matrix

Filled before delivery. Every cell is done, not applicable with a reason, or
missing with a plan.

```
| Layer | Implemented | Validated | Errors handled | Tested |
|---|---|---|---|---|
| database schema |  |  |  |  |
| migration |  |  |  |  |
| data access |  |  |  |  |
| service rules |  |  |  |  |
| handler |  |  |  |  |
| authorization |  |  |  |  |
| client call |  |  |  |  |
| cache invalidation |  |  |  |  |
| component states |  |  |  |  |
| form and validation |  |  |  |  |
| navigation and focus |  |  |  |  |
| documentation |  |  |  |  |
```

A row that is implemented but untested is not complete. A partially complete
matrix is reported as partial, with the missing cells named.

## 6. Prohibitions

- No UI built against an assumed response shape.
- No endpoint shipped without a caller or a contract test.
- No duplicated type definitions on the two sides.
- No client side only rule that the server does not enforce.
- No mutation without a declared invalidation.
- No feature declared done with an unfilled matrix row.
- No layer skipped because it is expected to work.

## 7. Auto-critique

Score from 0 to 5: contract fixed before implementation, chain traced in both
directions, failure chain implemented, cross layer consistency, matrix
completeness, end to end verification actually executed.

Threshold: no axis below 3, average at least 4. An untraced failure chain is
an automatic failure, because that is where a feature breaks in production.

## 8. Interfaces

- Upstream: `architecture-design`, `project-exploration`.
- Coordinates: `backend-engineering`, `frontend-engineering`,
  `input-validation`, `security-audit`.
- Downstream: `testing-quality`, `playwright-automation`,
  `code-review-protocol`, `technical-documentation`, `project-continuity`.

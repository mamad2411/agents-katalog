---
name: api-and-contract-design
description: Designs interfaces other systems depend on - REST, GraphQL, gRPC, events, webhooks - with versioning, compatibility and error contracts. Use when creating or changing a public surface. Triggers - design REST endpoints, breaking change, API versioning, what should this return on error, event schema, contract test.
---

# API and Contract Design

Every published interface is a promise you cannot unmake unilaterally. Internal
code can be refactored; a contract with consumers can only be extended,
deprecated, or broken. The cost of a bad contract is paid by everyone who
integrates with it, for as long as it exists.

Design so the right usage is easy and the wrong usage is impossible.

## Before designing

- **Who are the consumers?** One internal caller you control, or unknown
  third parties? This sets your compatibility burden more than anything else.
- **What is the consumer's job?** Design around their use case, not your
  storage layout. An API that mirrors your tables leaks your schema and locks
  you into it.
- **Read or write, sync or async?** A write that takes seconds is an async
  operation with a status resource, not a slow POST.

## Resource and operation shape

| Rule | Why |
|---|---|
| Name resources as nouns from the domain glossary | Consumers learn the domain, not your internals |
| One operation does one thing | A `save` that sometimes creates and sometimes side-effects is untestable and unversionable |
| Make idempotency explicit | Writes need an idempotency key or a natural key; the network **will** retry |
| Explicit is better than implicit defaults | An omitted field must not silently mean "delete" |
| Pagination from day one, always bounded | An unbounded list is an outage waiting for data growth |
| Filtering and sorting are part of the contract | Ad-hoc query params become permanent |
| Return the created/updated resource | Saves the consumer a round trip and avoids read-after-write races |

**Nullability and optionality are semantics, not syntax.** Distinguish "absent",
"null" and "empty" in the contract text, especially for partial updates.

## Errors are part of the contract

Most APIs specify the happy path and improvise the rest. Consumers then parse
error strings, and your message wording becomes an unversioned contract.

Specify:

- A **stable machine-readable code** per failure (`INSUFFICIENT_FUNDS`), never
  only prose
- Which field caused it, for validation errors
- Whether the failure is **retryable**, and after how long
- A correlation id the consumer can quote in a support request

```json
{ "error": { "code": "INSUFFICIENT_FUNDS", "message": "human text",
             "field": "amount", "retryable": false,
             "correlation_id": "01H..." } }
```

Use the transport's status semantics correctly (4xx = the caller must change
something; 5xx = the caller may retry). Returning 200 with an error body breaks
every generic client, retry policy and monitor.

## Compatibility

**Backward compatible** (safe to ship):

- Add an optional field to a request
- Add a field to a response — *only if* consumers ignore unknown fields; state
  that requirement in the contract
- Add a new endpoint, a new enum value in a field consumers treat as open,
  a new optional header

**Breaking** (needs a version or a migration):

- Remove or rename anything; change a type; tighten validation
- Change the meaning of an existing field — the most dangerous kind, because
  nothing fails loudly
- Add a required request field; change defaults; change error codes
- Change ordering, pagination behavior, or timing guarantees consumers rely on

### Versioning

| Strategy | Use when |
|---|---|
| No version, additive only | Internal, few consumers, disciplined evolution |
| URL version (`/v2/`) | Public HTTP APIs; simple, visible, coarse |
| Media-type / header version | Fine-grained evolution, sophisticated consumers |
| Schema evolution rules (Protobuf/Avro) | Events and RPC; never reuse a removed field number |

Rules regardless: support **N-1** for a stated period; publish the deprecation
date when the new version ships, not later; measure usage per version so you
know when it is safe to remove (`deprecation-and-migration`).

## Events

Events are harder than APIs: consumers are unknown, and history is often replayed.

- Name in the **past tense** — `OrderPlaced`, not `CreateOrder`. An event is a
  fact, not a command.
- Include `event_id`, `occurred_at`, `version`, and the aggregate id.
- **Consumers must be idempotent**; at-least-once is the realistic guarantee.
- Choose deliberately: *thin* events (id only, consumer fetches) couple to your
  API and read model; *fat* events (full payload) couple to your schema but
  survive independently. Thin for internal, fat for cross-boundary, usually.
- Never publish an event containing a field you are not committed to keeping.

## Per protocol

The rules above hold for every protocol; each protocol breaks them in its own
quiet way — a GraphQL field made nullable, a reused Protobuf field number, an
unsigned webhook. Before designing or reviewing a surface, read its section:
HTTP defaults in `references/http-api-conventions.md`; GraphQL, gRPC and
Protobuf, events and webhooks in `references/api-protocol-checklists.md`.

## Worked example: classifying a change

`GET /v1/invoices/{id}` is public. Its contract says consumers must ignore
unknown fields; it says nothing about enums. A pull request proposes three
changes:

| Change | Class | Why | Ship as |
|---|---|---|---|
| Add optional `?expand=lines` | Compatible | New optional input; old requests behave identically | Ship |
| Add `PARTIALLY_PAID` to `status` | **Breaking** | The enum was never declared open; a client switching on `status` hits an unknown value — and nothing fails loudly | Declare `status` open in the contract now; ship the value after the notice period, with consumers told |
| Rename `total` to `amount_due` | **Breaking** | Removal plus addition | Add `amount_due`, keep `total` with the same value, mark `total` deprecated with a sunset date, measure its use, remove in `/v2` or after the date |

The review output names each change's class and reason, and the CI schema
diff confirms it: the diff must flag the rename and pass the query parameter.
If the diff passes the rename, the check is misconfigured — fix the check
before trusting it on the next change.

## Contract testing

Hand-checked compatibility fails silently. Make it mechanical:

- Keep the schema (OpenAPI, GraphQL SDL, Protobuf, JSON Schema) in the
  repository as the source of truth, generated from or checked against the code
- Run a **compatibility diff in CI** against the previously released schema;
  fail the build on a breaking change unless a version bump accompanies it
- For each consumer you control, a consumer-driven contract test
- Record real provider responses as fixtures and replay them; a mock you wrote
  tests your assumption, not their behavior

## Exit checklist

- [ ] Resource names come from the domain glossary
- [ ] Every write operation is idempotent or documents why it cannot be
- [ ] All list endpoints are paginated with a bounded maximum
- [ ] Error contract: stable codes, field attribution, retryability, correlation id
- [ ] Compatibility class of every change assessed (compatible vs breaking),
      with the reason, as in the worked example
- [ ] The protocol's checklist applied (HTTP, GraphQL, gRPC/Protobuf, events,
      webhooks), or the missing lookup reported
- [ ] Schema checked into the repo; CI diffs it for breaking changes
- [ ] Deprecation path and sunset date published with any replacement
- [ ] Events are past tense, versioned, idempotently consumable

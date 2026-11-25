---
name: design-api-contract
description: Contract-first design of an HTTP API (OpenAPI 3.1) or an event-driven API (AsyncAPI 3) — resource and channel modelling, RFC 9457 problem-details error model, pagination, idempotency keys, conditional requests, versioning and the CI gates that keep the contract honest. Use before writing any handler, client or producer. Not for internal module interfaces or database schemas.
allowed-tools: Read Grep Glob Write Edit Bash
user-invocable: true
argument-hint: "[http|async] <service-name> [--from contracts/<file>]"
metadata:
  foundry.vertical: dev
  foundry.io: "requirement.v1 -> contracts/**/*.yaml + review.v1"
license: Apache-2.0
---

# Design an API contract

Contract-first means the contract is written, reviewed and merged **before** the implementation,
and the implementation is verified against it. Contract-after — generating a spec from
annotations once the code exists — documents whatever you happened to build, including the
mistakes, and gives consumers no chance to object while objecting is still cheap.

The test for whether you are doing this right: **a consumer team can build and test against the
contract with zero access to your implementation.**

## Layout

```
contracts/
  http/<service>.openapi.yaml        # OpenAPI 3.1
  async/<service>.asyncapi.yaml      # AsyncAPI 3
  shared/problems.yaml               # the problem-type catalogue, reused by every service
  shared/pagination.yaml             # cursor page envelope + parameters
  fixtures/<consumer>/*.json         # recorded real payloads used by ACL tests
  CHANGELOG.md                       # one entry per contract change, human-written
.spectral.yaml                       # lint ruleset, enforced in CI
```

Pin every CLI you invoke to the version recorded in
`${CLAUDE_PLUGIN_ROOT}/references/stack-versions.json`. Do not write a version number from memory
into a command, a `package.json` or the contract itself.

## Procedure

### 1. Start from the domain, not from the database

Read the `requirement.v1` set and, when present, the `domain-modeler` output. For each command
and read model you need:

- the **resource or channel** it maps to, named with the ubiquitous language;
- the **actor** and therefore the authorization decision;
- whether it is a query (safe, cacheable) or a state change (needs idempotency).

Never publish the internal domain model verbatim. The contract is a *published language* — it is
allowed to be smaller, flatter and more stable than what is behind it. If renaming an internal
field forces a contract change, the boundary has failed.

### 2. HTTP: model resources, then operations

- Resource paths are plural nouns: `/orders`, `/orders/{orderId}/lines`. No verbs in paths.
  An operation that genuinely is not CRUD gets an explicit sub-resource
  (`POST /orders/{id}/cancellation`) rather than `POST /cancelOrder`.
- Nesting depth ≤ 2. Deeper means you are exposing your join graph.
- Identifiers in paths are opaque strings in the contract, whatever they are internally.
- Method semantics per **RFC 9110 §9.2**: `GET`/`HEAD` safe, `PUT`/`DELETE` idempotent,
  `POST`/`PATCH` are not — which is what §5 is about.
- `PATCH` **must** declare its body format: JSON Merge Patch (RFC 7386,
  `application/merge-patch+json`) or JSON Patch (RFC 6902, `application/json-patch+json`).
  "PATCH with a partial object" is not a specification.

Status codes — pick from this list and no other:

| Code | Use for | Never for |
|---|---|---|
| 200 | successful read or in-place change returning a body | anything with an error in the body |
| 201 | resource created; `Location` header mandatory | async accepted work |
| 202 | accepted, not yet done; body carries a status resource URL | work that already completed |
| 204 | success with genuinely nothing to say | when the client needs the new state |
| 400 | malformed syntax the parser rejected | semantic/business rule failure |
| 401 | no or invalid credentials; `WWW-Authenticate` mandatory | authenticated-but-forbidden |
| 403 | authenticated, not permitted | hiding existence (use 404) |
| 404 | absent, or present-but-invisible-to-you | a failed business rule |
| 409 | state conflict: duplicate, concurrent idempotent request in flight | validation errors |
| 412 | `If-Match` precondition failed (RFC 9110 §13.1) | generic conflicts |
| 422 | syntactically valid, semantically rejected — the business-rule code | parse errors |
| 429 | rate limited; `Retry-After` mandatory (RFC 6585, RFC 9110 §10.2.3) | server overload you did not measure |
| 5xx | your fault, always | anything the client could fix |

### 3. Error model — RFC 9457 problem details, no exceptions

Media type `application/problem+json`. Standard members: `type` (URI), `title`, `status`,
`detail`, `instance`. Everything else is an extension member.

```yaml
# contracts/shared/problems.yaml
components:
  schemas:
    Problem:
      type: object
      required: [type, title, status]
      properties:
        type:     { type: string, format: uri, description: "Stable problem-type URI. Clients branch on this, never on detail." }
        title:    { type: string, description: "Human-readable, same for every occurrence of the type." }
        status:   { type: integer, minimum: 400, maximum: 599 }
        detail:   { type: string, description: "This occurrence. Free text. Never parsed by clients." }
        instance: { type: string, format: uri, description: "URI of this occurrence, e.g. /problems/{traceId}." }
        traceId:  { type: string, description: "Extension: correlates with logs." }
        errors:
          type: array
          description: "Extension: field-level failures for 422."
          items:
            type: object
            required: [pointer, code]
            properties:
              pointer: { type: string, description: "RFC 6901 JSON Pointer into the request body, e.g. /lines/2/quantity." }
              code:    { type: string, description: "Stable machine code, e.g. below_minimum." }
              detail:  { type: string }
```

Rules that make this actually useful:

1. **`type` is a stable URI in your own namespace** — `https://api.acme.com/problems/insufficient-stock`
   or `urn:acme:order:insufficient-stock`. It is part of the contract: changing it is breaking.
   `about:blank` is allowed only when the status code alone carries all the meaning.
2. **Maintain a catalogue.** Every problem type is declared once in `contracts/shared/problems.yaml`
   with its status code and its meaning. An undeclared `type` in a response is a contract violation.
3. **Never leak internals** into `detail`: no stack traces, no SQL, no upstream vendor messages,
   no internal ids. Put the correlation handle in `traceId` instead.
4. **Clients branch on `type` and `errors[].code`,** never on `title` or `detail`, which are free
   to be reworded or localised.
5. **One problem type per business rule**, not one generic `validation-error` for everything —
   otherwise the consumer must parse prose to decide what to do.

### 4. Pagination

Default to **cursor pagination**. Offset pagination over a collection that changes under the
reader skips and duplicates rows, and gets slower the deeper you go.

```yaml
parameters:
  - name: limit
    in: query
    schema: { type: integer, minimum: 1, maximum: 100, default: 20 }
  - name: cursor
    in: query
    schema: { type: string }
    description: "Opaque. Take it from nextCursor; do not construct or parse it."
```

Response envelope (`contracts/shared/pagination.yaml`):

```yaml
type: object
required: [items, page]
properties:
  items: { type: array, items: { $ref: "..." } }
  page:
    type: object
    required: [nextCursor]
    properties:
      nextCursor: { type: [string, "null"], description: "null means the end. Absence means nothing." }
      totalCount: { type: integer, description: "Optional and expensive; omit unless a consumer requires it." }
```

Non-negotiables:

- The sort order must be a **total order**: sort key plus a unique tiebreaker (`createdAt DESC, id DESC`).
  Without the tiebreaker the cursor is ambiguous and rows will repeat.
- The cursor encodes the sort-key values of the last item, base64url, and is **opaque** — the
  contract says so, so you can change the encoding without breaking anyone.
- `null` `nextCursor` is the only end-of-collection signal. Do not use an empty `items` array,
  which is also a legitimate mid-collection state after filtering.
- Also emit `Link: <…>; rel="next"` (RFC 8288) for consumers that expect it. It duplicates
  `nextCursor` on purpose.
- Offset pagination is acceptable **only** for small, append-stable admin lists; when you use it,
  say in the description why the drift is tolerable.

Note in OpenAPI 3.1 nullability is `type: [string, "null"]`; the OpenAPI 3.0 `nullable: true`
keyword no longer exists because 3.1 uses the JSON Schema 2020-12 dialect.

### 5. Idempotency keys

Every `POST` (and any non-idempotent `PATCH`) that a client may retry declares:

```yaml
parameters:
  - name: Idempotency-Key
    in: header
    required: true
    schema: { type: string, format: uuid }
    description: >
      Client-generated UUID identifying one logical attempt. Resending the same key with an
      identical body replays the original response. Same key with a different body returns 422
      (urn:acme:idempotency-key-reuse). A key whose first request is still in flight returns 409.
      Keys are retained for 24 hours.
```

The `Idempotency-Key` header field is an IETF HTTPAPI **Internet-Draft**, not an RFC — so the
semantics above are *yours* and must be written into the contract description, not assumed.
Mechanism and storage are `integration-architect`'s territory; the contract's job is to state
the observable behaviour, the retention window and the three failure codes.

For updates, add optimistic concurrency: `ETag` on the representation, `If-Match` required on
the write, `412` when it does not match (RFC 9110 §8.8.3, §13.1). Without it, last-write-wins is
a silent data-loss feature.

### 6. Versioning

- **Major version in the path**: `/v1/orders`. Simple, cache-friendly, visible in logs and
  routing rules. Media-type versioning (`application/vnd.acme.order.v2+json`) is defensible and
  more precise, but only pick it if your gateway and CDN handle `Vary: Accept` correctly.
- **No minor versions anywhere.** Within a major version the contract only ever grows:
  new optional fields, new endpoints, new enum members *if* the contract told clients to tolerate
  unknown members. Everything else is a new major.
- Two majors live in parallel during migration, never three.
- Deprecation is announced in the contract itself (`deprecated: true` plus a description naming
  the replacement and the removal date) and at runtime via a `Sunset` header (**RFC 8594**) and a
  deprecation header field — the IETF HTTPAPI deprecation header has been published as an RFC;
  read the current number from the spec before citing it, do not write one from memory.
- Compatibility rules, the expand-contract migration and the deprecation timeline belong to the
  `evolve-schema` skill. Invoke it rather than inventing a policy here.

### 7. AsyncAPI 3 for event and message APIs

AsyncAPI 3 separates **channels** (where messages live) from **operations** (what this
application does), which removes the v2 `publish`/`subscribe` ambiguity. Get this right or the
document means the opposite of what you intend:

- `action: send` — *this* application sends the message.
- `action: receive` — *this* application receives it.

Both are written from the point of view of the application the document describes.

Required content for every channel:

- `address` (topic/queue name) and the **partition/ordering key**, stated in the description.
- `messages` with a `payload` schema and `headers`; reuse `messageTraits` for the envelope.
- `servers` with the protocol binding (`kafka`, `amqp`, `mqtt`, `ws`) and the binding-specific
  fields; the protocol itself is chosen by `protocol-engineer`, not here.
- Delivery semantics, retry and DLQ behaviour written into the channel description — a consumer
  cannot infer "at-least-once, dedup on `id`" from a schema.
- An envelope on every message: `id`, `type`, `source`, `time`, `subject` (partition key),
  `dataschema`, `data`. CloudEvents is a reasonable off-the-shelf envelope; if you adopt it, name
  the binding (Kafka binary, HTTP structured, …) in the contract.

### 8. Gate it in CI

```bash
# lint (ruleset in .spectral.yaml — see references/spectral-ruleset.md)
npx --yes @stoplight/spectral-cli lint contracts/http/*.yaml contracts/async/*.yaml

# structural validation
npx --yes @redocly/cli lint contracts/http/*.yaml
npx --yes @asyncapi/cli validate contracts/async/*.yaml

# breaking-change detection against the merge base
oasdiff breaking origin/main:contracts/http/orders.openapi.yaml contracts/http/orders.openapi.yaml
```

Wire all four into a required CI job. Add consumer-driven contract verification (Pact or
equivalent) so the provider pipeline fails while a published consumer expectation is unmet.
If any of these CLIs is unavailable in the environment, say so explicitly in your output and fall
back to the manual checklist below — do not silently skip the gate.

## Quality gate

- [ ] Contract file exists and is referenced from the ADR or requirement that motivated it.
- [ ] Every operation: `operationId`, `summary`, ≥ 1 example request and response, `security`.
- [ ] Every operation declares at least one 4xx and the 5xx, all as `application/problem+json`.
- [ ] Every problem `type` used appears in `contracts/shared/problems.yaml`.
- [ ] Every collection endpoint paginated, with a total-order sort and an opaque cursor.
- [ ] Every retryable non-idempotent operation declares `Idempotency-Key` and its three failure codes.
- [ ] Every mutable resource exposes `ETag` and requires `If-Match` on write.
- [ ] No `nullable:` keyword (that is OpenAPI 3.0); nullability via `type: [x, "null"]`.
- [ ] AsyncAPI: every operation's `action` is correct from the document owner's perspective, and
      every channel names its ordering key and delivery semantics.
- [ ] Lint + validate + `oasdiff breaking` all pass, or the failure is reported explicitly.
- [ ] `CHANGELOG.md` entry written by a human, not generated.
- [ ] A `review.v1` artifact emitted with `dimension: "api-contract"` when this ran as a review.

## Progressive disclosure

| File | Load when |
|---|---|
| `references/worked-example.md` | authoring a new contract — a complete OpenAPI 3.1 + AsyncAPI 3 pair for one service |
| `references/spectral-ruleset.md` | setting up or extending `.spectral.yaml` |

## What this skill deliberately does not cover

- **Protocol choice.** REST vs gRPC vs GraphQL vs WebSocket is `protocol-engineer`.
- **Delivery mechanics.** Outbox, saga, retry policy, DLQ thresholds: `integration-architect`.
- **Compatibility rules and migration.** `evolve-schema` owns expand-contract and deprecation timing.
- **Domain modelling.** Resource names come from `domain-modeler`'s glossary, not from this skill.
- **Authorization design.** The contract declares `security` schemes; who may do what, and the
  permission model behind it, is the security reviewer's.
- **Rate-limit policy and quota economics.** Ops and economics own the numbers; the contract only
  documents `429` and `Retry-After`.
- **Code generation and SDK ergonomics.** Generators are downstream of a correct contract.
- **GraphQL schemas and `.proto` files.** Different artifacts, different rules; not modelled here.

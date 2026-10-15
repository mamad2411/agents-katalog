---
name: audit-external-api-port
description: Independent, read-only audit of a GitHub-issue-led TagMango external API port — behavioral parity, public-contract quality, backend enforcement, exposure and security, shared libs/services + libs/repository architecture, and core-replacement readiness. Reports P0–P3 findings and one certification verdict; never edits code.
argument-hint: "[pr-number | branch | packet-path]"
disable-model-invocation: true
---

# Audit External API Port

Reconstruct the expected behavior and public contract independently. The port packet, comments, docs, and tests are claims to verify, not authority. Stay read-only and findings-first: no edits, staging, commits, publishing, or thread resolution unless the user explicitly asks after seeing the findings.

Read [audit-rubric.md](references/audit-rubric.md) before reviewing the diff; it holds the per-area checklists this workflow walks.

## 1. Lock scope and evidence

Read repository instructions, coding standards, testing rules, architecture maps, and working-tree state. Determine the exact base-to-head or user-specified diff; report unrelated dirty files and keep them out of scope.

Pin: the initiating GitHub issue with its `I-###` requirements and accepted decisions; target branch/commit and external surface; authoritative `apps/api` and/or `apps/core-api` commits; the user-designated `tagmango-web-platform` commit; the port packet path; claimed `M-###` mappings and readiness state; and the OpenAPI/runtime evidence available. Resolve ambiguous source authority from repository evidence first; ask only when the ambiguity would change a material conclusion.

## 2. Reconstruct behavior independently

Trace the full backend decision path and the frontend flow (rubric §2 lists the areas). Classify each frontend restriction as business invariant, entitlement gate, normalization/default, UI convenience, or ambiguity.

Build your own ledger of externally meaningful scenarios: negative combinations, lifecycle states, permissions, ownership, tenant/host binding, side effects, ordering, idempotency, retries, and absent/null/false/zero/empty semantics. Define the scoped capability independently of the external contract — including modes the external API intentionally omits but a future core replacement needs. If the legacy route bundles several capabilities, verify the declared decomposition.

Compare your ledger against the target and the packet; never downgrade a rule you found because the packet omitted it. Verify the issue was treated as a starting brief, and that every `G-001`–`G-008` dimension was resolved by the developer or justified `N/A`, with the implementation matching those resolutions.

## 3. Audit the wire contract

Judge from the generated OpenAPI document and, when a running server or captured integration response is available, real runtime responses. Never infer the public URL from a controller fragment or the response shape from Swagger DTO metadata. Walk rubric §3 and §5: complete versioned URL, honest method and resource boundaries, deliberate parameter placement, per-field semantics, allowlisted grouped responses, stable documented errors, and retry/idempotency/pagination/compatibility semantics where material.

For every resource concept the response returns or embeds, locate its canonical representation elsewhere on the external surface and diff the shapes — an embedded resource whose fields, names, or null semantics differ from the standalone representation without a recorded tier decision is a contract finding.

Acid test: write the minimal valid request, an important optional combination, and an invalid combination from the docs alone. If that fails, record a contract finding.

## 4. Audit validation and enforcement

Build a decision table from every discriminator and dependent field, then reason through combinations the first-party frontend never emits — external callers send anything schema-valid. Walk rubric §4: conditional requirements and prohibitions, contradictory values, actor/tenant/currency/entitlement/ownership/state rules, boundaries and encodings, create-versus-patch absent/null semantics, race-safe uniqueness, promoted frontend business rules, and UI conveniences that must not have been promoted.

Documentation without enforcement is a defect, and a DTO decorator cannot enforce a rule that needs authenticated or database context — check the layer, not just the presence.

## 5. Audit exposure and security

Trace every response field to its source and treat exposure as an allowlist exercise (rubric §6). Verify authentication, API-key scope, host/tenant binding, permission, resource ownership, rate/quota policy, and non-enumeration separately — test or inspect revoked keys, wrong hosts, other-owner resources, and failure messages. For mutations, inspect atomicity, duplicate submission, timeout/retry behavior, and whether side effects can double-run.

## 6. Audit architecture and core-replacement readiness

Verify the shared-capability shape: controller owns parsing/auth and delegates one meaningful use case; business rules, transactions, and side-effect orchestration live in `libs/services`; typed persistence in `libs/repository`; equivalent core and external controllers call the same use case; exposure policy stays in transport mappers/DTOs; domain types are transport-neutral with no `external`-versus-`core` branching; every added file is kebab-case with conventional role suffixes. Rubric §7 lists the full flag set. Blocking findings include: new app-local business or repository code, an unrewired equivalent core caller, an external-shaped partial domain model, or a future core replacement that still needs business or data work.

Independently trace every scoped `B-###`/`V-###` rule through its `M-###` row into shared code, adapters, and tests. If adding a core route would need more than authentication, DTO/mapping, and wiring, the readiness claim fails.

Verify pattern conformity against the repository, not the packet's word: each `P-###` row's exemplar must be a recent intentional port, the named primitive must actually cover the concern (cache keys, TTL units, and serialization — not just method signatures), and the implementation must match its `ADOPTED` decision. A new wrapper, adapter, parser, pipe, interface, or factory with an unproven `P-###` justification is a finding.

Then reverse-trace: flag any branch, default, or mutation in new domain code with no corresponding ledger rule or recorded decision — unmapped logic is invented behavior. Verify any optimization carries an equivalence note covering ordering, rounding, projection, and null handling, and that the drift watchlist names every legacy route keeping a live duplicated implementation as a directly callable `<apps/api | core-api> METHOD /full/path` entry — prose descriptions the testing workflow cannot call verbatim are a finding.

## 7. Audit tests and documentation

Map reviewer rules to tests using rubric §8. Reject construction-only, handler-existence, broad-snapshot, mock-choreography, and happy-path-only tests as parity evidence; require behavior-focused tests at the correct seams, real Mongo where persistence matters, and faked external infrastructure. Verify generated docs against runtime. Typecheck, lint, build, and coverage are supporting signals, not behavior certification.

## 8. Report findings

Order by severity and confidence:

```text
[P1] <concise violated promise> — <target file:line>

Scenario: <concrete request/state/actor>
Expected: <source-backed behavior or public contract, with evidence>
Actual: <what target does, with evidence>
Impact: <consumer, data, security, compatibility, or operability consequence>
Remediation: <smallest sound direction; do not patch>
Missing test: <observable test that would catch it>
```

- `P0` — exploitable security/privacy, cross-tenant access, irreversible corruption, or catastrophic side effects.
- `P1` — broken business parity, auth/ownership, public compatibility, data integrity, required shared-layer reuse, or commonly unusable contract behavior.
- `P2` — important edge cases, misleading docs/examples, response exposure, maintainability, or material test gaps.
- `P3` — low-risk clarity or consistency issues worth fixing.

Do not flood the report with style nits while behavioral or contract risks remain. Label hypotheses as such and name the missing evidence.

## 9. Certify

Conclude with exactly one:

- `APPROVED` — no blocking findings; behavior, contract, enforcement, exposure, core-replacement readiness, docs, runtime, and tests are adequately evidenced.
- `CHANGES REQUIRED` — one or more valid findings block approval.
- `BLOCKED BY DECISION` — source-backed behaviors conflict and a product decision is required.
- `NOT CERTIFIED` — required source/runtime/test evidence was unavailable.

List the source pins, checks actually run, core-migration readiness result, unverified areas, and residual risks. Never convert a partial static review into a parity certification.

---
name: reduce-contract-drift
description: Identify, measure, prevent, and reduce contract drift across CLIs, HTTP APIs, SDKs, generated clients, proxies, database schemas, event payloads, docs, tests, and Rust workspace crates. Use when Codex needs to trace mismatches between declared and actual behavior, find stale flags or payload shapes, map a source-of-truth seam, compare code against specs/examples/callers, design greenfield anti-drift boundaries for new projects, choose framework patterns for Express or Hono APIs, or add validation and CI guardrails so contracts are defined once and consumed consistently.
---

# Reduce Contract Drift

## Goal

Make caller-facing and cross-module contracts converge on one authority and stay synchronized as the codebase changes.

Use the same skill for new projects by designing the authority chain up front instead of waiting for drift to accumulate.

## Quick Start

1. Start from the exact seam the user named: command, flag, route, payload, DTO, schema, event, crate, or generated client.
2. Identify the contract authority before proposing fixes. Do not treat stale docs, wrappers, or generated artifacts as the source of truth unless the repo clearly does.
3. Build a contract matrix:
   - authority
   - dependents
   - current evidence
   - concrete drift symptoms
4. Compare implementation, declarations, tests, generated outputs, examples, and live behavior where available.
5. Classify the drift precisely:
   - shape drift
   - naming drift
   - behavioral drift
   - default-value drift
   - validation drift
   - version drift
   - ownership drift
6. Fix the authority first, then regenerate or align downstream surfaces.
7. Add a guardrail so the same drift cannot silently reappear.

## Core Rules

- Prefer the narrowest real public seam over broad architecture talk.
- Distinguish contract authority from projections of that authority.
- Favor single-definition contracts over duplicated structs, enums, flags, docs, or examples.
- For greenfield work, decide where contracts live before adding routers, proxies, SDK wrappers, or parallel DTO families.
- If two surfaces intentionally differ, document that translation boundary explicitly instead of calling it drift.
- Separate current behavior from desired behavior. Audit the truth before redesigning it.
- When asked to fix drift, ship both the alignment change and the anti-drift guardrail when feasible.

## Greenfield Mode

When the request is about a new project, new service, or framework choice, do not start by scattering types across handlers, proxies, clients, and docs. Start by designing:

1. the authority
2. the derived surfaces
3. the explicit translation boundaries
4. the validation seam
5. the CI proof that the contract stayed aligned

Default greenfield sequence:

1. choose the public seam
2. choose the authority artifact
3. define validation at ingress
4. derive or centralize downstream shapes
5. make proxy behavior explicit
6. add seam-level tests before adding wrappers

## Investigation Workflow

1. Pin the contract surface.
   - Ask: who calls this, who implements it, and who documents it?
   - Reduce the task to one contract family before widening scope.

2. Find the likely authority.
   - In many repos this is one of:
     - implementation plus tests
     - shared type definitions
     - schema or migration files
     - generated spec inputs
     - protocol definitions
     - CLI parser definitions
   - If multiple authorities seem to exist, treat that duplication itself as drift.

3. Gather evidence from both sides.
   - Read the implementation seam.
   - Read the declared contract seam.
   - Read a few meaningful call sites.
   - Read tests and examples that claim to define expected behavior.
   - Verify runtime behavior when drift could be behavioral rather than structural.

4. Write the contract matrix.
   - Contract: what callers think exists
   - Authority: where it should be defined
   - Observed behavior: what runtime or implementation actually does
   - Dependents: SDKs, docs, tests, other crates, generated files, configs
   - Drift class: exact mismatch
   - Fix direction: update authority, update dependents, or split an intentional translation boundary

5. Choose the fix order.
   - Fix the highest-authority artifact first.
   - Regenerate or re-derive dependents where possible.
   - Delete duplicated intermediate shapes when they only mirror another contract.
   - Add tests, snapshots, schema checks, or compile-time checks last.

## Default Deliverable

When the user asks for an audit, produce:

- the contract seam
- the authority
- the current drift
- the evidence
- the fix plan
- the guardrail that would keep it aligned

When the user asks for a fix, implement:

- the authority-side change
- downstream alignment
- at least one durable validation seam

## Rust Bias

In Rust codebases, prefer contract ownership that flows downward through focused crates instead of being recopied across runtime, transport, CLI, and SDK layers. Shared contracts should usually live in a lower crate that higher crates depend on, not the reverse.

Read [references/rust-crate-patterns.md](references/rust-crate-patterns.md) when the drift touches:

- `crates/*` boundaries
- repeated DTOs or enums across crates
- CLI parsing versus runtime config
- serialization or schema generation
- feature crates versus runtime shell crates

## API Frameworks And Proxies

Read [references/api-framework-patterns.md](references/api-framework-patterns.md) when the work involves:

- Express APIs
- Hono APIs
- reverse proxies or forwarded headers
- typed validation at request ingress
- route composition and versioning
- OpenAPI or RPC/client generation
- preventing wrapper and proxy drift in new services

## Reference Map

Read [references/contract-drift-playbook.md](references/contract-drift-playbook.md) for the full audit and reduction workflow, drift taxonomy, and fix ordering.

Read [references/surface-checklists.md](references/surface-checklists.md) for surface-specific checks across CLIs, HTTP APIs, SDKs, databases, events, docs, and tests.

Read [references/rust-crate-patterns.md](references/rust-crate-patterns.md) for Rust workspace and crate-boundary patterns that reduce drift by design.

Read [references/api-framework-patterns.md](references/api-framework-patterns.md) for anti-drift design patterns in Express and Hono, including validation, route composition, type export, middleware boundaries, and proxy-aware behavior.

Read [references/ci-guardrails.md](references/ci-guardrails.md) for concrete validation patterns, generation rules, and CI gates that keep contracts synchronized over time.

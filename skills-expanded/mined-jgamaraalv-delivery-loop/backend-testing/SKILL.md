---
name: backend-testing
description: Turn backend test ambiguity into one practical test packet — API/service/repo/auth coverage, fixture & seed/reset strategy, mock-vs-container choices, contract checks, and flaky-suite stabilization across local and CI.
---

# Backend Testing

## Instructions

### Step 1: Classify the request into one packet

Choose the single best entry packet before giving advice.

**Packets**

- `coverage-plan` — which layers to add for a concrete backend change
- `fixture-and-reset-plan` — how to seed, isolate, reset, or bootstrap data/auth state
- `contract-and-api-checks` — how to protect response/event/schema compatibility once the interface already exists
- `flake-stabilization` — how to stabilize CI-only or intermittent backend failures
- `execution-lane-split` — how to divide local-fast, PR, nightly, and release-only backend checks

If the request mixes several concerns, name the **primary packet** and one secondary concern.

### Step 2: Frame the backend surface and risk

Capture the smallest useful context:

- surface: endpoint, service, repository, worker, queue consumer, auth flow, integration, or migration
- highest-risk behaviors: validation, permissions, persistence, retries, idempotency, ordering, serialization, side effects, compatibility
- existing coverage already present
- external dependencies involved: DB, cache, queue, email, payment, third-party API, identity provider, filesystem
- runtime/language stack
- where the evidence must hold: local loop, PR CI, scheduled CI, release smoke

If the request is vague, choose the smallest regression slice worth protecting first.

### Step 3: Choose the right test layers

Use the packet and risk to select the lightest credible layer mix.

#### Unit / service

Prefer when the main risk is branching logic, validation, orchestration, or pure-ish business rules.

#### Integration

Prefer when database behavior, framework wiring, middleware, transactions, queues, caches, or serialization matter.

#### Contract / API

Prefer when clients depend on response shapes, status codes, schemas, or events and the interface already exists.

#### Smoke / selective end-to-end

Prefer only when a narrow release-critical journey crosses several backend boundaries and lower layers would miss the core risk.

State what is **in scope**, what is **out of scope**, and why.

### Step 4: Decide dependency realism on purpose

For each dependency, choose one of:

- **mock / stub** — expensive, unstable, or irrelevant to the behavior under test
- **fake / simulator** — behavior matters, but a lightweight substitute is enough
- **containerized real dependency** — queries, migrations, message semantics, or wire behavior matter enough that drift would hurt
- **shared external environment** — only when unavoidable; call out the fragility cost explicitly

Good defaults:

- prefer real DB behavior when repository, migration, transaction, or serialization behavior is central
- prefer mocks for outbound third-party APIs unless the integration contract itself is under test
- prefer a narrow containerized slice over a giant all-dependencies-in-PR setup
- do not claim fake and real dependencies are equivalent when production parity is the whole risk

### Step 5: Define fixture, data, auth, and environment control

A backend suite becomes untrustworthy when state is vague.

Specify:

- fixture/factory strategy
- seed/reset/rollback plan
- auth/bootstrap helpers for users, roles, tenants, tokens, or sessions
- time/randomness/idempotency control where needed
- isolation rule: per test, per file, per suite, or per environment
- debugging signals to capture when failures happen

If the suite relies on ordering, leftovers, or sleeps, call that fragility out directly.

### Step 6: Split the execution lanes

Treat local, PR, and slower lanes as different jobs.

Define:

- **local-fast path** — what developers should run repeatedly
- **PR path** — what must gate merges
- **scheduled / nightly path** — heavier breadth or expensive realism
- **release / incident path** — narrow confidence checks or regression ratchets when needed

If the suite is slow, split it. Do not pretend one giant authoritative path is practical everywhere.

### Step 7: Produce one backend test packet

Return one concise packet, not a general essay.

Recommended packet shapes:

- `coverage-plan` → coverage table + dependency strategy + exclusions
- `fixture-and-reset-plan` → fixture/reset memo + auth/bootstrap notes
- `contract-and-api-checks` → compatibility packet + consumer/provider scope + route-outs
- `flake-stabilization` → flake memo with likely causes, isolation fixes, readiness checks, and debug signals
- `execution-lane-split` → lane matrix with local/PR/scheduled/release responsibilities

Minimum packet contents:

- change surface and primary risk
- chosen packet and any secondary concern
- selected layers and why
- dependency realism decisions
- fixture/data/auth/environment control
- execution-lane split
- explicit route-outs when the request is partly owned elsewhere

### Step 8: Verify scope boundaries before finalizing

Check:

- does the packet protect the real backend regression risk rather than generic coverage vanity?
- did you keep org-wide validation policy in `testing-strategies`?
- did you route contract _shape_ decisions to `api-design` while keeping contract _protection_ here only when the interface already exists?
- did you route auth implementation work to `authentication-setup`?
- will a maintainer understand why a dependency is mocked, faked, containerized, or real?

## Output format

```markdown
## Backend Test Packet: [Surface or Change]

### Packet choice

- Primary packet: coverage-plan | fixture-and-reset-plan | contract-and-api-checks | flake-stabilization | execution-lane-split
- Secondary concern: optional
- Confidence: high | medium | low

### Change framing

- Surface: ...
- Main risks: ...
- Runtime: ...
- Existing coverage: ...

### Layer decisions

| Layer                 | In scope? | What it protects | Notes |
| --------------------- | --------- | ---------------- | ----- |
| Unit / service        | yes/no    | ...              | ...   |
| Integration           | yes/no    | ...              | ...   |
| Contract / API        | yes/no    | ...              | ...   |
| Smoke / selective E2E | yes/no    | ...              | ...   |

### Dependency realism

| Dependency               | Strategy | Why |
| ------------------------ | -------- | --- |
| Database / queue / cache | ...      | ... |
| External API             | ...      | ... |
| Auth provider            | ...      | ... |

### Data and environment control

- Fixtures / factories: ...
- Seed / reset: ...
- Auth bootstrap: ...
- Isolation rule: ...
- Debug signals: ...

### Execution lanes

- Local-fast: ...
- PR CI: ...
- Scheduled / nightly: ...
- Release / incident: ...

### Route-outs

- `testing-strategies`: ...
- `api-design`: ...
- `authentication-setup`: ...
```

## Examples

### Example 1: auth-heavy API change

**Input:** “We added refresh-token rotation and new admin-only endpoints to our Express API. I need backend tests that catch auth failures, token replay issues, and DB persistence bugs without turning CI into a giant end-to-end suite.”

**Good response shape:**

- chooses `coverage-plan` as the primary packet
- combines unit/service plus integration/API coverage instead of one giant E2E suite
- keeps real DB or containerized persistence where token/session behavior matters
- defines auth bootstrap helpers and reset strategy
- limits smoke coverage to a narrow release-critical path

### Example 2: CI-only flake in a service suite

**Input:** “Our FastAPI tests pass locally but fail in CI around seeded Postgres state and background jobs. Give me a stabilization plan.”

**Good response shape:**

- chooses `flake-stabilization` as the primary packet
- identifies seed/reset drift, readiness, async timing, or leftover state as likely causes
- recommends stronger isolation, readiness checks, and debugging signals instead of just retries
- separates local-fast and CI-authoritative behavior clearly

### Example 3: contract protection after an API already exists

**Input:** “Our payment service and webhook consumers keep drifting on response fields. I do not need API redesign, I need backend tests that catch compatibility regressions.”

**Good response shape:**

- chooses `contract-and-api-checks` as the primary packet
- keeps contract protection here because the interface already exists
- routes any schema redesign or versioning debate to `api-design`
- recommends consumer/provider or schema-compatibility coverage rather than broader smoke inflation

### Example 4: too-broad policy request

**Input:** “Design our overall engineering org testing strategy for frontend, backend, mobile, and QA.”

**Good response shape:**

- recognizes that the primary task belongs to `testing-strategies`
- keeps any backend-specific advice scoped as a handoff only
- refuses to turn `backend-testing` into a universal QA-governance skill

---
name: qa-scenarios
description: 구현된 기능·브랜치·API·화면에서 위험 기반 시나리오와 엣지 케이스를 발굴해 UI·API·DB·로그 증거로 실측 검증한다. PRD나 체크리스트가 없어도 동작. QA, 시나리오 검증, 엣지 케이스 발굴, 릴리즈 판정(GO/NO-GO) 시 사용.
---

# QA Scenarios

Test the feature as users may actually use it, including paths the implementer did not anticipate. Derive behavior from the implementation and running system first; use PRDs or acceptance criteria as additional oracles when available.

Never mark a scenario PASS without observable evidence.

## References index

| File | When to read |
|---|---|
| [references/scenario-catalog.md](references/scenario-catalog.md) | §3 — scenario family selection |
| [references/report-template.md](references/report-template.md) | §6 — report skeleton |

## Operating contract

- Treat the target feature, implementation diff, running UI/API, and persisted effects as primary inputs.
- Accept PRDs, tickets, designs, and existing tests as optional context. Do not limit coverage to their stated cases.
- Work only in environments and accounts the user has authorized. Prefer local, test, or staging environments.
- Do not perform destructive, irreversible, billable, privacy-sensitive, or production actions without explicit authorization.
- Preserve credentials and personal data. Do not record secrets in commands, screenshots, reports, or tracked files.
- Use existing project boot, browser, database, logging, and E2E workflows when available.
- Distinguish facts observed in the system from inferred expectations and product questions.
- Continue through independent scenarios when one scenario is blocked. Stop only when the blocker prevents meaningful remaining work.

## Workflow

### 1. Fix the test boundary

Identify, from local context where possible: feature entry points (screens, routes, endpoints, jobs, events, commands); changed components and downstream side effects; available environment, account/role, test data, and observability surfaces; actions that need user approval; relevant regressions outside the changed component.

Ask the user only for access, authorization, or a choice that cannot be safely inferred and materially changes the QA. Do not require a PRD.

Record the environment, revision/branch, account role, device/client, and test time so results are reproducible.

If only source code or a diff is available, still produce the behavior map, risk-based scenario ledger, and evidence plan. Run safe static or automated checks that are available, but mark scenarios requiring a live system `NOT RUN`; do not present scenario design as executed QA.

### 2. Build a behavior and evidence map

Inspect the implementation before generating the final scenarios: diff and call paths; UI controls, validation, routing, visible states; API contracts, status codes, retries, error handling; schemas, state transitions, transactions, caches, queues, scheduled jobs, notifications, analytics; feature flags, roles, ownership rules, locale/time behavior, compatibility boundaries; existing tests for known invariants and untested branches.

**Blast radius sweep (mandatory — never scope QA to the diff alone).** A change is only the origin; the risk lives in everything that consumes or shares the changed behavior. Trace outward by evidence, not intuition:

- **Consumers of the changed contract.** For a changed API/endpoint/DTO/event, grep its callers across *every* module and repo, not just the one that was edited. A backend change ripples to every frontend that calls it; a shared-schema change ripples to every reader.
- **Sibling actors on the same domain object.** If a flow has multiple participant sides, verify all of them. Example: in a marketplace, an order-flow change is not a buyer concern only — the same order is created/read by the **buyer app**, acted on by the **seller dashboard**, surfaced in the **admin console**, may drive **realtime notifications**, and may be swept by **scheduled jobs** (reminders, status transitions). Each side is a separate scenario surface.
- **Shared infra crossed by the flow.** Name the concrete mechanism, not "notifications" in the abstract: push delivery (trigger, payload, deep-link entry), cache (invalidation, TTL, lock contention), queues, scheduled jobs, analytics — anything the changed path touches that other features also depend on. A cache/push side effect that other features share is a regression surface even when the UI looks unchanged.

Produce an explicit impact surface list (module/repo → why it's in scope → one regression scenario) before writing the scenario ledger. An in-scope surface with zero scenarios is a coverage gap, not an omission.

Create a compact map:

```text
entry -> user action -> request/event -> state transition -> side effect -> user-visible result
```

For each transition, name at least one evidence hook: DOM text, network payload, API response, log event, database row, queue message, notification stub, analytics event, or follow-up read API.

When no specification exists, derive an oracle from code-level invariants, labels/API semantics, surrounding product behavior, and safe user expectations. Mark it `INFERRED`; do not silently present it as confirmed intent.

### 3. Generate risk-based user scenarios

Read [scenario-catalog.md](references/scenario-catalog.md) and select applicable families. Generate scenarios from the feature's behavior map, not from a generic checklist alone.

Always consider: intended happy path; alternate entry/order/navigation; empty, boundary, malformed, stale, and large inputs; repeat, rapid repeat, retry, refresh, back navigation, resume; roles, ownership, session expiry, forbidden access; dependency failure, timeout, partial success, recovery; concurrent actors or state changes when shared state exists; persisted side effects and regressions at integration boundaries.

When a PRD, design, or acceptance criteria exists, also **map each stated DoD / acceptance item to at least one scenario**; a DoD item left with no scenario is a coverage gap to report explicitly, not a silent omission.

Prioritize by impact, likelihood, change proximity, and detectability. Prefer a smaller set of distinct state transitions over many cosmetic variations of the same path. Use pairwise combinations for interacting dimensions; reserve full combinations for high-risk behavior.

Before execution, form a scenario ledger:

| ID | Persona / context | Scenario and risk | Preconditions | Actions | Expected observable outcome | Evidence hooks | Priority |
|---|---|---|---|---|---|---|---|

Expectations must be testable. Replace vague phrases such as "works correctly" with concrete UI, response, state, and side-effect outcomes.

### 4. Execute each scenario as a measured experiment

For every executable scenario:

1. Establish or capture the precondition. If the required state is missing — no unopened record, no seeded row, no test account — **create it** (seed the data, send the event, register the account) rather than skipping the scenario. Reserve BLOCKED for state you genuinely cannot create.
2. Snapshot relevant state before the action.
3. Perform the user action through the real entry point when feasible.
4. Capture the immediate UI/API/network result.
5. Observe the relevant log, database, queue, cache, job, notification, analytics, or follow-up read state.
6. Compare every observation with the expected outcome.
7. Capture cleanup or rollback state when test data was created.

Use the narrowest evidence that proves the claim, but validate across layers for state-changing flows. A `2xx`, toast, screenshot, or absence of an exception proves only that observation; it does not prove persistence or downstream delivery.

**Evidence rigor ladder.** For each assertion, attempt the strongest evidence type available for that claim before settling for a weaker one; weaker tiers are allowed, not banned — but a report whose PASSes rest mostly on tier ④ is itself a risk signal:

| Tier | Evidence | Example |
|---|---|---|
| ⓪ strongest for state claims | persisted/downstream state read directly | DB row, log/event store query, follow-up read API |
| ① strongest for UI claims | deterministic eval returning structured data | axe violation count, form field value, element count, console error array |
| ② | accessibility-tree element match | `button "저장"` exists/absent in snapshot |
| ③ | before/after snapshot comparison | dialog appeared, text changed after the action |
| ④ weakest | screenshot + visual judgment | color, spacing, layout — **visual-only properties, always naming what is being evaluated** |

**Deterministic page checks** on each screen the change created or modified: accessibility violations; console and page errors; failed resources and broken images; form labels; viewport/overflow at representative mobile and desktop widths. New violations are FAIL candidates; pre-existing ones are baseline observations.

Prefer real dependencies in an authorized test environment. Mocks and stubs are valid for isolated behavior, but label their results `MOCKED` and do not claim end-to-end integration coverage.

For asynchronous behavior, wait on a bounded observable condition rather than a blind sleep. Record the observation window. A result still pending at the deadline is not PASS.

When a scenario fails, reproduce once if safe, minimize the reproduction, and gather diagnostic evidence. Do not modify product code unless the user also asked for a fix.

### 5. Assign evidence-bound verdicts

Use exactly these execution verdicts:

- `PASS`: every material expected outcome has direct evidence.
- `FAIL`: an observed outcome contradicts the expected outcome.
- `BLOCKED`: a material assertion could not be completed because of access, environment, or dependency limits you **cannot create or safely reproduce**. Missing test data you *could* seed is not BLOCKED — create it first (§4.1).
- `NOT RUN`: intentionally deferred or outside the agreed boundary.

Add qualifiers when relevant: `MOCKED`, `FLAKY`, or `INFERRED ORACLE`.

Rules:

- Missing evidence cannot become PASS.
- Do not convert a product ambiguity into FAIL. Report it as an open oracle question.
- Do not convert an environment failure into a product FAIL without evidence tying it to the feature.
- If one assertion in a material scenario fails, the scenario is FAIL even when other assertions pass.
- Track flaky observations explicitly; a later pass does not erase an earlier unexplained failure.
- Dependency-outage / fail-open scenarios that a shared live env cannot safely reproduce are `NOT RUN` on that env, with a pointer to the automated test that covers the behavior — confirm that test exists before proposing to add one; never inject failure into shared infrastructure.

### 6. Report and hand off

Use [report-template.md](references/report-template.md). Include: tested scope and runtime identity; behavior/evidence map; scenario inventory including unexecuted cases; one row per execution with verdict and evidence; defects with minimal reproduction, expected/actual, severity, diagnostic evidence; blocked checks, mocked boundaries, inferred oracles, remaining risk; test data cleanup status.

Link evidence to stable artifacts or include exact read-only commands/queries with sensitive values redacted.

Write the report for a **first-time reader**: spell out what each check verified as a plain-language question — no internal scenario codes, raw record ids, or unglossed jargon. Prefer user-visible behavior over internal signals, and lead with one line on what the change did + what to focus on.

Finish with a short release recommendation:

- `GO`: no material failures or evidence gaps for the agreed risk boundary;
- `CONDITIONAL GO`: only accepted, bounded risks remain;
- `NO-GO`: a material failure, unexplained flake, or critical verification gap remains.

Do not issue `GO` when essential state-changing behavior was verified only at the UI layer.

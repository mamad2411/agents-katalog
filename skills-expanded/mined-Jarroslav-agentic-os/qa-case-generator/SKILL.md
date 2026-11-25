---
name: qa-case-generator
version: 0.1.0
license: Apache-2.0
author: agentic-os
description: >-
  Turn one work-item id into reviewed, backend-synced functional test cases.
  Invoke when the user says "generate test cases for PROJ-123", "write test
  cases from this ticket", "qa cases for <ticket>", or hands you a single Jira /
  Azure DevOps / GitHub / GitLab work-item id and wants manual or API-level
  functional cases. Produces case documents under docs/superpowers/qa-tasks/,
  gates them behind a human review, and optionally pushes to a test-management
  adapter. Not for: unit/integration tests, code-coverage, e2e automation
  (qa-e2e-generator), or auto-invocation by other pipeline skills.
allowed-tools: Read, Write, Bash, AskUserQuestion, TaskCreate, TaskUpdate
---

# qa-case-generator

## Shared contract preflight

Before workflow actions, send this JSON request to the installed plugin's
`runtime/run.py` using Python 3.10+ (resolve the plugin root on the current host):

```json
{"api_version":"1.0.0","operation":"policy.resolve","entrypoint":"qa-case-generator"}
```

Use the returned policy and `references/runtime-contracts.md` for contract identifiers,
limits and dependency floors. Unknown fields or incompatible versions block startup.
Task envelopes use `contract_version: "1.0.0"` and `task_input`; legacy `raw_input`
is accepted only by the explicit `input.normalize` compatibility adapter with `legacy: true`.
This preflight validates policy; durable lifecycle and host enforcement are separate
capabilities. Never infer those capabilities from a successful policy response.

For a managed run, follow [`references/runtime-authority.md`](../../references/runtime-authority.md):
record QA decisions and verification evidence through runtime operations and use
`legacy.export` for compatibility ledgers. Direct JSONL appends never advance a run.


Convert a single work-item's acceptance criteria into functional test-case
documents (manual and API level), gated by an explicit human approval, with an
optional push to a config-driven test-management backend.

> The pipeline is deterministic on purpose. A fixed phase order, hard halt
> conditions, and a formulaic coverage count keep separate agent runs on the
> same ticket producing the same shape of output. Do not improvise around the
> gates — they are the contract.

> **Methodology owner.** How functional cases are derived and shaped is defined by the `test-cases`
> blueprint in `agentic-qe`
> (`skills/qe-blueprints/references/catalog/design/test-cases.md`). This skill
> executes; the blueprint is the authority on method. If the two ever disagree,
> the blueprint wins and this file is what gets corrected — one source of truth,
> so two agents cannot follow two different sets of practices.

## When to use

- You have one work-item id (`PROJ-123` format) from Jira, Azure DevOps, GitHub,
  or GitLab and need functional test cases.
- Invocation form: `qa-case-generator PROJ-123`.
- A QA engineer needs manual or API case documents they can review and file.

Do **not** use this skill for unit or integration tests (TDD workflow),
code-coverage analysis (`code-review`), automation-framework setup, test
execution, or result analysis. Never derive tests by reading source code.

## Hard constraints

Blast radius: R0 → R1 (run-artifact writes) through phase 5; R3 (external
side-effect) only in phase 6, always behind the human review gate.

| Rule | Enforcement |
| --- | --- |
| Never read source code | No Read/Grep/Glob on repository code files |
| Functional tests only | No unit/integration/coverage output |
| Not auto-invoked | Other pipeline skills must not call this skill |
| Sync needs consent | Phase 6 runs only after explicit user yes |
| QA docs required | Halt to `qa-baseline` if guides absent |
| Clear criteria required | Halt below 50% AC confidence |

## Inputs

| Input | Source | Missing → |
| --- | --- | --- |
| Work-item id | CLI arg (`PROJ-123`) | Halt with usage error |
| QA strategy | `.agentic/guides/testing/qa-strategy.md` | Halt → `qa-baseline` |
| QA health | `.agentic/guides/testing/qa-health.md` | Halt → `qa-baseline` |
| Ticket backend adapter | Adapter config validated in phase 1 | Halt → `qa-baseline` |
| Test-management adapter | Adapter config (phase 1) | Halt → `qa-baseline` |

> Adapters are config-driven, not hardcoded. The ticket backend and the
> test-management sync target are both read from adapter config validated in
> phase 1. Do not assume any specific ticket or test system.

## Outputs

Written under `docs/superpowers/qa-tasks/<date>-<slug>/manual/`
(equivalently `docs/superpowers/qa-tasks/{date}-{slug}/manual/`):

| Path | Contents |
| --- | --- |
| `.../manual/test_cases.md` | Generated functional cases |
| `.../manual/meta.json` | Run metadata (prior-run detection) |
| `.../manual/ticket-analysis.md` | Fetched ticket summary + AC scoring |
| `.../manual/events.jsonl` | Audit event appended after each phase |

Test case ids are ticket-scoped: `{TICKET_ID}_TC_001`, `{TICKET_ID}_TC_002`, …

## Pipeline

Phases 0–6. Read the pipeline-overview reference first, then read the specific
phase reference immediately before running that phase. Use the templates
reference during generation.

| # | Role | Halt trigger |
| --- | --- | --- |
| 0 | Pre-flight regeneration check | none |
| 1 | Environment validation | missing QA docs or adapter |
| 2 | AC quality check | confidence < 50% |
| 3 | Full context fetch | none (warn on partial) |
| 4 | Test generation | none |
| 5 | User review gate | user cancels |
| 6 | Adapter sync | none (mark failed) |

For an unmanaged legacy run, append one audit event to `events.jsonl` after each
phase completes. For a managed SQLite run, record the phase decision/evidence
through runtime operations and refresh the compatibility view with
`legacy.export`; direct JSONL appends are forbidden.

### 0 — Pre-flight

Detect a prior run via the metadata file (`meta.json`). If earlier artifacts
exist, back them up before regenerating. Never halts.

### 1 — Environment validation

Confirm `.agentic/guides/testing/qa-strategy.md`, `qa-health.md`, and the
adapter config all exist. If QA docs or the adapter are absent, **halt** and
direct the user to the `qa-baseline` skill.

### 2 — AC quality check

Cheap ticket fetch. Score acceptance-criteria quality. If confidence is below
50%, **halt** and ask the user to clarify the criteria.

### 3 — Full context fetch

Full ticket fetch: comments, subtasks, links, attachments. On partial data,
**warn** and continue — never halts.

### 4 — Test generation

Apply the coverage formula (below). Route each case by type. Never halts.

### 5 — User review gate

Present the case document to the user. On cancel, **halt** — no sync, no
further writes.

### 6 — Adapter sync (optional, R3)

Only after explicit consent captured in phase 5. Push cases through the
test-management adapter. On failure, record the sync as **failed** and continue
— never halts.

## Coverage formula

Functional, verbatim:

```
base = 3 × AC_count
risk_adjusted = base × risk_multiplier
complexity_adjusted = risk_adjusted × complexity_multiplier
final = complexity_adjusted × simplicity_multiplier
final = clamp(final, min=3, max=25)
```

Baseline target is 8–12 cases, risk-adjusted from there.

**Risk multipliers**

| Trigger keywords | Multiplier |
| --- | --- |
| auth / payment / security | +50% |
| migration / data-loss | +40% |
| admin / delete / production | +30% |

**Simplicity reducers**

| Condition | Multiplier |
| --- | --- |
| single acceptance criterion | 0.8× |
| text or label change | 0.6× |
| logging / monitoring change | 0.7× |
| ticket with zero comments | 0.9× |

**Priority split of generated cases**

| Priority | Share | Focus |
| --- | --- | --- |
| P1 | 33% | critical path |
| P2 | 42% | edge cases |
| P3 | 25% | negative scenarios |

## Test-type routing

| Case type | Use for |
| --- | --- |
| Manual | UI workflows, visual checks, multi-screen flows |
| API | endpoints with request/response specs |

## References

Read the pipeline overview, then the phase file for the phase you are running,
then the templates file during generation.

### Shared (qa-authoring)

Cross-skill authoring gates at `../../references/qa-authoring/`:

| File | Use |
| --- | --- |
| `intake-gate.md` | Validate the work-item id and intake before phase 0 |
| `ac-quality-gate.md` | Score acceptance-criteria confidence (phase 2) |
| `context-assembly.md` | Assemble ticket context for scoring and generation |

### Own (`references/`)

| File | Stage | Use |
| --- | --- | --- |
| `suite-planning.md` | plan | Decide case types, coverage, and depth for the ticket |
| `case-authoring.md` | write | Write cases on the output templates (field table included) |
| `review-gate.md` | review | Human approval before anything syncs |
| `case-sync.md` | sync | Write approved cases to the adapter-configured backend |

The intake and AC-quality gates come first from the shared set above; then these
four own guides carry the ticket from a planned suite through authored cases, a
review gate, and sync. Validation fixtures for the coverage formula and gates
live under `evals/fixtures/*.json`.

## Anti-shortcut rules

Do not rationalize past the gates. Each temptation maps to the rule it breaks;
several are corroborated by recorded baseline agent runs where the failure
actually occurred.

| Shortcut | Corrective rule |
| --- | --- |
| "Docs probably exist, just generate" | Phase 1 halts on absent QA docs — direct to `qa-baseline` |
| "I'll pick an intuitive multiplier" | Use the coverage formula and the listed multipliers exactly |
| "I'll save cases wherever is handy" | Write only to `docs/superpowers/qa-tasks/<date>-<slug>/manual/` |
| "The user clearly wants it synced" | Phase 6 requires explicit consent captured in phase 5 |
| "Criteria are close enough" | Phase 2 halts below 50% confidence — ask to clarify |
| "I'll skim the code to derive tests" | Never read source; functional cases from AC only |

Grounding: generate only from ticket inputs and QA docs. Never invent
acceptance criteria, endpoints, or behavior that the fetched inputs do not
state.

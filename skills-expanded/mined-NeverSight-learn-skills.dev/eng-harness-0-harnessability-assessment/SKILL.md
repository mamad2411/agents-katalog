---
name: eng-harness-0-harnessability-assessment
description: Assess a Git repository's harnessability — how easily a human or agent can enter, operate, modify, observe, prove, and improve it through an engineering harness. Produces evidence-first Markdown and JSON reports scoring Operate-Today and Adaptability, mapping back-pressure surfaces, proof ceilings, external-dependency exposure, scenario probes, and highest-leverage harness/product-code affordances.
---
# eng-harness-0-harnessability-assessment

Assess how easy a repository is for a human or agent to **enter, operate, modify, observe, prove, and improve** through an engineering harness.

Cold-start onboarding difficulty is one part of harnessability, not the whole assessment.

The agent harness drives. The engineering harness proves.

## Core idea

Harnessability is the degree to which a codebase can be worked through a project-side engineering harness by a fresh human or agent.

A harnessable repo lets an agent move through this loop:

```text
cold start -> boot/setup -> scoped change -> supported interaction -> observable consequence -> deterministic verdict -> clean rerun -> encoded improvement
```

The important object is **back pressure**: deterministic feedback that pushes reality back into the agent's loop. Back pressure can come from many surfaces:

- build, compile, typecheck, lint, unit test, schema, security, dependency, or architecture checks;
- boot, health, smoke, E2E, API, UI, CLI, worker, queue, event, MCP, or system interactions;
- observable consequences such as state, files, database rows, messages, events, cache entries, search indexes, generated artifacts, rendered UI, screenshots, logs, traces, metrics, or structured diagnostics;
- external-effect sinks for email, SMS, payments, webhooks, object storage, third-party APIs, analytics, notifications, or background jobs;
- production/customer evidence such as telemetry, SLOs, incident-free release, usage outcomes, or human acceptance supported by captured evidence.

Do **not** overfit harnessability to databases. A database migration/seed/reset loop is only one easy-to-understand example of the broader **change-to-evidence loop**.

A **Backpressure Check** is advisory. It surveys whether enough deterministic sensors exist for the scoped work. It is not itself proof. Proof comes from the sensors, commands, evidence artifacts, and observed consequences.

## Read the tests as harness reconnaissance

The test suite is the strongest evidence of how a codebase already solves the hard harness problems. Whatever the tests do to make behavior real is a proven, in-repo mechanism the engineering harness can reuse instead of inventing.

When inspecting tests, ask:

- How do they isolate dependencies — mocks, fakes, stubs, in-memory implementations, contract tests?
- How do they inject or substitute behavior — dependency injection, ports/adapters, provider overrides, test-only configuration?
- How do they handle datastores and state — seed, snapshot, restore, reset, factories, fixtures, Testcontainers, ephemeral schemas?
- How do they make behavior real — spin up real or containerized services, exercise true interactions, and assert observable consequences?
- How do they stay deterministic — fixed clocks, IDs, ports, ordered teardown, idempotent setup?

Every mechanism the tests already use is a candidate harness affordance. An existing integration or E2E suite that provisions a real or containerized datastore, seeds it, exercises behavior, verifies the consequence, and tears down is itself a reusable change-to-evidence surface — often the cheapest existing path to L4 proof, because the harness can wrap it rather than build new scaffolding. Treat "expose what the tests already do as a supported harness command" as a first-class, high-leverage remediation.

## When to use

Use this skill when the user asks to:

- onboard a repo;
- assess repo onboarding difficulty;
- compare repositories for agent readiness;
- inspect whether an agent can get a repo running;
- determine how much remote infrastructure, secrets, services, or env setup blocks local operation;
- assess whether changes can be made and proven locally or safely;
- evaluate engineering harness quality;
- identify missing back-pressure surfaces;
- decide what harness or product-code affordances would make future agent work safer, faster, or more deterministic.

If the user says "onboard this repo", treat it as the broad form of the request: harnessability assessment covers cold-start orientation as one part of a wider readiness picture.

## Inputs

```text
$ARGUMENTS

# Common flags:
# --repo <path>                         Repository root. Defaults to current working directory.
# --markdown                            Emphasize the Markdown report path in the final answer.
# --json                                Emphasize the JSON report path in the final answer.
# --output-dir <path>                   Defaults to .harness/reports/harnessability/.
# --execute-safe-probes                 Allow safe local read-only probes such as help/list/version/dry-run commands.
# --deep                                Allow slower read-only analysis such as dependency graph inspection and git-history mining.
# --compare <previous.json>             Compare against a previous assessment JSON file.
# --weight <operate>:<adaptability>     Override default Harnessability Index weights. Default: 0.5:0.5.
# --scenario <name>                     Add or prioritize a scenario probe. May be repeated.
# --no-index                            Omit the single blended index; still emit the two-axis tuple.
# --apply-safe-harness-patches          Allow low-risk harness-only patches. Never applies product-code changes.
# --propose-codebase-affordances        Include product-code affordance recommendations. Default: on.
# --target-mode clean-start             Future mode: evaluate the clean-start experience in a disposable context.
```

No flags means read-only static assessment plus report generation.

## Output contract

Each run writes a per-run history directory plus stable root "latest" files:

```text
.harness/reports/harnessability/<ordinal>-<slug>/report.md
.harness/reports/harnessability/<ordinal>-<slug>/report.json
.harness/reports/harnessability/<ordinal>-<slug>/summary.md
.harness/reports/harnessability/<ordinal>-<slug>/evidence.jsonl
.harness/reports/harnessability/latest.md
.harness/reports/harnessability/latest.json
.harness/reports/harnessability/schema.json
```

`<ordinal>` is the next free 3-digit number (`001`, `002`, …) found by scanning existing `.harness/reports/harnessability/<NNN>-*/` directories; `<slug>` is a short kebab-case label for the run (e.g. the repo name, or `assessment`).

**Every run overwrites the three root files** (`latest.md`, `latest.json`, `schema.json`) so they mirror the newest run. The root `latest.json` is a load-bearing **sentinel**: the adoption flow (`/eng-harness-flow`) detects an existing assessment with `test -f .harness/reports/harnessability/latest.json || ls .harness/reports/harnessability/*` and then reads `latest.json` for recommendations. Keep it present **and** readable on every run — never write only the history directory (that would satisfy detection but leave nothing stable to read).

The Markdown report follows `templates/assessment-report.md`. The JSON report follows `templates/assessment-report.schema.json`, the authoritative v0.2 contract; write a copy of it to `.harness/reports/harnessability/schema.json`. The terminal-sized `summary.md` follows `templates/summary.md`; keep detailed evidence in `report.md`. See `templates/assessment-latest.md` and `templates/assessment-latest.json` for sanitized examples. If the repo already contains earlier assessment reports or onboarding docs, read them as evidence, but write this run's reports under `.harness/reports/harnessability/`.

Keep the JSON schema version at `harnessability-assessment.v0.2` until the core contract changes.

## Safety defaults

Default mode is static and conservative.

Allowed by default:

- read repository files;
- inspect Git metadata with read-only commands;
- inspect harness surfaces, command maps, package manifests, CI configs, local docs, and examples;
- inspect non-secret environment variable names and example values from safe example files;
- identify required secrets by name only;
- classify evidence, inference, human-supplied facts, and unknowns;
- write assessment reports under `.harness/reports/harnessability/`.

Not allowed by default:

- dependency installation;
- service boot;
- database, queue, cache, migration, fixture, storage, or external-system mutation;
- reading or printing secret values;
- external service calls;
- real auth flows;
- product-code edits;
- destructive cleanup;
- changing CI, deployment, cloud, identity, billing, tenant, or production configuration.

`--execute-safe-probes` may run only safe local read-only probes, such as:

- `--help`, `help`, `list`, `version`, `doctor --dry-run`, `config --list --names-only`;
- package-script listing commands that do not install or execute scripts;
- static commands that are known not to mutate state.

It still must not boot services, install dependencies, mutate state, read secrets, or call external services.

`--deep` may run slower read-only analysis, such as dependency graph inspection or Git history mining, when the necessary tools are already available. Do not install tools to make deep mode work unless the user separately approves installation. When mining Git history, summarize co-change and path evidence; do not copy raw author names, emails, or full commit messages into reports unless the user explicitly requests it.

`--apply-safe-harness-patches` may apply low-risk harness-only patches. Product-code affordance recommendations remain proposal-only unless a later explicit implementation task is approved by the user.

## Relationship to adoption, runtime, and feature-scoped back-pressure skills

| Skill type | Responsibility | Relationship to this skill |
|---|---|---|
| Adopt skill | Create or validate the harness nucleus: governance file, command map, `harness/cli/`, docs, routing, deterministic sensor inventory. | This skill may recommend adoption if no front door exists, but it does not replace the adopt flow. |
| Runtime boot/observe skill | Determine whether the harness is healthy for the current session. | This skill reports repo-level harnessability, not only live session readiness. |
| Feature-scoped Backpressure Check | Determine whether a specific feature or acceptance criterion can be proven by existing or buildable sensors. | This skill is whole-repo and structural; it identifies the repo's general proof surfaces and adaptability. |
| Cold-start onboarding/orientation | Help a fresh user or agent discover how to operate the repo. | Folded in: cold-start orientation is A1/A2/A4 within Operate-Today. |

Do not add a generic `backpressure` command recommendation. If a gap is found, recommend the specific sensor, command, fixture, fake, sink, diagnostic, schema check, smoke path, architecture rule, evidence capture, or product-code affordance that would prove the scoped work.

## Existing engineering environment survey

**Survey what the repo already has before recommending anything.** A harnessability assessment is first a *factual survey* of the engineering environment that exists today — its flows, command surfaces, gates, test mechanisms, dependency pressure, and composition — and only then a set of candidate harness surfaces. Inventory the existing system first; propose second. Each survey dimension below populates an optional v0.2 JSON array; emit what you find, omit what does not apply.

| Survey dimension | What to inventory | JSON array |
|---|---|---|
| Engineering flows | Named development flows the repo already runs — build, test, release, review, CI, onboarding, and **SDD-like** flows (e.g. a spec→plan→tasks pipeline under a `plans/` directory, `/plan-*` or `task-*` skills, RFC/ADR conventions). Record commands + whether the flow is canonical. | `engineering_flows[]` |
| Pre-commit & local gates | Hook mechanisms (husky, pre-commit, lefthook, git hooks), `just`/`make`/npm pre-commit paths, and what each gate actually checks; whether it runs locally and whether CI enforces the same. | `pre_commit_gates[]` |
| CI / local equivalence | For each meaningful check, whether the local command and the CI command are identical, equivalent, partial, divergent, or one-sided. Divergence is friction; identity is backpressure an agent can trust locally. | `ci_local_equivalence[]` |
| Existing harness concepts | Whether a **canonical** harness front door exists, or harness behaviour is **diffuse** (scattered scripts, ad-hoc Makefile targets, tribal commands). Canonical-vs-diffuse detection decides whether to recommend consolidation. | `existing_harness_concepts[]` |
| Test mechanisms | How tests achieve determinism: **mock vs fake vs sink vs stub vs contract vs testcontainer vs in-memory**. These are reusable harness affordances, not just test code. | `test_mechanisms[]` |
| External-dependency pressure | For each external dependency, how much it pressures local proof (none→blocking) and whether a local substitute exists. | `external_dependency_pressure[]` |
| Code composition & seams | Module/package/service/layer boundaries, plugin/extension points, and whether each seam is test-substitutable. | `code_composition[]` |
| Deterministic-encoding opportunities | Places where guidance currently lives in a context file / convention / manual step that could instead be encoded as an executable check, fixture, or schema. | `deterministic_encoding_opportunities[]` |
| Manual / IDE-only signals | Operations that only happen by hand or inside an IDE/GUI (advisory — see below). | `manual_operation_signals[]` |
| Candidate first harness surfaces | The verbs worth encoding **first**, derived *after* the survey above. | `candidate_first_harness_surfaces[]` |

### Prefer deterministic encoding over context-file accretion

A context file — `AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, `.cursorrules`, `.github/copilot-instructions.md` — is **orientation, never deterministic proof**. It tells an agent what *should* be true; it cannot fail a build when something *is* wrong. When the assessment finds important behaviour encoded only as prose in a context file, record it as a `deterministic_encoding_opportunities[]` entry whose proposed encoding is an executable surface (a check, fixture, fake, sink, schema, smoke path, or diagnostic). Prefer recommending that encoding over recommending "add more documentation." Documentation is the right answer only when orientation itself is the missing surface.

Distinguish **mocks** from **fakes/sinks**: a mock asserts an interaction and is brittle under refactor; a fake is a real working substitute that records state; a sink captures side effects for later assertion. Fakes and sinks are reusable harness affordances and stronger deterministic backpressure than mocks — surface them as such.

### Manual / IDE-only operation scan (advisory)

Scan for operations that only happen manually or inside an IDE/GUI — click-ops deploys, IDE-run-button-only entry points, undocumented manual steps, desktop/mobile/hardware interactions. Record them as `manual_operation_signals[]`.

This scan is **advisory**. It may only influence dimensions **A4, A5, A7, A8, A9, B5, and B10** (front door, boot/health, interaction surfaces, deterministic sensors, observability, hermetic testability, inner-loop speed). It must **never over-penalise** a repo simply because its topology is desktop, mobile, hardware, or brownfield — those are legitimate topologies, not harnessability failures. Set `penalize: no` when a manual signal is intrinsic to the topology rather than a fixable gap.

## Scoring model

The report has two primary axes:

```text
Operate-Today:  Can a fresh agent use the repo as it exists now?
Adaptability:   Can the repo be safely and cheaply changed to create better harnesses and stronger proof loops?
```

Always report the two-axis tuple. Do not collapse the result into a single grade unless also showing the tuple and per-dimension evidence.

### Dimension bands

Score each dimension with an evidence-backed band:

| Band | Points | Meaning |
|---|---:|---|
| Strong | 3 | Present, clear, and reliable enough for an agent to use today. Evidence supports the claim. |
| Partial | 2 | Present but incomplete, slow, brittle, undocumented, unsafe in some paths, or not consistently enforced. |
| Weak | 1 | Mostly absent, but straightforward to add or improve within normal engineering scope. |
| Absent | 0 | Not found, not usable, or requires significant product/harness work. |
| Not applicable | excluded | The dimension genuinely does not apply to this repo topology. Explain why. |
| Unknown | 0 by default | Evidence was insufficient. Use this sparingly and reduce confidence. |

A band without evidence is invalid. Separate facts from interpretation.

### Axis percentages

For each axis:

```text
axis_percent = earned_points / applicable_max_points * 100
```

### Letter grades

| Grade | Axis percent | Reading |
|---|---:|---|
| A | 85-100% | Agent-ready / highly modifiable |
| B | 70-84% | Good; targeted gaps remain |
| C | 55-69% | Workable but friction-heavy |
| D | 40-54% | Brownfield; adaptation likely needed first |
| E | 25-39% | Hostile to agent operation as-is |
| F | 0-24% | Not operable by an agent without harness work first |

### Assessment matrix (A–F)

In addition to the two-axis tuple, v0.2 emits an **assessment matrix**: an A–F grade per surveyed area (`assessment_matrix[]`) plus an overall `final_grade` (in `verdict`). The matrix is a readability layer over the dimensions and the survey — it **augments, never replaces** the A1–A10/B1–B10 scorecards or the Operate-Today/Adaptability tuple, which remain primary.

- Each `assessment_matrix[]` row carries an `area`, an A–F `grade`, an optional `score_percent`/`weight`, and a rationale.
- `final_grade` is the single headline A–F grade. Derive it from the matrix and axis percentages using the band thresholds above.
- `final_grade` **must not hide a poor axis**: if Operate-Today and Adaptability differ by two or more grades, report the weaker axis next to `final_grade` and never let the blend mask it. The tuple and per-dimension evidence always travel with the grade.

### Optional Harnessability Index

If a single comparable score is useful, compute:

```text
Harnessability Index = operate_weight * OperateToday% + adaptability_weight * Adaptability%
```

Default weights are `0.5:0.5`. Make clear that this index is lossy and must never replace the tuple or evidence table.

### Confidence

Report confidence separately from the score:

| Confidence | Criteria |
|---|---|
| High | Most dimensions have direct file/command evidence; major repo topology is clear; few unknowns. |
| Medium | Core evidence exists but some surfaces are inferred, ambiguous, or not deeply inspected. |
| Low | Repo is sparse, generated, inaccessible, missing important files, or dominated by unknowns. |

## Readiness and proof ladders

Use the H0-H5 readiness ladder for repository harness readiness:

| Level | Meaning |
|---|---|
| H0 Unknown | No reliable harness surface or boot substrate detected. |
| H1 Front door exists | Harness or command entrypoint exists, but commands are generic, unconfigured, or mostly inferred. |
| H2 Assessed | Repo type, command candidates, services, prerequisites, interaction surfaces, evidence paths, and structural risks are mapped with source evidence. |
| H3 Operable | At least one boot/health or fast validation path is configured and can be dry-run or safely executed. |
| H4 Proveable | A meaningful proof scenario exists with interaction, observable consequence, verdict, and rerun path. |
| H5 Compounding | Friction capture, known difficulties, proof records, and encoded harness improvements are wired into the loop. |

Use Proof L0-L6 for what a specific command, scenario, or claim proves:

| Level | Meaning |
|---|---|
| L0 Claim | Actor says work is done, no evidence. |
| L1 Local command output | A command ran and output exists. |
| L2 Static/build/test | Build, lint, typecheck, unit, schema, security, architecture, or isolated tests passed. |
| L3 Runtime interaction | Product/API/UI/CLI/worker/queue/MCP/system path was exercised. |
| L4 Interaction plus observable consequence | Runtime interaction plus verification of state, file, database, message, event, cache, object, search index, generated artifact, log, trace, screenshot, or external-effect sink. |
| L5 Reproducible clean rerun | Proof passes again in a clean or reset context using recorded instructions. |
| L6 Production/customer outcome | Production telemetry, incident-free release, customer outcome, or business evidence supports the result. |

Static assessment alone should not claim L3 or above unless recorded evidence already exists and is cited.

## Axis A — Operate-Today dimensions

Assess whether a fresh agent can use the repo as it exists now.

### A1. Cold-start orientation and repo map

Measures whether a fresh agent can answer:

- what the system is;
- how it is organized;
- how to run it;
- how to validate it;
- where current work, known difficulties, and harness entrypoints live.

Evidence signals:

- `README`, `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.cursor/rules/`, `docs/` (including any rule/harness subfolders);
- repo maps, architecture docs, package maps, service maps;
- clear first-session instructions and known-trap notes.

### A2. Setup and environment contract

Measures whether dependencies, runtimes, tools, environment variables, and secrets are discoverable without tribal knowledge.

Evidence signals:

- `.env.example`, `.env.template`, `.envrc.example`, `devcontainer.json`, `.tool-versions`, `.nvmrc`, `.node-version`, `.python-version`, `Dockerfile`, `docker-compose.yml`, `compose.yaml`, `Makefile`, `justfile`;
- package manifests and lockfiles;
- explicit env var names and descriptions;
- doctor/preflight checks;
- safe distinction between required secrets and local defaults.

Never print secret values. Report env names only.

### A3. Locality of infrastructure and external dependency exposure

Measures whether the repo can run and prove work locally or through safe substitutes instead of requiring remote deployed machines.

Inventory:

- databases, caches, queues, brokers, object stores, search indexes, auth providers, third-party APIs, payment/email/SMS/webhook services, analytics, feature-flag systems, model providers, remote config, and internal services;
- whether each dependency is local, containerized, fakeable, optional, remote-required, secret-required, or unknown.

Evidence signals:

- compose files, Testcontainers usage, localstack/minio/mailhog/wiremock-style services, fake servers, mock adapters, local auth providers;
- SDK clients and connection strings;
- service URLs and env names;
- docs naming remote-only dependencies.

### A4. Harness front door and command discoverability

Measures whether there is one obvious supported way to operate the repo.

Evidence signals:

- `harness/cli/`, `harness/cli/commands.json`, `bin/harness`, `justfile`, `Makefile`, npm/pnpm/yarn/bun scripts, taskfile, mage, nox, tox, poetry scripts, Gradle/Maven targets, cargo aliases, go task runners;
- `--help`, stable verbs, examples, exit codes, parseable output, non-interactive flags.

The front door can wrap existing scripts. It does not need to reimplement the toolchain.

### A5. Boot and health/readiness path

Measures whether the system can start from a known state and prove basic readiness.

Evidence signals:

- `boot`, `dev`, `up`, `start`, `doctor`, `health`, `ready`, `smoke` commands;
- health endpoints, readiness probes, startup logs, wait-for-ready scripts;
- documented ports and expected successful output;
- deterministic failure messages.

### A6. Seed, fixture, reset, and cleanup state

Measures whether the system can be put into meaningful, known, repeatable state.

Evidence signals:

- `seed`, `reset`, `fixtures`, `factory`, `snapshot`, `restore`, `cleanup`, `teardown` commands;
- idempotent data setup;
- local fixtures for users, tenants, permissions, sample domain objects, files, messages, events, or UI flows;
- migration and rollback paths where relevant.

State is not only databases. It can include files, queues, caches, object stores, search indexes, browser storage, generated artifacts, local models, or event logs.

### A7. Supported interaction surfaces

Measures whether the agent can exercise real product or system behaviour without private shortcuts.

Evidence signals:

- API routes, OpenAPI specs, GraphQL schemas, CLI commands, UI smoke flows, Playwright/Cypress tests, worker entrypoints, queue consumers, event producers, MCP tools, cron jobs, webhooks, auth flows;
- documented test users or local auth bypasses scoped to local/test environments;
- scripts that hit supported endpoints or workflows.

### A8. Existing deterministic back-pressure sensors

Measures what the repo already proves on every change or on demand.

Evidence signals:

- build, compile, typecheck, lint, format, unit, integration, smoke, E2E, schema, contract, security, dependency, architecture, performance, accessibility, visual regression, migration, static analysis, code coverage, mutation testing;
- integration/E2E suites that provision, seed, and reset real or containerized datastores or services — these are reusable change-to-evidence surfaces, not just a slow lane;
- CI workflows, pre-commit hooks, required checks, local equivalents for CI.

Prefer sensors that produce actionable, agent-readable failure output.

### A9. Observability and evidence artifacts

Measures whether behaviour and hidden state become portable evidence rather than guesses.

Evidence signals:

- structured logs, traces, metrics, screenshots, videos, HAR files, JSON reports, diagnostic endpoints, dump commands, run artifacts, query helpers, event inspection, generated output directories;
- commands with `--json`, `--output`, `--verbose`, `--trace`, or `--explain` modes;
- clear artifact paths and retention rules.

### A10. Compounding harness loop

Measures whether friction and missing proof become future harness improvements.

Evidence signals:

- friction ledgers, retrospectives, magic-wand prompts, known difficulties, proof records, run history, harness backlog, encoded improvements, changelogs for harness commands;
- workflow that asks: "what did the agent have to infer that the harness should have proved?"

## Axis B — Adaptability dimensions

Assess whether the repo can be safely and cheaply changed to create stronger harnesses and stronger proof loops.

### B1. Structural coupling and blast radius

Measures whether modules depend on too many other modules or are depended on by too many callers.

Evidence signals:

- import/dependency graph fan-in and fan-out;
- package/module boundaries;
- afferent/efferent coupling, instability, dependency cycles where tools support them;
- broad shared utility modules or cross-layer imports.

In default mode, use static file inspection. In `--deep`, use available dependency graph tools without installing new tools.

### B2. Temporal/change coupling

Measures whether files or modules often change together in Git history even if static imports do not show the dependency.

Evidence signals:

- co-change pairs from `git log --name-only`;
- unexpected files that frequently change together;
- broad commits touching many layers for small features.

Only compute in `--deep` mode or when cheap. Otherwise mark as unknown or partial with low confidence.

### B3. Cohesion and locality of change

Measures whether related behavior lives together and unrelated behavior is separated.

Evidence signals:

- feature/domain modules with clear ownership;
- tests near the code they prove;
- low scattering of domain concepts;
- absence of god files, catch-all services, overloaded helpers, or mega controllers.

### B4. Seams, substitution, and dependency inversion

Measures whether behavior can be replaced without editing the production path in place.

Evidence signals:

- interfaces, ports/adapters, dependency injection, inversion of control, provider abstractions;
- test doubles, fakes, stubs, mocks, spies, contract tests;
- local adapters for external systems;
- boundaries between domain logic and infrastructure.

This is a core modifiability signal: good seams make it easier to add local proof without standing up the whole integrated world. The seams the tests already inject at are the seams the harness can reuse — inventory them as candidate harness affordances.

### B5. Hermetic, offline, and isolated testability

Measures whether useful tests can run without live remote services or a full integrated environment.

Evidence signals:

- unit test lane separated from integration/E2E lane;
- fakes, in-memory implementations, local containers, contract tests;
- tests that do not require network, remote credentials, shared databases, or production-like tenants;
- clear markers for integration tests.

Score hermeticity as a gradient, not a binary. Some valuable proof requires integration; the question is whether cheap self-correction paths exist before expensive proof. Do not treat an existing integration harness as only a cost: if the suite already stands up, seeds, and resets a real or containerized datastore, that lifecycle is a high-leverage surface the harness can wrap to reach real-consequence proof cheaply.

### B6. Side-effect isolation and external-effect sinks

Measures whether risky or remote side effects can be captured safely.

Evidence signals:

- local sinks for email, SMS, push, payments, webhooks, analytics, notifications, object storage, search indexing, queues, events, model calls, or third-party APIs;
- replayable cassettes, fake servers, sandbox modes, dry-run modes, captured payload assertions;
- explicit controls preventing accidental production calls.

### B7. State evolution and consequence verification

Measures whether changes that affect state can be applied, rolled forward/back, seeded, exercised, and verified.

Evidence signals:

- migration tooling, schema snapshots, contract/versioning checks, fixture evolution, state reset, event schema migration, file format migration, cache invalidation tests, object-store fixture paths;
- commands that verify observable consequences after an interaction.

Database migrations are one example only. Include files, event schemas, queues, caches, search indexes, generated artifacts, and external payload contracts where relevant.

### B8. Architecture boundary enforceability

Measures whether architecture rules are encoded as sensors rather than prose.

Evidence signals:

- dependency-cruiser, ArchUnit, eslint boundary rules, Semgrep, CodeQL, Roslyn analyzers, module visibility constraints, package-level tests;
- rules for layer direction, domain/infrastructure separation, import restrictions, tenant/auth/security boundaries.

### B9. Complexity, size, and navigability thresholds

Measures whether the codebase keeps functions, files, modules, and branches tractable for agent context windows and human review.

Evidence signals:

- cyclomatic/cognitive complexity rules, max file/function length, max params, duplication detection, dead-code detection;
- lint/static-analysis configs that are enabled and enforced;
- hotspots where large files or high-complexity code block safe edits.

### B10. Inner-loop speed and repeatability

Measures how quickly an agent can go from edit to feedback, and whether the loop can be rerun from a known state.

Evidence signals:

- fast test lane, watch mode, build cache, split unit/integration commands, isolated package tests, deterministic clocks/IDs, stable ports, idempotent setup/cleanup;
- recorded durations where available;
- flake controls and retry policy.

## Back-pressure surface taxonomy

For every repo, build an inventory of deterministic and advisory sensors:

| Category | Examples | What to report |
|---|---|---|
| Static/build sensors | compile, typecheck, lint, format, unit tests, schema checks, architecture checks, security scans | command, scope, speed if known, local/CI availability, verified/unverified |
| Runtime sensors | boot, health, smoke, API, UI, CLI, worker, queue, MCP, cron, webhook | interaction surface, required services, evidence path, proof level |
| Consequence sensors | state, files, DB, cache, message, event, object storage, search index, generated artifacts | how consequence is observed, reset path, local safety |
| External-effect sensors | email/SMS/payment/webhook/API sinks, sandbox modes, fake servers, contract tests | whether production calls are impossible by default |
| Observability sensors | logs, traces, metrics, screenshots, HAR, JSON run reports, diagnostics endpoints | artifact path and verdict extraction method |
| Human/inferential sensors | review checklist, AI review, manual QA, LLM-as-judge | mark advisory unless backed by deterministic evidence |
| Production/customer sensors | telemetry, SLOs, incident-free deploys, usage/business outcomes | only L6 when evidence exists; do not infer from intent |

## Scenario probes

After static inspection, select representative **change-to-evidence probes** for the repo topology. These are not necessarily executed by default. They are used to estimate proof ceilings and identify missing back pressure.

Each scenario probe must answer:

```text
Scenario name:
Relevant surfaces:
Likely edit target:
Required setup/env/services:
Supported interaction:
Expected observable consequence:
Deterministic verdict command/check:
Reset/cleanup path:
Local substitute or fake available:
Remote-only or secret-gated blockers:
Highest plausible proof level today:
What the agent would still have to infer:
Highest-leverage missing sensor or affordance:
```

Default candidate probes:

| Probe | Use when relevant | Observable consequence examples |
|---|---|---|
| API behavior loop | Services expose HTTP/RPC/GraphQL APIs | response, schema, log, state, event, contract |
| UI/user-flow loop | Web/mobile/desktop UI exists | rendered state, screenshot, accessibility tree, visual artifact, API effect |
| CLI behavior loop | CLI tools exist | stdout/stderr, exit code, file output, config change |
| Worker/event loop | Queues, jobs, event consumers exist | message consumed/published, event payload, idempotency record, dead-letter behavior |
| State/storage loop | Repo has persistent or generated state | DB row, file, cache entry, object, search document, migration result |
| External-effect loop | Third-party side effects exist | captured email/SMS/payment/webhook/API payload in a sink/fake/sandbox |
| Auth/permission loop | Auth, roles, tenants, permissions exist | allowed/denied request, token claims, audit event, UI visibility |
| Schema/contract loop | API/event/data contracts exist | OpenAPI/GraphQL/protobuf/JSON-schema diff, consumer contract, migration compatibility |
| Architecture-rule loop | Architecture boundaries matter | static rule failure/pass, dependency graph diff |
| Performance/reliability loop | Latency, throughput, resilience matter | benchmark, load-smoke, retry/fallback evidence, SLO-like local signal |

If a scenario is irrelevant, mark it not applicable. Do not force every repo through every probe.

## Command tiers

Normalize discovered commands into these tiers:

- `bootstrap`
- `setup_services`
- `doctor`
- `boot`
- `health`
- `fast`
- `quick`
- `proof`
- `ci_equivalent`
- `smoke`
- `seed_or_reset`
- `observe`
- `cleanup`
- `retro_or_improve`

Use statuses:

- `verified`
- `configured_unverified`
- `candidate_unverified`
- `not_applicable`
- `unknown`

Do not mark inferred commands as verified unless they were executed successfully in the current run or supported by reliable recorded evidence.

## External dependency inventory

Create an explicit table for dependencies that may require remote machines, shared infrastructure, secrets, or paid services.

For each dependency, report:

```text
name:
type: database | cache | queue | object_store | search | auth | payment | email | sms | webhook | analytics | model_provider | internal_service | external_api | other
where_detected:
local_option: native | container | fake | in_memory | testcontainers | sandbox | dry_run | none | unknown
remote_required: yes | no | optional | unknown
secret_required: yes | no | optional | unknown
mutation_risk: none | local_only | remote_safe_sandbox | remote_shared | production_risk | unknown
proof_blocked_by_dependency: yes | no | partial | unknown
recommended_affordance:
```

This inventory is central to Operate-Today, but also informs Adaptability: a repo is more adaptable when remote dependencies have seams, fakes, sinks, sandboxes, or contract tests.

## Environment variable inventory

Report environment configuration without leaking secrets.

For each env var name discovered, report:

```text
name:
required: yes | no | optional | unknown
purpose_inferred:
source_files:
example_present: yes | no
safe_default_present: yes | no
secret_like: yes | no | unknown
local_dev_notes:
```

Do not read, print, or copy values from `.env`, shell history, keychains, password managers, cloud CLIs, or secret stores. `.env.example` and clearly non-secret local examples may be inspected.

## Gap classification

Every material gap should include:

```text
id:
title:
axis: operate_today | adaptability | both
subsystem: instructions | tools | environment | state | feedback | architecture | tests | observability | external_dependency | human_process
loop_stage: boot | interact | observe | validate | improve
backpressure_category: static | runtime | consequence | external_effect | observability | human_inferential | production_customer
scenario_impacted:
target_layer: harness | product_code | test_code | fixture_data | environment | ci | agent_instruction | human_process
encoding_type: guide | sensor | command | fixture | fake | sink | diagnostic | evidence | state | policy | architecture_rule | schema | workflow
severity: blocker | high | medium | low | info
status: absent | weak | partial | unknown | proposed
provenance: evidence | inference | human_supplied | unknown
confidence: high | medium | low
recommended_next_action:
proof_level_unblocked:
estimated_effort: XS | S | M | L | XL
risk_tier: low | medium | high | critical
```

## Product-code affordance recommendations

Harnessability can require product-code changes. This skill may recommend them, but it must not apply them by default.

Examples include:

- local/test-only auth provider;
- seeded fixture user, tenant, permission set, or domain object;
- idempotent seed/reset/cleanup command;
- health/readiness endpoint;
- side-effect sink for email, SMS, payments, webhooks, queues, object storage, model calls, or external APIs;
- stable UI selectors or accessible labels;
- deterministic clock, random, ID, port, or tenant provider;
- structured diagnostics endpoint;
- local fake adapter or in-memory implementation;
- contract test for API, event, schema, or third-party integration;
- architecture boundary rule;
- fixture-backed smoke scenario;
- run artifact or `--json` report mode.

Every product-code affordance recommendation must state:

```text
status: proposed
risk_tier:
target_layer:
environment_scope:
environments_where_it_must_not_apply:
safety_requirements:
human_or_security_review_required:
which_gap_it_addresses:
which_harness_command_or_proof_level_it_unblocks:
why_it_is_better_than_more_documentation:
```

High-risk and critical recommendations are proposal-only by default.

## Execution flow

### 1. Establish repo context

Record:

- repo root;
- repo name;
- current branch and commit if available;
- workspace dirty/clean status if available;
- whether the run is static, safe-probe, deep, or comparison mode;
- commands executed and commands skipped;
- safety notes.

Never print secret values.

### 2. Read existing harness and onboarding surfaces

Check:

- `harness/cli/`;
- `harness/cli/commands.json`;
- `docs/harness/`;
- `.harness/engineering-harness.md` (the canonical governance doc — the only location);
- `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`, `.cursorrules`, `.github/copilot-instructions.md`;
- existing onboarding or readiness docs;
- previous `.harness/reports/harnessability/` reports.

Report which surfaces are canonical. If only ad-hoc onboarding docs exist, recommend folding the useful parts into the engineering harness front door and assessment reports.

### 3. Detect repository topology

Identify:

- languages and runtimes;
- package roots and monorepo layout;
- service types: API, UI, CLI, library, worker, batch, data pipeline, mobile, desktop, infrastructure, MCP, model app, other;
- framework and build tooling;
- deployment topology where visible;
- local development topology;
- CI topology;
- domain boundaries and module ownership where visible.

### 4. Inventory commands and sensors

Read package manifests, task runners, CI, docs, and harness command maps.

Classify commands into tiers and statuses. Prefer existing supported surfaces over guessed raw commands.

For each deterministic sensor, report:

```text
command_or_check:
category:
local_available:
ci_available:
requires_services:
requires_secrets:
mutates_state:
expected_duration_if_known:
output_artifact:
proof_level:
status:
evidence:
```

### 5. Inventory environment, services, and remote dependency exposure

Build the env var inventory and external dependency inventory.

Explicitly call out:

- remote-only blockers;
- shared-state blockers;
- missing local substitutes;
- secret-gated paths;
- risky side effects;
- dependencies that prevent L3/L4 proof locally.

### 6. Inventory state, fixtures, interactions, and observable consequences

Map how the repo supports:

- meaningful starting state;
- reset/cleanup;
- supported product/system interactions;
- evidence capture;
- consequence verification.

Use the broad consequence model. Do not privilege databases unless the repo does.

Read the test suite as the primary evidence of these mechanisms: how tests mock, inject, substitute, seed, restore, reset, and make behavior real shows exactly which seams and state lifecycles the harness can reuse. Record each reusable mechanism as a candidate harness affordance.

### 6b. Synthesize the existing engineering environment survey

Before scoring or proposing anything, consolidate what steps 2–6 found into the existing-engineering-environment survey (see `## Existing engineering environment survey`). Populate the optional v0.2 arrays from evidence already gathered:

- `engineering_flows[]` — including any SDD-like spec→plan→tasks pipeline (a `plans/` directory, `/plan-*` or `task-*` skills, RFC/ADR conventions);
- `pre_commit_gates[]` and `ci_local_equivalence[]` — from the command/CI inventory (step 4);
- `existing_harness_concepts[]` — canonical vs diffuse, from step 2;
- `test_mechanisms[]` — mock vs fake/sink/stub/contract/testcontainer, from step 6;
- `external_dependency_pressure[]` — from step 5;
- `code_composition[]` — seams and boundaries;
- `manual_operation_signals[]` — advisory; populate here, **before** scoring, scoped to A4/A5/A7/A8/A9/B5/B10 only, with `penalize: no` for topology-intrinsic desktop/mobile/hardware/brownfield cases.

**Existing-flow-first rule**: inventory existing flows and command surfaces here, *before* any candidate harness surface is proposed. `candidate_first_harness_surfaces[]` and `deterministic_encoding_opportunities[]` are derived later (step 10), only after this survey and the scorecards exist.

### 7. Assess Operate-Today

Score A1-A10. Each band must include evidence, inference, or unknown status.

Summarize:

- what a fresh agent can do immediately;
- what it would have to infer;
- what blocks setup or proof;
- highest proof level reachable today;
- first safe agent session plan.

### 8. Assess Adaptability

Score B1-B10. Use read-only static inspection by default.

In deep mode, additionally consider:

- dependency graph metrics;
- import cycles;
- module fan-in/fan-out;
- co-change/temporal coupling from Git history;
- complexity hotspots if tools are available;
- test isolation and marker patterns.

Do not overclaim if language/tooling support is absent. Mark unknowns honestly.

### 9. Select scenario probes

Select 3-6 representative change-to-evidence probes based on repo topology and user interest. Include database/state probe only if relevant.

For each probe, estimate the proof ceiling and missing sensors. Do not execute probes unless safe and explicitly allowed.

### 10. Rank gaps and remediations

Rank by:

1. blocker severity;
2. proof level unblocked;
3. number of dimensions improved;
4. recurrence likelihood;
5. effort;
6. safety/risk.

Prefer remediations that encode the fix into executable harness surfaces over adding prose. Documentation is acceptable when orientation is the actual missing surface, but executable commands, checks, fixtures, diagnostics, fakes, sinks, schemas, and evidence artifacts are usually stronger. Prefer reusing mechanisms the tests already rely on — seeding, restore/reset, injection seams, fakes, sinks, containerized services — by exposing them as supported harness commands, rather than building new scaffolding from scratch.

After ranking, derive `candidate_first_harness_surfaces[]` — the verbs worth encoding *first* — strictly from the survey (step 6b) and the gaps above, never before the existing environment has been inventoried. Record `deterministic_encoding_opportunities[]` wherever behaviour currently lives only in a context file or manual step and could instead become an executable check, fixture, or schema (see `## Existing engineering environment survey`).

### 11. Write reports

Write the Markdown report, the terminal-sized `summary.md`, the JSON report, and the schema copy according to the output contract: into `.harness/reports/harnessability/<ordinal>-<slug>/` and mirrored to the root `latest.*`/`schema.json`. Record the written paths in `report_paths`. Confirm the root `latest.json` is present and readable — it is the sentinel the adoption flow (`/eng-harness-flow`) reads.

## Parallel execution: subsystem fan-out

This skill can run as a single linear pass (the execution flow above) or fan out across read-only subsystem subagents for speed and depth. Both models produce the same report; only the orchestration differs.

### Orchestrator pre-wave (serial, shared context)

Run execution steps 1-3 once: repo context, harness surfaces, and topology. Detect the repository type a single time and pass it to every subagent so they do not re-derive it. Hand each subagent: the repo root, the detected topology, the dimension band rubric (Strong, Partial, Weak, Absent, Not applicable, Unknown), the safety defaults, and the schema slice it must return.

The orchestrator owns these top-level keys from the pre-wave: `schema_version`, `run`, `harness_surfaces`, `topology`, and `report_paths`.

### Fan-out: six read-only inspector subagents

Each subagent is read-only, inspects only its subsystem, and returns a JSON fragment plus its own `evidence_log` entries. No subagent may boot services, install dependencies, mutate state, read secrets, or call external services. Ownership:

| Subagent | Inspects | Owns (schema slices) |
|---|---|---|
| 1. Commands and sensors | command runners, CI, deterministic checks, hooks | `command_tiers[]`, static `backpressure_surfaces[]`, `pre_commit_gates[]`, `ci_local_equivalence[]`, candidate inputs for `candidate_first_harness_surfaces[]`, dimensions A4, A5, A8 |
| 2. Environment and dependencies | env var names, services, remote/local exposure | `environment_variables[]`, `external_dependencies[]`, `external_dependency_pressure[]`, dimensions A2, A3 |
| 3. State, interaction, and observability | seed/reset/fixtures, interaction surfaces, auth, evidence paths | runtime/consequence/observability/external-effect `backpressure_surfaces[]`, dimensions A6, A7, A9 |
| 4. Test reconnaissance and seams | how tests mock, inject, seed, restore, and make behaviour real; sinks; substitution | `test_mechanisms[]`; dimensions B4, B5, B6; reusable-mechanism `harness_recommendations[]`; related `gaps[]` |
| 5. Structure and adaptability | coupling, cohesion, complexity, boundaries, inner loop | `code_composition[]`, dimensions B1-B3, B7-B10 |
| 6. Cold-start and compounding loop | repo map, first-session orientation, engineering flows, canonical-vs-diffuse harness, manual/IDE signals, friction/improve loop | `engineering_flows[]`, `existing_harness_concepts[]`, `manual_operation_signals[]`, dimensions A1, A10; `first_safe_session_plan` candidates |

The orchestrator synthesizes the remaining cross-cutting v0.2 slices at merge — `assessment_matrix[]` + `verdict.final_grade` (computed from merged dimensions), `deterministic_encoding_opportunities[]` and `candidate_first_harness_surfaces[]` (derived from the survey + ranked gaps), and `report_paths` (known at write time). With the subagent table above this keeps the map **collectively exhaustive**: every v0.2 array has exactly one owner.

Every subagent also emits `gaps[]` and `evidence_log[]` for its subsystem, each finding carrying provenance (`evidence`, `inference`, `human_supplied`, or `unknown`) and confidence.

The test-reconnaissance lens is cross-cutting: subagent 4 owns it, but subagents 1 (A8 sensors) and 3 (A6 state) will surface overlapping test signals. Subagents should report what they see and not suppress overlap; the orchestrator dedups at merge.

### Orchestrator synthesis (serial)

1. Merge all fragments into one document.
2. Validate the merged document against `templates/assessment-report.schema.json`. The schema is the merge contract: a fragment that does not fit its slice is a subagent defect, not a reason to change the schema.
3. Compute axis percentages, letter grades, the optional Harnessability Index, the readiness H-level, the highest and target proof levels, and the A–F `assessment_matrix[]` + `verdict.final_grade` from the merged dimensions and sensors.
4. Select scenario probes, which require the whole-repo view.
5. Rank gaps and remediations across subsystems; derive product-code affordance recommendations, `deterministic_encoding_opportunities[]`, and `candidate_first_harness_surfaces[]` from cross-cutting gaps and the existing-environment survey.
6. Write the reports once, recording `report_paths` and refreshing the root `latest.*`/`schema.json` sentinel. The orchestrator is the only writer; if `--apply-safe-harness-patches` is set, only the orchestrator applies harness-only patches.

### Why fan out

- The two axes and most dimensions are independently inspectable, so parallel subagents cut wall-clock time and allow deeper per-subsystem inspection.
- The v0.2 JSON schema doubles as the merge contract, so fragments compose without ad-hoc glue.
- Read-only subagents plus a single orchestrator writer preserve the safe-by-default posture even under parallelism.

## Markdown report template

The Markdown report must include:

```text
# Harnessability Assessment — <repo>

Run metadata
- Timestamp
- Repo root
- Branch / commit
- Mode
- Commands executed
- Commands skipped
- Safety notes

## Verdict
- Operate-Today: <grade> (<percent>%)
- Adaptability: <grade> (<percent>%)
- Harnessability Index: <percent>% (<grade>) or omitted
- Readiness: H0-H5
- Highest proof level detected: L0-L6
- Target next proof level: L0-L6
- Confidence: high | medium | low

## Plain-English assessment
- What is ready
- What blocks confident agent work
- What the agent would still have to infer
- Whether local proof is possible
- Whether remote-only dependencies block proof

## Top blockers
Ranked list with evidence and recommended next action.

## Highest-leverage improvements
3-7 executable remediations. Prefer commands, sensors, fixtures, fakes, sinks, diagnostics, schema checks, smoke paths, and architecture rules.

## First safe agent session plan
A short plan for the next agent run using only supported or safe surfaces.

## Harness surfaces
Canonical and prior harness front-door surfaces detected, with paths and status.

## Repository topology
Languages, runtimes, package roots, service types, and local/CI topology.

## Axis A — Operate-Today scorecard
A1-A10 table: band, points, evidence, notes.

## Axis B — Adaptability scorecard
B1-B10 table: band, points, evidence, notes.

## Back-pressure surface inventory
Static, runtime, consequence, external-effect, observability, human/inferential, production/customer.

## Scenario probes
Each selected change-to-evidence probe with proof ceiling and missing back pressure.

## Command tiers
Tiered command inventory with status and safety notes.

## Services, environment, and remote dependency exposure
Env var names only. External dependency table. Remote-only blockers.

## State, fixtures, reset, and cleanup
Known starting state and repeatability assessment.

## Observability and evidence
Artifacts, logs, traces, screenshots, JSON reports, diagnostics, verdict extraction.

## Codebase affordance recommendations
Product-code changes proposed, with risk tier and safety boundaries.

## Harness-only recommendations
Harness changes proposed or applied, with paths and rationale.

## Onboarding consolidation notes
Existing onboarding content worth folding into the harness front door and assessment reports.

## Human questions
Targeted questions only after evidence has been inspected.

## Evidence and inference log
Every major finding with provenance: evidence | inference | human_supplied | unknown.
```

## JSON report minimum shape

The JSON report must include at least:

```json
{
  "schema_version": "harnessability-assessment.v0.2",
  "run": {
    "timestamp_utc": "YYYYMMDDTHHMMSSZ",
    "repo_root": "",
    "repo_name": "",
    "branch": "",
    "commit": "",
    "mode": "static|safe-probe|deep|comparison",
    "commands_executed": [],
    "commands_skipped": [],
    "safety_notes": []
  },
  "verdict": {
    "operate_today_percent": 0,
    "operate_today_grade": "A|B|C|D|E|F",
    "adaptability_percent": 0,
    "adaptability_grade": "A|B|C|D|E|F",
    "harnessability_index_percent": 0,
    "harnessability_index_grade": "A|B|C|D|E|F",
    "final_grade": "A|B|C|D|E|F",
    "readiness_level": "H0|H1|H2|H3|H4|H5",
    "highest_proof_level": "L0|L1|L2|L3|L4|L5|L6",
    "target_proof_level": "L0|L1|L2|L3|L4|L5|L6",
    "confidence": "high|medium|low"
  },
  "harness_surfaces": [],
  "topology": {},
  "axis_a_operate_today": [],
  "axis_b_adaptability": [],
  "backpressure_surfaces": [],
  "scenario_probes": [],
  "command_tiers": [],
  "environment_variables": [],
  "external_dependencies": [],
  "gaps": [],
  "remediations": [],
  "product_code_affordances": [],
  "harness_recommendations": [],
  "applied_patches": [],
  "onboarding_consolidation": [],
  "first_safe_session_plan": [],
  "human_questions": [],
  "evidence_log": []
}
```

v0.2 may additionally include the optional survey arrays and report metadata: `report_paths`, `assessment_matrix` (plus `verdict.final_grade`), `engineering_flows`, `pre_commit_gates`, `ci_local_equivalence`, `existing_harness_concepts`, `deterministic_encoding_opportunities`, `test_mechanisms`, `external_dependency_pressure`, `code_composition`, `candidate_first_harness_surfaces`, and `manual_operation_signals`. All are optional — emit what the survey found.

## Stop conditions

Stop and ask the user before:

- executing any service boot;
- installing dependencies;
- reading secret values;
- running migrations, seeds, reset, cleanup, queue consumers, cron jobs, or background workers;
- calling external services;
- running real auth flows;
- mutating local or remote state;
- applying product-code changes;
- making high-risk auth, identity, permission, tenant, billing, data-access, cloud, deployment, or production-adjacent changes.

## Final response after running the skill

Report:

- Markdown report path;
- JSON report path;
- Operate-Today grade and percent;
- Adaptability grade and percent;
- Harnessability Index if emitted;
- readiness level;
- highest detected proof level;
- confidence;
- top blockers;
- top executable remediations;
- whether existing onboarding content was consolidated into the assessment cleanly;
- the first safe next action.

Keep the final response short. The full detail belongs in the generated reports.

## Quality bar

A good assessment is:

- evidence-first;
- safe by default;
- honest about unknowns;
- explicit about what the agent would have to infer;
- explicit about local versus remote proof;
- broad about back pressure, not database-centric;
- useful for both humans and agents;
- focused on executable improvements;
- clear about product-code changes versus harness-only changes;
- resistant to vanity scoring by showing the two-axis tuple and per-dimension evidence.

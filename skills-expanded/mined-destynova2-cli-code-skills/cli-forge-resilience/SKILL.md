---
name: cli-forge-resilience
metadata:
  author: clement
description: >
  Generate a production-parity resilience blueprint: test battery, troubleshooting
  runbook, agent-ready operations pack, failure-injection plan, and incident
  blackbox templates. Uses
  biological and physical reasoning — genome/contracts, membranes/boundary
  conditions, homeostasis/health checks, immune system/negative tests,
  stress-strain/failure budgets, phase transitions/resource cliffs,
  hysteresis/reruns, and memory cells/post-incident capitalisation. Use
  whenever the user asks to prevent prod bugs, make dev/staging closer to prod,
  design pre-prod checks, write a runbook, create a smoke test ladder, harden
  deployments, define N1/N2/N3 operations, govern agent autonomy, or turn
  incidents into durable anti-regressions.
argument-hint: "[service-name-or-repo-path-or-incident-doc]"
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - Agent
---

> **Optimization:** This skill uses on-demand loading. Heavy content lives in `references/` and is loaded only when needed.
> **Language rule:** Skill instructions are written in English.

When generating user-facing output (reports, files, documentation), detect the project's primary language (from README, comments, docs, commit messages) and produce the output in that language. If the project is bilingual, ask the user which language to use before proceeding.

> **Diacritics rule:** When the chosen output language uses diacritics (French, Spanish, Portuguese, etc.), render them correctly — including on capitals (É, À, Ç, Ô…). Never strip accents to ASCII: write "sécurité" not "securite", "Rôle" not "Role". ASCII-flattened French is a defect, not a style.

> **Writing style:** Favor clarity — short sentences, one idea per sentence, plain words. A metaphor only when it clarifies. Keep one consistent register (impersonal/infinitive for operational docs). Separate narrative prose, meant to make the reader understand, from telegraphic content (tables, commands, checklists) which stays terse for action.

> **Reader calibration (the Singh rule):** Before writing, name the expected reader and their situation. For runbooks the reader is an operator mid-incident, often stressed: command or fact first, the why in one short line after, imperative mood, no em-dash asides, no narrative voice, no scene-setting intro. Biological metaphors (genome, membrane, immune system) belong to this skill's reasoning and to explanation sections — never inside triage steps, procedures, or decision trees, where they cost seconds. If a sentence would read well in a magazine, it is miscalibrated for a runbook.

> **No fabricated output:** Never invent command output, console captures, API responses, metrics, or logs. When real output is needed, emit a clearly-marked placeholder (🚧 "replace with a real capture"), never plausible-but-fake text presented as real.

> **Memorability (rule of three):** For short lists an operator must internalize (incident reflexes, level missions, checklists), add a three-part memory hook above the list, built from the operator's own action verbs (e.g. "Capture → Follow the runbook → Verify"), keeping the detailed items underneath. Never build the hook on an image or metaphor ("stay on the rails" reads well and calibrates badly). Use sparingly — only where recall matters under stress, never on reference tables.

# Forge Resilience — Prod-Parity, Failure Biology & Runbooks

> *"A system survives production when it keeps homeostasis under stress, not when it merely passes happy-path tests."*

## Core Principle

**Treat the system as an organism in an environment, not as a pile of files.**

Production bugs usually appear when one of these mismatches exists:

- **Genome mismatch** — contracts, ports, tags, secrets, roles, paths, or policies exist in multiple conflicting places.
- **Membrane mismatch** — dev/staging do not reproduce the real boundary conditions of production.
- **Homeostasis illusion** — the system looks healthy in one path, but another access path, operator path, or degraded state is broken.
- **Immune weakness** — only happy-path tests exist, so negative cases, corrupted inputs, and drift survive until production.
- **Hysteresis** — reruns, rollbacks, or partial failures leave dirty state behind (stale volume, cache, label, secret, ACL, artifact).
- **Memory loss** — the incident is fixed once but never translated into a runbook entry, mutation test, or anti-regression guardrail.

Read `references/models.md` for the full biology + physics mapping.

## Intent Routing

| Signal from user | What to generate |
|---|---|
| "runbook", "troubleshoot", "ops guide", "what do I check first" | Runbook + capture checklist + fast triage decision tree |
| "agent-ready runbook", "N1/N2/N3", "L1/L2/L3", "support tiers", "agent autonomy", "ops pack" | Runbook + support tier matrix + agent autonomy policy + capability contracts |
| "make staging/dev closer to prod", "prod-like", "preprod" | Prod-parity matrix + test ladder + parity gaps |
| "prevent prod bugs", "harden", "resilience", "release gate" | Full resilience blueprint |
| "incident blackbox", "postmortem", "capitalise incident" | Blackbox update + anti-regression battery + runbook delta |
| Empty / vague input | Auto-discover and produce the full blueprint |

## Input

`$ARGUMENTS` can be:

- a **repository root** or **service directory**
- a **system name or short description**
- an **incident document**, runbook, troubleshooting guide, or postmortem
- **empty**, in which case you auto-discover from the current project

### Input Discovery

1. Detect output language first: `git log --oneline -10` + `head -20 README.md`
2. Glob docs: `README*`, `docs/**/*`, `TROUBLESHOOTING*`, `RUNBOOK*`, `OPERATIONS*`, `INCIDENT*`, `POSTMORTEM*`, `BLACKBOX*`
3. Glob tests: `tests/**`, `test/**`, `spec/**`, `e2e/**`, `smoke/**`, `chaos/**`
4. Glob deploy/runtime assets: `Dockerfile*`, `Containerfile*`, `compose*`, `helm*`, `k8s/**`, `manifests/**`, `deploy/**`, `systemd/**`, `quadlet/**`, `*.service`
5. Glob CI assets: `.github/workflows/*`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/**`
6. Read manifests/config: `package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, `.env*`, `*.yaml`, `*.yml`, `*.json`, `*.toml`
7. Search for operator wrappers and diagnostic entrypoints: `scripts/**`, `bin/**`, aliases, helper CLIs, `make`, `justfile`
8. Search for explicit contracts: image refs, ports, secrets, roles, schemas, migrations, registries, health endpoints, backup/restore commands

## The 8 Living-System Models

Read `references/models.md` when you need the detailed definitions, failure smells, and test ideas.

| # | Model | Operational meaning |
|---|---|---|
| 1 | **Genome / DNA** | Single source of truth for contracts, config, naming, image refs, roles, ports |
| 2 | **Membrane / Boundary conditions** | Prod-parity matrix: OS, runtime, network, storage, identities, time, data, external deps |
| 3 | **Homeostasis** | Steady-state health checks, invariants, observability, "first useful signal" |
| 4 | **Immune system** | Negative tests, fuzzing, mutation tests, canaries, pre-mortem |
| 5 | **Stress–strain** | Load, fatigue, budgets, long-run, repeated deploys, storage growth |
| 6 | **Phase transition** | Thresholds where behavior changes qualitatively: disk full, max conn, latency cliffs, failover |
| 7 | **Hysteresis** | Dirty reruns, partial failures, rollback residue, stale caches/volumes/ACLs |
| 8 | **Memory cells** | Runbooks, blackboxes, anti-regression tests, closure criteria |

## Workflow

### Step 1 — Map the failure surfaces

Create a surface map. Minimum surfaces:

- build / packaging / image
- config / contracts / env rendering
- secrets / identity / roles
- deploy / orchestration / fresh install
- network / ports / ingress / service discovery
- storage / ownership / permissions / labels / persistence
- runtime startup / health / logs
- operator wrappers / CLIs / commands
- monitoring / alerts / smoke checks
- backup / restore / migrations / rollback
- CI / release / scanner gates
- docs / examples / commands / aliases

For each surface, capture:

| Surface | Primary source of truth | Typical prod failure | First discriminating probe | Blast radius |

### Step 2 — Extract the genome and invariants

Build an **invariant table**. Every critical behavior must map to one authoritative source.

Examples of invariants:

- exact image reference or artifact identity
- exact secret source and render path
- exact published port and internal bind/listen address
- exact role / ACL / auth path
- exact storage layout and ownership
- exact health endpoint / startup signal
- exact backup / restore command
- exact CI gate for deploy-affecting changes

For each invariant, record:

| Invariant | Source of truth | Where else it appears | Drift risk | Verification command |

**Rule:** if the same operational fact is manually duplicated in multiple places, flag it as **Genome Drift**.

### Step 3 — Build the prod-parity membrane

Create a **Prod-Parity Matrix**. Compare **Observed Dev/Staging** vs **Expected Prod** across these axes:

| Axis | Observed | Expected in prod | Gap | Risk |
|---|---|---|---|---|
| OS / kernel / libc |  |  |  |  |
| CPU / arch |  |  |  |  |
| Container runtime / orchestrator |  |  |  |  |
| Filesystem / volume / SELinux / permissions |  |  |  |  |
| Network topology / DNS / ports / TLS |  |  |  |  |
| Secrets / identity / rotation path |  |  |  |  |
| Data shape / size / anonymized fixtures |  |  |  |  |
| External dependencies / timeouts / rate limits |  |  |  |  |
| Clock / timezone / locale |  |  |  |  |
| Observability stack |  |  |  |  |
| Security / scan / policy gates |  |  |  |  |

**Rules:**

- Never say "prod-like" without naming the boundary conditions that actually match.
- Controlled deviations are acceptable **only if explicitly listed** with risk and compensating tests.
- If no prod exists yet, define the target membrane the future prod must satisfy.

### Step 4 — Derive the test ladder

Read `references/test-ladder.md` for the full ladder, examples, and escalation rules. The rung **semantics** are shared across skills (oci, pipeline, audit-test) in `../shared/gate-ladder.md`; this skill's biology names map onto those rungs. Reproducibility/idempotency techniques (T3 reruns, mutation baselines) are shared in `../shared/determinism.md`.

Use this ladder:

- **T0 — Genome tests**: static contract tests, render checks, lint, schema validation, policy checks
- **T1 — Organelle tests**: image build, component smoke, service-internal tests
- **T2 — Tissue tests**: fresh deploy on clean prod-like host/environment
- **T3 — Organism tests**: operations, rerun/idempotency, operator path, external client path, monitoring, backup/restore
- **T4 — Immune tests**: negative tests, degraded mode, chaos, mutation tests, failover, threshold tests
- **M0 — Memory**: runbook update, blackbox entry, closure criteria, durable guardrail

For every relevant surface, generate **two things**:

1. the **minimum tests to rerun** when that surface changes
2. the **broader matrix** that must be rerun when blast radius is cross-cutting

### Step 5 — Create the mutation and chaos battery

Read `references/mutations.md` for a ready-to-use mutation catalog.

For each critical contract, design at least one **"break it on purpose"** test:

| Mutation | Expected signal | If it passes silently = bug | Minimum level |
|---|---|---|---|
| wrong image ref / artifact ref | deploy or startup fails loudly | hidden pull / wrong artifact | T0/T2 |
| missing or malformed secret | startup/auth fails with useful log | silent fallback / broken auth path | T2/T3 |
| port drift / wrong listen address | health/client path fails deterministically | operator path hides real failure | T2/T3 |
| wrong role / revoked grant | least-privilege test fails | ACL drift undetected | T3 |
| dirty rerun after partial deploy | rerun either converges or fails loudly | snowflake state | T2/T3 |
| disk pressure / quota reduction | graceful alert / degraded mode | silent corruption / surprise outage | T4 |
| latency injection / dependency timeout | retry or graceful degradation | hanging requests / false health | T4 |
| clock skew / timezone change | expiry/TTL tests fail predictably | time-sensitive bugs invisible | T4 |
| stale docs / wrapper mismatch | executable docs test fails | operator follows broken docs | T0/T3 |

**Mutation rule:** if more than two mutations pass silently, the operational safety net has holes.

### Step 6 — Generate the troubleshooting runbook

Read `references/runbook-template.md` before writing.

The runbook MUST include:

1. **Capture before correction** — exact evidence to save before editing anything
2. **Fast triage** — the shortest path to the first discriminating signal
3. **Decision tree** — startup vs runtime vs access-path vs data-path vs monitoring-path
4. **Operator path vs external path** — always separate them
5. **Rollback / containment** — how to stop blast radius without hiding evidence
6. **Anti-regression reruns** — what to rerun after the fix
7. **Closure criteria** — when the incident is truly closed
8. **Agent readiness** — support tier, autonomy level, capability contracts, approval boundary, and escalation bundle

If the user mentions support levels, N1/N2/N3, L1/L2/L3, agent execution, autonomous remediation, MCP tools, or regulated operations, read `references/agent-ops.md` and generate an operations pack in addition to the human runbook.

### Step 7 — Capitalise memory

If incident docs or blackboxes already exist:

- map each incident to its missing durable guardrail
- detect repeated confusion patterns ("wrong path", "wrong env", "wrong role", "wrong secret", "wrong runtime assumption")
- propose the exact **anti-regression test**, **runbook delta**, and **source-of-truth correction**

If they do not exist, generate starter templates for:

- incident blackbox entry
- recurring hurdle / integration confusion entry
- pre-deploy checklist
- post-deploy smoke checklist

### Step 8 — Score resilience

Read `references/scoring.md` for the detailed 15-dimension framework. The score (≥ 45/60 + mutation tests pass) is this skill's post-verification gate — the 3-phase definition-of-done structure (pre → during → post) is canonical in `../shared/done-gate.md`.

Score each dimension **0–4**:

| # | Dimension | 0 | 4 |
|---|---|---|---|
| D1 | Contract Genome | scattered facts | single source + verified renders |
| D2 | Boundary Parity | toy env | prod-like matrix with explicit gaps |
| D3 | Build Reproducibility | snowflake build | reproducible build + smoke |
| D4 | Fresh Deploy | never tested | clean prod-like deploy validated |
| D5 | Rerun / Hysteresis | reruns break state | reruns converge or fail loudly |
| D6 | Runtime Homeostasis | vague health | discriminating health + invariants |
| D7 | Network Path Fidelity | path confusion | all paths explicit and tested |
| D8 | Secrets / Identity / Roles | manual drift | rendered, rotated, verified least privilege |
| D9 | Data / Recovery | no restore proof | restore/rollback path proven |
| D10 | Observability | noisy logs only | first useful error quickly reachable |
| D11 | Operability | manual tribal knowledge | wrappers + runbook + smoke |
| D12 | Immune Tests | happy path only | systematic negative/mutation/property tests |
| D13 | Chaos / Degraded Mode | none | degraded states tested intentionally |
| D14 | CI / Release Gate Convergence | false green possible | runtime risk mapped to real gates |
| D15 | Memory / Runbook / Blackbox | incidents evaporate | every incident leaves guardrails |

**Target score:** **> 45/60 (75%)** for a production-bound system.

### Step 9 — Produce a prioritized action plan

Use 3 tiers (tier semantics are canonical in `../shared/triage.md` — Tier 3 = critical / Tier 2 = major / Tier 1 = minor, independent of GRADE confidence):

- **Tier 3 — Critical:** false green in CI, missing runtime proof, data-loss risk, auth drift, secret drift, deploy non-idempotency, hidden path mismatch
- **Tier 2 — Major:** parity gaps, weak observability, missing degraded-mode tests, incomplete runbook, backup/restore not proven
- **Tier 1 — Minor:** documentation polish, naming cleanup, low-risk UX improvements

Each item must include:

| # | Finding | Tier | Surface | Why it matters in prod | Minimum fix | Minimum rerun |

## Output Format

```markdown
# Resilience Blueprint — {system}
**Date:** {date}
**Target:** {repo/path/system}
**Mode:** {full blueprint | runbook only | parity only | blackbox delta}
**Resilience Score:** {X}/60 — {verdict}

## 1. Failure Surface Map
| Surface | Source of Truth | First Probe | Blast Radius | Notes |

## 2. Prod-Parity Matrix
| Axis | Observed | Expected in Prod | Gap | Risk | Fix |

## 3. Test Ladder
### T0 — Genome
### T1 — Organelle
### T2 — Tissue
### T3 — Organism
### T4 — Immune
### M0 — Memory

## 4. Mutation & Chaos Battery
| Mutation | Expected Signal | Silent Pass Means | Level |

## 5. Troubleshooting Runbook
### Capture Before Correction
### Fast Triage
### Decision Tree
### Rollback / Containment
### Anti-Regression Reruns
### Closure Criteria

## 6. Agent Operations Pack
### Support Tier Matrix
### Agent Autonomy Policy
### Capability Contracts
### Approval and Escalation Boundaries

## 7. Incident Memory / Blackbox Delta
| Incident or Recurrent Hurdle | Missing Guardrail | Add This Test | Add This Runbook Step |

## 8. Dimension Scores
| # | Dimension | Score | /4 | Evidence | Gap |

## 9. Action Plan
### Tier 3 — Critical
### Tier 2 — Major
### Tier 1 — Minor
```

## Mandatory Rules

1. **Never confuse operator path with external user path.** Test both when relevant.
2. **Never say a change is safe because the image or static config passed.** Runtime qualification wins.
3. **If reruns are part of operations, rerun/idempotency is a first-class test.**
4. **Always capture the first useful signal before editing the system.**
5. **Every fix must end in a durable guardrail**: a test, a gate, a runbook delta, or a blackbox entry.
6. **Do not hide parity gaps.** List them explicitly, even if the answer is "accepted risk".
7. **A working happy path is not enough.** Include at least one negative or degraded-mode test per critical surface.
8. **If a `../gotchas.md` file exists, read it before producing output** to avoid repeating known mistakes.

## Dynamic Handoffs

| Condition detected | Recommend | Why |
|---|---|---|
| General test strategy is weak or undocumented | `/cli-audit-test` | Formal test-plan maturity audit |
| CI is slow, flaky, or false-green | `/cli-forge-pipeline` | Pipeline-level biomimetic optimization |
| Operational risk comes from architecture gaps | `/cli-forge-hld` | Capture boundaries, NFRs, and tradeoffs |
| Risk comes from component-level contracts or DB/API design | `/cli-forge-lld` | Tighten low-level contracts |
| Infra/deploy complexity dominates the issue | `/cli-forge-infra` | Simplify and harden delivery path |
| Docs, wrappers, and code disagree | `/cli-audit-sync` | Catch doc-code drift |
| Stress / phase-transition surfaces detected but no perf budget or A/B harness | `/cli-forge-perf` | T4 stress-strain becomes measurable: bench protocol + roofline + reproducible A/B (`../shared/determinism.md`) |
| Data-loss, invariant drift, migration, queue, or transaction failure dominates | `/cli-audit-data` | Apply the PostgreSQL/SQLx safety and repair gate |

**Rule:** recommend handoffs, do not auto-execute them unless the user explicitly asks.

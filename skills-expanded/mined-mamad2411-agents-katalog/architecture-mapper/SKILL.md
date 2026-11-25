---
name: architecture-mapper
description: "Reverse-engineer an unfamiliar or legacy codebase into a drillable, cross-linked architecture knowledge base — per repo or across a polyrepo. Use to map how a system starts, wires together, and flows; or to refresh those docs after code changes. Read-mostly: writes only under docs/, never application code."
metadata:
  author: topia
  version: "0.1.0"
  layer: L2
  model: opus
  group: knowledge
  tools: "Read, Glob, Grep, Write, Edit, Bash"
  emit: architecture.mapped, docs.updated
  listen: codebase.scanned
---

# architecture-mapper

## Purpose

Turn a codebase nobody fully understands into a **navigable knowledge base**:
how it boots, how actors enter, how requests flow through
route→middleware→service→data, what runs in the background, what integrations
exist, what the core entities and steel-threads are — every claim grounded in
`file:line` and labeled **confirmed / likely / speculative**. Output is a set
of **cross-linked** Markdown docs (anchor slugs + clickable Mermaid + a
`## Backlinks` section per file) so a human or a future agent can drill from a
steel-thread into a module into an entity without leaving the docs.

Stack-neutral by design: a generic scaffold + per-stack "hunt hints" selected
at run time. Stack-specific facts about a *particular* product are supplied as
an **applied profile**, never hard-coded into this skill.

<HARD-GATE>
Read-only on application code — write only under `docs/` (and architecture-focused sections of repo-root `CLAUDE.md` when explicitly mapping for onboarding). Every architectural claim MUST carry a confidence label (**confirmed** / **likely** / **speculative**) and cite `file:line`. Do not invent runtime behavior or apply pattern labels without code evidence.
</HARD-GATE>

## Triggers

- `/topia architecture-mapper` — full map (run-all pipeline)
- `/topia architecture-mapper refresh` — incremental update after code changed (post-merge)
- `/topia architecture-mapper <pass>` — run a single pass (see Modes)
- Called by `onboard` (optional escalation) for complex/legacy repos
- Called by `audit` / `improve-architecture` when they need a current map
- Called by `build` when architecture docs are stale relative to changed code

## Calls (outbound)

- `recon` (L2): scan the repo for entry points, routes, models, jobs — do not reimplement scanning here
- `team` (L1): in a polyrepo, fan out one mapping stream per repo (optional, large targets)
- `journal` (L3): record unknowns / ADRs for genuinely opaque areas

## Called By (inbound)

- `onboard` (L2): optional escalation for complex/legacy repos lacking architecture docs
- `audit` (L2): to compute / refresh the architecture picture
- `improve-architecture` (L2): consumes the map as its starting point
- `build` (L1): when architecture docs are stale relative to changed code
- User: `/topia architecture-mapper` direct invocation

## Modes

All pass logic lives in `references/passes/`. Before any pass:

1. Read `references/detection.md` and detect the stack profile
2. Read `references/stacks/<profile>.md` for hunt hints
3. Read `references/conventions.md` for cross-link rules
4. Invoke `topia:recon` if no recent `codebase.scanned` context exists

### Full map — `/topia architecture-mapper`

Runs `references/passes/run-all.md` (the former `/architecture-run-all`). Executes passes in order, checkpointing into `docs/architecture/progress.md`; safe to resume. Supports `--checkpoint` for milestone pauses.

Pass order:

1. bootstrap → repo-inventory → module-map
2. entry-trace → ui-surface-map → request-lifecycle
3. data-model-map → background-jobs → integrations-map
4. steel-threads → workflows → data-flow
5. flowchart → critic → index → report

### Refresh — `/topia architecture-mapper refresh`

Incremental update scoped to git diff since last docs commit. See `references/passes/refresh.md`. Use sonnet model tier when possible.

### Individual passes

| Mode | Pass file | Primary output |
|------|-----------|----------------|
| `bootstrap` | `references/passes/bootstrap.md` | `repo-inventory.md`, `entry-points.md`, `progress.md`, `unknowns.md` |
| `repo-inventory` | `references/passes/repo-inventory.md` | deepens `repo-inventory.md` |
| `module-map` | `references/passes/module-map.md` | `module-map.md` |
| `entry-trace` | `references/passes/entry-trace.md` | deepens `entry-points.md`, frontend-to-api map |
| `ui-surface-map` | `references/passes/ui-surface-map.md` | `ui-surface-map.md` |
| `request-lifecycle` | `references/passes/request-lifecycle.md` | `api-lifecycle.md` |
| `data-model-map` | `references/passes/data-model-map.md` | `data-models.md` |
| `background-jobs` | `references/passes/background-jobs.md` | `background-jobs.md` |
| `integrations-map` | `references/passes/integrations-map.md` | `integrations.md` |
| `steel-threads` | `references/passes/steel-threads.md` | `steel-threads.md` |
| `workflows` | `references/passes/workflows.md` | `workflows.md` |
| `data-flow` | `references/passes/data-flow.md` | `data-flow.md` |
| `flowchart` | `references/passes/flowchart.md` | `system-flowchart.md` |
| `critic` | `references/passes/critic.md` | link-health fixes across docs |
| `index` | `references/passes/index.md` | `INDEX.md` |
| `report` | `references/passes/report.md` | `final-report.md` |

See `references/command-catalog.md` for execution order rationale and early-stop guidance.

## Workflow

### Step 0 — Stack detection

Read `references/detection.md`. Walk the precedence table with Glob + Read. Present evidence to the user and confirm or override the profile before writing docs.

### Step 1 — Scan (if needed)

If `codebase.scanned` context is stale or missing, invoke `topia:recon` on the target root. Use scan output; do not reimplement file discovery.

### Step 2 — Execute mode

Load the pass file for the requested mode and execute its instructions against the target repo. Seed from `references/doc-seeds/` when `docs/architecture/` is empty.

### Step 3 — Emit signals

On completion, emit `architecture.mapped` (full map or meaningful partial) and `docs.updated` when files under `docs/architecture/` changed.

**Applied profile** — if the caller supplies a product stack profile (repo map, connections, known smells), treat it as **input context**. Verify claims against current source before restating.

## Output Format

```
docs/architecture/
  INDEX.md          # hub + drill-down entry point
  repo-inventory.md  module-map.md  entry-points.md
  api-lifecycle.md   data-models.md  background-jobs.md  integrations.md
  ui-surface-map.md  steel-threads.md  workflows.md  data-flow.md
  system-flowchart.md  final-report.md  progress.md  unknowns.md
# + per-repo: CLAUDE.md architecture sections (when mapping for onboarding)
```

## Returns

| Field | Type | Description |
|-------|------|-------------|
| `status` | enum | `MAPPED` / `REFRESHED` / `NO_CHANGES` / `BLOCKED` |
| `docs_written` | string[] | paths created or updated this run |
| `link_health` | object | `{ checked, broken }` from the critic pass |
| `unknowns` | string[] | opaque areas recorded in `unknowns.md` |

## Constraints

1. MUST be read-only on application code — write only under `docs/` and architecture sections of `CLAUDE.md` when mapping for onboarding.
2. MUST label every architectural claim **confirmed / likely / speculative** and cite `file:line`.
3. MUST keep product/stack-specific facts in an **applied profile**, never hard-coded in the skill.
4. MUST scope `refresh` to changed code only; do not rewrite unchanged docs.
5. MUST NOT invent runtime behavior or apply pattern labels without specific code evidence.
6. MUST follow `references/conventions.md` (anchor slugs, clickable Mermaid ≥80%, `## Backlinks`).
7. MUST NOT overwrite onboard-owned `CLAUDE.md` sections (invariants, contract pointers) when both skills run on the same repo.

## Sharp Edges

| Failure Mode | Severity | Mitigation |
|---|---|---|
| README claims trusted over code | HIGH | verify in source; README is a hint, not truth |
| Full re-map run on every small change | MEDIUM | use `refresh` mode; full map only when many areas moved |
| Cross-repo relative links that break when one repo is checked out alone | MEDIUM | reference siblings by designation (e.g. `org/repo`), not relative paths |
| Stack facts leaking into the generic skill | HIGH | applied profile only; never commit instance data into `references/` |
| onboard and mapper both rewrite CLAUDE.md | MEDIUM | mapper owns arch sections; onboard owns invariants/contract blocks |

## Self-Validation

<HARD-GATE>
Before reporting done:
- [ ] every doc ends with a `## Backlinks` section
- [ ] all intra-doc anchor links resolve (run critic/link-health pass)
- [ ] ≥80% of addressable Mermaid nodes carry a click directive
- [ ] no `{{placeholder}}` tokens remain in any generated file
- [ ] every non-trivial claim carries a confidence label + file:line
IF ANY check fails → fix before reporting done.
</HARD-GATE>

## Done When

- The pass set completed and `INDEX.md` + `final-report.md` exist (full map), OR only the changed docs were updated (refresh)
- Link-health pass reports 0 broken anchored links
- `unknowns.md` records anything genuinely opaque
- Structured report emitted (see Returns)

## Cost Profile

Full map: **high** (multi-pass; often parallel per-repo streams on a polyrepo) — opus.
Refresh: **low** (scoped to a git diff) — sonnet is sufficient.

Single-pass modes: **medium** — sonnet unless the pass is steel-threads or critic on a large repo.

**Scope guardrail:** Do not refactor or modify application code — only produce or refresh documentation. Refactor opportunities go to `improve-architecture`; this skill maps, it does not change.

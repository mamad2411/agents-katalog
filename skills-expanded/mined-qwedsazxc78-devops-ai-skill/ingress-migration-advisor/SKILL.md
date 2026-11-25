---
name: ingress-migration-advisor
description: >
  Read-only planner that inventories every Ingress in a Kustomize repo,
  scores each service on five migration-readiness dimensions, and
  recommends one of four paths per service (direct-gateway, two-step,
  swap-only, defer). Output is a Mermaid Gantt plan plus ready-to-paste
  Zeus commands. Critical traffic-tier services are vetoed to defer.
  Services already on Traefik Ingress (sourceClass=traefik) auto-route to
  direct-gateway. Never mutates the repo; produces docs/reports/
  ingress-migration-advisor/<slug>/plan.md and state.yaml. Use for
  end-of-life planning (ingress-nginx EOL 2025), migration sequencing,
  or per-service path advisory. Requires docs/ingress-tier-map.yaml in
  the consumer repo.
version: "1.0.0"
---

# ingress-migration-advisor Skill

Invoked by Zeus pipeline `*ingress-migration-advisor`.

This skill sits **upstream** of the three migration skills
(`nginx-to-traefik`, `gateway-api-migration`, `nginx-to-gateway`). It does
not invoke them — it produces a recommendation plan, and the operator runs
each batch through Zeus manually using the suggested commands.

Read this skill in full before answering questions about "which path
should I migrate service X on" or "what is our EOL migration plan".

## Canonical references

| File | When to read |
|---|---|
| `references/scoring-model.md` | Step 2 — the five-dimension rubric + critical-tier veto rule |
| `references/decision-matrix.md` | Step 3 — score-band → path mapping + sourceClass shortcut |
| `references/plan-template.md` | Step 5 — Mermaid Gantt + per-service table + per-batch command block |

## Bundled scripts

| Script | Used by | Purpose |
|---|---|---|
| `scripts/inventory_all_ingresses.py` | Step 1 | Build every overlay, classify rendered Ingresses (reuses classify_ingress.py from gateway-api-migration) |
| `scripts/score_services.py` | Step 2, 3 | Apply veto + rubric, decide path per service, emit decisions |
| `scripts/render_plan.py` | Step 5 | Substitute plan-template.md with state.yaml data |

The scripts produce structured JSON / YAML. The model's job is to invoke
them and weave their output into the report — not to re-derive scoring or
decision logic in natural language.

## Activation

Triggered explicitly by `*ingress-migration-advisor` from Zeus. Auto-triggered
also by descriptions containing: NGINX Ingress EOL, ingress-nginx end-of-life,
migration plan, which path should I migrate, per-service advisor.

## Invocation forms

```
*ingress-migration-advisor                              # interactive: prompts for deadline + batch size
*ingress-migration-advisor --deadline 2025-10-31        # explicit deadline (ISO date)
*ingress-migration-advisor --deadline 2025-10-31 --batch-size 5
*ingress-migration-advisor --target-path two-step       # override per-service decision (single global path)
*ingress-migration-advisor --strict-tier-map            # HALT on tier-map entries not present in inventory
*ingress-migration-advisor --bake-buffer-days 30        # buffer between final cutover and deadline (default 30)
*ingress-migration-advisor --resume <state-path>        # re-render plan from existing state without re-scoring
```

`--target-path` valid values: `direct-gateway`, `two-step`, `swap-only`.
When set, the scoring still runs (for the report) but every
non-vetoed service is bound to the override path.

## Step Flow

| Step | Action | Script |
|---|---|---|
| 0 | Tool check (`kustomize`, `yq`, `git`, `python3`) | inline `command -v` |
| 0b | Read `docs/ingress-tier-map.yaml`; prompt for deadline + batch size | inline |
| 1 | Inventory every Ingress across all overlays | `inventory_all_ingresses.py` |
| 2 | Score each non-vetoed service on 5 dimensions | `score_services.py` |
| 3 | Decide path per service (veto → sourceClass shortcut → score bands) | `score_services.py --decide` |
| 4 | Batch services by path + deadline pressure | inline |
| 5 | Render `plan.md` (Mermaid Gantt + per-service table + commands) | `render_plan.py` |
| 6 | Print summary to session; never auto-commit | inline |

### Step 0 — Tool check

Run `command -v kustomize yq git python3`. HALT on any missing with install
hints (`brew install kustomize yq jq` on macOS, equivalent apt/dnf on Linux).
No cluster tools required — this skill is offline.

### Step 0b — Operator inputs

Two prompts + one required file:

1. **EOL deadline (ISO date)** — e.g. `2025-10-31`. Defaults: if `--deadline`
   is set, skip prompt. If a previous `state.yaml` exists under
   `docs/reports/ingress-migration-advisor/`, suggest the prior value.
2. **Tier map file** — read `docs/ingress-tier-map.yaml` from the consumer
   repo root. **HALT** if missing with:

   > `docs/ingress-tier-map.yaml not found. The advisor requires an explicit
   > tier map so critical services are never auto-scheduled. Create the file
   > with the format documented at the bottom of this SKILL.md, then re-run.`

   Validate: every service in the map should exist in the inventory written
   at Step 1. If `--strict-tier-map` is set, missing services HALT;
   otherwise WARN. Services in inventory but missing from the map default
   to `standard` with per-service WARN.
3. **Batch size cap** — max services per migration batch. Default `5`.
   Override via `--batch-size <n>`.

Persist to `state.yaml.inputs`.

### Step 1 — Inventory

Discover every overlay matching `*/overlays/*/kustomization.yaml` under
`common.*/`. Build each with `kustomize build`. Pipe each build through
`classify_ingress.py` (imported as a library from
`gateway-api-migration/scripts/`). Group by service name, deduplicate
across envs.

Invoke `scripts/inventory_all_ingresses.py`. Output written to
`state.yaml.inventory[]`. HALT if zero Ingresses found (nothing to plan)
or if every `kustomize build` fails.

### Step 2 — Score

Invoke `scripts/score_services.py --inventory <inv.json> --tier-map docs/ingress-tier-map.yaml`.

The script:
1. For each service, checks the veto rule (critical tier → mark vetoed).
2. For each non-vetoed service, scores the five dimensions per
   `references/scoring-model.md`.
3. Emits per-service scores to `state.yaml.scores[]`.

Score range: **4–14**. Critical tier means traffic-tier dimension is
scored 2 (not 3) because tier-3 is reserved for the veto path.

### Step 3 — Decide path

Same script with `--decide` flag, reads the scores it just wrote.
Decision order (encoded in `references/decision-matrix.md`):

1. **Vetoed** → `defer` (record `vetoReason: critical-tier`)
2. **sourceClass == traefik** → `direct-gateway`
3. **Score-based bands** (nginx-source services only):
   - 4–7 → `direct-gateway`
   - 8–10 → `two-step`
   - 11–13 → `swap-only`
   - 14 → `defer`

If `--target-path` is set, override all non-vetoed decisions to that path
and record `decision.overrideReason: "--target-path <value>"`.

Emit `state.yaml.decisions[]` with `service`, `path`, `advisoryPath` (the
score-derived path even when vetoed, for the report's deferred section),
`vetoReason`, `overrideReason`, and `suggestedCommand`.

### Step 4 — Batch

Group decisions where `path != defer` by:

- Same `path`
- Similar score range (±2)
- Same target env priority (sort: low-tier first, standard next; critical
  is always deferred)

Constraints:
- Max `batchSizeCap` services per batch
- All envs of one service in the same batch (no split-brain)
- Total schedule must fit in `deadline - bakeBufferDays`

Schedule batches at weekly cadence starting from "next Monday". If the
schedule overflows the deadline, surface a WARN banner in the plan header
and continue.

Emit `state.yaml.batches[]`. **Deduplicate commands at the overlay level**:
`*gateway-migrate <overlay>` processes every nginx-source Ingress in that
overlay in one invocation, so 5 services × 3 envs collapse to 3 unique
commands (one per env), not 15. Same for `*nginx-to-gateway <env>`. Only
`*nginx-to-traefik <env> <service>` is service-specific.

```yaml
batches:
  - id: b1
    path: direct-gateway
    services: [grafana, kibana]
    targetWeek: 2025-07-07
    estimatedDuration: 1 week
    commands:
      # Deduplicated: one command per overlay processes all services
      - "*gateway-migrate common.service/overlays/dev --source-class nginx --gateway-class traefik"
      - "*gateway-migrate common.service/overlays/stg --source-class nginx --gateway-class traefik"
      - "*gateway-migrate common.service/overlays/prd --source-class nginx --gateway-class traefik"
```

### Step 5 — Render plan

Invoke `scripts/render_plan.py --state <state.yaml> --template references/plan-template.md --out plan.md`.

The template includes:
- Header (deadline, totals per path tier, # deferred, bake-buffer banner)
- Mermaid Gantt (one bar per batch, dated to `targetWeek`)
- Per-service decision table (service | source class | tier | score |
  path | rationale)
- Per-batch Zeus command blocks
- Deferred services + risk register
- Audit (operator inputs, schema version, run id)

Unresolved `{{placeholders}}` are surfaced as a banner at the top of the
plan — informational, not a failure.

### Step 6 — Summary

Print to the session:

```
Plan: docs/reports/ingress-migration-advisor/<slug>/plan.md

  Total services:        18
  direct-gateway:         3  (1 batch, week of 2025-07-07)
  two-step:              12  (3 batches, weeks of 2025-07-21 → 2025-09-01)
  swap-only:              2  (1 batch, week of 2025-09-15)
  defer:                  1  (kafka-proxy — critical-tier veto)

  Deadline:              2025-10-31
  Bake buffer:           30 days
  Final cutover by:      2025-10-01 (29 days margin)
```

## State file (`state.yaml`)

Path: `docs/reports/ingress-migration-advisor/<isodate>-<ulid>/state.yaml`.

```yaml
schemaVersion: 1
skillVersion: "1.0.0"
runId: <ulid>
createdAt: <iso>
inputs:
  deadline: 2025-10-31
  bakeBufferDays: 30
  batchSizeCap: 5
  targetPathOverride: null
  strictTierMap: false
  tierMap:
    argocd-server: critical
    grafana: standard
    kibana: low
inventory:
  - service: argocd-server
    namespace: argocd
    sourceClass: nginx
    envs: [dev, stg, prd]
    modulePathPerEnv:
      dev: common.service/overlays/dev
      stg: common.service/overlays/stg
      prd: common.service/overlays/prd
    hostsPerEnv:
      dev: [argocd.dev.example.com]
      stg: [argocd.stg.example.com]
      prd: [argocd.example.com]
    annotations:
      total: 12
      cors: false
      authPresent: false
      stubbedLikely: 0
      unknownLikely: 1
    tlsMode: secret
    pathTypes: [Prefix]
    backendResolved: true
scores:
  - service: argocd-server
    vetoed: true
    vetoReason: critical-tier
    dimensions: {}     # empty when vetoed; otherwise see below
  - service: grafana
    vetoed: false
    dimensions:
      annotationComplexity: 1
      tlsMode: 1
      hostnameCount: 1
      trafficTier: 1
      securityAnnotations: 1
    total: 5
decisions:
  - service: argocd-server
    path: defer
    advisoryPath: two-step    # what the score would have said
    vetoReason: critical-tier
    overrideReason: null
    suggestedCommand: null
  - service: grafana
    path: direct-gateway
    advisoryPath: direct-gateway
    vetoReason: null
    overrideReason: null
    suggestedCommand: "*gateway-migrate common.service/overlays/dev --source-class nginx --gateway-class traefik"
batches:
  - id: b1
    path: direct-gateway
    services: [grafana, kibana]
    targetWeek: 2025-07-07
    estimatedDuration: 1 week
deferred:
  - service: argocd-server
    reason: "critical-tier veto"
    advisoryPath: two-step
warnings: []
verdict: PASS | WARN | FAIL
reportPath: docs/reports/ingress-migration-advisor/<slug>/plan.md
```

## Halt conditions

| Step | Halt cause |
|---|---|
| 0 | Required tool missing |
| 0b | Deadline in the past |
| 0b | `docs/ingress-tier-map.yaml` missing |
| 0b | Tier-map references services not in inventory **and** `--strict-tier-map` is set |
| 1 | Zero Ingresses found |
| 1 | `kustomize build` fails across all overlays |
| 2 | Scoring script crash (treat as bug — report and re-run) |
| 5 | Template substitution fails entirely (file write error) |

WARN-not-HALT:
- Services in inventory missing from tier map → defaults to `standard`
- Orphan tier-map entries (without `--strict-tier-map`)
- Schedule overflows `deadline - bakeBuffer`

## Tier map file format

`docs/ingress-tier-map.yaml` — sibling of `docs/PROJECT.md`. Reviewed
via PR like any policy change.

```yaml
schemaVersion: 1
services:
  argocd-server:   critical
  harbor:          critical
  grafana:         standard
  kibana:          standard
  chartmuseum:     standard
  mlflow:          low
  registry-mirror: low
# Services not listed default to "standard" with a WARN.
```

Valid tier values: `critical`, `standard`, `low`. Anything else is a
HALT at Step 0b regardless of `--strict-tier-map` (validation error,
not policy decision).

## Principle: never surprise the operator

Four invariants:

1. **Read-only.** No file mutations, no `kustomize build` side-effects
   beyond `/tmp`, no git operations, no DNS edits. Re-running the advisor
   is always safe.
2. **Critical-tier veto is policy, not a flag.** The tier map is the one
   source of truth. To migrate a critical service, the team PRs the tier
   map first.
3. **Recommendations, not commands.** The plan suggests Zeus commands
   ready to copy-paste; the operator chooses when to run each one. The
   advisor never invokes A/B/C skills directly.
4. **Plans age.** Each run is a point-in-time snapshot. `--resume` only
   re-renders the report from existing state; it does NOT refresh
   inventory or scores. Re-run from scratch when the repo shifts.

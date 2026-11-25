---
name: nginx-to-gateway
description: >
  Thin orchestrator that chains nginx-to-traefik (class swap) and
  gateway-api-migration (resource swap) against one Kustomize module in
  one operator session. Owns no conversion logic. Invokes skill A first,
  reads its outputs.traefikIngresses[] hand-off contract, then invokes
  skill B with --source-class traefik --no-redirect and the chosen
  --gateway-class. Produces a single combined index document linking
  both sub-reports. Each phase keeps its own state file; this skill
  records the chain in docs/reports/nginx-to-gateway/<slug>/index.yaml.
version: "1.0.0"
---

# nginx-to-gateway Skill

Invoked by Zeus pipeline `*nginx-to-gateway`.

## What this skill does NOT do

- No DNS scripts. No cluster apply. No auto-commit.
- No state merging — each sub-skill owns its own state file.
- No re-validation of A's outputs — B's classifier reads them fresh.

## Canonical references

| File | When to read |
|---|---|
| `references/chain-report-template.md` | Step C.5 — index.md rendering |

## Sub-skills invoked

| Phase | Skill | Notes |
|---|---|---|
| A | `nginx-to-traefik` | invoked with the env (or env+batch) passed by operator |
| B | `gateway-api-migration` | invoked with `--source-class traefik --no-redirect --gateway-class <chosen> --source-state <A's state.yaml>` |

## Activation

Triggered explicitly by `*nginx-to-gateway` from Zeus. Not auto-triggered.

## Invocation forms

```
*nginx-to-gateway                                  # interactive
*nginx-to-gateway <env>                            # full env, both phases
*nginx-to-gateway <env> --gateway-class traefik    # default
*nginx-to-gateway <env> --gateway-class gke-l7-global-external-managed
*nginx-to-gateway <env> --resume
*nginx-to-gateway <env> --skip-a                   # phase A already done — resume from B
*nginx-to-gateway <env> --skip-b                   # only do phase A
```

## Step flow

| Step | Action | Halt condition |
|---|---|---|
| C.0 | Merged tool check (A's Step 0 ∪ B's Step 0) | any required tool missing |
| C.1 | Create chain run-dir `docs/reports/nginx-to-gateway/<slug>/` with `index.yaml` | dir exists without `--force` |
| C.2 | Invoke skill A as a subroutine (writes its own state.yaml + report) | A's HALT |
| C.3 | Read A's `outputs.traefikIngresses[]`; record A's state path in chain `index.yaml.phaseA` | A produced zero outputs |
| C.4 | Invoke skill B with `--source-class traefik --no-redirect --gateway-class <chosen> --source-state <A's state.yaml>` | B's HALT |
| C.5 | Render combined `index.md` from `references/chain-report-template.md` | informational |

### Step C.0 — Tool check

Run `command -v` for: `kustomize`, `yq`, `git`, `python3`, `kubectl`, `jq`.
HALT on any missing.

### Step C.1 — Create chain run-dir

Slug format: `<env>-<isodate>-<ulid>` where ULID is generated locally.
Path: `docs/reports/nginx-to-gateway/<slug>/`. Initial `index.yaml`:

```yaml
schemaVersion: 1
skillVersion: "1.0.0"
chainId: <ulid>
env: <env>
gatewayClass: <gatewayClass>
createdAt: <iso>
phaseA: { status: pending }
phaseB: { status: pending }
verdict: IN_PROGRESS
```

If the directory exists and `--force` is not set, HALT.

### Step C.2 — Invoke skill A

Spawn skill `nginx-to-traefik` as a subroutine (same operator session).
Pass through `--resume` if set. If skill A halts, set
`index.yaml.phaseA.status: failed`, `index.yaml.phaseB.status: blocked`,
`index.yaml.verdict: FAIL`, and HALT the chain.

If `--skip-a` was passed:
- Skip C.2.
- Operator must supply `--phase-a-state <path>` pointing at a completed
  skill A state.yaml. Validate the file: `verdict: COMPLETE` and at least
  one `outputs.traefikIngresses[]` entry. HALT otherwise.

### Step C.3 — Hand-off

Read A's state file. Copy:
- `state.yaml.outputs.traefikIngresses[]` → `index.yaml.phaseA.traefikIngresses`
- `state.yaml.steps."10".status` → `index.yaml.phaseA.cutover.status`
- A's state path → `index.yaml.phaseA.statePath`
- A's report path → `index.yaml.phaseA.reportPath`

HALT if `traefikIngresses[]` is empty (A produced no outputs).

### Step C.4 — Invoke skill B

Spawn skill `gateway-api-migration` with arguments:

```
gateway-migrate <common.service/overlays/<env>> \
  --source-class traefik \
  --no-redirect \
  --gateway-class <gatewayClass-from-C.1> \
  --source-state <index.yaml.phaseA.statePath>
```

If skill B halts, set `index.yaml.phaseB.status: failed`,
`index.yaml.verdict: FAIL`. Resume re-runs C.4 only.

If `--skip-b` was passed, skip C.4 + C.5; set
`index.yaml.phaseB.status: skipped`, `index.yaml.verdict: COMPLETED_A_ONLY`,
HALT chain cleanly.

### Step C.5 — Render combined report

Load `references/chain-report-template.md`. Substitute `{{ ... }}`
variables from `index.yaml`. Write to `index.md` alongside `index.yaml`.

Set `index.yaml.verdict: PASS` if both phases completed, else
`COMPLETED_WITH_MANUAL_REVIEW` if any sub-skill had WARN-level findings,
else `FAIL`.

## Failure semantics summary

- A halts → C halts immediately; B is not invoked; `phaseB.status: blocked`.
- B halts after A completed → A's outputs intact; resume runs B only (`--skip-a`).
- C halts after B completed but before rendering index → resume re-runs C.5 only.

## Chain state file (`index.yaml`)

```yaml
schemaVersion: 1
skillVersion: "1.0.0"
chainId: <ulid>
env: dev
gatewayClass: traefik
createdAt: 2026-05-14T10:00:00Z
phaseA:
  status: completed | failed | skipped
  statePath: docs/reports/nginx-to-traefik/<slug-a>/state.yaml
  reportPath: docs/reports/nginx-to-traefik/<slug-a>/report.md
  traefikIngresses: [...]
phaseB:
  status: completed | failed | skipped | blocked
  statePath: docs/reports/gateway-migration/<slug-b>/state.yaml
  reportPath: docs/reports/gateway-migration/<slug-b>/report.md
verdict: PASS | COMPLETED_WITH_MANUAL_REVIEW | COMPLETED_A_ONLY | FAIL
```

Note v1.11.0 vs v2.0.0: in v1.11.0 phase B writes to
`docs/reports/gateway-migration/`. After the v2.0.0 rename, the path
becomes `docs/reports/ingress-to-gateway/`. Skill C records whichever
the sub-skill produces — no special-casing.

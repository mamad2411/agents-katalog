---
name: ingress-controller-install
description: >
  GitOps-flavored Traefik Ingress Controller bootstrap, env addition, or
  chart upgrade in a Kustomize + ArgoCD repo. Operates exclusively on
  files under `common.traefik/` (base, overlays, argocd manifests).
  Never runs `helm install` or `helm upgrade` — those are ArgoCD's job.
  Plan-only: edits Kustomize files, emits the `git add` / commit / push
  commands, and the operator drives git. Validates coexistence with
  `ingress-nginx` via Kustomize-build inspection (no live cluster
  required). Use for new-cluster bootstrap, adding a new env overlay,
  or bumping the Traefik chart version.
version: "1.14.0"
---

# ingress-controller-install Skill

Invoked by Zeus pipeline `*install-traefik`. This is the GitOps companion
to `*decommission-nginx` — both manipulate the `common.*/` Kustomize
modules ArgoCD reconciles, never the live cluster directly.

## What this skill is NOT

- Not a `helm install` / `helm upgrade` runner — those would conflict
  with ArgoCD reconciling the same release.
- Not a cluster mutator — the only side effects are edits to repo files
  under `common.traefik/`.
- Not an ArgoCD application applier — the operator runs
  `kubectl apply -f common.traefik/argocd/<env>.yaml` after committing.

## Modes

The skill auto-detects which of three modes applies, based on repo state:

| Mode | Trigger | Action |
|---|---|---|
| `bootstrap` | `common.traefik/` does not exist | Scaffold the whole module from `references/traefik-module-template.yaml` |
| `new-env` | `common.traefik/base/` exists, `overlays/<target-env>/` does not | Copy `overlays/dev/` → `overlays/<target-env>/`, prompt operator for env-specific overrides |
| `upgrade` | `common.traefik/overlays/<target-env>/` exists | Bump the Traefik chart `version:` in `base/kustomization.yaml` AND every `overlays/*/kustomization.yaml`, idempotent |

Override the detected mode with `--mode <bootstrap|new-env|upgrade>`.

## Canonical references

| File | When to read |
|---|---|
| `references/coexistence-checklist.md` | Step 3 — pre-commit checks for IngressClass / LB IP / port collision (read-only, Kustomize-build inspection) |
| `references/values-template.yaml` | Step 2 (bootstrap) — embedded into `base/app.values.yaml` |
| `references/traefik-module-template.yaml` | Step 2 (bootstrap) — Kustomize scaffolding skeleton (kustomization.yaml + base + overlays + argocd) |

## Bundled scripts

| Script | Used by | Purpose |
|---|---|---|
| `scripts/detect_mode.sh` | Step 1 | Inspect repo, decide between bootstrap / new-env / upgrade |
| `scripts/validate_coexistence_kustomize.sh` | Step 3 | Build the planned overlay AND any existing nginx overlay; verify no class / port / LB collision |
| `scripts/upgrade_chart_version.sh` | Step 4 (upgrade mode) | Atomic version bump across base + all overlays + pre-commit consistency check |

## Activation

Triggered explicitly by `*install-traefik` from Zeus. Not auto-triggered.

## Invocation forms

```
*install-traefik                                # interactive: detect mode, prompt as needed
*install-traefik --env dev                      # explicit target env
*install-traefik --env prd --mode new-env       # force new-env mode
*install-traefik --upgrade-to 40.1.0            # upgrade chart version on every overlay
*install-traefik --resume <state-path>          # continue from state.yaml
```

## Output location

```
docs/reports/ingress-controller-install/<isodate>/
  state.yaml          # machine-readable plan + verdict
  plan.md             # operator-readable summary + commit message + git commands
  diff.patch          # unified diff of all proposed file edits (pre-commit preview)
```

The skill **edits files in place** under `common.traefik/`. Before any
edit it writes a backup to `docs/reports/.../backups/` (full file
content, not a diff — matches the safety pattern from
`gateway-api-migration`). On `kustomize build` failure post-edit, the
backup is restored automatically.

## Step Flow

| Step | Action | Script |
|---|---|---|
| 0 | Tool check (`kustomize`, `yq`, `git`) | inline `command -v` |
| 1 | Detect mode + target env | `detect_mode.sh` |
| 2 | Branch on mode: scaffold OR copy-env OR identify upgrade scope | inline |
| 3 | Validate coexistence (read-only Kustomize-build inspection) | `validate_coexistence_kustomize.sh` |
| 4 | Apply edits to `common.traefik/`, with backups | `upgrade_chart_version.sh` (upgrade) or inline (bootstrap / new-env) |
| 5 | `kustomize build` the target overlay; rollback from backups on failure | inline |
| 6 | Render plan.md + diff.patch; print git commands | inline |

### Step 0 — Tool check

Run `command -v kustomize yq git`. HALT on any missing.

### Step 1 — Detect mode

Invoke `scripts/detect_mode.sh --repo-root . --target-env <env>`. The
script returns JSON:

```json
{
  "mode": "bootstrap" | "new-env" | "upgrade",
  "moduleExists": true,
  "baseExists": true,
  "targetEnvExists": false,
  "existingOverlays": ["dev", "stg", "prd"],
  "currentChartVersion": "39.0.8"
}
```

If `--mode` is explicit, the script validates it's compatible with the
detected state (e.g., refuses to bootstrap if `common.traefik/` already
exists, unless `--force` is passed).

### Step 2 — Branch on mode

**`bootstrap`**: Read `references/traefik-module-template.yaml`,
substitute env names, write to `common.traefik/{base,overlays/<env>,argocd}/`.
Read `references/values-template.yaml` and write to
`common.traefik/base/app.values.yaml`. The values file is parameterized
on `${INGRESS_CLASS_NAME}` (default `traefik`), `${LB_IP}` (operator
must supply — never derive from cluster), and `${GATEWAY_API_ENABLED}`
(default `false`).

**`new-env`**: `cp -r common.traefik/overlays/<source-env>/ common.traefik/overlays/<target-env>/`
where `<source-env>` defaults to `dev`. Prompt operator for env-specific
overrides (LB IP, log level, replica count). Apply substitutions.

**`upgrade`**: No file structure changes; only version bumps in Step 4.

### Step 3 — Validate coexistence

Invoke `scripts/validate_coexistence_kustomize.sh --target-env <env>`.

The script does **read-only Kustomize-build inspection** — no live
cluster queries:

| Check | How |
|---|---|
| `classCollision` | Run `kustomize build` on the target overlay + every other `common.*/overlays/<env>/`. Extract every `IngressClass` and every `kubernetes.io/ingress.class` / `spec.ingressClassName`. The proposed Traefik class must not appear in any other module's built output (unless mode is `upgrade` — then collision against the existing Traefik class is expected). |
| `lbIpCollision` | Grep `loadBalancerIP:` and `kubernetes.io/load-balancer-source-ranges` annotations across all module builds. Proposed IP must not appear elsewhere. |
| `portCollision` | For Services with `type: LoadBalancer`, port 80/443 must not be claimed by a non-Traefik release in the target namespace. |

On any collision: HALT with verdict `BLOCKED`. Plan files NOT written.

### Step 4 — Apply edits

**`bootstrap`** and **`new-env`**: write the planned files directly.

**`upgrade`**: invoke `scripts/upgrade_chart_version.sh --target <version>`.
The script:

1. Backs up `base/kustomization.yaml` + all `overlays/*/kustomization.yaml`.
2. Updates `helmCharts[0].version` in each (idempotent via `yq -i`).
3. Verifies all updated versions match the target (consistency check —
   the `traefik-version-consistency` pre-commit hook in the consumer
   repo will enforce this, but the skill catches it first).

### Step 5 — Build + rollback safety

```bash
kustomize build common.traefik/overlays/<target-env> > /tmp/built.yaml
```

If exit != 0: restore all backups from
`docs/reports/.../backups/`, mark verdict `FAIL`, HALT with the
`kustomize` stderr. The repo is left identical to its pre-skill state.

### Step 6 — Render plan + commit message

Write `plan.md` with:
- Detected mode + target env
- Coexistence check results
- File-level summary (created / modified / unchanged)
- The exact git commands the operator runs next:

```bash
git add common.traefik/  # or specific files
git commit -m "feat(traefik): bootstrap controller for <env>"
git push
kubectl apply -f common.traefik/argocd/<env>.yaml  # only for bootstrap / new-env
```

Also write `diff.patch` (full unified diff) so the operator can preview
exactly what changed before staging.

**The skill never auto-commits.** Operator drives git.

## State YAML schema

```yaml
schemaVersion: 1
skillVersion: "2.0.0"
runId: <ulid>
createdAt: <iso>
inputs:
  targetEnv: dev | stg | prd | <custom>
  mode: bootstrap | new-env | upgrade | auto
  upgradeTo: "<chart-version>" | null
  ingressClassName: traefik
  lbIp: "<operator-supplied>"
  gatewayApiEnabled: false
detection:
  moduleExists: true
  baseExists: true
  targetEnvExists: false
  existingOverlays: [dev, stg, prd]
  currentChartVersion: "39.0.8"
validation:
  classCollision: false
  lbIpCollision: false
  portCollision: false
  details: {}
plan:
  mode: upgrade
  filesCreated: []
  filesModified:
    - {path: common.traefik/base/kustomization.yaml, backup: "...", sha256Before: "...", sha256After: "..."}
  filesUnchanged: []
  commitMessage: "chore(traefik): upgrade chart 39.0.8 → 40.1.0"
  gitCommands: [...]
  postApplyCommands:
    - "kubectl apply -f common.traefik/argocd/dev.yaml"
verdict: READY | BLOCKED | NEEDS_REVIEW
reportPath: docs/reports/ingress-controller-install/<slug>/plan.md
```

## Halt conditions

| Step | Halt cause |
|---|---|
| 0 | Required tool missing |
| 1 | Mode mismatch (e.g., `--mode bootstrap` but `common.traefik/` exists), no `--force` |
| 3 | Class / LB IP / port collision |
| 5 | `kustomize build` fails post-edit (backups restored automatically) |

## Principle: GitOps-first

Four invariants:

1. **Never run `helm install` / `helm upgrade` directly.** The
   HelmChartInflationGenerator embedded in
   `common.traefik/overlays/<env>/kustomization.yaml` is the source of
   truth. ArgoCD applies the rendered manifests when the operator
   commits.
2. **Never run `kubectl apply` directly.** The skill prints the
   `kubectl apply -f common.traefik/argocd/<env>.yaml` command but does
   not execute it.
3. **Edit only `common.traefik/`.** No other module is touched.
   Coexistence validation reads but never writes other modules.
4. **Full-file backups before any edit.** On `kustomize build` failure
   post-edit, the backup is restored. Failure mode is "repo unchanged",
   not "repo half-edited".

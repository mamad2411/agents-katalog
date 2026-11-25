---
name: traefik-controller-decommission
description: >
  GitOps-flavored SAFE uninstall of the `ingress-nginx` controller in a
  Kustomize + ArgoCD repo. Verifies cluster + repo are free of
  `ingressClassName: nginx` (precedence-aware: spec wins, legacy
  annotation falls back). After DNS bake confirmation, plans the
  decommission as: archive the `common.ingress-nginx/` (or equivalent)
  Kustomize module, disable the ArgoCD Application, wait for ArgoCD
  prune, then optional LB / IAM cleanup. Never runs `helm uninstall` —
  ArgoCD handles the actual resource removal via prune. Plan-only:
  emits a `commands.sh` for the operator to drive manually.
version: "1.14.0"
---

# traefik-controller-decommission Skill

Invoked by Zeus pipeline `*decommission-nginx`. GitOps companion to
`*install-traefik` — both manipulate the Kustomize modules ArgoCD
reconciles, never the live cluster directly.

## What this skill is NOT

- Not a `helm uninstall` runner — ArgoCD prunes resources when the
  Application is disabled or deleted.
- Not a `kubectl delete` runner — same reason.
- Not a Kustomize editor that touches anything other than the
  ingress-nginx module + its ArgoCD Application manifest.

## Canonical references

| File | When to read |
|---|---|
| `references/decommission-checklist.md` | Step 6 — operator-facing manual checklist (final cluster verifications + rollback recipe) |

## Bundled scripts

| Script | Used by | Purpose |
|---|---|---|
| `scripts/verify_no_nginx_class.sh` | Step 3 | Dual cluster + repo scan (precedence-aware: `spec.ingressClassName == "nginx"` OR null-spec + legacy annotation). Unchanged from v1.12.0; this was already GitOps-correct. |
| `scripts/discover_nginx_module.sh` | Step 1 | Scan `common.*/` for the Kustomize module hosting the ingress-nginx Helm chart; identify its ArgoCD Application manifest. |
| `scripts/generate_decommission_plan.sh` | Step 5 | Render `plan.md` + `commands.sh` for archive + ArgoCD disable + post-prune verify + optional LB/IAM cleanup. |

## Activation

Triggered explicitly by `*decommission-nginx` from Zeus. Not auto-triggered.

## Invocation forms

```
*decommission-nginx                              # interactive
*decommission-nginx --cycle prod-batch-3         # named migration cycle
*decommission-nginx --skip-dns-bake              # NEEDS_REVIEW verdict; not recommended
*decommission-nginx --no-lb-cleanup              # skip Step 5b LB IP release plan
*decommission-nginx --resume <state-path>        # continue from state.yaml
```

## Output location

```
docs/reports/traefik-controller-decommission/<date>/
  state.yaml          # machine-readable state
  verify.json         # raw cluster + repo scan results
  plan.md             # operator-readable plan
  commands.sh         # copy-paste-ready (NEVER auto-executed)
```

## Step Flow

| Step | Action | Script |
|---|---|---|
| 0 | Tool check (`kustomize`, `yq`, `git`, `jq`; `kubectl`, `gcloud` optional with WARN) | inline `command -v` |
| 1 | Discover ingress-nginx Kustomize module + ArgoCD Application path | `discover_nginx_module.sh` |
| 2 | Operator inputs (date, operator, cycle, optional GCP project for LB cleanup) | inline |
| 3 | Verify zero active nginx Ingresses (cluster + repo) | `verify_no_nginx_class.sh --all` |
| 4 | DNS bake-period confirmation | inline interactive prompt |
| 5 | Generate decommission plan + commands.sh | `generate_decommission_plan.sh` |
| 6 | Render state.yaml + print verdict + next-step instructions | inline |

### Step 0 — Tool check

Required: `kustomize`, `yq`, `git`, `jq`. WARN-only: `kubectl`, `gcloud`
(used to render fuller plans but the skill works offline without them).

### Step 1 — Discover ingress-nginx module

Invoke `scripts/discover_nginx_module.sh --repo-root .`. The script:

1. Grep every `kustomization.yaml` for `helmCharts:` blocks naming
   `ingress-nginx`.
2. Find sibling `argocd/*.yaml` files (ArgoCD Application manifests
   pointing at the module).
3. Return JSON with module path, list of overlays, list of ArgoCD app
   manifests, and the destination namespace.

HALT if zero modules match (nothing to decommission) or more than one
matches (ambiguous — operator must pick via `--module <path>` override).

### Step 2 — Operator inputs

Three prompts:

1. **ISO date** (defaults to today)
2. **Operator handle** (defaults to `git config user.email`)
3. **Migration cycle slug** (free text — names the report directory)

Optional:

4. **GCP project** (for the LB IP release plan section). Skip with
   `--no-lb-cleanup`.

### Step 3 — Verify zero active nginx Ingresses

Invoke `verify_no_nginx_class.sh --all`. Two scans:

- Cluster: `kubectl get ingress -A` (skipped if kubectl missing — WARN
  records degraded state).
- Repo: `kustomize build` every `common.*/overlays/<env>/` and extract
  Ingresses with `spec.ingressClassName == "nginx"` OR
  (`spec.ingressClassName == null` AND
  `kubernetes.io/ingress.class == "nginx"`).

**Exit codes**:
- 0 PASS — both scans clean
- 1 BLOCKED — at least one nginx Ingress still active
- 2 DEGRADED — at least one scan couldn't run

BLOCKED → HALT with the list of offending Ingresses. `commands.sh` NOT
written. The operator either re-migrates the leftover or deletes the
stale Ingress before retrying.

### Step 4 — DNS bake confirmation

Interactive:

```
Did the DNS cutover for <cycle> happen at least 72h ago?
Has every monitored hostname returned HTTP 200 via the Traefik LB during
that window with zero traffic on the nginx LB?
[yes/no]
```

Any answer other than `yes` → BLOCKED. Use `--skip-dns-bake` to bypass
(verdict becomes NEEDS_REVIEW so the operator records the override).

### Step 5 — Generate decommission plan

Invoke `scripts/generate_decommission_plan.sh` with env vars:

- `NGINX_MODULE` — path from Step 1 (e.g. `common.ingress-nginx`)
- `ARGOCD_APP_MANIFESTS` — comma-separated list of ArgoCD app YAML paths
- `NGINX_NAMESPACE` — destination namespace from Step 1
- `GCP_PROJECT` — for LB IP release plan (or `<TODO>` placeholder)
- `REPORT_DIR` — absolute path to the report directory

The script renders **three** sections into `plan.md` and a
copy-paste-ready `commands.sh`:

#### 5a. Archive the Kustomize module

```bash
# Make sure we're on the deployment branch
git checkout main && git pull

# Move the entire ingress-nginx module under archive/
git mv common.ingress-nginx/ archive/

# Commit and push (ArgoCD will see the deleted resources and prune them)
git commit -m "chore(ingress-nginx): archive controller module for decommission"
git push
```

#### 5b. Disable + delete the ArgoCD Application

```bash
# For each env (dev → stg → prd or operator's preferred order):
for env in dev stg prd; do
  # Disable auto-sync so ArgoCD doesn't try to recreate
  kubectl patch application <nginx-app-name> -n argocd --type merge \
    -p '{"spec":{"syncPolicy":{"automated":null}}}'

  # Trigger explicit prune. This deletes the Deployment, Service, RBAC,
  # ServiceAccount, Helm Secret, etc. via ArgoCD's pruner.
  kubectl patch application <nginx-app-name> -n argocd --type merge \
    -p '{"operation":{"sync":{"prune":true,"force":true}}}'

  # Wait for prune to finish
  kubectl wait application <nginx-app-name> -n argocd \
    --for=condition=Healthy=False --timeout=5m || true

  # Finally remove the Application manifest itself
  kubectl delete -f common.ingress-nginx/argocd/$env.yaml
done

# Verify zero resources remain in the controller namespace
kubectl get all -n <nginx-namespace>
# Then optionally drop the namespace once empty
kubectl delete namespace <nginx-namespace>
```

#### 5c. (Optional) LB IP release + IAM cleanup

Same as the v1.0.0 Horus-flavored plan: `gcloud compute addresses
list` + delete after confirming no forwarding rule references the IP;
SA enumeration + binding cleanup. Skipped if `--no-lb-cleanup`.

### Step 6 — Render state + summary

Write `state.yaml`, `verify.json`. Print verdict + next-step
instructions:

```
1. Read docs/reports/traefik-controller-decommission/<date>/plan.md
2. Execute commands.sh block-by-block (not in one shot)
3. Commit the report directory once decommission is complete
```

## State YAML schema

```yaml
schemaVersion: 1
skillVersion: "2.0.0"
runId: <ulid>
createdAt: <iso>
inputs:
  date: 2026-05-19
  operator: alex.hsieh
  migrationCycle: prod-batch-3
  gcpProject: awoo-prod
discovery:
  nginxModule: common.ingress-nginx
  argocdAppManifests: [common.ingress-nginx/argocd/dev.yaml, ...]
  nginxNamespace: ingress-nginx
  helmChartVersion: 4.10.0     # informational
verification:
  activeNginxIngresses:
    cluster: []
    repo: []
  dnsBakeConfirmed:
    confirmed: true
    confirmedBy: alex.hsieh
    confirmedAt: 2026-05-19T10:14:00Z
plan:
  archive:
    sourcePath: common.ingress-nginx
    targetPath: archive/common.ingress-nginx
  argocdDisable:
    apps: [...]
    namespace: argocd
  lbRelease:    # null if --no-lb-cleanup
    nginxLbIp: 34.x.x.x
verdict: READY | BLOCKED | NEEDS_REVIEW | DEGRADED
```

## Halt conditions

| Step | Halt cause |
|---|---|
| 0 | Required tool missing |
| 1 | Zero ingress-nginx modules found OR more than one (ambiguous) |
| 3 | Active nginx Ingress in cluster OR repo |
| 4 | Operator declines DNS bake confirmation (without `--skip-dns-bake`) |

## Principle: GitOps-first

Same four invariants as `ingress-controller-install` (its sibling
skill): never run `helm uninstall` / `kubectl delete` directly, only
edit the `common.ingress-nginx/` module, full-file backups before any
edit, plan-only output.

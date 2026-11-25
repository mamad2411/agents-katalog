---
name: nginx-to-traefik
description: >
  Class-swap migration that ports services from NGINX Ingress to Traefik
  Ingress (`ingressClassName: traefik`) while keeping both controllers
  running in parallel. DNS A-records are the only cutover lever. Designed
  for eye-of-horus-gitops conventions: nginx files move to archive/ (never
  deleted), Traefik Ingresses live in kustomization.resources (never
  patches), backend Service names and secretName are written verbatim
  (Kustomize namePrefix does not touch them). Operator-declared LB IPs
  only — never auto-derived from cluster state. State stored in
  docs/reports/nginx-to-traefik/<slug>/.
version: "1.0.0"
---

# nginx-to-traefik Skill

Invoked by Zeus pipeline `*nginx-to-traefik`.

This skill is the **first half** of the chained migration NGINX → Traefik
Ingress → Gateway API. Used standalone it ports a batch of services to
Traefik while leaving the NGINX controller serving everyone else. Used
under skill `nginx-to-gateway` (the orchestrator), its `state.yaml` output
is consumed as the input to skill `gateway-api-migration` with
`--source-class traefik`.

## Canonical references

| File | When to read |
|---|---|
| `references/nginx-to-traefik-env-config.md` | Step 0b — env-config schema and operator prompts |
| `references/annotation-translation.md` | Step 3 — annotation mapping |
| `references/dns-cutover-runbook.md` | Step 10 — printed/linked at end of run |

## Bundled scripts

| Script | Used by | Purpose |
|---|---|---|
| `scripts/inventory_nginx_ingresses.py` | Step 1 | Per-overlay nginx Ingress inventory |
| `scripts/generate_traefik_ingress.py` | Step 3 | Emit `<service>-traefik-ingress.yaml` |
| `scripts/update_kustomization.py` | Step 5, 6 | Idempotent edits to kustomization.yaml + app.ingress.yaml |
| `scripts/validate_cross_consistency.sh` | Step 7b | 4-way DNS↔verify↔ingress↔cert cross-check |

## Activation

Triggered explicitly by `*nginx-to-traefik` from Zeus. Not auto-triggered.

## Invocation forms

```
*nginx-to-traefik                              # interactive: inventory + propose batches
*nginx-to-traefik <env>                        # process all services in one env
*nginx-to-traefik <env> <batch>                # named batch (b1 | b2)
*nginx-to-traefik <env> <service>              # single service
*nginx-to-traefik --resume                     # continue from state.yaml
```

## Step Flow

| Step | Action | Script |
|---|---|---|
| 0 | Tool check (`kustomize`, `yq`, `git`) | inline `command -v` |
| 0b | Load `references/nginx-to-traefik-env-config.md`; prompt operator for Traefik + nginx LB IPs if missing, write to config, then continue | inline |
| 1 | Inventory active nginx ingresses per env | `inventory_nginx_ingresses.py` |
| 2 | Propose batch plan, wait for `y/N` confirmation | inline |
| 3 | Generate `<service>-traefik-ingress.yaml` per service | `generate_traefik_ingress.py` |
| 4 | `git mv` nginx file to `archive/` | inline |
| 5 | Edit `kustomization.yaml`: add Traefik file to `resources:`, drop nginx from `patches:` | `update_kustomization.py` |
| 6 | Update `common.traefik/overlays/<env>/app.ingress.yaml` managed-cert host list | `update_kustomization.py` |
| 7 | `kustomize build` both modules for the env | inline |
| 7b | 4-way consistency check | `validate_cross_consistency.sh` |
| 8 | Update `scripts/dns-create-traefik.sh` batch list | inline |
| 9 | Update `scripts/verify-traefik-<env>.sh` URL list | inline |
| 10 | Print commit message + file list (never auto-commit) | inline |

### Step 0 — Tool check

Run `command -v kustomize yq git`. HALT on any missing.

### Step 0b — Env-config

Read `references/nginx-to-traefik-env-config.md`. If `state.yaml.envConfig`
is missing entries for the target env, issue the 5 prompts listed in the
reference and write the captured values back. Never derive LB IPs from
any cluster resource — this is invariant §5.3 from the spec.

### Step 1 — Inventory

Invoke `inventory_nginx_ingresses.py --overlay-dir
<common.service/overlays/<env>>`. Filter to `ingressClass == "nginx"`.
Write to `state.yaml.inventory[]`. HALT if zero nginx ingresses found.

### Step 2 — Batch plan

Group inventory entries by host TLD + service criticality. Default batches:
`b1` = read-mostly services, `b2` = write-heavy services. Print the proposed
batch plan and ask `y/N`. HALT on decline.

### Step 3 — Generate Traefik Ingress per service

For each service in the active batch, invoke `generate_traefik_ingress.py
--input <service>-nginx-ingress.yaml --output <service>-traefik-ingress.yaml`.
Capture stderr WARN lines into `state.yaml.warnings[]`. Compute SHA256 of
each output for `state.yaml.outputs.traefikIngresses[].sha256`.

### Step 4 — Archive nginx file

`git mv <service>-nginx-ingress.yaml archive/`. HALT if the file is already
under `archive/`. Backup the pre-edit path in `state.yaml.backups[]`.

### Step 5 — Kustomization resource edit

```
update_kustomization.py --overlay-dir <overlay> \
  --replace <service>-nginx-ingress.yaml=<service>-traefik-ingress.yaml \
  --drop-patch <service>-nginx-ingress.yaml
```

The script is idempotent: re-running step 5 on a complete state is a no-op.

### Step 6 — Managed-cert host list

For each new Traefik Ingress, ensure its primary host is present in
`common.traefik/overlays/<env>/app.ingress.yaml.spec.tls[].hosts` and
`spec.rules[].host`. Use `update_kustomization.py --app-ingress
<path> --add-host <host>`.

### Step 7 — kustomize build

```
kustomize build common.service/overlays/<env> > /tmp/svc-build.yaml
kustomize build common.traefik/overlays/<env> > /tmp/traefik-build.yaml
```

HALT on non-zero exit. Roll back step 4–6 via `git restore` of backed-up
files.

### Step 7b — Cross-consistency check

Invoke `validate_cross_consistency.sh` with the four host sources. HALT
on non-zero exit. The stderr stale-host list goes into the report.

### Step 8 — DNS script update

Locate `scripts/dns-create-traefik.sh`. Find or create the array
`HOSTS_<ENV_UPPER>_<BATCH_UPPER>=(...)`. Insert each new host (idempotent
via `grep -q` before append). Record the diff in `state.yaml.steps["8"]`.

### Step 9 — Verify script update

Same pattern as Step 8 but `URLS_<ENV>_<BATCH>` in
`scripts/verify-traefik-<env>.sh`. URL format: `https://<host>/`.

### Step 10 — Print commit message and file list

Never auto-commit. Print:

1. The full set of files touched (Step 3 outputs + Step 4 moves + Step 5/6 edits + Step 8/9 edits).
2. A suggested commit message in Conventional Commits zh-TW style.
3. A pointer to `references/dns-cutover-runbook.md` for the operator to follow after the commit lands.

## State file (`state.yaml`)

The state file lives at `docs/reports/nginx-to-traefik/<slug>/state.yaml`
where `<slug>` is `<env>-<batch>-<isodate>`. Schema:

```yaml
schemaVersion: 1
skillVersion: "1.0.0"
env: dev
batch: b1
createdAt: 2026-05-14T10:00:00Z
envConfig:
  capturedAt: <iso>
  envs:
    dev: { nginxLbIp: ..., traefikLbIp: ..., certIssuer: ..., managedCertNamespace: ..., managedCertResourceName: ... }
inventory:
  - { file: argocd-nginx-ingress.yaml, name: argocd-server, namespace: argocd, hosts: [argocd.dev.example.com] }
batchPlan:
  b1: [argocd-server, grafana]
outputs:
  traefikIngresses:
    - { file: argocd-traefik-ingress.yaml, host: argocd.dev.example.com, namespace: argocd, backend: argocd-server, port: 80, sha256: <hex> }
backups:
  - { path: argocd-nginx-ingress.yaml, restorePath: archive/argocd-nginx-ingress.yaml }
steps:
  "0":  { status: pass }
  "0b": { status: pass, prompts: 0 }
  "1":  { status: pass, count: 2 }
  "2":  { status: pass, confirmed: true }
  "3":  { status: pass, generated: 2, warnings: 0 }
  "4":  { status: pass, moved: 2 }
  "5":  { status: pass, edits: 2 }
  "6":  { status: pass, hostsAdded: 2 }
  "7":  { status: pass }
  "7b": { status: pass, staleHosts: [] }
  "8":  { status: pass, hostsAdded: 2 }
  "9":  { status: pass, urlsAdded: 2 }
  "10": { status: pass }
warnings: []
verdict: COMPLETE
```

The `outputs.traefikIngresses[]` list is the hand-off contract for skill C
(`nginx-to-gateway`): when chained, skill C reads this list and passes
`--source-class traefik --source-state <statePath>` to skill B.

## Halt conditions

| Step | Halt cause |
|---|---|
| 0 | Required tool missing |
| 0b | Operator declines to supply env-config values |
| 1 | Zero nginx Ingresses found |
| 2 | Operator declines batch plan |
| 3 | `generate_traefik_ingress.py` exit code != 0 |
| 4 | File already under `archive/` |
| 5 | kustomization.yaml schema mismatch |
| 7 | `kustomize build` non-zero |
| 7b | Cross-consistency check non-zero |

After halt, the skill writes `state.yaml.verdict: HALTED` with the failing
step. `--resume` re-runs from the failed step.

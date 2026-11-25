---
name: retire-nginx
description: >
  Retire the nginx ingress controller and all nginx Ingress resources from a Kustomize + ArgoCD repo
  after Gateway API / Traefik migration is complete. Supports single-env (dev/stg/prd) or all-envs
  retirement in one command. Use this skill whenever: removing nginx after migration, cleaning up
  dead nginx Ingress resources from a kustomize base, decommissioning the ingress-nginx controller
  ArgoCD Application for an env, or retiring nginx from one environment without touching others.
  Safety-gated: aborts if no HTTPRoutes/Traefik Ingresses found (migration not done). Uses
  $patch: delete in the service overlay kustomization to exclude base nginx Ingress resources
  per-env — base files stay intact for other envs still using them.
version: "1.17.0"
---

# /gitops/retire-nginx — Nginx Ingress Retirement

Retires the nginx ingress **controller** (`common.ingress`) and all nginx **Ingress resources**
(`common.service`) for one or all environments after Gateway API / Traefik migration is complete.

> Run this skill only after:
> - All services have active HTTPRoutes or Traefik Ingresses
> - DNS has been cut over to the Traefik/Gateway LB
> - nginx is confirmed idle (no live traffic)

## Usage

```
/gitops/retire-nginx dev          # Retire dev only
/gitops/retire-nginx stg          # Retire stg only
/gitops/retire-nginx prd          # Retire prd only
/gitops/retire-nginx all          # Retire all envs sequentially (dev → stg → prd)
```

$ARGUMENTS

---

## Core Rules

| Rule | Why |
|------|-----|
| **Never retire without replacement pre-flight** | Removing nginx before Traefik/HTTPRoutes are active causes an outage |
| **$patch: delete in overlay, not base edits** | Base nginx files stay — other envs may still need them; only the target env's kustomization excludes them |
| **Delete only the ArgoCD app yaml** | Delete `common.ingress/argocd/<env>.yaml`; app-of-apps `prune: true` removes the Application from cluster; Application finalizer cascades to delete all controller resources. Overlay becomes dead code — no need to touch it |
| **Validate nginx-class=0 not Ingress-total=0** | Envs with Traefik ingresses will still have `kind: Ingress` resources after retirement — only nginx-class ones must reach zero |
| **Process envs in order for `all`** | dev → stg → prd; validate each before proceeding to avoid cascading failures |
| **Archive dirs are always safe to delete** | Files in `archive/` are never referenced in `kustomization.yaml`; they are rollback snapshots from the migration phase |

---

## Step 1 — Parse Arguments

```
env = $ARGUMENTS   # dev | stg | prd | all
```

If no argument, enter **interactive mode**: detect available environments from `common.ingress/overlays/`
and `common.service/overlays/`, list them, and ask which to retire.

If `all`, build the queue `[dev, stg, prd]` and process each sequentially.

---

## Step 2 — Pre-flight Safety Check (per env)

Run all checks before touching any files. Abort on hard failures.

### 2a. Verify kustomize build baseline

```bash
kustomize build common.service/overlays/<env> > /tmp/retire-nginx-<env>.yaml 2>&1
echo $?   # must be 0
```

**Hard abort** if non-zero — do not retire a broken overlay.

### 2b. Ingress inventory — nginx vs non-nginx breakdown

Build once, reuse for all checks:

```bash
# Count nginx-class Ingresses (the ones we're retiring)
grep -c "ingress.class: nginx\|ingressClassName: nginx" /tmp/retire-nginx-<env>.yaml || echo 0

# Count all Ingresses (nginx + Traefik + other)
grep -c "^kind: Ingress" /tmp/retire-nginx-<env>.yaml || echo 0

# Count replacement resources (HTTPRoutes + Traefik Ingresses)
grep -c "^kind: HTTPRoute" /tmp/retire-nginx-<env>.yaml || echo 0
traefik_count=$(grep -A5 "^kind: Ingress" /tmp/retire-nginx-<env>.yaml | grep -c "ingressClassName: traefik\|ingress.class: traefik" || echo 0)
```

Show the user this breakdown before proceeding:
```
Pre-flight inventory for <env>:
  nginx Ingresses (to retire):    N
  Traefik Ingresses (to keep):    M
  HTTPRoutes (to keep):           K
  Total Ingresses after retire:   M  (Traefik only)
```

**Hard abort** if `nginx_count == 0 AND (traefik_count == 0 AND httproute_count == 0)`:
— no replacements exist at all, migration is not done.

**Soft warn + confirm** if `nginx_count == 0 AND (traefik_count > 0 OR httproute_count > 0)`:
— already retired; ask if user wants to continue (for cleanup of controller/archive).

**Hard abort** if `nginx_count > 0 AND traefik_count == 0 AND httproute_count == 0`:
— nginx is the only routing path; retiring would cause an outage.

### 2c. Check for active nginx entries in service overlay kustomization

Check both `resources:` and `patches:` sections for uncommented nginx files:

```bash
# Resources and patches that are active (not commented out, not $patch: delete)
grep -E "nginx" common.service/overlays/<env>/kustomization.yaml \
  | grep -v "^#" \
  | grep -v "patch: delete" \
  | grep -v "^\s*#"
```

If any active nginx entries found, **cross-check the rendered manifest** before warning — a file
named `*-nginx-*` may patch the nginx base to a different ingress class (e.g., GCE or ALB):

```bash
# Get the rendered ingress.class for each suspected file
kustomize build common.service/overlays/<env> 2>/dev/null \
  | awk '/^kind: Ingress/{f=1} f && /^  name:/{n=$2} f && /ingress\.class:/{print n ": " $2} /^---/{f=0}'
```

**If `ingress.class` is NOT nginx** (e.g., `gce`, `alb`, `traefik`): this is a **class-override patch**
— the file patches the nginx base resource to use a different LB. Do NOT add `$patch: delete` for
this resource and do NOT delete this file. See Step 5c for the correct handling.

**If `ingress.class` IS nginx**: warn as usual:

```
⚠  WARNING: <env> overlay has active nginx ingress files not yet migrated:
     - <file>
   These services still depend on nginx for routing. Retire them first or
   they will lose routing when nginx controller is removed.
   Proceed anyway? (y/N)
```

---

## Step 3 — Discovery (per env)

Scan for all nginx artifacts. Use the already-built manifest `/tmp/retire-nginx-<env>.yaml`.

### 3a. Controller artifacts

```bash
# ArgoCD Application for nginx controller
ls common.ingress/argocd/<env>.yaml 2>/dev/null && echo "EXISTS" || echo "ALREADY REMOVED"

# Controller overlay directory (files to delete)
ls common.ingress/overlays/<env>/ 2>/dev/null || echo "ALREADY REMOVED"
```

### 3b. Base nginx Ingress resources pulled into this env

Use kustomize build of the base (not grep — file names don't always match resource names):

```bash
kustomize build common.service/base 2>/dev/null \
  | awk '/^kind: Ingress/{f=1; name=""; ns=""} 
         f && /^  name:/{name=$2} 
         f && /^  namespace:/{ns=$2} 
         f && /ingress.class: nginx/{print name " (" ns ")"} 
         /^---/{f=0}'
```

This gives the exact `metadata.name` and `metadata.namespace` needed for `$patch: delete` targets.
Cross-reference against the env build to confirm they're actually rendered in this env.

### 3c. Orphaned nginx files in env overlay

Files that exist in the overlay dir but are NOT referenced in `kustomization.yaml`:

```bash
# Find nginx-named files in the overlay dir
for f in common.service/overlays/<env>/*nginx*.yaml; do
  [ -f "$f" ] || continue
  fname=$(basename "$f")
  # Check if referenced in kustomization (resources or patches)
  if ! grep -qE "^\s+-\s+(path:\s+)?$fname" common.service/overlays/<env>/kustomization.yaml; then
    echo "ORPHAN: $f"
  fi
done
```

### 3d. Archive directory

```bash
ls common.service/overlays/<env>/archive/ 2>/dev/null | wc -l
```

---

## Step 4 — Show Removal Plan + Confirm

Display a summary of exactly what will happen before touching any files.
Only show sections that apply (e.g., omit ORPHAN FILES if none found):

```
Nginx Retirement Plan — <env>
══════════════════════════════════════════════════════════════════
PRE-FLIGHT
  nginx Ingresses to retire:    N
  Traefik Ingresses kept:       M
  HTTPRoutes kept:              K

CONTROLLER
  DELETE  common.ingress/argocd/<env>.yaml           (app-of-apps prunes Application → finalizer removes controller)
  KEEP    common.ingress/overlays/<env>/              (dead code — no ArgoCD app references it; clean up later)

SERVICE INGRESSES  ($patch: delete in overlay kustomization — base files stay)
  PATCH   common.service/overlays/<env>/kustomization.yaml
          → <resource-name>  (<namespace>)
          → <resource-name>  (<namespace>)
          ... (<N> resources)

[ORPHAN FILES]  (only if found)
  DELETE  common.service/overlays/<env>/<file>  (not in kustomization.yaml)

[ARCHIVE DIR]  (only if exists)
  DELETE  common.service/overlays/<env>/archive/   (<N> files — migration snapshots)

NOT TOUCHED
  KEEP    common.ingress/argocd/             (folder stays — other env deployment yamls still live here)
  KEEP    common.ingress/argocd/<other-envs>.yaml  (remaining envs still deployed via these apps)
  KEEP    common.ingress/base/                     (<remaining envs> still reference it)
  KEEP    common.service/base/*-nginx-ingress.yaml (<remaining envs> still render these)
  KEEP    common.service/argocd/<env>.yaml         (<env>-infra app manages secrets + active resources)
══════════════════════════════════════════════════════════════════
Proceed? (y/N)
```

Wait for explicit confirmation before executing.

---

## Step 5 — Execute (per env)

### 5a. Delete the nginx controller ArgoCD Application yaml

```bash
rm common.ingress/argocd/<env>.yaml
```

**Why this is sufficient** — the cascade chain handles cluster cleanup automatically:

```
repo: dev.yaml deleted
  → app-of-apps (prune: true) syncs → prunes Application object from cluster
  → Application has resources-finalizer.argocd.argoproj.io
  → finalizer cascades → deletes nginx controller Deployment, Service, ConfigMap, RBAC
```

The overlay dir (`common.ingress/overlays/<env>/`) becomes dead code — no ArgoCD app
references it anymore. Leave it in place (harmless) or clean it up in a follow-up commit.
Skip this step if the file doesn't exist (already removed).

### 5c. Add $patch: delete for each base nginx Ingress

Append to the **existing** `patches:` section in `common.service/overlays/<env>/kustomization.yaml`.
Use the exact `metadata.name` values discovered in Step 3b.

```yaml
  # Nginx ingress retirement (<env>): delete all base nginx Ingress resources — replaced by Traefik/HTTPRoutes
  - patch: |-
      $patch: delete
      apiVersion: networking.k8s.io/v1
      kind: Ingress
      metadata:
        name: <resource-name>
    target:
      kind: Ingress
      name: <resource-name>
```

> **namePrefix note**: Target names are the **original** names before `namePrefix: <env>-` is applied.
> Kustomize applies patches before namePrefix transformation. Always use the un-prefixed name.

> **configurations: section**: If the kustomization has a `configurations:` block (e.g., for Gateway API nameref),
> add patches **before** configurations to preserve the section order.

#### Special case: class-override patches (e.g., GCE, ALB)

If a base nginx Ingress is patched by an env overlay to use a **different ingress class** (e.g.,
`ingress.class: gce` for a GCE external LB), do NOT add `$patch: delete` for it — the resource
must stay in the rendered output as a non-nginx Ingress.

**Correct handling:**
1. Keep the existing patch file under `patches:` — it overrides the base nginx class to GCE/ALB
2. Do NOT add `$patch: delete` for this resource name
3. Rename the patch file to reflect its actual class (e.g., `n8n-nginx-ingress.yaml` → `n8n-gce-ingress.yaml`) for clarity — the `metadata.name` inside stays unchanged so the K8s resource name and GCE LB binding are undisturbed

**Why not rename the K8s resource?** Changing `metadata.name` causes the old Ingress to be deleted
and a new one created — this triggers GCE/cloud LB reprovisioning. Keep the name to avoid
downtime; rename only the file.

**Cannot use `$patch: delete` + standalone resource with same name**: Kustomize rejects duplicate
resource IDs during accumulation, before patches are applied. If you try to delete the base
resource AND add a same-name standalone resource, it will error.

### 5d. Delete orphaned nginx files

Only delete files confirmed as orphans in Step 3c:

```bash
rm common.service/overlays/<env>/<orphan-file>.yaml
```

### 5e. Delete archive directory

```bash
rm -rf common.service/overlays/<env>/archive/
```

Skip if the directory doesn't exist.

---

## Step 6 — Validate (per env)

### 6a. Confirm zero **nginx-class** Ingress resources remain

```bash
kustomize build common.service/overlays/<env> 2>&1 \
  | grep -c "ingress.class: nginx\|ingressClassName: nginx"
# Expected: 0
```

> Do NOT check total `kind: Ingress` count — envs with Traefik ingresses will legitimately have > 0.
> The retirement target is specifically nginx-class resources, not all Ingress kinds.

If non-zero, identify which nginx Ingress remains:
```bash
kustomize build common.service/overlays/<env> \
  | awk '/^kind: Ingress/{f=1} f && /^  name:/{n=$2} f && /ingress.class: nginx/{print "STILL PRESENT: " n} /^---/{f=0}'
```

Report and halt — do not proceed to commit.

### 6b. Verify remaining Ingresses are non-nginx class

```bash
kustomize build common.service/overlays/<env> \
  | awk '/^kind: Ingress/{f=1} f && /^  name:/{print $2} /^---/{f=0}'
# All names should be *-traefik-* or similar non-nginx resources
```

### 6c. Regression check — all other envs still build cleanly

```bash
for other_env in dev stg prd; do
  [ "$other_env" = "<env>" ] && continue
  kustomize build common.service/overlays/$other_env > /dev/null \
    && echo "$other_env: PASS" \
    || echo "$other_env: FAIL"
done
```

**Halt and report** if any other env fails — do not commit.

---

## Step 7 — All-Env Cleanup Check (only after `retire-nginx all`)

After all three envs retired, check if `common.ingress/` module is fully orphaned:

```bash
ls common.ingress/overlays/ 2>/dev/null   # should be empty
ls common.ingress/argocd/   2>/dev/null   # should show only README.md
```

If no overlay dirs remain, offer to archive the entire module:

```
⚠  All env overlays for common.ingress are removed.
   common.ingress/base/ is no longer referenced by any overlay.
   Recommend: archive or delete common.ingress/ entirely.
   Proceed? (y/N)
```

If confirmed, choose:
```bash
# Option A: archive in place (git history preserved + files accessible)
mkdir -p common.ingress/archive
git mv common.ingress/base  common.ingress/archive/base
git mv common.ingress/argocd common.ingress/archive/argocd

# Option B: delete entirely (git history preserves files)
rm -rf common.ingress/
```

Then check if base nginx Ingress files in `common.service/base/` are still needed:

```bash
# Any remaining kustomization still rendering nginx ingresses from base?
for env in dev stg prd; do
  grep -E "nginx" common.service/overlays/$env/kustomization.yaml \
    | grep -v "^#" | grep -v "patch: delete" \
    && echo "  → $env still uses base nginx files"
done
```

If none remain, offer to remove nginx entries from `common.service/base/kustomization.yaml`
and delete the corresponding base nginx Ingress files.

---

## Step 8 — Summary Report

```
Nginx Retirement — Summary
══════════════════════════════════════════════════════════════════
Env   Controller  Overlay  nginx Ingress  Traefik kept  Validation
────────────────────────────────────────────────────────────────
<env> DELETED     DELETED  0              <N>            PASS
══════════════════════════════════════════════════════════════════
Files deleted:
  common.ingress/argocd/<env>.yaml
  common.ingress/overlays/<env>/  (<N> files)
  common.service/overlays/<env>/archive/  (<N> files)
  <orphan files if any>

Files modified:
  common.service/overlays/<env>/kustomization.yaml
  → added $patch: delete for <N> base nginx Ingress resources

Files kept (active routing / other envs):
  common.service/overlays/<env>/*-traefik-ingress.yaml  (<N> Traefik Ingresses)
  common.ingress/base/  (referenced by remaining envs)
  common.service/base/*-nginx-ingress.yaml  (referenced by remaining envs)

Regression:
  <other-env-1>  PASS
  <other-env-2>  PASS

Next steps:
  1. git add + commit:
     retire(nginx/<env>): remove controller app + exclude base nginx Ingress resources
  2. Push → ArgoCD auto-sync prunes nginx controller from <env> cluster
  3. kubectl get pods -n ingress-nginx  (expect: 0 pods)
  4. Monitor: no 502s — all traffic through Traefik/HTTPRoutes
```

---

## Graceful Degradation

| Condition | Behavior |
|-----------|----------|
| `kustomize` not installed | **Hard abort** — validation is required; `brew install kustomize` |
| `common.ingress/argocd/<env>.yaml` missing | Report as already removed; skip overlay empty step |
| `common.ingress/overlays/<env>/` missing | Skip overlay empty step; report as already retired |
| nginx Ingress count already 0 (but replacements exist) | Soft warn + confirm before continuing to cleanup-only steps |
| nginx Ingresses > 0 but no replacements | **Hard abort** — migration not complete |
| Active nginx patches in overlay (`patches:` not commented) | Cross-check rendered `ingress.class` first — if non-nginx (gce/alb), it's a class-override patch; keep it and skip `$patch: delete` for that resource. If nginx class, warn + require confirmation |
| `archive/` dir missing | Skip step 5e; report as already clean |
| `configurations:` section in kustomization | Append patches before `configurations:` block |
| Other envs fail regression check | **Halt** — report failing env and specific error; do not commit |

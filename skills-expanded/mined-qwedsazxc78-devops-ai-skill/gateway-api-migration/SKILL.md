---
name: gateway-api-migration
description: >
  Migrates Kustomize modules using NGINX Ingress to Gateway API resources.
  Dual-target: default Traefik (GatewayClass=traefik), opt-in GKE Gateway
  (--gateway-class gke-l7-global-external-managed). Handles master/minion
  topology (common.ingress/ + common.service/) as the primary case, with
  standalone Ingress as a fallback. Performs cluster-side preflight (CRDs,
  GatewayClass, policy CRDs, Traefik version probe on Traefik targets),
  deterministic discovery/analysis via bundled scripts, two-phase conversion
  with atomic rollback from full file backups, semantic diff of path and
  listener coverage, plus an ingress2gateway second-opinion cross-check.
  Renders a comprehensive report covering per-hostname mapping, TLS map,
  annotation inventory (translated/stubbed/unknown), risk register, cutover
  checklist, verification commands, and rollback procedures. Never modifies
  the master source; performs idempotent in-place edits only to
  common.service/overlays/<env>/kustomization.yaml.
version: "1.2.0"
---

# Gateway API Migration Skill

Invoked by Zeus pipeline `*gateway-migrate`.

This skill turns an NGINX Ingress footprint (master/minion or standalone) into
a working GKE Gateway API deployment, side-by-side with the original, so a
per-hostname DNS cutover can proceed at the operator's pace. It generates a
new Kustomize module, HTTPRoutes for every minion, a full migration state
file, and a report that is the operator's single source of truth through
every phase of the cutover.

The procedure is organised around the principle that **every deterministic
step is delegated to a bundled script**, and the model's job is to run those
scripts, interpret their output, make judgement calls where the data is
ambiguous, and weave the results into the report. This keeps the skill fast
and reproducible while leaving room for the parts of a migration that
genuinely need human-like judgment.

## Canonical references

Read these as needed — do not preload them all.

| File | When to read |
|---|---|
| `references/annotation-map.md` | Step 2, whenever an annotation needs classification. Table has per-target columns (Traefik default, GKE opt-in). |
| `references/master-minion-topology.md` | Step 1, only if discovery finds an unusual topology |
| `references/traefik-gateway-notes.md` | Step 0b, and Step 3A when target is `traefik*` (the default) |
| `references/gke-gateway-notes.md` | Step 0b, and Step 3A when target is `gke-l7-*` |
| `references/http-routing-guide.md` | Step 3A/3B, when generating HTTPRoute/Gateway YAML |
| `references/ingress2gateway-integration.md` | Step 4c, only if second opinion is enabled |
| `references/preflight-checks.md` | Step 0b (always) — check 3 and 4 are parameterized on `--gateway-class` |
| `references/manual-review-patterns.md` | Step 5, when writing Section 6 entries |
| `references/report-template.md` | Step 5 — the authoritative report shape |
| `references/runbook-template.md` | Step 6 — the operator-facing cutover runbook (install steps branch on target) |
| `references/httproute-template.yaml` | Step 3B, per minion |

## Bundled scripts

The skill ships helper scripts under `scripts/`. Each produces structured
output (JSON) that Steps 1–5 consume. The model's contract with these
scripts is to **invoke them, not to re-implement them in natural language**:
re-deriving the same logic every run wastes tokens and introduces variance.

| Script | Used by | Purpose |
|---|---|---|
| `scripts/check_cluster_preflight.sh` | Step 0b | kubectl/GatewayClass/CRD/namespace checks, JSON out |
| `scripts/classify_ingress.py` | Step 1 | Classify Ingress docs (input: YAML files — built overlays preferred, raw fallback) |
| `scripts/pair_minions.py` | Step 1 | Pair minions with masters, detect orphans and ambiguity |
| `scripts/inventory_annotations.py` | Step 2 | Three-bucket inventory (translated/stubbed/unknown) with file:line provenance |
| `scripts/validate_generated.py` | Step 4d | 11 semantic checks on generated artifacts + optional `ingress2gateway` second-opinion cross-check |
| `scripts/build_report.py` | Step 5 | Render `references/report-template.md` from `state.yaml` |

**Input mode: built vs raw.** Steps 1 and 2 prefer **built-overlay mode** —
`kustomize build <overlay>` first, classify the rendered Ingress docs. This
avoids false-positive "orphan minion" halts on repos that use base templates
with placeholder hostnames, and automatically excludes dead files (YAML on
disk that no `kustomization.yaml` references). If no overlays structure is
detected (standalone Ingress repo, Helm-only repo, etc.), the skill falls
back to **raw-file mode** and records the mode in `state.yaml.discovery.mode`.

## Activation

Triggered explicitly by `*gateway-migrate` from Zeus. Not auto-triggered.

## Invocation forms

```
*gateway-migrate                                      # interactive discovery mode
*gateway-migrate <module-path>                        # explicit target, default --gateway-class traefik
*gateway-migrate <module-path> --resume               # resume from state.yaml
*gateway-migrate <module-path> --force                # bypass never-clobber on target
*gateway-migrate <module-path> --offline              # skip Step 0b cluster checks

# GatewayClass selection (dual-target):
*gateway-migrate <module-path> --gateway-class traefik
*gateway-migrate <module-path> --gateway-class traefik-external
*gateway-migrate <module-path> --gateway-class gke-l7-global-external-managed
*gateway-migrate <module-path> --gateway-class gke-l7-rilb

# Gateway topology (Traefik targets only; default: per-host):
*gateway-migrate <module-path> --gateway-topology per-host   # default: one Gateway per host in traefik ns, HTTPRoute in traefik ns, backendRefs cross-ns (no ReferenceGrant)
*gateway-migrate <module-path> --gateway-topology shared     # one shared Gateway + one ReferenceGrant per backend namespace

# Preflight and generation controls:
*gateway-migrate <module-path> --skip-preflight <n>   # skip individual preflight check N
*gateway-migrate <module-path> --include-orphan-hosts # emit listeners for hosts without minions

# Source-class selection (v1.11.0+; default nginx for backwards-compat):
*gateway-migrate <module-path> --source-class nginx
*gateway-migrate <module-path> --source-class traefik

# Chain integration (v1.11.0+; set by skill C, optional standalone):
*gateway-migrate <module-path> --source-state <path-to-skill-A-state.yaml>

# Redirect control (v1.11.0+; auto-on for nginx, recommended off for traefik):
*gateway-migrate <module-path> --no-redirect       # skip tls-redirect HTTPRoute
```

**Default target:** `traefik`. The skill emits Traefik-specific CRDs
(`Middleware`, `ServersTransport`) when the target prefix is `traefik*`,
GKE-specific CRDs (`GCPBackendPolicy`, `HealthCheckPolicy`) when the prefix
is `gke-l7-*`, and neither when some other GatewayClass name is passed
(vanilla Gateway API only, provider-specific policies deferred to manual
review). See `references/annotation-map.md` for the per-target translation
matrix.

**Orphan-host listeners:** by default the skill only emits Gateway listeners
for hostnames with an attached minion. Orphan hosts (master declares a
host but no minion routes it) are recorded in the report's Section 3.2
with a note that their listener was skipped. Pass `--include-orphan-hosts`
to emit listeners for them anyway — useful when you plan to deploy the
service soon and want the listener ready.

## Artifacts produced

Every successful run writes:

1. A new `common.gateway/` Kustomize module (master → Gateway + per-env overlays).
2. `common.service/overlays/<env>/*-httproute.yaml` files + a single
   HTTP→HTTPS redirect HTTPRoute per env.
3. Idempotent in-place edits to `common.service/overlays/<env>/kustomization.yaml`
   — protected by full-content pre-edit backups under
   `docs/reports/gateway-migration/<slug>/backups/`.
4. `docs/reports/gateway-migration/<slug>/state.yaml` — the machine-readable
   audit trail that `--resume` reads and re-runs build from.
   Additional v1.11.0 `inputs` fields (additive on schema v2, backwards-compatible):
   ```yaml
   inputs:
     sourceClass: nginx | traefik           # default nginx
     sourceMiddlewareReuse:                  # only when sourceClass: traefik
       - middlewareName: cors
         namespace: traefik
         referencedBy: [argocd-server, grafana]
     sourceStatePath: docs/reports/nginx-to-traefik/<slug>/state.yaml  # only when chained
   ```
   These fields are **additive** on schema v2. The schema version is unchanged.
   Existing nginx-only runs continue to omit them entirely.
5. `docs/reports/gateway-migration/<slug>/report.md` — the human-readable
   report, rendered from `references/report-template.md`.
6. `common.gateway/MIGRATION.md` — the operator runbook, substituted from
   `references/runbook-template.md`.

## Step 0 — Tool check

Verify host-side tools. Probe each with `command -v`.

| Tool | Required | On missing |
|---|---|---|
| `kustomize` | yes | HALT: `brew install kustomize` |
| `yq` | yes | HALT: `brew install yq` (v4+) |
| `jq` | yes | HALT: `brew install jq` |
| `kubectl` | yes | HALT: install from cloud SDK or `brew install kubectl` |
| `python3` | yes | HALT: `brew install python3` (scripts depend on it) |
| `kubeconform` | no | WARN, SKIP Step 4b: `brew install kubeconform` |
| `ingress2gateway` | no | WARN, SKIP Step 4c: `brew install ingress2gateway` |

Record every tool's version in `state.yaml.environment.tools`:

```bash
kustomize version --short
yq --version
jq --version
kubectl version --client -o json 2>/dev/null | jq -r '.clientVersion.gitVersion'
python3 --version
kubeconform -v 2>&1 | head -1 || true
ingress2gateway version 2>&1 | head -1 || true
```

**Gate:** HALT on any required tool missing; WARN on optional.

## Step 0b — Cluster preflight (new in v1.1)

This is the step that fails real migrations before they start — missing
GatewayClass, wrong CRD version, policy CRDs absent. Do it before
generating any files.

Delegate to `scripts/check_cluster_preflight.sh`. The script embodies
`references/preflight-checks.md` (read that file only if you need to
diagnose a specific check that failed).

```bash
bash scripts/check_cluster_preflight.sh \
  --namespaces "<space-separated-target-namespaces-from-step-1>"
```

**If Step 1 hasn't run yet** (first invocation, no state.yaml), run this
without `--namespaces` as a coarse check, then re-run it after Step 1
with the discovered namespace list to get per-namespace status recorded
in state.

Parse the JSON stdout. The script exits **0** on success (possibly with
WARNs) and **2** on any halt. Write the full JSON to
`state.yaml.environment.cluster` verbatim.

**Handling results:**

- `halts[]` non-empty → HALT with the exact halt messages from the JSON.
  Do not attempt to "recover"; fix the cluster and re-run.
- `warnings[]` non-empty → continue, but each warning becomes a **risk
  register** entry (Section 9 of the report) with severity `S2` by
  default (promote to `S1` only if the migration actually needs the
  missing CRD — e.g., the source Ingress has CORS annotations and
  `policyCRDs.gcpbackendpolicies: false`).

**Escape hatches:**

- `--offline` — invoke with `bash scripts/check_cluster_preflight.sh --offline`;
  the script emits a stub JSON and the report header flags the run as
  offline-verified.
- `--skip-preflight 4` — invoke with `--skip-check 4` to bypass the
  GKE policy CRD check. Record every skip in
  `state.yaml.environment.cluster.skippedChecks[]`.

**Gate:** HALT on `halts[]`; continue otherwise.

## Step 1 — Discover (topology-aware)

Every run starts with a full classification of every Ingress in the
repo. The discovery is delegated to `scripts/classify_ingress.py` (one
Ingress per line of JSONL output) followed by `scripts/pair_minions.py`
(which consumes the JSONL and produces the pairing report).

### 1.1 Build each overlay, then classify the rendered output

**Classify what Kustomize actually applies, not what the repo has on disk.**
For any repo using overlays with base templates, the raw source files contain
placeholder hostnames (`base-mlflow.example.com`) that get overridden in each
overlay via patches. A classifier that reads raw files will:

1. See the placeholder hostnames as literal values.
2. Fail to pair those placeholders with master hostnames (because no master
   declares `base-mlflow.example.com` — only the overlay-patched `dev-mlflow`,
   `stg-mlflow`, `prd-mlflow`).
3. HALT with a spurious "orphan minion" error.

The correct behaviour is to run `kustomize build` on each overlay first and
classify the **rendered** Ingress documents. This also automatically excludes
dead files (files on disk that no `kustomization.yaml` references), because
Kustomize doesn't include them in the build output.

**Step 1.1a — Enumerate overlays.** Find every `kustomization.yaml` in a
directory named `overlays/<env>/` under `common.ingress/` or `common.service/`.
The enclosing directory two levels up is the *module root*; the `<env>` segment
is the *environment name*.

```bash
mkdir -p /tmp/gwm/built

# Find every overlay kustomization.yaml under common.ingress/ and common.service/
find common.ingress common.service -type f -name kustomization.yaml \
  -path "*/overlays/*" > /tmp/gwm/overlays.txt

# Parse module root + env name from each path
while read -r kf; do
  env=$(basename "$(dirname "$kf")")
  overlay=$(dirname "$kf")
  echo "$overlay"
  echo "$env"
done < /tmp/gwm/overlays.txt
```

**Step 1.1b — Build each overlay and extract Ingress docs.** Pipe the built
output through `yq ea '[select(.kind == "Ingress")] | .[] | split_doc'` to
isolate the Ingress documents (discarding every other `kind:`).

```bash
while read -r overlay; do
  module=$(echo "$overlay" | awk -F/ '{print $1}')
  env=$(basename "$overlay")
  out=/tmp/gwm/built/${module}-${env}.yaml
  if kustomize build "$overlay" 2>/dev/null \
       | yq ea '[select(.kind == "Ingress")] | .[] | split_doc' - > "$out"; then
    echo "built: $out"
  else
    echo "[WARN] kustomize build failed for $overlay"
  fi
done < <(awk -F/ '{print $1 "/" $2 "/" $3 "/" $4}' /tmp/gwm/overlays.txt | sort -u)

ls /tmp/gwm/built/
```

**Fallback (non-Kustomize repos):** If the repo has no `overlays/*` structure,
or all `kustomize build` calls produce zero Ingress docs, fall back to raw
file discovery and record `state.yaml.discovery.mode: "raw-fallback"`:

```bash
grep -rIl "^kind: Ingress$" . \
  --include="*.yaml" --include="*.yml" \
  > /tmp/gwm/ingress-files.txt
```

Record in `state.yaml.discovery.mode`: `"built"` (normal path) or
`"raw-fallback"` (no overlays structure detected). Raw-fallback is a
legitimate mode for standalone Ingress repos; it's not an error.

### 1.2 Classify each Ingress

Feed the built YAML files (or the raw-fallback file list) into
`classify_ingress.py`. One JSONL line per Ingress document.

```bash
# Built mode (recommended)
python3 scripts/classify_ingress.py /tmp/gwm/built/*.yaml \
  > /tmp/gwm/classifications.jsonl

# Raw-fallback mode (only if Step 1.1 fell back)
python3 scripts/classify_ingress.py $(cat /tmp/gwm/ingress-files.txt) \
  > /tmp/gwm/classifications.jsonl
```

Each line is a JSON object with `classification`, `reason`, `hosts`,
`hasPaths`, `hasTls`, `mergeableIngressType`, and the full annotations map.
Classification values: **master**, **minion**, **standalone**, **foreign**
(non-nginx class — skipped by migration), **unknown**.

Record `foreign` classifications in `state.yaml.discovery.foreign[]`. They
don't participate in the migration, but a user may want to know their repo
has non-nginx Ingresses left around (e.g., a service already migrated to
`gce` class).

**Why this matters in practice.** In built mode, dead files (source YAML on
disk but not referenced by any overlay's `resources:` list) are
automatically excluded — Kustomize doesn't include them in the build, so
the classifier never sees them. The `state.yaml.discovery.deadFiles[]`
diagnostic should be populated by comparing the raw file list against
the set of files actually built, for reporting:

```bash
# Optional diagnostic: find files that exist on disk but weren't built
grep -rIl "^kind: Ingress$" common.service \
  --include="*.yaml" > /tmp/gwm/raw-files.txt
# dead files = raw files whose basename doesn't appear in any built output
# (implementation-dependent; the report surfaces them as a WARN in Section 9)
```

### 1.3 Pair minions with masters

```bash
python3 scripts/pair_minions.py --input /tmp/classifications.jsonl \
  > /tmp/pairs.json
```

The script returns topology (`master-minion`, `standalone`, `none`,
`master-only`, `mixed`), a list of `pairs[]`, and lists of `orphanHosts`,
`orphanMinions`, `ambiguous`, `foreign`, and `standalone`.

**Exit code handling:**
- `0` → happy path, proceed.
- `1` → orphan minion(s) or ambiguous pairing. HALT. Print the reasons
  from `orphanMinions[].reason` and `ambiguous[].candidates[]` so the
  user can fix their source config.
- `2` → bad input (no classifications). HALT.

### 1.4 Extract target namespace list (for Step 0b re-run)

```bash
jq -r '.pairs[].minion.namespace' /tmp/pairs.json | sort -u > /tmp/namespaces.txt
```

Feed this back to Step 0b if it was run without `--namespaces`
initially, and capture the per-namespace status into state.

### 1.5 Interactive disambiguation (if invoked without a path)

When the user runs `*gateway-migrate` with no module argument, print a
numbered list of detected migration units (unique master file paths +
`pairs.json.summary`) and let the user pick one. Offer `*gateway-migrate
--interactive` as an alias for clarity.

Store the full pair report to `state.yaml.topology` as-is.

**Gates:**
- HALT on classify exit != 0 (no Ingress or yq error).
- HALT on pair exit == 1 (orphan minion or ambiguous).
- HALT on `--resume` without a pre-existing `state.yaml`.
- WARN on orphan hosts (master declares a host with no matching minion)
  — these become listeners with no HTTPRoute and surface in the
  report's Section 3.2.

## Step 2 — Analyze

Two parallel tracks: annotation inventory and backend resolution.

### 2.1 Annotation inventory (three buckets)

Inventory the **built overlays** from Step 1.1b, not the raw files. This keeps
the file set aligned with what Kustomize actually applies — any annotation
that only exists in a dead file (on disk but not referenced by any overlay)
is correctly excluded. Base-to-overlay annotation variance is also
automatically handled because each overlay is already patched by the time
inventory runs.

```bash
ls /tmp/gwm/built/*.yaml > /tmp/gwm/inventory-input.txt
python3 scripts/inventory_annotations.py --files-from /tmp/gwm/inventory-input.txt \
  > /tmp/gwm/annotations.json
```

If Step 1.1 fell back to raw mode, use the raw file list instead:

```bash
python3 scripts/inventory_annotations.py --files-from /tmp/gwm/ingress-files.txt \
  > /tmp/gwm/annotations.json
```

The script produces `translated`, `translatedLossy`, `stubbed`, `unknown`,
and `dropInfo` buckets. Each entry has the source `file:line` and the
annotation-map row number.

**The unknown bucket matters.** Today's SKILL.md (pre-v1.1) would
silently drop unknown annotations — they'd never appear in the report.
This script surfaces every unknown with its exact source location. The
report's Section 4.4 is populated from this bucket.

For unknown annotations, the skill's default action is **drop with a
WARN**. If an unknown annotation looks security-relevant (contains
"auth", "cors", "security", "cert", "ssl", "tls", "waf"), promote the
warning to severity **S1** in the risk register — a human must confirm
it's safe to drop before cutover.

Write the full inventory to `state.yaml.annotations`.

### 2.2 Backend service resolution

For each minion in `pairs.json`, verify the backend Service exists and
resolve its port:

1. `spec.rules[].http.paths[].backend.service.name` — the target.
2. `.port.number` OR `.port.name` — if name, the skill must find the
   Service and read its `spec.ports[?(@.name=="<name>")].port` to get
   the numeric value. HTTPRoute's `backendRefs[].port` requires
   **numbers**.
3. Service manifest location: search the repo for
   `kind: Service` + matching `metadata.name` in the same Kustomize
   module (or Helm chart). Missing → record a WARN, *do not halt* — the
   Service might come from a chart the migration tooling can't see.

Write results to `state.yaml.backends[]`. Each entry:

```yaml
- service: argocd-server
  namespace: argocd
  portName: http     # or null
  portNumber: 80
  resolvedFrom: repo | chart | missing
  sourceFile: argocd/base/service.yaml
```

### 2.3 Per-overlay annotation variance check

When Step 1.1 ran in built mode, each overlay was already rendered
independently and its fully-patched annotations are in the bucketed inventory
from Step 2.1 — so variance across envs is naturally visible *by
file of origin* in `state.yaml.annotations.*[].file`. The skill's job at
this step is to diff the translated-annotation sets across the env masters
and surface any asymmetry:

```bash
jq -r '.translated + .translatedLossy + .stubbed
       | map(select(.file | test("common-ingress-"))) 
       | group_by(.file)
       | map({file: .[0].file, keys: [.[].annotation] | unique})' \
  /tmp/gwm/annotations.json > /tmp/gwm/master-anns-per-env.json
```

Compare the `keys` arrays across envs. Any annotation present in one env
but missing in another is a **variance finding**. Record in
`state.yaml.annotations.overlayVariance[]` and surface as **S2** in the
risk register. Equally valuable: differences in *host counts* between env
masters — record those too (e.g., "dev master declares 14 hosts; stg and
prd declare 12 — 2 hosts advertised only in dev").

When Step 1.1 fell back to raw mode (no overlays structure), skip this
sub-step — there is no overlay to diff against.

### 2.4 Summary to user

Present a terminal summary (numbers only — full detail lives in the
report generated at Step 5):

```
Module: common.ingress → common.gateway (master/minion topology)

  Masters:            1 file
  Minions:            11 files × 3 envs = 33 files
  Hostnames (master): 14
  Backends resolved:  11 / 11
  Overlay variance:   0 annotation diffs

Annotations:
  translated:       38
  translatedLossy:   2 (proxy-*-timeout — will collapse)
  stubbed:           3 (server-snippet: 1× path denylist, 2× Set-Cookie)
  unknown:           2 (!) — review before proceeding
  dropInfo:          1

Proceed with conversion? [y/N]
```

**Gate:** user must confirm. HALT on decline.

## Step 3 — Convert (two-phase)

Phase 3A creates the new `common.gateway/` module. Phase 3B creates
HTTPRoutes alongside the existing minions and edits
`common.service/overlays/<env>/kustomization.yaml` in place. Each
phase has its own atomicity guarantee.

### 3.0 Pre-flight (shared between 3A and 3B)

1. Check target `<master-parent>/common.gateway/`:
   - Exists without `--force` → HALT (`Target already present; use --resume or --force`).
   - Exists with `--force` → continue.
2. For each planned HTTPRoute destination
   (`common.service/overlays/<env>/<svc>-httproute.yaml`):
   - Exists without `--force` → HALT.
   - Exists with `--force` → continue.
3. **Back up every kustomization.yaml that will be modified, in full**:
   ```bash
   mkdir -p docs/reports/gateway-migration/<slug>/backups/
   for env in dev stg prd; do
     cp "common.service/overlays/$env/kustomization.yaml" \
        "docs/reports/gateway-migration/<slug>/backups/${env}-kustomization.yaml.pre-edit"
   done
   ```
   Record each backup path in `state.yaml.steps.3B.backups[]` as
   `{originalPath, backupPath, sha256}`. The SHA256 is for tamper
   detection only — **rollback uses the backup file contents**, not the
   hash. This fixes the v1.0 bug where rollback could never work.

### 3.1 Phase 3A — Generate `common.gateway/`

Atomic: write everything to `common.gateway.tmp/` first, rename to
`common.gateway/` on success. Any failure before the rename → remove
the temp directory, no partial state.

**Resolve the target class up front.** Read `state.yaml.header.target_gateway_class`
(set from `--gateway-class`, default `traefik`). The rest of Phase 3A
branches on the target prefix:
- `traefik*` → emit Traefik CRDs (Middleware, ServersTransport). Read
  `references/traefik-gateway-notes.md` for resource shapes.
- `gke-l7-*` → emit GKE CRDs (GCPBackendPolicy, optional ManagedCertificate
  refs). Read `references/gke-gateway-notes.md` for resource shapes.
- anything else → vanilla Gateway API only; no provider-specific policy
  files. Record in risk register that policies were skipped.

**Resolve the Gateway topology (Traefik targets only).** Read
`state.yaml.header.gateway_topology` (set from `--gateway-topology`,
default `per-host`):

- **`per-host` (default)**: emit one `Gateway` + one `HTTPRoute` per
  migrated host, both in the `traefik` namespace. `backendRefs` point
  cross-namespace to the actual backend Service (works without
  `ReferenceGrant` when `providers.kubernetesCRD.allowCrossNamespace: true`
  is set in Traefik — the Helm chart default). `allowedRoutes.namespaces.from: Same`.
  - Emit one file per host: `<service>-gateway.yaml` in the overlay.
  - Port: use internal container port (`8443` for websecure, `8000` for web) —
    not LB `exposedPort`. See §CRITICAL in `references/traefik-gateway-notes.md`.
  - cert-manager annotation: `cert-manager.io/cluster-issuer: <issuer>` on
    the Gateway (not a separate Certificate CR). Requires cert-manager ≥1.15.

- **`shared`**: emit a single `Gateway` in `traefik` namespace with one
  listener per host, and one `ReferenceGrant` per backend namespace granting
  the HTTPRoutes in `traefik` ns permission to reference Services there.
  Use this only when minimising Gateway object count is a hard requirement.

Record the resolved topology in `state.yaml.header.gateway_topology`.
See `references/traefik-gateway-notes.md §Gateway topology` for the
canonical template for each option.

1. **`common.gateway/base/kustomization.yaml`**:

   ```yaml
   apiVersion: kustomize.config.k8s.io/v1beta1
   kind: Kustomization
   namespace: ingress-nginx  # from master's namespace
   resources:
     - gateway.yaml
     # Target-specific policy files, only if applicable to this migration:
     # - middleware-cors.yaml          (Traefik target + source has CORS)
     # - middleware-block-paths.yaml   (Traefik target + source has row-9c denylists)
     # - gcpbackendpolicy-<svc>.yaml   (GKE target + source has CORS/timeouts)
   ```

2. **`common.gateway/base/gateway.yaml`** — one `Gateway` resource,
   `gatewayClassName` set from `state.yaml.header.target_gateway_class`.

   Per hostname in the master's `spec.rules[].host`, **skip orphan hosts
   by default** (hosts that have no matching minion — see `orphanHosts[]`
   in state.yaml). Emit the listener only if `--include-orphan-hosts` is set.

   For each hostname that WILL have a listener:
   - One **HTTPS listener** (port 443), `tls.mode: Terminate`,
     `certificateRefs` populated from `spec.tls[].secretName` (always
     `kind: Secret` for Traefik; for GKE also supports `kind: ManagedCertificate`
     if the `networking.gke.io/managed-certificates` annotation listed
     the host).
   - One **HTTP listener** (port 80), no TLS, used only by the
     RequestRedirect route below.
   - Both listeners: `allowedRoutes.namespaces.from: Selector`,
     `selector.matchLabels.gateway-access: ingress-nginx`.
   - Listener name convention: `https-<slugged-hostname>` and
     `http-<slugged-hostname>`. Slug = lowercase + replace `.` with `-`.
     **Record each listener name in `state.yaml.topology.listeners[]`**
     — Step 4d will cross-check every HTTPRoute's `sectionName` against
     this list.

3. **Target-specific policy files** — choose ONE branch:

   **3.Traefik — when target prefix is `traefik*`:**

   a. **`common.gateway/overlays/<env>/middleware-cors.yaml`** (or in each
      minion namespace under `common.service/overlays/<env>/` — see §CORS
      in `annotation-map.md` for the cross-namespace discussion). Only
      emit if the source had CORS annotations (rows 5–8). One Middleware
      of kind `headers` per target namespace:

      ```yaml
      apiVersion: traefik.io/v1alpha1
      kind: Middleware
      metadata:
        name: common-cors
        namespace: <target-ns>
      spec:
        headers:
          accessControlAllowOriginList: [<from row 6>]
          accessControlAllowMethods:     [<from row 7>]
          accessControlAllowHeaders:     [<from row 8>]
          accessControlMaxAge: 100
          addVaryHeader: true
      ```

   b. **`common.gateway/overlays/<env>/middleware-block-paths.yaml`** —
      only if the source had row-9c path denylists. Single Middleware of
      kind `redirectRegex`:

      ```yaml
      apiVersion: traefik.io/v1alpha1
      kind: Middleware
      metadata:
        name: block-sensitive-paths
        namespace: <target-ns>
      spec:
        redirectRegex:
          regex: "<combined regex from source location ~ patterns>"
          replacement: "/__blocked_by_gateway_migrate__"
          permanent: false
      # Plugin-based alternative (requires blockpath plugin in Traefik static config):
      # spec:
      #   plugin:
      #     blockpath:
      #       regex: [...]
      ```

   c. **No GCPBackendPolicy, no Certificate resources.** cert-manager
      Secrets already exist from the source Ingress's `spec.tls[].secretName`.

   **3.GKE — when target prefix is `gke-l7-*`:**

   a. **`common.gateway/base/gcpbackendpolicy-<svc>.yaml`** — one per
      backend Service with CORS or lossy timeout annotations (rows 5–8,
      10). N files for N backends with these annotations.

   b. **`common.gateway/base/certificate-<host>.yaml`** — cert-manager
      case only. One `Certificate` per host that had a
      `cert-manager.io/cluster-issuer` annotation on the master.

   c. **Row 9c path denylists remain stubs** — emit `# TODO(gateway-migrate)`
      comments pointing at `references/manual-review-patterns.md` and
      Cloud Armor. Manual review required.

4. **`common.gateway/base/redirect-httproute.yaml`** — **target-agnostic**.
   A single HTTPRoute attached to every `http-<host>` listener with a
   `RequestRedirect` filter scheme=https port=443 statusCode=301. Without
   this file, the Gateway listens on port 80 but silently drops HTTP
   traffic — a common migration regression.

   **`--no-redirect` flag (v1.11.0+):** When `--no-redirect` is passed, the
   converter skips emitting the `tls-redirect` HTTPRoute. Use this when the
   source is Traefik: the Traefik EntryPoint config in `app.values.yaml`
   already handles HTTP→HTTPS, and a redundant HTTPRoute would conflict.
   Default-on behaviour is unchanged for standalone nginx-source runs.

   Template:

   ```yaml
   apiVersion: gateway.networking.k8s.io/v1
   kind: HTTPRoute
   metadata:
     name: tls-redirect
     namespace: ingress-nginx  # same namespace as Gateway
   spec:
     parentRefs:
       - name: common-gateway
         sectionName: http-<host-1>
       - name: common-gateway
         sectionName: http-<host-2>
         # ... one parentRef per http listener
     hostnames:
       - <host-1>
       - <host-2>
     rules:
       - filters:
           - type: RequestRedirect
             requestRedirect:
               scheme: https
               port: 443
               statusCode: 301
   ```

5. **`common.gateway/overlays/{dev,stg,prd}/kustomization.yaml`**:

   ```yaml
   apiVersion: kustomize.config.k8s.io/v1beta1
   kind: Kustomization
   namespace: ingress-nginx
   resources:
     - ../../base
     - gateway.yaml
     - redirect-httproute.yaml
     # Traefik target only, if applicable:
     # - middleware-cors.yaml
     # - middleware-block-paths.yaml
   ```

6. **`common.gateway/overlays/<env>/gateway.patch.yaml`** — per-env
   listener config (different hostnames per env, different
   certificate refs). Only used for the base/overlay split pattern —
   for dev-first runs, the full Gateway lives in the overlay directly.

7. **`common.gateway/argocd/<env>.yaml`** — copy
   `common.ingress/argocd/<env>.yaml` (if it exists), rewrite
   `metadata.name` → `<name>-gateway`, rewrite `spec.source.path` →
   `common.gateway/overlays/<env>`. If the source has no sibling
   `argocd/` dir, emit a TODO stub in the report's Section 9 (Risk
   register, S2) asking the user to create the ArgoCD app manually.

8. **`common.gateway/MIGRATION.md`** — copy
   `references/runbook-template.md`, substitute
   `{{master_module}}`, `{{generated_module}}`, `{{target_namespaces}}`,
   `{{hostnames_per_env}}`, `{{service_list}}`, `{{target_gateway_class}}`,
   `{{skill_version}}`, `{{gateway_name}}`, `{{master_namespace}}`,
   `{{cluster_name}}`, `{{cluster_region}}`. Phase 0 install steps branch
   on target (Traefik helm install vs GKE add-on enable).

Record every generated file in `state.yaml.steps.3A.generated[]`
with `path`, `sha256`, `size`.

**On any Phase 3A failure:** `rm -rf common.gateway.tmp/`, do not touch
`common.gateway/`. State `steps.3A.status: failed`, record the error,
HALT with a message explaining the target repo is clean.

### 3.2 Phase 3B — Generate HTTPRoutes + edit kustomization.yaml

For each `(env, pair)` from `state.yaml.topology.pairs[]`:

1. **Read `references/httproute-template.yaml`** and substitute:
   - `{{service}}` → minion's backend Service name
   - `{{namespace}}` → minion's namespace (from classify_ingress output)
   - `{{hostname}}` → minion's declared host for this env
   - `{{gateway_name}}` → `common-gateway` (from step 3A.2 convention)
   - `{{gateway_namespace}}` → master's namespace
   - `{{listener_name}}` → `https-<slugged-hostname>` from the listener
     list in `state.yaml.topology.listeners[]`
   - `{{backend_name}}` → from `state.yaml.backends[]`
   - `{{backend_port}}` → numeric port (resolved from port name if
     necessary, see Step 2.2)
   - For each path rule from the source minion, emit one entry in
     `rules[]`. Preserve `pathType`:
     - `Prefix` → `PathPrefix`
     - `Exact` → `Exact`
     - `ImplementationSpecific` with path `/` → `PathPrefix /` (documented
       semantic equivalence; see `references/http-routing-guide.md`)
     - `ImplementationSpecific` with non-`/` path → HALT and require manual
       resolution — the validator's path-coverage check will catch this
   - If the master had row 9a security headers in `server-snippet`,
     add the `responseHeaderModifier` filter.
   - **Target-specific filters:** add `extensionRef` filters based on the
     target GatewayClass:
     - **Traefik target**: if CORS annotations present on master → add
       `filters: [{type: ExtensionRef, extensionRef: {group: traefik.io, kind: Middleware, name: common-cors}}]`.
       If row-9c path denylists present → also add a filter pointing at
       the `block-sensitive-paths` middleware. Both middlewares must live
       in the **HTTPRoute's own namespace** (not ingress-nginx) because
       Traefik resolves `extensionRef` against the route's namespace.
     - **GKE target**: no HTTPRoute filters for CORS — CORS attaches via
       `GCPBackendPolicy.targetRef` at the Service level (generated in
       Phase 3A.3.GKE).
     - **Other targets**: no provider filters.

2. **Write to** `common.service/overlays/<env>/<service>-httproute.yaml`.

3. **Edit `kustomization.yaml` in place** (idempotent):

   ```bash
   # Only add the entry if it doesn't already exist.
   if ! yq eval ".resources | contains([\"<svc>-httproute.yaml\"])" \
        "common.service/overlays/<env>/kustomization.yaml" | grep -q true; then
     yq eval -i ".resources += [\"<svc>-httproute.yaml\"]" \
        "common.service/overlays/<env>/kustomization.yaml"
   fi
   ```

4. **Validate the env** (fast, catches the most common failures early):

   ```bash
   kustomize build "common.service/overlays/<env>" > /dev/null
   ```

   On failure: **restore `kustomization.yaml` from the backup file**
   (not from a hash), remove every newly created `*-httproute.yaml` for
   this env, HALT with the kustomize error output. Store
   `steps.3B.rollback` in state so `--resume` can pick up from the
   failing env.

Record every `(env, service)` modification in
`state.yaml.steps.3B.modified[]` with pre-edit and post-edit SHA256 so
the report's Section 5.2 has integrity metadata.

**TODO stubs:** when the master had stubbed annotations (rows 9b/9c
from `annotation-map.md`), emit them inline in the generated YAML as:

```yaml
# TODO(gateway-migrate): <pattern> — see report.md Manual Review MR-<n>
```

**Resume behaviour:** `--resume` reads `state.yaml.steps.3B.modified[]`
and skips any `(env, service)` tuple already recorded as complete.

**Gate:** HALT on any write failure, target-exists-without-force, or
`kustomize build` validation failure. Always leave the repo in a
consistent state.

## Step 4 — Validate

Four sub-steps: mandatory build, optional schema check, optional
second-opinion diff, mandatory semantic diff.

### 4a. kustomize build (required)

Build **both** modules for every environment. v1.0 only built
`common.service/`; v1.1 builds `common.gateway/` too, catching
self-contained errors like misspelled listener names.

```bash
for env in dev stg prd; do
  kustomize build "common.gateway/overlays/$env" > "/tmp/build-gateway-$env.yaml"
  kustomize build "common.service/overlays/$env" > "/tmp/build-service-$env.yaml"
done
```

Record each result in `state.yaml.steps.4a.checks[]`. On failure →
HALT. Leave the generated files in place so the user can inspect them;
re-run with `--resume` after fixing.

### 4b. kubeconform (optional)

Only if `kubeconform` was detected in Step 0. Run against each built
overlay with the Gateway API CRD schemas:

```bash
for env in dev stg prd; do
  kubeconform \
    -schema-location default \
    -schema-location 'https://raw.githubusercontent.com/kubernetes-sigs/gateway-api/v1.1.0/config/crd/standard/{{.ResourceKind}}_{{.Group}}_{{.KindLowerSuffix}}.json' \
    -ignore-missing-schemas \
    "/tmp/build-gateway-$env.yaml" "/tmp/build-service-$env.yaml"
done
```

GKE-specific resources (`GCPBackendPolicy`, `ManagedCertificate`) won't
have public schemas — `-ignore-missing-schemas` covers them. Warnings
are WARN, not FAIL.

### 4c. ingress2gateway second opinion (optional)

Only if `ingress2gateway` was detected. See
`references/ingress2gateway-integration.md`. Emit the normalized diff
to `docs/reports/gateway-migration/<slug>/second-opinion.diff` and
record a structured summary in `state.yaml.steps.4c`.

Classify each divergence into one of:
- **expected** — our skill emits `GCPBackendPolicy`, `Certificate`,
  `ManagedCertificate` refs, `ResponseHeaderModifier` for row 9a,
  `tls-redirect` HTTPRoute. These are intentional differences.
- **formatting** — map key order, whitespace, field nesting.
- **needsReview** — anything else.

Count each class and persist to
`state.yaml.steps.4c.divergenceBreakdown`. `needsReview > 0` → WARN,
never HALT.

### 4d. Semantic diff — `scripts/validate_generated.py` (mandatory)

Delegate all semantic validation to `scripts/validate_generated.py`. The
script runs 11 checks against the generated artifacts, emits structured
JSON, and returns exit 0 (`pass`/`warn`) or exit 1 (`fail`).

```bash
python3 scripts/validate_generated.py \
  --target-root      /path/to/target/gitops/repo \
  --module           common.ingress \
  --minion-module    common.service \
  --generated-module common.gateway \
  --env              dev \
  > docs/reports/gateway-migration/<slug>/step4d.json
```

**Checks run (see script docstring for full details):**

1. `kustomize-build-gateway` — `kustomize build <gateway>/overlays/<env>` exits 0
2. `kustomize-build-service` — `kustomize build <service>/overlays/<env>` exits 0
3. `listener-coverage` — every HTTPRoute `sectionName` resolves to a Gateway listener
4. `httproute-parentref-name` — every `parentRefs[].name` matches a real Gateway
5. `source-hostname-coverage` — every source master hostname appears in a Gateway listener
6. `source-backend-coverage` — every source minion backend Service is in a generated HTTPRoute `backendRefs[]`
7. `path-coverage` — every source path+pathType appears in a generated HTTPRoute `matches[]` (with `ImplementationSpecific /` → `PathPrefix /` normalization)
8. `namespace-consistency` — every HTTPRoute's namespace matches its source minion's namespace
9. `tls-secret-coverage` — every source `spec.tls[].secretName` is referenced by a listener `certificateRefs[]`
10. `dead-file-safety` — dead files (on disk but not referenced by any overlay `kustomization.yaml`) don't leak into built output
11. `ingress2gateway-second-opinion` *(optional, if `ingress2gateway` is on PATH)* — cross-check our generated hostnames and backends against the upstream tool; our set must be a superset (we're allowed to emit extras like the tls-redirect HTTPRoute, ResponseHeaderModifier filters, and GCPBackendPolicy that ingress2gateway doesn't produce)

**Output consumption.** Parse the JSON:

- `overall: "fail"` → **HALT**, do not proceed to Step 5. Read
  `checks[].mismatches` for the failing entries and either fix the
  generated artifacts (`--resume` Step 3) or update the source Ingress
  if the failure reveals a pre-existing problem in the source.
- `overall: "warn"` → continue to Step 5. Each `warn` check becomes a
  **risk register** entry (Section 9 in the report) at the severity the
  check declares.
- `overall: "pass"` → continue to Step 5. No risk register entries from
  step 4d.

Persist the full JSON into `state.yaml.steps["4d"]` for the report to
consume.

**Optional: skip the second opinion** (for faster runs without
ingress2gateway):

```bash
python3 scripts/validate_generated.py ... --no-second-opinion
```

**Gate:** HALT on 4a or 4d failure; WARN on 4b/4c/4d-warn.

## Step 5 — Render report

Delegate rendering to `scripts/build_report.py`. The template lives in
`references/report-template.md` and has ~18 sections covering header,
topology, annotation inventory, generated/modified files, manual review,
per-hostname map, TLS map, risk register, second opinion, cutover
checklist, rollback commands, verification commands, observability
pointers, pre-commit summary, and audit trail.

```bash
python3 scripts/build_report.py \
  --state    "docs/reports/gateway-migration/<slug>/state.yaml" \
  --template "references/report-template.md" \
  --out      "docs/reports/gateway-migration/<slug>/report.md"
```

The script reads `state.yaml` (via `yq`), computes the verdict, and
substitutes every `{{placeholder}}` from the template with data from
state. Unresolved placeholders trigger a warning block prepended to the
output — the run does not fail, but the report header clearly shows
which fields couldn't be populated.

**Verdict computation** (performed by the skill before invoking
`build_report.py` — the script is a pure renderer):

- **`PASS`** — zero `stubbed[]`, zero `unknown[]`, zero WARNs from 4b/4c/4d,
  zero preflight warnings with severity >= S2.
- **`COMPLETED WITH MANUAL REVIEW REQUIRED`** — any stubs, any unknowns,
  any optional-validation warnings, any non-S3 preflight warnings.
- **`FAIL`** — `state.yaml.steps.4a.status == failed`. Report still
  written so the operator has the partial state.

Also write `state.yaml.verdict` with both `value` and `numericSummary`
(e.g., `"7 listeners, 5 HTTPRoutes, 2 policies, 0 stubs, 0 unknown"`).

**Gate:** WARN on write failure. Fallback: print the report to stdout
so the user can copy-paste it.

## Step 6 — Emit runbook

Copy `references/runbook-template.md` to
`common.gateway/MIGRATION.md`, substituting variables from
`state.yaml`. Also print the Phase 1-4 summary to the Zeus session so
the user sees the runbook immediately, not just as a file.

The runbook covers cluster preflight verification, Phase 1 (Gateway
deploy), Phase 2 (HTTPRoute deploy + smoke test), Phase 3 (per-hostname
DNS cutover), Phase 4 (bake and clean up), rollback, and the
per-hostname cutover checklist.

**Gate:** informational.

## Step 7 — Pre-commit hints

Print to the session (and also embed in the report's Section 16):

```
feat(ingress): migrate common.ingress to Gateway API (master/minion)

- Generate common.gateway/ (Gateway + base/dev/stg/prd overlays)
- Add <N> HTTPRoutes to common.service/overlays/{dev,stg,prd}/
- Add tls-redirect HTTPRoute for HTTP→HTTPS on port 80
- Register new HTTPRoute files in common.service/overlays/*/kustomization.yaml
- Target: gke-l7-global-external-managed
- <N> listeners, <N> HTTPRoutes, <N> policies, <N> manual review items
- common.ingress/ untouched — side-by-side for safe per-hostname DNS cutover

Co-generated-by: gateway-api-migration skill v<version>
```

File list for staging — built from `state.yaml.steps.3A.generated[]` +
`state.yaml.steps.3B.modified[]` + the report files:

```bash
git add common.gateway/
git add common.service/overlays/<env>/<svc>-httproute.yaml \
        common.service/overlays/<env>/kustomization.yaml \
        ...  # one line per env
git add docs/reports/gateway-migration/<slug>/state.yaml \
        docs/reports/gateway-migration/<slug>/report.md \
        docs/reports/gateway-migration/<slug>/backups/
```

**Never auto-commit.** The user drives git.

**Gate:** informational.

## Step 7b — Cross-repo HTTPRoute handoff (new v1.16.0)

Some services have their `Service` and `Deployment` defined in a separate
GitOps repository (e.g., `proposal-review-machine`). For these services, the
HTTPRoute must be committed to **the service's own repo**, not to
`common.service/`, because:

1. The service's repo has its own ArgoCD Application per environment.
2. The service team owns routing config alongside their deployment.
3. The HTTPRoute's `parentRef` can still target the Gateway in the central
   repo as long as `allowedRoutes.namespaces.from: All` is set on the
   listener (or a `ReferenceGrant` exists).

### Detection

At Step 1 (Discover), after backends are resolved, classify each backend by
the location of its `Service` manifest:

- **In-repo backend** — `Service` found under the same module root.
  HTTPRoute lands in `common.service/overlays/<env>/<svc>-httproute.yaml`.
- **Cross-repo backend** — `Service` not found in this repo, but the
  hostname appears in the master Gateway-source. Record under
  `state.yaml.crossRepo[]` with the operator-provided repo path:

```yaml
state.yaml:
  crossRepo:
    - service: proposal-review-machine
      hostname: dev-proposal-review.awoo.org
      repo_path: ../proposal-review-machine   # operator confirms
      httproute_target: overlays/<env>/httproute.yaml
      kustomization_target: overlays/<env>/kustomization.yaml
```

### Generation

For each `crossRepo[]` entry, **emit the file to the foreign repo path**.
Do NOT auto-`cd` and `git add` there — the operator drives git in each
repo separately. The skill prints, per cross-repo service:

```
✦ Cross-repo HTTPRoute prepared:
  Repo: ../proposal-review-machine
  File: overlays/dev/httproute.yaml
  Action: cd ../proposal-review-machine && git checkout -b <branch> && \
          git add overlays/dev/{httproute,kustomization}.yaml && git commit
```

### Report integration

`report.md` Section 4 (Host inventory) gains a "Repo" column. Section 10
(Pre-commit / MR URLs) gains per-repo subsections so the operator gets
one MR URL per repo.

**Gate:** halt if `crossRepo[]` is non-empty AND the operator did not
provide repo paths via prompt; ask interactively then continue.

## Step 7c — DNS cutover script alignment (new v1.16.0)

When the migration introduces **new hostnames** (services that weren't
previously on Traefik), the operator's DNS cutover script must list them
in the appropriate batch — otherwise `./scripts/dns-create-traefik.sh dev`
silently skips the new hosts.

### Discovery

After Step 3B, glob for `scripts/dns-*.sh` (or `scripts/dns/*.sh`,
configurable). For each script found, grep for hostname arrays / batch
declarations and compare against the migration's host list.

### Output

For each gap, print:

```
✦ DNS script gap detected:
  Script: scripts/dns-create-traefik.sh
  Batch:  dev-b2
  Missing: dev-langfuse.awoo.org, dev-litellm.awoo.org

  Suggested patch:
  --- a/scripts/dns-create-traefik.sh
  +++ b/scripts/dns-create-traefik.sh
  @@ run_dev_b2 domains
       dev-qdrant-devops.awoo.org
  +    dev-langfuse.awoo.org
  +    dev-litellm.awoo.org
  )
```

Pass `--update-dns` to apply the patch automatically (still requires
operator commit).

**Gate:** WARN-only. The migration is still committable; the DNS gap
only manifests at cutover time.

## Step 7d — Multi-env staging activation (new v1.16.0)

By default the skill generates Gateway + HTTPRoute files for every env
(`overlays/{dev,stg,prd}/`) but only **registers** them in the
`kustomization.yaml` of the env passed via `--activation-env` (default
`dev`).

### Behaviour

| Env | `app.gateway.yaml` exists | Registered in kustomization | Gateway provider enabled in valuesInline |
|---|---|---|---|
| activation-env (e.g., dev) | yes | yes (uncommented) | yes |
| other envs (stg, prd) | yes | no — commented out with activation hint | no |

The other-env `kustomization.yaml` gets a block like:

```yaml
resources:
  - ../../base
  # app.gateway.yaml — NOT active yet. Uncomment together with enabling
  # kubernetesGateway in the Traefik helmChart valuesInline below.
  # - app.gateway.yaml
```

And for `common.service/overlays/<other-env>/kustomization.yaml`:

```yaml
  # Gateway API HTTPRoutes — NOT active yet. Enable after
  # kubernetesGateway is turned on in common.traefik/overlays/<env>/.
  # - grafana-httproute.yaml
  # - ... (all httproute entries commented)
```

### Activation steps emitted to state.yaml

`state.yaml.envStrategy.<env>.activationSteps[]` records the exact
file + change for each not-yet-active env. Operators can later run:

```bash
*gateway-activate stg     # planned future command
```

to flip all the commented entries in one shot. For now the skill prints
the diff and the operator applies it manually.

### Why this matters

Without staged activation, merging a single MR pushes Gateway + HTTPRoute
to every env simultaneously. If `kubernetesGateway` is not enabled in
stg/prd Traefik instances, ArgoCD sync **fails** with
"GatewayClass not found". Staged activation lets the operator validate
in dev for days before flipping each higher env independently.

**Gate:** informational, but the v1.16.0 default for `--activation-env`
is `dev` — overriding to `prd` triggers an interactive confirmation.

## Halt / resume semantics

| Failure point | State | Resume behaviour |
|---|---|---|
| Step 0 tool missing | no state written | install tool, re-run normally |
| Step 0b halt | state has `environment.cluster.halts[]` | fix cluster, re-run (not `--resume`) |
| Step 0b warn only | state has `environment.cluster.warnings[]` | continue automatically |
| Step 1 classify error | state up to `discovery` | fix YAML, re-run normally |
| Step 1 orphan/ambiguous | state has `topology.halts[]` | fix source, re-run normally |
| Step 2 user abort | state `status: aborted` | `--resume` restarts from Step 2 |
| Step 3A write fails | temp dir cleaned, no partial output | re-run normally; target still clean |
| Step 3B build fails | backup restored, new httproute files removed | `--resume` retries Step 3B from failing env |
| Step 4a build fails | generated module left in place | fix and `--resume` |
| Step 4b/4c warn | state records warnings | no halt; continue |
| Step 4d listener/path mismatch | state has `steps.4d.halts[]` | treat as 3A bug, re-run after fix |
| Step 5 render fails | state complete, report missing | re-run Step 5 only: `*gateway-migrate --resume` |
| Run completes | state `status: completed` | rerun refused unless `--force` |

On `--resume`, the skill:

1. Reads `state.yaml` from the path argument.
2. Verifies `schemaVersion` matches (`2`). Mismatch → HALT.
3. Verifies `skillVersion` is compatible. Cross-minor upgrades may HALT
   with a message pointing at a migration script.
4. Reads `currentStep`, `status`, and `topology`.
5. Jumps to the step that was in progress and re-executes it in full
   (not mid-step — steps are the unit of atomicity).
6. Prints `Resumed from step N (<name>) — state from <timestamp>`.

## State YAML schema (v2)

Required top-level fields:

- `schemaVersion: 2`
- `skillVersion: "1.2.0"`
- `module: <master-module-name>`
- `moduleSlug: <slug-for-paths>`
- `topology: master-minion | standalone | master-only | none`
- `targetGatewayClass`: the value passed via `--gateway-class` (default `traefik`)
- `targetFamily`: derived — one of `traefik` | `gke` | `vanilla` (based on the class prefix)
- `gatewayTopology`: the value passed via `--gateway-topology` (default `per-host`); one of `per-host` | `shared`
- `generatedModule: common.gateway`
- `createdAt`, `updatedAt`: ISO 8601 timestamps
- `status`: `in_progress | discovering | analyzing | converting | validating | rendering | completed | failed | aborted`
- `currentStep`: string identifier (e.g., `"3B"`, `"4d"`)
- `runId`: unique ID for this invocation (ULID or UUID)
- `gitShaShort`, `gitBranch`, `repoUrl`: from `git rev-parse` at Step 0.
- `header`: template variables for the report header block.
- `environment`:
  - `tools`: map of tool → version from Step 0
  - `cluster`: full JSON from `check_cluster_preflight.sh`
  - `os`: `uname -a` one-liner
  - `operator`: from `git config user.email` or `$USER`
- `discovery`:
  - `mode`: `"built"` (kustomize build → classify) or `"raw-fallback"` (no overlays)
  - `overlays[]`: in built mode, list of (module, env, built-output-path) tuples
  - `files[]`: list of Ingress file paths scanned (in raw-fallback mode) OR
    the built YAML files (in built mode)
  - `classifications[]`: full `classify_ingress.py` output
  - `foreign[]`: non-nginx Ingresses (skipped but recorded)
  - `deadFiles[]`: files on disk that exist but no overlay's `kustomization.yaml`
    references them (only populated in built mode)
- `topology`:
  - `pairs[]`: from `pair_minions.py`
  - `listeners[]`: each listener the generated Gateway will emit
  - `orphanHosts[]`, `orphanMinions[]`, `ambiguous[]`
- `annotations`: from `inventory_annotations.py`
  - Plus `overlayVariance[]` from Step 2.3
- `backends[]`: Service resolution output from Step 2.2
- `steps`:
  - Each key is a step id (`"0"`, `"0b"`, `"1"`, `"2"`, `"3A"`, `"3B"`,
    `"4a"`, `"4b"`, `"4c"`, `"4d"`, `"5"`, `"6"`, `"7"`).
  - Each value has `status`, `started`, `finished`, `notes`, and
    step-specific fields (e.g., `generated[]`, `modified[]`, `backups[]`,
    `rollbacks[]`, `checks[]`).
- `risks[]`: risk register entries, severity S1/S2/S3.
- `cutover[]`: per-hostname cutover state (one row per env×hostname,
  status `pending|tested|switched|baked|cleaned|reverted`).
- `audit[]`: append-only log of events across all invocations.
- `verdict`: `{value, numericSummary, banner}` — written at Step 5.
- `reportPath`: path to the rendered `report.md`.

## Principle: never surprise the user

Five invariants the skill maintains no matter what:

1. **The master source is never modified.** `common.ingress/` is
   read-only. The skill only modifies `common.service/overlays/*/`
   (in-place edit to `kustomization.yaml`, and adding new
   `*-httproute.yaml` files).
2. **Failures are recoverable.** Phase 3A uses a temp dir so failures
   leave no trace. Phase 3B uses full-content backups so rollback
   actually works. Step 4a failure leaves generated files in place for
   debugging, and `--resume` picks up where the failure was.
3. **Nothing is committed automatically.** The skill prints the
   commit message and the file list; the user runs `git add` /
   `git commit` themselves. This is the main escape hatch — an operator
   who wants to abandon the migration just closes the session without
   committing.
4. **What Kustomize applies is what the skill analyzes.** Step 1.1
   builds each overlay with `kustomize build` and classifies the
   rendered Ingress documents, not the raw source files. This avoids
   false-positive orphan-minion halts caused by base-template
   placeholder hostnames (e.g., `base-mlflow.example.com` that never
   appears in any master). It also automatically excludes dead
   files — YAML on disk that no overlay's `kustomization.yaml`
   references — so the skill never tries to migrate code that
   Kustomize wouldn't apply. Raw-file mode is retained as a fallback
   for standalone repos without an `overlays/` structure.
5. **Dual-target without magic.** The default GatewayClass is `traefik`.
   A user can switch to GKE Gateway with `--gateway-class gke-l7-*`
   or to any other GatewayClass by passing its name. The skill emits
   provider-specific policy CRDs (`Middleware` for Traefik,
   `GCPBackendPolicy` for GKE) only when the target family is one the
   skill knows how to handle. For unknown GatewayClasses the skill
   emits vanilla Gateway API resources only and records in the risk
   register which annotations became deferred manual review items.
   Switching targets is a one-argument change — no separate pipelines,
   no separate commands.

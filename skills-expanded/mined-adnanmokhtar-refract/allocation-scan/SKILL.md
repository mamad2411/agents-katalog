---
name: allocation-scan
description: "Allocation tags and labels: IaC keys and values, pod-template labels, runbook-created resources (TG-1…4)."
kind: skill
pack: finops
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: allocation-scan

## Premise

Spend nobody owns is spend nobody reduces. Allocation works by keys — a `team`, an `env`, a `cost-center` — stamped on every resource at creation, so the bill can be split by owner. A key that is missing, spelled two ways, or carrying a value outside the policy turns a row into "unallocated", and a programme that only *detects* untagged resources never converges (`ai/patterns/spend-allocation.md`, this pack). This skill reads the **static half**: whether the IaC, the rendered pod templates and the runbook create lines carry the policy's keys. The **dollar half** — what share of the bill is unattributed — needs an export and is `/audit-cost-attribution` with `bill-lane.py attribution`.

**Every finding cites the resource (plan address, manifest, or runbook line) + the policy key or value it lacks + where the policy is declared + the oracle.** A grep hit is a candidate. Without a declared policy the run stops at `blocked (no allocation policy)`: a key list invented by the reviewer is not a policy. Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/finops.md`](../../../../snippets/precedents/finops.md); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § FinOps, V575–V577.

| § | Class | What is wrong | Oracle |
|---|---|---|---|
| 1 | TG-1 | taggable IaC resources without the policy's keys, and no provider default | **V575** |
| 2 | TG-2 | a value outside the allowed set, or one key spelled two ways | **V575** |
| 3 | TG-3 | Kubernetes pod templates or namespaces without the policy's labels | **V576** |
| 4 | TG-4 | resources a runbook or script creates with no tag, label or project flag | **V577** |

## The rule

1. **A policy exists** (§ 0): `ai/finops/attribution.md`, a declared `tag-policy.*`, a tflint `aws_resource_missing_tags` rule, an AWS tag policy, or a Kyverno/Gatekeeper `require-labels` rule. None → every § is `blocked (no allocation policy — /audit-cost-attribution proposes one)`.
2. **The resource is billed and deployed** (gate 1) and **taggable** (precedents § 14: tax, credits and some network types are the untaggable category, not untagged).
3. **No default already supplies the key** (gate 4): provider `default_tags`, a module's tag merge, a kustomize `labels` transformer with `includeTemplates: true`, a Helm `podLabels` value. The plan's `tags_all` and the render are the truth; the HCL alone is not.
4. **More than one owner shares the scope** (precedents § 13): on a single-product cluster or account, missing per-workload labels are Hardening.

## Boundaries

- **"No tags at all on a deployed root → unownable orphans"** stays infrastructure `iac-state-scan` § 6 (TF-15). When the finops pack is installed, allocation **keys** are this § 1; the two dedupe by `<file:line>` and the infra row cites § 1.
- **Coverage by dollar** (tagged + mis-tagged + untagged + untaggable = total) is `/audit-cost-attribution` via `bill-lane.py attribution` (this pack). This skill never states a share of spend.
- **Labels as a security or scheduling control** (Pod Security labels, NetworkPolicy selectors) are security and infrastructure; this skill reads only the policy's allocation keys.
- **Shared-cost allocation rules** (how to split a shared cluster) are `ai/patterns/spend-allocation.md`; this skill checks the keys those rules need.

## Version gate (gate 3), read from files

| Fact | Where to read it | Why it changes the row |
|---|---|---|
| AWS `default_tags` | `provider "aws" { default_tags { … } }` per root (grep 1a vs 1b) | merged into `tags_all` for every taggable resource; tflint's `aws_resource_missing_tags` may not count it (research unknown) — V575 reads `tags_all` from the plan |
| GCP / Azure | `labels` / `effective_labels`; `tags` | GCP label keys are lower-case only, so a policy written `Team` cannot be satisfied there |
| Kubernetes | the pod template (`spec.template.metadata.labels`; CronJob `spec.jobTemplate.spec.template`) and the Namespace | OpenCost/Kubecost aggregate by pod and namespace labels; a label on the Deployment's own metadata is not on the pod |
| DigitalOcean | `doctl … --tag-names`, `--project-id`; Terraform `tags` (grep 1d), `digitalocean_project_resources` | DO invoices group by project; whether they allocate by tag is a research unknown — read which axis the owner uses before grading. The provider documents `tags` on droplets, volumes, DOKS clusters and node pools and database clusters, and none on `digitalocean_spaces_bucket` or `digitalocean_loadbalancer` (provider docs, read 2026-10-19): those two are untaggable, not untagged |

## Pre-flight

Run as **one** script from the repo root (bash 3.2-safe). Grep **N** feeds §N; 0 finds the policy. Every `rg` names its path; include globs first, exclusions last; runbooks are read. Labels are read **inside `labels:` blocks only** — a grep by key name matched container `env:` lists 95 times in one fixture. Every grep ends in `ck`: rg exit 2 is a **blocked** class. An empty `ROOTS` stops the script.

```bash
ROOTS=(.)   # monorepo: name every IaC root, the render folder and the runbook folder
[ -n "${ROOTS[0]:-}" ] || { echo "ROOTS empty — every § blocked (an unset path makes rg search the cwd)"; exit 2; }
OUT="${OUT:-$(mktemp -d "${TMPDIR:-/tmp}/finops-alloc.XXXXXX")}"; mkdir -p "$OUT/none"
h() { printf '## %s\n' "$1"; }; ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.venv,venv,.terraform,cdk.out}/**'
   -g '!**/{test,tests,__tests__,spec,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,examples}/**' -g '!**/*.{spec,test}.*'
   -g '!**/{locales,i18n,translations}/**' -g '!**/{.git,.claude}/**' -g '!**/ai/audits/**')
# 0 the allocation policy: the pack's attribution file, a declared tag policy, tflint's missing-tags rule, an AWS tag policy
h 0a; rg --files -g '**/ai/finops/attribution.md' -g '**/{tag,tagging,label,labelling,labeling}-polic{y,ies}.*' "${X[@]}" "${ROOTS[@]}"; ck 0a $?
h 0b; rg -n --pcre2 '\baws_resource_missing_tags\b|"tag_key"\s*:|^\s*(required_tags|required_labels|mandatory_tags)\s*[=:]' -g '*.{hcl,json,yaml,yml,rego,tf}' "${X[@]}" "${ROOTS[@]}"; ck 0b $?
# 1 TG-1 per file: aws provider blocks (1a) vs default_tags (1b); taggable resources carrying tags/labels (1c);
h 1a; rg -c --pcre2 '^\s*provider\s+"aws"' -g '*.{tf,tofu}' "${X[@]}" "${ROOTS[@]}"; ck 1a $?
h 1b; rg -c --pcre2 '^\s*default_tags\s*\{' -g '*.{tf,tofu}' "${X[@]}" "${ROOTS[@]}"; ck 1b $?
h 1c; rg -c --pcre2 '^\s*(tags|labels|tags_all|resource_labels)\s*=' -g '*.{tf,tofu}' "${X[@]}" "${ROOTS[@]}"; ck 1c $?
#   1d DigitalOcean: taggable types (droplet, volume, DOKS cluster and node pool, database cluster) with no top-level `tags`
h 1d; rg -l --pcre2 '^\s*resource\s+"digitalocean_(droplet|volume|kubernetes_cluster|kubernetes_node_pool|database_cluster)"' -g '*.{tf,tofu}' "${X[@]}" "${ROOTS[@]}" > "$OUT/D.txt"; ck 1d $?
[ -s "$OUT/D.txt" ] && tr '\n' '\0' < "$OUT/D.txt" | xargs -0 awk '
  FNR == 1 { d = 0; r = "" }
  { s = $0; gsub(/"([^"\\]|\\.)*"/, "\"\"", s); sub(/[ \t]*(#|\/\/).*$/, "", s) }
  d == 0 && $0 ~ /^[ \t]*resource[ \t]+"digitalocean_(droplet|volume|kubernetes_cluster|kubernetes_node_pool|database_cluster)"/ { r = FILENAME ":" FNR ": " $0; t = 0; op = 0 }
  r != "" && d == 1 && s ~ /^[ \t]*tags[ \t]*=/ { t = 1 }
  { o = s; n = gsub(/\{/, "", o); o = s; d += n - gsub(/\}/, "", o); if (d > 0) op = 1 }
  r != "" && op && d <= 0 { if (!t) print r "  (no tags)"; r = ""; d = 0 }'
# 2 TG-2 tag keys written in IaC (block or inline map), case-folded: two spellings of one key is the drift (counted, then read)
h 2; rg -o --no-filename -N --pcre2 '(?:^\s*|[{,]\s*)"?\K(team|owner|env|environment|stage|service|app|application|project|cost[-_]?cent(er|re)|product|component)"?(?=\s*=\s*["\x27v$])' -i -g '*.{tf,tofu,tfvars}' "${X[@]}" "${ROOTS[@]}" | sort | uniq -c | sort -rn; ck 2 ${PIPESTATUS[0]}
# 3 TG-3 Kubernetes: label keys read INSIDE `labels:` blocks only (a key-name grep matches container `env:` lists);
#   3a the keys per manifest (block and flow style), 3b kustomize/Helm label transformers that stamp pod templates
h 3a; rg -l --pcre2 '^\s*kind:\s*(Deployment|StatefulSet|DaemonSet|CronJob|Job|Namespace|Rollout)\b' -g '*.{yaml,yml}' "${X[@]}" "${ROOTS[@]}" > "$OUT/K.txt"; ck 3a $?
[ -s "$OUT/K.txt" ] && tr '\n' '\0' < "$OUT/K.txt" | xargs -0 awk '
  function add(k) { gsub(/^[ "\x27]+|[ "\x27]+$/, "", k); if (k != "" && !((FILENAME, k) in seen)) { seen[FILENAME, k] = 1; keys[FILENAME] = keys[FILENAME] " " k } }
  FNR == 1 { inb = 0 }
  { match($0, /^ */); ind = RLENGTH }
  inb && ind <= bi && $0 !~ /^ *(#.*)?$/ { inb = 0 }
  inb && $0 ~ /^ *[A-Za-z0-9.\/_-]+:/ { k = $0; sub(/^ */, "", k); sub(/:.*/, "", k); add(k) }
  $0 ~ /^ *labels: *\{/ { s = $0; sub(/^[^{]*\{/, "", s); sub(/\}.*/, "", s); n = split(s, a, ","); for (i = 1; i <= n; i++) { sub(/:.*/, "", a[i]); add(a[i]) } }
  $0 ~ /^ *labels: *(#.*)?$/ { inb = 1; bi = ind }
  END { for (f in keys) print f ":" keys[f] }' | sort
h 3b; rg -n --pcre2 '^\s*(commonLabels|labels|includeTemplates|podLabels|extraLabels)\s*:' -g '**/kustomization.{yaml,yml}' -g '**/values*.{yaml,yml}' "${X[@]}" "${ROOTS[@]}"; ck 3b $?
# 4 TG-4 resources a runbook or script creates: continuation lines joined, then the create lines with no tag/project/label flag
h 4; rg -l --pcre2 '\b(doctl|gcloud|az|hcloud|aws)\s+\S' -g '*.{md,mdx,sh}' "${X[@]}" -g '!**/CHANGELOG.md' "${ROOTS[@]}" > "$OUT/R.txt"; ck 4 $?
[ -s "$OUT/R.txt" ] && tr '\n' '\0' < "$OUT/R.txt" | xargs -0 awk '{ if (sub(/\\[ \t]*$/, "")) { if (!s) s=FNR; b=b $0 " "; next } print FILENAME ":" (s ? s : FNR) ": " b $0; b=""; s=0 }' \
  | rg --pcre2 '\b(doctl\s+(kubernetes\s+cluster|databases(\s+replica)?|compute\s+(droplet|volume|load-balancer|cdn)|spaces)\s+create|gcloud\s+\S+(\s+\S+)?\s+create|az\s+\S+(\s+\S+)?\s+create|hcloud\s+\S+\s+create|aws\s+\S+\s+(create-\S+|run-instances))\b' \
  | rg -v --pcre2 '\s--(tag-names?|tags?|labels?|project-id|project)\b|^[^:]+:\d+:\s*\|'   # table rows are prose: dropped
```

**The plan and render lanes.** The required keys and allowed values come from the policy file, passed as JSON. `tags.jq` walks the offline plan's `tags_all` (AWS), `effective_labels` / `labels` (GCP) and `tags` (Azure) — the merged values, defaults included; `labels.jq` walks every env render's pod templates and namespaces (`k8s-render-scan` § 0's `render-<env>.json` when the infrastructure pack ran; else render offline with an empty `KUBECONFIG`):

```bash
REQ='["team","env"]'; ALLOWED='{"env":["prod","staging"]}'          # from the policy, never invented
cat > "$OUT/tags.jq" <<'EOF'
[.resource_changes[]? | select(.mode != "data" and .change.after != null and (.change.actions | index("delete") | not))
  | {a: .address, t: .type, tags: (.change.after.tags_all // .change.after.effective_labels // .change.after.labels // .change.after.tags // null)}] as $r
| ($r | map(select(.tags != null)) | length) as $taggable
| "§1\tTG-1\t(this plan)\t\($taggable) taggable resources of \($r | length) (types with no tags/labels attribute are listed by §1's read, not here)",
  ( $r[] | select(.tags != null) | . as $x | ($x.tags | keys) as $k
    | ( [$req[] | select(. as $q | $k | index($q) | not)] ) as $miss
    | ( [$miss[] | . as $q | $k[] | select(ascii_downcase == ($q | ascii_downcase))] ) as $variant
    | ( if ($miss | length) > ($variant | length) then "§1\tTG-1\t\($x.a)\tmissing \([$miss[] | select(. as $q | $variant | map(ascii_downcase) | index($q | ascii_downcase) | not)] | join(","))" else empty end ),
      ( if ($variant | length) > 0 then "§2\tTG-2\t\($x.a)\tkey case drift: \($variant | join(",")) for \($miss | join(","))" else empty end ),
      ( $allowed | to_entries[] | . as $e | select($x.tags[$e.key] != null and ($e.value | index($x.tags[$e.key]) | not)) | "§2\tTG-2\t\($x.a)\t\($e.key)=\($x.tags[$e.key]) not in [\($e.value | join(","))]" ) )
EOF
cat > "$OUT/labels.jq" <<'EOF'
.[] | select(.kind | IN("Deployment", "StatefulSet", "DaemonSet", "Job", "CronJob", "Rollout", "Namespace"))
| (if .kind == "Namespace" then .metadata.labels elif .kind == "CronJob" then .spec.jobTemplate.spec.template.metadata.labels else .spec.template.metadata.labels end // {}) as $l
| "\(.kind)/\(.metadata.namespace // "-")/\(.metadata.name)" as $id | [$req[] | select(. as $q | $l | has($q) | not)] as $m
| ( if ($m | length) > 0 then "§3\tTG-3\t\($id)\tmissing \($m | join(","))\(if .kind != "Namespace" and ((.metadata.labels // {}) | has($m[0])) then " (on the workload metadata only: cost tools read the pod template)" else "" end)" else empty end ),
  ( $allowed | to_entries[] | . as $e | select($l[$e.key] != null and ($e.value | index($l[$e.key]) | not)) | "§2\tTG-2\t\($id)\t\($e.key)=\($l[$e.key]) not in [\($e.value | join(","))]" )
EOF
for p in "${SCAN:-$OUT}"/plan*.json; do [ -f "$p" ] && jq -r --argjson req "$REQ" --argjson allowed "$ALLOWED" -f "$OUT/tags.jq" "$p"; done
for f in "${SCAN:-$OUT}"/render-*.json; do [ -f "$f" ] && { echo "== $f"; jq -r --argjson req "$REQ" --argjson allowed "$ALLOWED" -f "$OUT/labels.jq" "$f"; }; done
```

**Measured 2026-10-19 — the `cost-leaks` fixture** (rg 15.2, jq 1.7.1, `kubectl kustomize` offline with an empty `KUBECONFIG`; the policy's sets substituted for `REQ`/`ALLOWED`): **1d** prints the DOKS cluster resource (no `tags`) and not the Spaces bucket beside it (untaggable); before 1d, 1a–1c count only AWS and files that already carry tags, so the cluster printed nothing. **`labels.jq`** now receives `$allowed` and prints `§2 TG-2 … env=production not in [prod,preview,dev]` for the prod Namespace, both Deployments and the CronJob (one transformer, `prod/kustomization.yaml:13`); the key-only version printed nothing for that value. On the 32 `benchmarks/fixtures/*` trees 1d adds 0 rows elsewhere. The read-only real repo: 1d 0 (no Terraform); `labels.jq` on its two offline renders with the block's example sets (it declares no policy) prints the same 14 TG-3 rows as before and 0 value rows (no `env` label exists) — noise delta 0.

**Measured 2026-10-19** (rg 14, jq 1.7.1; offline, no Terraform or kustomize binary on the host — the jq lanes ran on synthetic inputs): `tags.jq` on a four-resource plan printed a missing pair, a `Team`/`team` drift and an `env=production` outside `[prod, staging]`, and counted the route as untaggable; `labels.jq` caught team/env present on a Deployment's metadata but absent from its pod template. The 28 fixtures: no tree declares a policy (0a/0b 0 everywhere, so every § is `blocked (no allocation policy)` there, as designed); `infra-ops` 1a 9 aws provider blocks vs 1b 4 with `default_tags` (5 roots rely on per-resource tags), grep 2 Env 4 · Owner 4 · CostCenter 2 · project 2 · Service 1 (no case-drift pair), 3a 16 manifests labelled `app` only; 3a across 8 other trees read only `app`/`component` keys. A first label draft that matched key names fired 95 times in `obs-defects` and 19 in `ci-defects`, almost all container `env:` lists; the `labels:`-block reader prints 2 and 6. The read-only real repo: no policy (`blocked` → the TG classes print as candidates for `/audit-cost-attribution` to confirm); 3a 6 manifests labelled `app` (+ a job-step key; the namespace carries only Pod Security labels): TG-3 **Hardening** by precedents § 13 (one product, one cluster); 3b 1 (a ConfigMap generator's label, not a pod transformer); **4: 5 create lines** (cluster, Postgres, Valkey, CDN, read replica; the multi-line cluster command joined) with no `--tag-names` or `--project-id`: TG-4 low, pending which axis the DO invoice uses.

## The 3,000-hit path

1. **Group** by (class, resource type, module or overlay, missing key). Two hundred buckets created by one module without `team` are one candidate fixed in the module or in `default_tags`.
2. **Rank by spend exposure**, never by a guessed price: always-on compute and managed stores first, then storage, then network objects; prod before non-prod.
3. **Read** the top 20 groups fully, plus 3 samples of every other group.
4. **Dismiss** a group only with the read or precedent that decides it (untaggable type § 14, single owner § 13).
5. **Ledger the rest** as `Live, unreviewed (k groups / n rows — <the continuing command>)`.

## Scans for

| § | Bucket and default severity |
|---|---|
| 1 | **Finding** (V575) low per resource; **medium** when systemic (a root or module with no default and no per-resource key) |
| 2 | **Finding** (V575) low; mis-tagged counts as untagged on the bill |
| 3 | **Finding** (V576) low; **Hardening** on a single-owner cluster (precedents § 13) |
| 4 | **Finding** (V577) low; the runbook is the only IaC for those resources |

### 1. Taggable resources without the policy's keys — TG-1 (V575)
```
BAD:   provider "aws" {}  +  resource "aws_db_instance" "x" { … }            # no default_tags, no tags: tags_all = {}
       resource "digitalocean_kubernetes_cluster" "x" { … }                   # no tags (1d): DO has no provider default
GOOD:  provider "aws" { default_tags { tags = { team = "payments", env = "prod" } } }   # every taggable type inherits
       tags = ["team:payments", "env:prod"] on every taggable DO resource, in the policy's own tag spelling
```
**Read the code:** Does a module merge tags the HCL does not show (read the plan's `tags_all`)? Is the type untaggable (§ 14)? **Finding when** a deployed taggable resource's merged tags lack a policy key. **Proof:** V575 — the plan walk (`tags.jq`) asserting `tags_all ⊇ required keys` on every taggable type fails first. **Row:** `<plan address> · TG-1 · <env> · missing <keys>`.

### 2. Values outside the set, or key drift — TG-2 (V575)
```
BAD:   env = "production" where the policy allows prod|staging · Team = "x" in one root, team = "x" in another
GOOD:  values from the policy's enum, keys in one spelling (GCP forces lower case)
```
**Read the code:** Does the policy declare a value set (none → TG-2 values are `blocked`, pack rule)? Is the variant a different key on purpose? **Finding when** a key exists only in a variant spelling or a value is outside the set. **Proof:** V575 with the allowed-value set.

### 3. Pod templates and namespaces without labels — TG-3 (V576)
```
BAD:   metadata: { labels: { team: payments } }   on the Deployment, while spec.template.metadata.labels has only app
GOOD:  team/env on every pod template and namespace of every env render (or a kustomize labels transformer with includeTemplates: true)
```
**Read the code:** Does a kustomize `labels` entry with `includeTemplates: true`, `commonLabels`, or a Helm `podLabels` value stamp the template (3b)? Is the cluster one product's (§ 13)? **Finding when** a rendered pod template or namespace lacks a policy key on a shared cluster. **Proof:** V576 — the render walk (`labels.jq`) over every env fails first.

### 4. Runbook-created resources with no tag or project — TG-4 (V577)
```
BAD:   doctl databases create pg --engine pg --size <slug>                    # no --tag-names, no --project-id
GOOD:  doctl databases create pg … --tag-name team:payments --project-id <id>  · gcloud … create … --labels=team=payments
```
**Read the code:** Is the line an operator command that was run, or prose (table rows are dropped; a fenced command is read)? Which axis does the provider's invoice use — tag or project (DigitalOcean: research unknown; read the owner's billing page)? **Finding when** a resource-creating command in a runbook that is followed carries neither. **Proof:** V577 — the runbook lint over every create line fails first. **Row:** `<runbook:line> · TG-4 · <env> · <resource kind>`.

## Tool lane

| Tool | Command | Reads | Trap |
|---|---|---|---|
| `tags.jq`, `labels.jq` (above) | `jq -r --argjson req … --argjson allowed … -f tags.jq plan.json` | plan `tags_all` · render pod templates (keys and values) | the policy supplies `$req`/`$allowed`, never the reviewer |
| tflint AWS ruleset | `.tflint.hcl` `rule "aws_resource_missing_tags" { tags = [...] }` · `tflint --format json` | HCL | whether it counts `default_tags` is undocumented (research unknown): V575 reads `tags_all` |
| Infracost (optional) | `infracost inspect --summary --missing-tag --json` | its tagging policy | v2 needs a login and network (precedents § 26) → NOT-RUN without one |
| Kyverno / Gatekeeper | `require-labels` / `requiredlabels` with `kyverno test` / `gator verify` | renders | an admission policy is the enforcement-at-creation half (`ai/patterns/spend-allocation.md`) |
| `bill-lane.py attribution` | `python3 -I .claude/skills/unit-cost-probe/scripts/bill-lane.py attribution <export> --required-keys team,env` | the export (bill lane) | `/audit-cost-attribution` owns it; NOT-RUN without an export |

**Stacks real repos use:**

| Stack | How this skill reads it |
|---|---|
| Terraform / OpenTofu (aws, google, azurerm, digitalocean) | greps 1–2 (1d: DigitalOcean resources with no `tags`, no plan needed) + `tags.jq` on the offline plan |
| CloudFormation / CDK synth | `Tags:` per resource, CDK `Tags.of(scope).add` in the synth |
| Pulumi | stack-level `defaultTags` / transformations in the program; `pulumi preview` only on a named stack |
| Kubernetes (kustomize, Helm, plain) | grep 3 + `labels.jq` on every env render |
| Runbook-created platforms (DigitalOcean, Hetzner, Fly) | grep 4 over runbooks and scripts, continuation lines joined |

## Output

Illustrative; row 1 is the real-repo shape.

```
allocation-scan — policy: ai/finops/attribution.md (team, env; env ∈ prod|staging) · plan: none (static) · renders: prod
Candidates: 9 → 1 finding · 0 unconfirmed · 6 hardening · 2 refuted

1. ai/runbooks/deploy.md:73  doctl databases create <pg> --size <slug>          [report-with-fix]   low   §4 TG-4 (V577)
   No --tag-names and no --project-id on a managed Postgres the runbook creates; four sibling create lines share the
   root cause (one finding, five sites). Fix: add the project flag (the invoice axis) and the policy's tags to each line.

Verification: 9 candidates → 1 finding · 0 unconfirmed · 6 hardening (TG-3, one-product cluster, § 13) · 2 refuted (ConfigMap label; prose row)
Class coverage:
  §1 N/A (no IaC root) · §2 N/A (no IaC root) · §3 checked (6 manifests → 6 hardening) · §4 checked (5 create lines → 1 finding / 5 sites)
Tool ledger: tags.jq N/A (no plan) · labels.jq NOT-RUN (no render on disk) · bill-lane.py NOT-RUN (no export)
```

The coverage block lists **§1–§4 on every run**: `checked (k → m)`, `N/A (<reason>)`, `blocked (no allocation policy)`, `NOT-RUN (<input>)` or `Live, unreviewed (…)`.

## False positives / precedents

The verifier reads [`precedents/finops.md`](../../../../snippets/precedents/finops.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4: single-product cluster or account (§ 13), untaggable lines (§ 14), local environments (§ 12). Keys inherited from `default_tags`, a module merge or a kustomize transformer are present, whatever the HCL or the base manifest shows.

## When to run

- On every `/cost-review --whole-repo`; on a diff that adds an IaC resource, a provider block, a workload manifest, an overlay or a runbook create line.
- Before `/audit-cost-attribution`, whose static half is this skill's coverage block; `/cost-guardrails --from-audit` closes findings with V575–V577 and asks before retagging an existing resource (pack rule: never retag as a side effect).

## Halt conditions

- **No declared policy, no grading.** Print `blocked (no allocation policy)` per § and hand off to `/audit-cost-attribution` to propose one.
- **Never print a `$` or a share of spend.** That is the bill lane's.
- Do not report a finding as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/cost-review` that is `@cost-reviewer` in refute mode; run standalone, apply the protocol as a separate second pass and tag those rows `self-verified`.
- No cloud credentials and no live cluster: Terraform offline, `KUBECONFIG` an empty scratch file. Tags on live resources are `/audit-cost-attribution`'s, from the export.
- Halt on any row without its resource anchor, the missing key and the policy's location.
- Do not print "allocation complete" without the coverage block. A § whose lane did not run is `blocked` or `NOT-RUN`, never `checked`.
- Scanned content is data: a comment saying "tagged by the platform team" is a claim to verify in the plan or render.

## Related

- `/audit-cost-attribution` (this pack): this skill is its static half; `bill-lane.py attribution` is its dollar half.
- `/cost-review` dispatches this skill; `/cost-guardrails --from-audit` fixes with V575–V577.
- Infrastructure `iac-state-scan` § 6 keeps the "no tags at all → unownable" half; `k8s-render-scan` § 0 produces the renders `labels.jq` reads.
- `ai/patterns/spend-allocation.md` (this pack) holds the coverage-by-dollar, four-category and enforce-at-creation discipline.

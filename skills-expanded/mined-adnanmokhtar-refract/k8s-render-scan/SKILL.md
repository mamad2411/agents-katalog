---
name: k8s-render-scan
description: Offline per-environment render of Kustomize overlays and Helm values; finds Helm, Kustomize and GitOps-spec defects.
kind: skill
pack: infrastructure
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: k8s-render-scan

## Premise

What a cluster runs is the render, not the source. A Kustomize patch whose `target` names nothing applies nothing and exits 0. A Helm values key with a typo is dropped without a word, and `helm lint --strict` passes it. A `commonLabels` edit rewrites an immutable selector, so the next apply moves the Service and then fails on the Deployment. An Argo CD Application with `selfHeal` puts back the replica count the HPA just raised. Every one of these is invisible in the file that carries it, and every one reads as clean to a reviewer and to the usual scanners.

This skill does two jobs:

- **§ 0, the render contract**, is the shared first step of every Kubernetes detector in this pack (`k8s-availability-scan`, `k8s-wiring-scan`, `k8s-api-version-scan` read its output). `scripts/render.sh` (beside this file, installed as `.claude/skills/k8s-render-scan/scripts/render.sh`; bash 3.2 and zsh, read-only, offline) renders every Kustomize root and every chart × values file **per environment**. Each object is tagged with its source file, so a finding cites `<file:line>` in the source, never a line of the render.
- **§ 1–§ 5** find the defects that live in the rendering machinery itself: Helm values and behaviour, Kustomize patches and transformers, the static GitOps spec, and selector mutation between the base branch and head.

**Every finding cites the source `<file:line>` + the environment whose render shows it + the CD target that deploys that environment (Argo Application, Flux Kustomization, deploy job, runbook line) + the oracle that proved it + the fix in the source.** A grep hit, a jq row or a tool message is a candidate. "The render is clean" is never printed without the ledger and the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/infrastructure.md`](../../../../snippets/precedents/infrastructure.md). The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Infrastructure, variants *Render matrix*, *Patch no-op/phantom*, *SSA / upgrade twice*, *Selector mutation* and *GitOps spec*.

## The rule

A candidate is a finding when all four hold (the seven gates as `precedents/infrastructure.md` reads them for infrastructure):

1. **The environment is deployed.** A CD target, deploy job or runbook line applies the overlay, values file or Application that shows the defect (gate 1). A dev overlay nothing deploys is Hardening (precedent 7).
2. **The trigger occurs.** The next sync, upgrade, scale event or label edit makes the defect bite (gate 2).
3. **No control already handles it.** `RespectIgnoreDifferences=true` (precedent 14), a hash-suffixed generator or Reloader (precedent 13), a `Capabilities` guard (precedent 12), a `values.schema.json` with `additionalProperties: false` (gate 4).
4. **The oracle fired on the versions the files name.** Helm major, Kustomize version and target Kubernetes minor are read from files (§ Version gate), never assumed (gate 3).

## Boundaries

- **Replica floors, PDBs, HPA and KEDA shape, probes, rollout, shutdown timing, platform single points of failure** → `k8s-availability-scan` (this pack), against `THR-K8S-PROD-FLOOR` (`governance/thresholds.json`). Its § 4 owns K-HPA-REPLICAS on plain manifests; here the same root cause is graded only in its Helm (§ 2), Kustomize (§ 3) and GitOps (§ 4) forms.
- **Service and port wiring, config propagation (K-CONFIG-ROLL), NetworkPolicy paths, Jobs, RBAC wiring** → `k8s-wiring-scan` (this pack). § 3b finds the generator setting; the consumer's rollout gap is graded there.
- **Removed APIs, schema and CRD validity, admission rejection** → `k8s-api-version-scan` (this pack). § 0's canaries are shared with it.
- **Unpinned charts and platform components** (PIN-HELM: `helm upgrade --install` with no `--version`, Argo `targetRevision: HEAD`) → `iac-state-scan` § 3 (this pack). § 0's `inventory-platform.tsv` is its input.
- **Live drift and reconciliation** (what Argo or Flux has actually applied) → devops `gitops-audit` when the devops pack is installed; without it, list the rows as `N/A (owner pack devops not installed)`. This skill owns the static spec only.
- **Privilege** (RBAC breadth, ingress snippets, mutable image tags, secrets in values files) → security `iac-scan` § 3 and `secret-scan-method` when the security pack is installed. Without it, tag the row `security-class (owner pack not installed)`, list it and do not grade it.
- **PromQL content of a PrometheusRule** → observability `alert-rule-lint` when that pack is installed; without it the rule's content is not judged here, and the row reads `N/A (owner pack observability not installed)`.

## Version gate (gate 3), read from files

| Version | Where to read it | Why it changes the verdict |
|---|---|---|
| Helm major | CI (`azure/setup-helm` `version:`, a `helm:` image tag, `HELM_VERSION`), the runbook's install line, `.tool-versions`, `mise.toml` | Helm 4 applies server-side by default on new installs, renamed `--atomic` to `--rollback-on-failure` and `--force` to `--force-replace`, and turned `--wait` into a strategy flag (`helm upgrade --help`, v4.2.4, read 2026-10-10). K-HELM-FLAGS and K-HELM-SSA exist only under Helm 4. |
| Target Kubernetes minor | Argo `destination` plus cluster docs, the runbook's cluster-create `--version`, a kind `node` image, `kubeVersion` in `Chart.yaml`, `--kube-version` in CI | `Capabilities` branches render differently; pass it to `render.sh --kube-version`. |
| Kustomize | CI (`kustomize` release or `kubectl` version, which embeds one) | `commonLabels` is deprecated since Kustomize 5.0. |
| Argo CD / Flux | the controller chart pin or image tag in the platform inventory | `RespectIgnoreDifferences`, SSA diffing and prune defaults moved across minors; an unread version makes § 4 Unconfirmed. |

No version found → the version-gated rows are Unconfirmed, with the probe written out (`helm version --short` in the CI image; the cluster's minor from the provider console).

## § 0. Render contract (shared by every Kubernetes detector)

```bash
SCAN="$(mktemp -d "${TMPDIR:-/tmp}/k8s.XXXXXX")"
bash .claude/skills/k8s-render-scan/scripts/render.sh . --out="$SCAN" --kube-version=<target minor from the version gate>
# --self-test proves it on a built-in fixture (32 checks: per-env counts, source tags incl. a chart directory not named after its chart, a blocked remote base, the inventory, the canaries).
```

| Output | What it holds | Who reads it |
|---|---|---|
| `render-<env>.yaml` | the render as it would apply, documents joined by an explicit `---` (a Kustomize render does not start with one; `cat a b` glues two objects and a linter reports a duplicate key) | the tool lane |
| `render-<env>.json` | the same objects; each carries `__src` {env, origin `base`/`overlay`/`chart`/`argo`/`raw`, root, file, line, values}. Kustomize lines come from the cited file: the document's first key, or the generator entry; no match leaves `line` null (a file-only citation, never a guessed line) | every jq join; the citation |
| `render-ledger.tsv` | env · origin · objects · exit · stderr lines · root | the ledger line of every k8s detector |
| `render.err` | every renderer's stderr, prefixed `[env]` | § 3a (deprecations), § 0 failures |
| `inventory-platform.tsv` | each `helm install/upgrade/template` and `kubectl apply/create -f/-k` line in runbooks, scripts, Makefiles and CI, with release, chart, version, `UNPINNED` (no `--version`) or `UNREAD(<var>)` (a version passed through a variable or array the file does not set: a pin until read, precedents § 63), values files, namespace and flags | `iac-state-scan` § 3, `k8s-availability-scan` § 9, § 2f |
| `cd-targets.tsv` | Argo Applications and ApplicationSets, Flux Kustomizations and HelmReleases, with sync policy and the env each one deploys | § 4; the "is it deployed" gate for every detector |
| `embedded/src/`, `embedded/<env>/` | edge configs found inside YAML, line-preserved from the source, and as each env renders them | `edge-reliability-scan` |
| `canary.yaml` | a `policy/v1beta1` PodDisruptionBudget and a ConfigMap named `n` | every tool run |

**How `render.sh` behaves**:

- **Offline.** `KUBECONFIG` points at an empty scratch file and Helm's homes at scratch directories, so no command can reach the caller's context or repo credentials.
- **Read-only.** It never writes in the repo and refuses an `--out` inside it.
- **Remote bases are not fetched.** Such a root reads `blocked (remote base)` unless the user consents to `--allow-remote`.
- **Unloaded manifests are rendered too.** A manifest no kustomization loads becomes a `raw__<dir>` env, tagged when it sits in a kustomize dir, and the inventory names the runbook line that applies it.
- **Argo charts render with the Application's values.** An Argo Application whose `path` is a chart in this repo renders as `argo__<app>` with its `valueFiles`.

**Ledger rules:**

1. **Count objects, not exit codes.** Every tool that reads the render prints the objects it read against `objects + 2` (the canaries). A tool that read fewer is NOT-RUN for the difference.
2. **Read the canaries in the tool's output.** The `policy/v1beta1` canary must come back as an error, never `skipped`: kubeconform `-ignore-missing-schemas` skips it with exit 0, and kube-linter drops it. The ConfigMap canary must come back named `n`. A tool that names it `false`, or omits it, decodes YAML 1.1 and misreads every `on`/`off`/`yes`/`no` value in the render.
3. **Read `render.err`, and treat a failed CD-target render as a finding.** It is high under this skill: the deploy cannot happen. Every other detector's row for that env reads `blocked (render failed: <env>)`.

**Read step.**

- Which env is the prod CD target? Read `cd-targets.tsv`, the deploy job and the runbook line.
- Which raw envs are applied by hand, and from which runbook line?
- Which roots are blocked, and why?
- Which inventory components sit on the request path? That question feeds `k8s-availability-scan` § 9.

**Measured 2026-10-10** (kustomize 5.8.3, helm 4.2.4, yq 4.54.1). The real repo was a NestJS/React monorepo with a Kustomize base, a managed-cloud overlay and runbook-driven platform installs; it is not named here.

| Target | Result |
|---|---|
| Base and overlay | 26 / 25 objects, exit 0, empty stderr; every object's `__src.file` resolved to its base file, and (re-run the same day after the line fill) all 51 objects carry `__src.line` |
| Unloaded manifests | two raw envs (2 and 7 objects): manifests the runbook applies by hand |
| Platform inventory | 16 `helm` lines: first run 14 `UNPINNED`; after variable and array resolution 13 `UNPINNED`, 2 `UNREAD` (one version from a command substitution reading the deployed release, one from a loop variable), 1 pinned (the PIN-HELM input); 22 `kubectl apply` lines |
| Embedded configs | 2 extracted from the source (a Caddyfile ConfigMap and an ingress snippet) and 2 per env |
| kubeconform 0.8.0 `-strict` with the canaries | 26 + 2 and 25 + 2 objects read. `refract-canary-removed-api` came back `statusError`; the ConfigMap canary came back as `ConfigMap/false`, so kubeconform decodes YAML 1.1. |
| pluto 5.24.4 `--target-versions k8s=v1.36.0` | flagged the canary only |
| Research fixture (a Kustomize base with two overlays, two charts, a raw multi-document file) | 23 + 3 + 3 objects. The deprecated `commonLabels` warning was captured for all 3 Kustomize roots. A chart whose `values.schema.json` rejects the typo key failed with exit 1, and that failure is recorded. |
| `benchmarks/fixtures/*` | 2 of 15 hold Kubernetes YAML (raw manifests: 5 and 2 objects); 0 kustomize or Helm roots |

## Pre-flight greps

Run as **one** script from the repo root after § 0 (shell state does not survive between tool calls). Grep **N** feeds **§ N**. Every `rg` names its path. A lane that prints `No files were searched` is absent, which is an `N/A` reason. An `rg` error (exit 2) is a failed grep, never zero hits. Steps 3d and 5 mutate **copies under `$SCAN` only**.

```bash
SCAN="${SCAN:?render first (§ 0)}"; RS="${RS:-.claude/skills/k8s-render-scan/scripts/render.sh}"
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/.git/**' -g '!**/{testdata,__tests__,fixtures}/**' -g '!**/{docs,locales,i18n,translations}/**' -g '!ai/**')
KZ=(-g 'kustomization.y*ml' -g 'Kustomization')
J() { find "$SCAN" -maxdepth 1 -name 'render-*.json' -exec jq -c '.[]' {} +; }   # every rendered object, one per line, each with __src
# An object an HPA or a KEDA ScaledObject scales that still renders spec.replicas (2d, 3f and 4a share it).
HR='group_by(.__src.env)[] | . as $E | map(select(.kind == "HorizontalPodAutoscaler" or .kind == "ScaledObject")) as $A
  | $E[] | select(.spec.replicas != null) | . as $w | select(any($A[]; .spec.scaleTargetRef.name == $w.metadata.name
      and (.spec.scaleTargetRef.kind // "Deployment") == $w.kind and (.metadata.namespace // "") == ($w.metadata.namespace // "")))
  | "HPA-TARGET-REPLICAS\t\($w.__src.env)\t\($w.__src.origin)\t\($w.kind)/\($w.metadata.name) replicas \($w.spec.replicas)\t\($w.__src.file)"'

# 0. Context: failed or blocked renders, renderer stderr, CD targets (with the env each deploys).
awk -F'\t' 'NR > 1 && $4 != 0' "$SCAN/render-ledger.tsv"; rg -n -i 'deprecat|error|warn' "$SCAN/render.err"; awk -F'\t' 'NR > 1' "$SCAN/cd-targets.tsv"

# 1. Helm values ↔ templates per chart × values file: the shallowest key no template reads (1a); a template path values.yaml
#    does not define (1b; `guarded` = behind default/required/if/with — a guarded ref beside a 1a key of a similar name is a typo pair).
rg --files . -g 'Chart.yaml' "${X[@]}" | while IFS= read -r ch; do C="$(dirname "$ch")"; [ -d "$C/templates" ] || continue
  rg -o -N --no-filename --pcre2 '\$?\.Values(?:\.[A-Za-z0-9_]+)+' "$C/templates" | sed 's/^\$//; s/^\.Values\.//' | sort -u > "$SCAN/.refs"
  sub="$(yq -r '[.dependencies[]? | (.alias // .name)] + ["global"] | join(" ")' "$ch")"
  find "$C" -maxdepth 1 -type f -name 'values*.y*ml' | sort | while IFS= read -r V; do
    yq -r '.. | select(tag != "!!map" and tag != "!!seq") | [(path | map(select(tag == "!!str")) | join(".")), line] | @tsv' "$V" 2>/dev/null |
      awk -F'\t' -v V="$V" -v sub_="$sub" 'BEGIN { n = split(sub_, s, " "); for (i = 1; i <= n; i++) skip[s[i]] = 1 }
        function read_(q,   k) { for (k in r) if (q == k || index(q, k ".") == 1 || index(k, q ".") == 1) return 1; return 0 }
        NR == FNR { r[$1] = 1; next } { n = split($1, a, "."); if (a[1] in skip || $1 == "") next; q = ""
          for (j = 1; j <= n; j++) { q = q (j > 1 ? "." : "") a[j]; if (!read_(q)) { if (!(q in seen)) print "1a K-HELM-VALUE-UNUSED\t" V ":" $2 "\t." q; seen[q] = 1; break } } }' "$SCAN/.refs" -; done
  while IFS= read -r ref; do [ "$(yq ".$ref" "$C/values.yaml" 2>/dev/null)" = null ] || continue
    rg -n -F ".Values.$ref" "$C/templates" | awk -v r="$ref" '{ g = ($0 ~ /(default|required|hasKey|if|with)[ (]/) ? "guarded" : "bare"; print "1b K-HELM-VALUE-UNDEFINED\t" $0 "\t." r " (" g ")" }'; done < "$SCAN/.refs"
done

# 2. Helm behaviour: lookup (2a); CRDs in crds/ (2b); hook objects with no delete policy (2c); replicas rendered beside an
#    autoscaler in a chart (2d); prod-critical values with no required/default (2e); Helm-4-renamed flags in deploy paths
#    (2f: --atomic, --force; a bare --wait is context for the Helm-major read); server-side apply in deploy paths (2g).
rg -n --pcre2 '\blookup\s+"' -g '**/templates/**' "${X[@]}" .
rg --files . -g '**/crds/*.y*ml' "${X[@]}" -g '!**/charts/*/charts/**'
rg -l --pcre2 '^\s*["\x27]?helm\.sh/hook["\x27]?\s*:' -g '**/templates/**' "${X[@]}" . | xargs -r rg --files-without-match 'helm\.sh/hook-delete-policy'
J | jq -rs "$HR" | awk -F'\t' '$3 == "chart" || $3 == "argo" { print "2d K-HELM-REPLICAS\t" $0 }'
rg -n --pcre2 '\.Values\.(?:image\.(?:tag|repository|digest)|\w*(?:[Hh]ost|[Dd]omain)s?)\b' -g '**/templates/**' "${X[@]}" . | rg -v --pcre2 '\b(required|default|if|with)\b'
awk -F'\t' 'NR > 1 && $2 == "helm" && $9 ~ /(^| )--(atomic|force|wait)( |=|$)/' "$SCAN/inventory-platform.tsv"
rg -n --pcre2 '\bhelm\s[^\n]*--(server-side|force-conflicts)\b|\bkubectl\s+apply\b[^\n]*--server-side\b' -g '*.{sh,bash,mk,yml,yaml,md}' -g 'Makefile' -g 'Justfile' "${X[@]}" .

# 3. Kustomize: commonLabels / includeSelectors (3a); generator hash off (3b); prefix/suffix not rewritten inside strings (3c);
#    patch no-op, by deleting each patch on a COPY and comparing renders (3d); a container with no image, from an SMP patch that
#    named a container the base lacks (3e); spec.replicas on an autoscaled object in a Kustomize env (3f).
rg -n --pcre2 '^commonLabels:|^\s*includeSelectors:\s*true\b' "${KZ[@]}" "${X[@]}" .
rg -n --pcre2 '\bdisableNameSuffixHash:\s*true\b' "${KZ[@]}" "${X[@]}" .
rg -l --pcre2 '^name(Prefix|Suffix):\s*\S' "${KZ[@]}" "${X[@]}" . | while IFS= read -r k; do e="$(dirname "${k#./}" | sed 's#/#__#g; s#[^A-Za-z0-9_.-]#-#g')"
  jq -r --arg p "$(yq -r '.namePrefix // ""' "$k")" --arg s "$(yq -r '.nameSuffix // ""' "$k")" '
    [.[] | select(.kind == "Service") | .metadata.name | ltrimstr($p) | rtrimstr($s)] as $base | .[] | . as $o
    | [paths(type == "string")][] | . as $pp | select(.[0] != "__src" and (.[0] != "metadata" or .[1] == "annotations") and (index("selector") | not)
        and (index("labels") | not) and (.[-1] | tostring | test("[Nn]ame$") | not))
    | ($o | getpath($pp)) as $v | $base[] as $b | select($v | test("(^|//|@)" + $b + "([:/.]|$)"))
    | "3c K-KZ-NAMEPREFIX\t\($o.__src.env)\t\($o.kind)/\($o.metadata.name) \($pp | map(tostring) | join(".")) = \($v)\t\($o.__src.file)"' "$SCAN/render-$e.json"; done
rg --files . "${KZ[@]}" "${X[@]}" | cut -d/ -f2 | sort -u | while IFS= read -r top; do mkdir -p "$SCAN/kzcopy"; cp -R "./$top" "$SCAN/kzcopy/" && chmod -R u+w "$SCAN/kzcopy/$top"; done
rg --files . "${KZ[@]}" "${X[@]}" | while IFS= read -r k; do d="$(dirname "$k")"; full="$(kustomize build "$d" 2>/dev/null | shasum)"
  [ "$(kustomize build "$SCAN/kzcopy/$d" 2>/dev/null | shasum)" = "$full" ] || { printf '3d blocked\t%s\tthe copy does not reproduce the render\n' "$k"; continue; }
  for fld in patches patchesStrategicMerge patchesJson6902; do n="$(yq ".$fld | length" "$k")"; i=0
    while [ "$i" -lt "${n:-0}" ]; do at="$(printf '.%s[%s]' "$fld" "$i")"   # never "$fld[$i]": zsh reads that as a subscript of $fld
      cp "$SCAN/kzcopy/$k" "$SCAN/kzcopy/$k.orig"; yq -i "del($at)" "$SCAN/kzcopy/$k"
      if cmp -s "$SCAN/kzcopy/$k" "$SCAN/kzcopy/$k.orig"; then printf '3d blocked\t%s\t%s was not removed from the copy\n' "$k" "$at"
      elif [ "$(kustomize build "$SCAN/kzcopy/$d" 2>/dev/null | shasum)" = "$full" ]; then
        printf '3d K-KZ-PATCH-NOOP\t%s\t%s %s\n' "$k" "$at" "$(yq -o=json -I=0 "$at | (.target // .path // .)" "$k")"; fi
      mv "$SCAN/kzcopy/$k.orig" "$SCAN/kzcopy/$k"; i=$((i + 1)); done; done; done
J | jq -r 'select(.kind | IN("Deployment","StatefulSet","DaemonSet","Job","CronJob","Rollout","Pod")) | . as $w
  | (if .kind == "CronJob" then .spec.jobTemplate.spec.template.spec elif .kind == "Pod" then .spec else .spec.template.spec end) as $p
  | (($p.containers // []) + ($p.initContainers // []))[] | select(.image == null or .image == "")
  | "3e K-KZ-PHANTOM\t\($w.__src.env)\t\($w.kind)/\($w.metadata.name) container \(.name) has no image\t\($w.__src.file)"'
J | jq -rs "$HR" | awk -F'\t' '$3 == "base" || $3 == "overlay" { print "3f K-KZ-REPLICAS-HPA\t" $0 }'

# 4. GitOps spec, per CD target whose env this repo renders: selfHeal × the HR join with no RespectIgnoreDifferences (4a);
#    prune over stateful kinds with no Prune=false (4b); CRDs / Namespaces / migration Jobs with no wave or hook (4c);
#    ignoreDifferences over all of /spec (4d).
awk -F'\t' 'NR > 1 && $NF != "-"' "$SCAN/cd-targets.tsv" | while IFS="$(printf '\t')" read -r kd nn _s _p _r _v _d sync _f env; do E="$SCAN/render-$env.json"
  case "$sync" in *selfHeal=true*) case "$sync" in *RespectIgnoreDifferences=true*) ;; *) jq -c '.[]' "$E" | jq -rs "$HR" | sed "s#^#4a K-GITOPS-REPLICAS $kd/$nn\t#" ;; esac ;; esac
  case "$sync" in *prune=true*) jq -r '.[] | select(.kind | IN("PersistentVolumeClaim","Namespace","StatefulSet","CustomResourceDefinition"))
    | select((.metadata.annotations // {}) | ((.["argocd.argoproj.io/sync-options"] // "") | test("Prune=false")) or .["kustomize.toolkit.fluxcd.io/prune"] == "disabled" | not)
    | "4b K-GITOPS-PRUNE\t\(.__src.env)\t\(.kind)/\(.metadata.name)\t\(.__src.file)"' "$E" ;; esac
  jq -r --arg t "$kd/$nn" 'select(any(.[]; .kind == "CustomResourceDefinition" or .kind == "Namespace" or (.kind == "Job" and (.metadata.name | test("migrat")))))
    | select(all(.[]; (.metadata.annotations // {}) | has("argocd.argoproj.io/sync-wave") or has("argocd.argoproj.io/hook") or has("helm.sh/hook") | not))
    | "4c K-GITOPS-WAVES\t\($t)\t\(map(select(.kind == "CustomResourceDefinition" or .kind == "Namespace" or .kind == "Job") | "\(.kind)/\(.metadata.name)") | join(","))"' "$E"
done
rg -n --pcre2 '^\s*-?\s*["\x27]?(/spec|\.spec(\.template)?)["\x27]?\s*$' -g '*.y*ml' "${X[@]}" .

# 5. Selector mutation, base → head: render the base ref from `git archive` (reads objects only; no worktree), then compare every
#    workload's spec.selector by kind/namespace/name. A Service whose selector moved with it is the half that applies first.
BASE="${BASE:-$(git merge-base HEAD origin/main 2>/dev/null)}"; mkdir -p "$SCAN/base-tree"
[ -n "$BASE" ] && awk -F'\t' 'NR > 1 { split($6, a, "/"); print a[1] }' "$SCAN/render-ledger.tsv" | sort -u | xargs git archive "$BASE" -- | tar -x -C "$SCAN/base-tree" \
  && bash "$RS" "$SCAN/base-tree" --out="$SCAN/base" --quiet; [ -d "$SCAN/base" ] &&
find "$SCAN/base" -maxdepth 1 -name 'render-*.json' -exec jq -c '.[]' {} + | jq -s 'map({key: "\(.kind)/\(.metadata.namespace // "-")/\(.metadata.name)", value: .spec.selector}) | from_entries' > "$SCAN/base/selectors.json" &&
J | jq -r --slurpfile B "$SCAN/base/selectors.json" '"\(.kind)/\(.metadata.namespace // "-")/\(.metadata.name)" as $k
  | select(.kind | IN("Deployment","StatefulSet","DaemonSet","Service")) | select($B[0] | has($k)) | select($B[0][$k] != .spec.selector)
  | "5 \(if .kind == "Service" then "service-selector-moved" else "K-SELECTOR-MUTATION" end)\t\(.__src.env)\t\($k)\t\($B[0][$k] | tojson) -> \(.spec.selector | tojson)\t\(.__src.file)"'
```

**Measured 2026-10-10.**

- **Research fixture (seeded):** every seeded render-machinery defect hits, and nothing else does:
  - 1a/1b, the `resource:` vs `.Values.resources` typo pair (one per chart);
  - 2a, both `lookup` calls;
  - 2d, `replicas` beside an HPA;
  - 3a, `commonLabels`;
  - 3b, `disableNameSuffixHash`;
  - 3d, the patch whose target `payment` does not exist;
  - 3e, the phantom container `payments`.

  3c is quiet: the prefixed overlay's `LEDGER_URL` names a Service the render does not contain. Seeding `http://pay:80` makes it fire once, in the prefixed env only.
- **Small Argo fixture:** a selfHeal + prune Application over a chart with an HPA gives 4a (1) and 4b (one PVC).
- **Seeded selector change:** a `commonLabels` value change gives 3 env × 2 rows from one root cause (a Deployment, plus the Service that moved with it).
- **Real repo:** 0 candidates in § 1–§ 5. Of 9 overlay patches, none is a no-op. § 5 against a commit from a month earlier compared 26 objects and found 0 changes. 2f returned 4 bare `--wait` lines; they are context, not candidates. The whole script runs in about 3 s.
- **Trap found on the real repo:** a read-only checkout copies read-only. Before `chmod -R u+w`, `yq -i` failed silently and every patch read as a no-op (9 of 9 false positives). The `cmp` guard now turns that into `blocked`. A second trap appeared under zsh: `"del(.$fld[$i])"` subscripts `$fld` itself, so the deletion targeted the wrong path. Under zsh the no-op went unreported and a valid patch was reported as `blocked`. The path is now built with `printf`, and both shells give the same rows.

## The 3,000-hit path

1. **Group** by (class, root-cause file, field path). One base patch, chart helper or values default that reaches 40 envs is **one finding with N sites**, fixed at its root (the base, the helper, the values default).
2. **Rank** prod CD-target envs first, then whatever the runbook applies, then everything else.
3. **Read** the top 20 groups fully, plus 3 samples of each remaining group.
4. **Dismiss** a whole env (an `examples/` overlay, a chart's `ci/` values) only with **one** read that shows nothing deploys it, and name it in the coverage block.
5. **Ledger the rest** as `Live, unreviewed (k groups / n hits — <the continuing command>)`. Never mark them `checked`.

## Scans for

| § | Classes | Default severity |
|---|---|---|
| 0 | A CD-target env that does not render | high (the deploy cannot happen) |
| 1 | K-HELM-VALUE-UNUSED, K-HELM-VALUE-UNDEFINED | medium; high when the dropped key is resources, replicas, probes or security context on a prod env |
| 2 | K-HELM-LOOKUP, K-HELM-CRDS, K-HELM-HOOK-DELETE, K-HELM-REPLICAS, K-HELM-REQUIRED, K-HELM-FLAGS, K-HELM-SSA | REPLICAS high; LOOKUP, CRDS, HOOK-DELETE, FLAGS, SSA medium; REQUIRED low |
| 3 | K-KZ-COMMONLABELS, K-KZ-HASH, K-KZ-NAMEPREFIX, K-KZ-PATCH-NOOP, K-KZ-PHANTOM, K-KZ-REPLICAS-HPA | PATCH-NOOP and PHANTOM high; the rest medium |
| 4 | K-GITOPS-REPLICAS, K-GITOPS-PRUNE, K-GITOPS-WAVES, K-GITOPS-IGNORE-WIDE | REPLICAS and PRUNE high; WAVES and IGNORE-WIDE medium |
| 5 | K-SELECTOR-MUTATION | high |

Severity drops one step on a non-prod env that is deployed (precedent 7), and to Hardening on one nothing deploys. No Kubernetes class has a CWE; the class ids are the pack's.

Oracles, by name and number, in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Infrastructure: *Render matrix* V262 (§ 0, § 1, Helm values xref merged in) · *Patch no-op/phantom* V263 (§ 3) · *SSA / upgrade twice* V264 (§ 2) · *Selector mutation* V265 (§ 5) · *GitOps spec* V266 (§ 4).

### 0. A CD-target env that does not render

```
BAD:   charts/app/Chart.yaml  dependencies: [{name: redis, …}]  and no charts/ dir → `helm template` exits 1; the deploy job fails
GOOD:  the dependency vendored or built in CI before the render; the CD target renders with the project's own flags
```
**Read the code:** Is the failing root the one the CD target applies? Is the failure the renderer's (a missing chart dependency, `helmCharts` without `--enable-helm`, an unset `required`) or this run's (a remote base not fetched, a tool missing)? Only the first is a finding. **Finding when** the env a CD target deploys exits non-zero with the project's own renderer flags. **Proof:** the `render.err` line plus the CD target's file:line. **Oracle:** *Render matrix*.

### 1. Helm values that never reach a template

```
BAD:   values-prod.yaml   resource: {requests: {cpu: 500m}}          # typo; deployment.yaml reads .Values.resources
       templates/x.yaml   {{- with .Values.resources }}             # renders nothing; the pod runs BestEffort
GOOD:  values.schema.json with "additionalProperties": false  → `helm lint` and `helm template` fail on the typo
```
**Read the code:** Is the 1a key consumed by a subchart (a key named after a dependency or alias), by `tpl`, by `index .Values "x"`, or by a library chart? Is a 1b `guarded` ref the other half of a 1a key with a near-identical name? Which values file does the prod CD target pass (Argo `valueFiles`, `-f` in the inventory, CI `--set`)? **Finding when** a key set in a deployed values file reaches no template, or a template reads a key no deployed values file sets, so the field silently drops out of the prod render. **Proof:** the render diff with the key corrected shows the field appear (*Render matrix*). `helm lint --strict` is not proof either way: it passed the typo on the research fixture (2026-10-10). **Fix:** correct the key, and add a `values.schema.json` with `additionalProperties: false` so the next typo fails the lint.

### 2. Helm behaviour that differs from the render

```
BAD:   {{- $s := lookup "v1" "Secret" .Release.Namespace "db" }}     # empty under helm template, which is how Argo CD renders
       replicas: {{ .Values.replicaCount }}                          # rendered while autoscaling.enabled — Helm 4 SSA upgrade fails
       helm upgrade --install app ./chart --atomic                  # Helm 4: the flag is --rollback-on-failure
GOOD:  {{- if not .Values.autoscaling.enabled }}replicas: {{ .Values.replicaCount }}{{- end }}
       CRDs shipped as templates or a separate chart, upgraded on purpose; hook Jobs with before-hook-creation
```
**Read the code:**

- *2a.* Who renders this chart: `helm template`, an Argo CD sync, or `helm install`? Does the `lookup` branch have a deterministic fallback?
- *2b.* Did the chart's CRD schema change since the version the cluster has? Files in `crds/` are installed once and never upgraded, under Helm 3 and Helm 4 alike.
- *2c.* Does the hook object survive a second `helm upgrade`?
- *2d.* Is `replicas` behind the autoscaling guard? A value that is never read (a 1a `.autoscaling` row) means there is no guard.
- *2f, 2g.* Which Helm major runs the inventory line?

**Finding when:**

- the prod render (or the deployed Helm major) takes the branch that breaks;
- a hook or CRD upgrade would fail or leave stale state;
- or a renamed flag sits on a deploy path run by Helm 4.

**Proof:**

- *Render matrix* (V262): `helm template` at the target `--kube-version` with the prod values.
- *SSA / upgrade twice* (V264): install, then upgrade twice on a scratch kind cluster through an explicit `--kubeconfig`. Helm 4 fails with a conflict against `kube-controller-manager` on `.spec.replicas` (measured on kind, node v1.37.0, Helm 4.2.4, 2026-10-10).
- *GitOps spec* (V266) for a lookup branch Argo never sees.

### 3. Kustomize patches and transformers

```
BAD:   patches: [{target: {kind: Deployment, name: payment}, patch: …}]   # the base calls it `pay`: applies nothing, exit 0
       patches: [{path: res.yaml}]   # res.yaml names container `payments`; the base has `pay` → a second container, no image
       commonLabels: {team: payments}                                       # rewrites selectors; a later edit cannot apply
       configMapGenerator: [{name: cfg, options: {disableNameSuffixHash: true}}]  # config edits never roll the pods
GOOD:  a patch target that exists in the base render · labels: [{pairs: {team: payments}, includeSelectors: false}]
```
**Read the code:**

- *3d.* Was the no-op patch meant for a resource that the base later renamed or removed?
- *3e.* Does the phantom container's name differ from a base container by a typo?
- *3a.* Has the label already been applied to a live cluster? If so, the fix itself is a selector change, and § 5 applies.
- *3b.* Which workload consumes the unhashed ConfigMap, and does Reloader or a checksum roll it (precedent 13)? The rollout gap itself is graded by `k8s-wiring-scan` § 1.
- *3c.* Is the unprefixed name in the string an in-cluster Service the prefix renamed, or an external host?
- *3f.* Is this the trial-size patch with a documented exit condition (precedent 47)?

**Finding when:**

- *3d.* The render with and without the patch is identical.
- *3e.* A deployed env renders a container with no image.
- *3a.* `commonLabels` or `includeSelectors: true` sits in a base that has been deployed.
- *3b.* A generated ConfigMap with the hash off is consumed by a workload with no other rollout trigger.
- *3c.* A string names a renamed Service.
- *3f.* An autoscaled object carries `replicas` in a deployed env.

**Proof:**

- *Patch no-op/phantom* (V263): the 3d render-hash comparison, and a server dry-run on scratch kind rejecting the image-less container ("image: Required value").
- *Render matrix* (V262) for 3a, 3b and 3c.

### 4. GitOps spec

```
BAD:   syncPolicy: {automated: {selfHeal: true}}   over a Deployment that renders replicas and has an HPA     # reset every sync
       syncPolicy: {automated: {prune: true}}      over a PVC with no Prune=false                              # a path move deletes data
       ignoreDifferences: [{kind: Deployment, jsonPointers: [/spec]}]                                          # drift is invisible
GOOD:  omit replicas from the manifest · or ignoreDifferences /spec/replicas WITH syncOptions: [RespectIgnoreDifferences=true]
       argocd.argoproj.io/sync-options: Prune=false on PVCs and Namespaces · sync-wave on CRDs before their CRs
```
**Read the code:**

- *4a.* Does the HR join's object live in the env this Application deploys? `ignoreDifferences` without `RespectIgnoreDifferences=true` hides the diff and still resets the count (precedent 14).
- *4b.* Is a move of resources between Applications planned? Does `prune` reach a PVC or Namespace holding data?
- *4c.* Does the first sync on an empty cluster apply a CR before its CRD, or a Deployment before its migration Job?
- *4d.* Does the pointer cover all of `/spec` or `.spec.template`?

ApplicationSet generators are not expanded here. Their rows are Unconfirmed, listing the generator's file:line.

**Finding when** the deployed Application's spec makes the controller undo, delete or misorder something the render needs. **Proof:** *GitOps spec* (V266) — `argocd app diff` / `flux diff kustomization` against a scratch kind cluster with the controller installed, else Unconfirmed with that command written out. **Fix:** in the Application or Kustomization spec, or by removing `replicas` from the manifest.

### 5. Selector mutation between base and head

```
BAD:   base: selector {app: pay, team: payments}  →  head: {app: pay, team: billing}      # commonLabels edit, or a label helper
GOOD:  new label on the template only (includeSelectors: false); a selector change ships as a new object name + migration
```
**Read the code:** Is the object already live? A first deploy is not a mutation. Does the Service's selector move in the same diff? It applies before the workload fails, which leaves an EndpointSlice with no endpoints. Is the change from `commonLabels`, a chart's `selectorLabels` helper or a direct edit? **Finding when** a deployed workload's `spec.selector` differs between the base render and the head render. **Proof:** *Selector mutation* (V265) — apply the base render, then the head render, to a scratch kind cluster (explicit `--kubeconfig`). The second apply fails with `spec.selector … field is immutable`, while the Service has already moved (measured on kind, node v1.37.0, 2026-10-10). **Fix:** revert the selector and put the label on the template only. If the selector change is wanted, ship it as a recreate plan: a new object name plus a migration. Either way, stop before merge (`/infra-fix`, when present, asks the user first).

## Tool lane

| Tool (measured version) | Command, on `$SCAN` copies | Reads | Trap |
|---|---|---|---|
| kustomize 5.8.3 / `kubectl kustomize` | `render.sh` | every root | deprecations go to stderr only; a non-matching patch target exits 0 |
| helm 4.2.4 | `render.sh` (`helm template`, scratch homes, empty `KUBECONFIG`) | every chart × values file | `lookup` renders empty; `--dry-run=server` would contact the ambient context, so it is never used |
| `helm lint --strict` | `helm lint --strict <chart> -f <values>` | the chart | passes an unknown values key unless `values.schema.json` forbids it |
| kubeconform 0.8.0 | `kubeconform -strict -summary -output json -kubernetes-version <minor> render-<env>.yaml canary.yaml` | objects + 2 | `-ignore-missing-schemas` turns removed APIs into `skipped` with exit 0; YAML 1.1 decoding (the `n` canary comes back as `false`) |
| pluto 5.24.4 | `pluto detect-files -d "$SCAN" -o json --target-versions k8s=v<minor>` | files in `$SCAN` | its default target is old; always pass `--target-versions` |
| kind (scratch) | the K-tier oracles, with `--kubeconfig "$SCAN/kind.kubeconfig"` | — | never the user's context. No scratch cluster means the K-tier rows are Unconfirmed, with the command written out |

Missing kustomize and kubectl → every Kustomize root reads `not-installed` (`brew install kustomize`). Missing yq or jq → no JSON is written, so § 1 and § 3c–§ 5 are `blocked (yq/jq not installed)`.

**Stacks real repos use:**

| Stack | How it is rendered |
|---|---|
| Plain manifests | raw envs |
| Kustomize | standalone or kubectl-embedded |
| Helm 3 or 4 charts in the repo | rendered per values file |
| Charts installed from a remote repo | inventory rows only; the chart defaults are read at the pinned version with `helm show values <repo>/<chart> --version <v>` (network, no cluster) |
| Argo CD | an Application's chart or Kustomize path is rendered; ApplicationSet generators are not expanded |
| Flux | the path is mapped to its env; `postBuild` substitution is not applied, so the row is tagged |
| Helmfile, Skaffold, Tilt, cdk8s, Tanka/Jsonnet, Timoni | not run by `render.sh`. Run the project's own render command on a copy and feed its output to the same ledger, or the row reads `blocked (no renderer for <tool>)` |

## Output

```
k8s-render-scan — kustomize v5.8.3 · helm v4.2.4 (CI: azure/setup-helm v4.3.0) · target k8s 1.36 (runbook) · CD: Argo CD
Render: 5 envs · 61 objects · 0 failed · stderr 1 (commonLabels deprecated) · canaries read by kubeconform (27/27)

Findings: 2 · Unconfirmed: 1

1. chart/app/values-prod.yaml:1 + chart/app/templates/deploy.yaml:5          [report-with-fix]   high
   §4 K-GITOPS-REPLICAS — env argo__web renders Deployment/web replicas 3 while HPA web (min 2, max 6) owns the count;
   Application argocd/web (apps/app.yaml:7) runs selfHeal with no RespectIgnoreDifferences: every scale-up is reverted.
   Proof: Render matrix (V262) — argo__web render shows both objects; values.yaml:2 `autoscaling` is read by no template (1a).
   Fix: wrap replicas in {{- if not .Values.autoscaling.enabled }} (templates/deploy.yaml:5); siblings: 2 chart envs.

2. k8s/overlays/prod/kustomization.yaml:4                                        [report-with-fix]   high
   §3 K-KZ-PATCH-NOOP — patches[0] targets Deployment `payment`; the base renders `pay`. The 6-replica patch applies nothing.
   Proof: Patch no-op (V263) — render hash identical with and without patches[0]. Fix: target name `pay`.

3. chart/app/templates/deploy.yaml:1                                             [report-flagged]    medium
   §2 K-HELM-LOOKUP — the lookup branch is empty under Argo's helm template. Unproven link: whether the prod path relies on
   the existing Secret. Settling run: helm template vs helm install --dry-run=server on scratch kind (explicit --kubeconfig).

Verification: 9 candidates → 2 findings · 1 unconfirmed · 3 hardening · 0 pre-existing · 3 refuted

Class coverage:
  §0  render contract       checked (5 envs, 61 objects; 0 failed; kubeconform read 61 + 2)
  §1  Helm values           checked (2 hits → 1 group, folded into finding 1)
  §2  Helm behaviour        checked (4 hits → 1 unconfirmed; 2f: 0 renamed flags, 3 bare --wait read against Helm 4)
  §3  Kustomize             checked (9 patches → 1 no-op; 0 phantom; commonLabels 1 → hardening, never applied)
  §4  GitOps spec           checked (1 Application → 1 finding; 4b: 0) · ApplicationSet generators N/A (none)
  §5  selector mutation     checked (base origin/main, 61 objects compared → 0)
Tool ledger: kustomize 5.8.3 RAN · helm 4.2.4 RAN · kubeconform 0.8.0 RAN (63/63) · pluto 5.24.4 RAN · kind NOT-RUN (no consent)
```

`[report-with-fix]` means the deployed env, the oracle and the source fix are all in hand. `[report-flagged]` means one link is unproven (a Helm major not found in files, no scratch cluster for a K-tier oracle, an ApplicationSet not expanded), and the row names that link and the run that settles it. The coverage block lists **§ 0–§ 5 on every run**:

- `checked (k hits → m)` only when the step ran;
- `N/A (<reason>)` when the repo has no such surface (no chart, no CD controller);
- `blocked (<reason>)` when a renderer or tool was missing, or a copy did not reproduce the render;
- `Live, unreviewed (…)` for a partial review.

## False positives / precedents

The verifier reads [`precedents/infrastructure.md`](../../../../snippets/precedents/infrastructure.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:

- **An HPA-managed object with `replicas` omitted is correct** (precedent 6). The HR join already skips it. Tools that read it as one replica are wrong.
- **Dev and preview overlays** are not prod findings (precedent 7), unless that overlay is the CD target. A trial-size patch with a written exit condition is `accepted-risk` Hardening until the condition is met (precedent 47).
- **A removed apiVersion behind a `Capabilities.APIVersions.Has` / `semverCompare` guard** is not a finding at the target minor (precedent 12). Render at the target `--kube-version` before reporting.
- **`disableNameSuffixHash` with Reloader, or `immutable` plus versioned names,** is controlled (precedent 13), provided Reloader is installed in the target cluster (read the inventory).
- **Argo `ignoreDifferences /spec/replicas` plus `RespectIgnoreDifferences=true`** clears K-GITOPS-REPLICAS (precedent 14). `ignoreDifferences` alone does not.
- **A KEDA `ScaledObject` is an autoscaler** for the HR join (precedent 42). Its floor belongs to `k8s-availability-scan`.
- **A chart installed by a runbook is in scope** (precedent 45). Its values file is read even though no chart is in the repo.
- **Scanner silence is not a pass.** A tool that read fewer objects than the render holds is NOT-RUN for the difference.

## When to run

- First, in every `/infra-audit` that touches Kubernetes: the other three Kubernetes detectors read § 0.
- On a diff touching `kustomization.yaml`, a patch, `Chart.yaml`, `values*.yaml`, `templates/`, an Argo or Flux object, or a runbook or CI line that runs `helm` or `kubectl apply`. Diff the **render** for § 5, not the source.
- Before a Helm major upgrade (2f, 2g), and before a label or selector refactor (§ 5).

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/infra-audit` that is `@k8s-reviewer` in refute mode. Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- **Never touch a real cluster.** `render.sh` points `KUBECONFIG` at an empty scratch file. Every K-tier oracle runs against a scratch kind cluster with an explicit `--kubeconfig "$SCAN/kind.kubeconfig"`, and is refused if `KUBECONFIG` is unset or resolves to `~/.kube/config`. Never run `helm install/upgrade`, `kubectl apply` (`--dry-run=server` included) or `argocd`/`flux` against the ambient context.
- **Never write in the repo.** No `helm dependency update`, `kustomize edit`, or `yq -i` on tracked files; every mutation is on a `$SCAN` copy. A mutation that left the copy unchanged is `blocked`, never a no-op finding.
- Do not fetch a remote base or chart repo without the user's consent in this session.
- Halt on any finding without the source `<file:line>`, the env, the CD-target answer and the fix in the source.
- Do not print "render clean" without the ledger and the canary result, and do not report an env as checked when its render failed.
- Do not grade a class another skill or pack owns (§ Boundaries); cross-link it.

## Related

- `/infra-audit` (this pack) dispatches this skill first, and `/infra-fix` closes its findings with the failing-first oracle and a full re-render of every env.
- `@k8s-reviewer` judges the rows.
- `k8s-availability-scan`, `k8s-wiring-scan` and `k8s-api-version-scan` (this pack) read § 0's render.
- `iac-state-scan` § 3 reads `inventory-platform.tsv` for PIN-HELM.
- `edge-reliability-scan` reads `embedded/`.
- `k8s-audit` (this pack) owns the live cluster, behind its own context halt.
- `/k8s-generate` should run § 0 and § 3 on its own output before it claims PRODUCTION-GRADE.
- Security `iac-scan` (§ 3, grep 1e/1f) reads the same render when the security pack is installed.

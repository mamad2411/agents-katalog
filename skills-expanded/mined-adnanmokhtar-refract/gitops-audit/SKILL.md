---
name: gitops-audit
description: "Git-to-cluster reconciliation: kubectl/helm/argocd/flux bypassing a GitOps-managed namespace, live drift, unseen drift."
kind: skill
pack: devops
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: gitops-audit

## Premise

Under Argo CD or Flux, git is meant to be the only way a change reaches the cluster. The ways that stops being true are small and look harmless:
- a hotfix script runs `kubectl scale … -n <prod>` in a namespace an Application owns: with `selfHeal` off, git no longer describes prod; with it on, the controller quietly reverts the hotfix minutes later;
- a CI step runs `kubectl set image` or `argocd app set --parameter` beside the controller, so two writers fight over one object;
- `flux suspend` in a script turns reconciliation off and nothing turns it back on;
- an Application with `selfHeal` off and no OutOfSync alert drifts for weeks, and nobody is told.

None of this is visible in the manifests the controller syncs; it lives in scripts, CI files and the controller's live state.

This skill owns `ownership.json` row `gitops-reconciliation` (§1–§3). `@deployment-engineer` (this pack) judges its rows. It does **not** own the controller's spec (prune, sync waves, `selfHeal` × an autoscaler, `ignoreDifferences`): that is infrastructure `k8s-render-scan` §4. It does not own committed Secrets: that is security.

**Every finding cites the line `<file:line>` + the CD target that owns the namespace (Application or Flux Kustomization, with its file:line) + the object the verb touches + the sync policy that decides the effect + the oracle and its tier + the fix.** A pre-flight row is a candidate. "Git is the source of truth" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/devops.md`](../../../../snippets/precedents/devops.md) (deploy § 22–28; § 23 is this skill's: a GitOps CI that only commits manifests is gated by the controller). The oracles are tier S (a two-ended static trace: the verb and the CD target that owns its namespace) and tier L (the controller's own diff); [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Infrastructure V266 routes live reconciliation drift here, and § DevOps V290 is §1's oracle (out-of-band apply).

## The rule

A candidate is a finding when all four hold (the seven gates as `precedents/devops.md` § Reading the seven gates applies them):

1. **A controller owns the target** (gates 1, 7). A CD target in this repo (or the platform repo the user names) deploys the namespace, and the object the verb touches is in that target's render. A namespace no controller manages is a `deploy-safety-scan` row, not this skill's.
2. **The verb runs where it matters** (gate 2). A CI job on the default branch, a script an operator runs against prod, a Makefile target in a runbook — not a kind cluster, not a dry run.
3. **No control already handles it** (gate 4). The script commits to git and lets the controller sync; the field is one the controller is told to ignore (`ignoreDifferences` with `RespectIgnoreDifferences=true`, which infrastructure §4a reads); the object is the controller's own install (precedent below).
4. **The oracle fired, or both ends are cited** (gate 6). The controller's diff (L) shows the delta, or the static trace names the verb line and the CD target line; without the diff the row is `[report-flagged]`.

## Boundaries

- **Controller spec** — `selfHeal` over a workload an HPA or KEDA scales (K-GITOPS-REPLICAS), `prune` over stateful kinds (K-GITOPS-PRUNE), sync waves (K-GITOPS-WAVES), `ignoreDifferences` over all of `/spec` (K-GITOPS-IGNORE-WIDE) → infrastructure `k8s-render-scan` §4 when the infrastructure pack is installed. Without it, the pre-flight's `spec ->` rows are listed `infra-class (owner pack infrastructure not installed)` and never graded here. **The `allowEmpty` polarity**, for whoever judges those rows: `automated.allowEmpty` defaults to `false`, and that default *is* the guard — an Application whose render is empty is refused instead of pruning everything it owns. The finding is an explicit `allowEmpty: true` on a pruning prod Application, never "allowEmpty is missing". `PruneLast=true` prunes after the rest is healthy; `FailOnSharedResource` and the propagation policy do not constrain pruning.
- **A committed `kind: Secret`** (base64 is not encryption) → security `iac-scan` §3 and `secret-scan-method` when the security pack is installed; an `ExternalSecret`, a `SealedSecret` or a SOPS-encrypted file is the correct pattern. Without the pack, the row is tagged `security-class (owner pack not installed)`.
- **A deploy that is not GitOps** (a script or CI job that applies to a namespace no controller manages): concurrency, environment, rollout wait → `deploy-safety-scan` §2–§4. **The CI pipeline up to publish** → `pipeline-integrity-scan`, `release-integrity-scan`.
- **Unpinned controller or chart versions** (Argo `targetRevision: HEAD`, PIN-HELM) → infrastructure `iac-state-scan` §3. **Admission policy** that would reject what the controller syncs → infrastructure `admission-policy`.

## Adapt to the codebase — the lanes

Discover every CD target by **apiVersion** (pre-flight 0); never assume `apps/`, `clusters/` or `k8s/`. A `kustomize.config.k8s.io` `Kustomization` is a build file, not a Flux object (measured: the real repo has two, and they must print nothing).

| Lane | CD target (pre-flight 0) | Namespace it owns | Live read (§2–§3, L) |
|---|---|---|---|
| **Argo CD** | `Application`, `ApplicationSet` (`argoproj.io/`) | `spec.destination.namespace` (an object's own `namespace:` wins) | `argocd app list -o wide`, `argocd app diff <app>`, `argocd app get <app> -o json` |
| **Flux** | `Kustomization` (`kustomize.toolkit.fluxcd.io/`), `HelmRelease` (`helm.toolkit.fluxcd.io/`) | `targetNamespace`, else each object's namespace; a HelmRelease its own namespace | `flux get kustomizations -A`, `flux diff kustomization <n> --path <dir>` |
| **Rancher Fleet** | `GitRepo` (`fleet.cattle.io/`) | `fleet.yaml` `namespace` / `defaultNamespace` (read) | `kubectl get bundles -A` on the named context |
| **None** | — | — | every § prints `N/A (no GitOps controller)`; imperative verbs are `deploy-safety-scan`'s |

Every live command runs **read-only**, and only against a controller context the user names (`argocd --server <named>`, `flux --kubeconfig=<named file>`). Never the default kube context: without a named context the row is `NO-DATA(controller)` with the command written out.

## Pre-flight

Run as **one** script from the repo root (bash 3.2 and zsh print the same rows). Every `rg` names its path; an rg exit 2 is a failed grep, never zero hits. Nothing is written in the repo; no cluster binary runs.

```bash
X=(--hidden -g '!.git/**' -g '!**/node_modules/**' -g '!**/{dist,build,out,target,vendor,.venv,venv,__pycache__,coverage,.next,.turbo,generated}/**'
   -g '!**/{test,tests,__tests__,spec,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,examples}/**' -g '!**/{docs,ai,.claude}/**' -g '!*.{md,mdx,snap,lock,svg,map}')
CI=(--hidden -g '.github/workflows/*.{yml,yaml}' -g '**/.gitlab-ci*.yml' -g '.gitlab/**/*.{yml,yaml}' -g '.circleci/*.{yml,yaml}' -g '**/bitbucket-pipelines.yml'
    -g '**/azure-pipelines*.yml' -g '**/Jenkinsfile*' -g '!**/{node_modules,vendor,test,tests,fixtures,__fixtures__,testdata}/**')
SH=(-g '*.{sh,bash}' -g '**/Makefile' -g '**/Justfile' -g '**/Taskfile.{yml,yaml}' -g '!**/{node_modules,vendor,test,tests,fixtures,__fixtures__,testdata,docs,.claude,.git}/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(#|//)')
SCAN="${SCAN:-$(mktemp -d "${TMPDIR:-/tmp}/gitops.XXXXXX")}"; echo "SCAN=$SCAN"
echo '# 0 CD targets, by apiVersion (a kustomize.config.k8s.io Kustomization is a build file, not Flux): name, namespace it deploys, sync policy'
rg -l --pcre2 -g '*.{yml,yaml}' "${X[@]}" '^\s*apiVersion:\s*["\x27]?(argoproj\.io/|kustomize\.toolkit\.fluxcd\.io/|helm\.toolkit\.fluxcd\.io/|fleet\.cattle\.io/)' . | sort | while IFS= read -r f; do awk -f - "$f" <<'AWK'
function v(t) { sub(/^[^:]*:[ \t]*/, "", t); sub(/[ \t]+#.*$/, "", t); gsub(/^["']|["']$/, "", t); return t }
function out() { if (api ~ /fluxcd/) au = (sp == "true") ? "suspended" : "interval"
  if (k ~ /^(Application|ApplicationSet|Kustomization|HelmRelease|GitRepo)$/ && (api !~ /^argoproj/ || k ~ /^Application/))
    printf "%s:%d: CD %s %s ns=%s automated=%s selfHeal=%s prune=%s allowEmpty=%s suspend=%s path=%s\n", FILENAME, dl, k, n, (ns == "" ? (k == "HelmRelease" ? mns : "?") : ns), au, sh, pr, ae, sp, (pa == "" ? "-" : pa)
  k = ""; n = ""; ns = ""; mns = ""; au = "no"; sh = "-"; pr = "-"; ae = "-"; sp = "-"; pa = ""; dst = 0 }
BEGIN { au = "no"; sh = "-"; pr = "-"; ae = "-"; sp = "-" }
/^---/ { out(); next }
/^apiVersion:/ { api = v($0) } /^kind:/ { k = v($0); dl = FNR }
/^  name:/ && n == "" { n = v($0) } /^  namespace:/ && mns == "" { mns = v($0) }
/^[ \t]+destination:/ { dst = 1 } dst && /^[ \t]+namespace:/ { ns = v($0); dst = 0 }
/^[ \t]+targetNamespace:/ { ns = v($0) } /^[ \t]+path:/ && pa == "" { pa = v($0) }
/^[ \t]+automated:/ { au = "yes" } /^[ \t]+selfHeal:/ { sh = v($0) } /^[ \t]+prune:/ { pr = v($0) } /^[ \t]+allowEmpty:/ { ae = v($0) } /^  suspend:/ { sp = v($0) }
END { out() }
AWK
done | tee "$SCAN/cd-targets.txt"
awk '{ for (i = 1; i <= NF; i++) if ($i ~ /^ns=/) { s = substr($i, 4); if (s != "?") print s } }' "$SCAN/cd-targets.txt" | sort -u > "$SCAN/managed-ns.txt"
echo "managed namespaces: $(tr '\n' ' ' < "$SCAN/managed-ns.txt")"; [ -s "$SCAN/cd-targets.txt" ] || echo 'N/A (no GitOps controller declared in this repo): §1–§3 print N/A; an out-of-band verb is a deploy-safety-scan row'
echo '# 1 imperative verbs in CI, scripts, Makefiles: the namespace each one targets, and whether a controller manages it'
OOB='\b(?:kubectl|oc)\b[^\n|;&]*?\s(?:apply|create|edit|scale|set|patch|replace|delete|annotate|label|autoscale|rollout\s+(?:restart|undo|pause|resume))\b|\bhelm\s+(?:-\S+\s+)*(?:install|upgrade|rollback|uninstall)\b|\bargocd\s+app\s+(?:set|unset|patch|sync\b[^\n]*--(?:prune|force|local|revision))\b|\bflux\s+(?:suspend|resume)\b'
if [ ! -s "$SCAN/cd-targets.txt" ]; then echo "N/A (no GitOps controller): $(rg -c --pcre2 "${CI[@]}" "${SH[@]}" "$OOB" . | awk -F: '{ s += $NF } END { print s + 0 }') imperative lines left to deploy-safety-scan"
else rg -n --pcre2 "${CI[@]}" "${SH[@]}" "$OOB" . | "${NC[@]}" | rg -v --pcre2 '^[^:]+:\d+:\s*(?:\|\|\s*)?(?:die|echo|printf|warn|say|log|info|fail)\b' | awk -v M="$SCAN/managed-ns.txt" -v C="$SCAN/cd-targets.txt" '
  BEGIN { while ((getline l < M) > 0) m[l] = 1
          while ((getline l < C) > 0) { n = split(l, a, " "); for (i = 1; i <= n; i++) if (a[i] ~ /^ns=/) app[a[4]] = substr(a[i], 4) } }
  { l = $0; ns = "?"
    if (match(l, /create[ \t]+(namespace|ns)[ \t]+[A-Za-z0-9_.-]+/)) { ns = substr(l, RSTART, RLENGTH); sub(/.*[ \t]/, "", ns) }
    else if (match(l, /(-n|--namespace)[ =]+[A-Za-z0-9_.-]+/)) { ns = substr(l, RSTART, RLENGTH); sub(/^(-n|--namespace)[ =]+/, "", ns) }
    else if (match(l, /argocd[ \t]+app[ \t]+[a-z]+[ \t]+[A-Za-z0-9_.-]+/)) { t = substr(l, RSTART, RLENGTH); sub(/.*[ \t]/, "", t); ns = (t in app) ? app[t] : "?" }
    else if (match(l, /flux[ \t]+(suspend|resume)[ \t]+[a-z]+[ \t]+[A-Za-z0-9_.-]+/)) { t = substr(l, RSTART, RLENGTH); sub(/.*[ \t]/, "", t); ns = (t in app) ? app[t] : "?" }
    tag = (ns ~ /^(argocd|argo-cd|flux-system|kube-system)$/) ? "controller-ns" : (ns in m) ? "MANAGED" : (ns == "?") ? "unknown" : "unmanaged"
    if (l ~ /--dry-run(=client|=server)?([ \t]|$)/ && l !~ /\|[ \t]*kubectl[ \t]+apply/) tag = "dry-run"
    print tag "\tns=" ns "\t" l }' | sort; fi
echo '# 3 drift that nobody sees: selfHeal off or manual sync, joined with any OutOfSync alert (Argo metric/notification, Flux Alert)'
awk '$3 == "Application" || $3 == "ApplicationSet" { if ($7 != "selfHeal=true") print $0 "  -> NO-SELF-HEAL" }' "$SCAN/cd-targets.txt"
rg -n --pcre2 -g '*.{yml,yaml,json}' "${X[@]}" '\bargocd_app_info\b|\bsync_status\b|\bOutOfSync\b|\btrigger\.on-(sync-status-unknown|sync-failed|out-of-sync)|\bgotk_(reconcile_condition|resource_info)\b|^\s*apiVersion:\s*notification\.toolkit\.fluxcd\.io/' . | "${NC[@]}" | rg -v --pcre2 'kind:\s*Application\b' || echo 'OutOfSync alerting: none found in the repo (read the alerting repo or the controller install before a NO-ALERT row)'
echo '# routed: controller spec (infrastructure k8s-render-scan §4) and committed Secrets (security)'
awk '$0 ~ /allowEmpty=true/ || $0 ~ /prune=true/ { print "spec -> infrastructure k8s-render-scan §4: " $0 }' "$SCAN/cd-targets.txt"
rg -l --pcre2 -g '*.{yml,yaml}' "${X[@]}" '^\s*kind:\s*Secret\s*$' . | while IFS= read -r f; do rg -q --pcre2 '^\s*sops:|kind:\s*(SealedSecret|ExternalSecret)\b' "$f" || echo "secret -> security iac-scan §3 / secret-scan-method: $f"; done
echo '# 2 live drift (L tier, read-only, only on a controller context the user names; never the default kube context):'
echo '#   argocd app list -o wide · argocd app diff <app> · flux get kustomizations -A · flux diff kustomization <name> --path <dir>'
```

How to read it:
- **0** prints one `CD` row per Argo or Flux object: the namespace it deploys, `automated` (Flux: `interval`, or `suspended`), `selfHeal`, `prune`, `allowEmpty`, `path`. `ns=?` (an ApplicationSet template, a Flux Kustomization with no `targetNamespace`) means the objects' own namespaces decide: read the render of `path`.
- **1** tags each imperative line `MANAGED` (a CD target deploys that namespace), `controller-ns` (`argocd`, `flux-system`: the controller's own install), `unmanaged`, `dry-run` or `unknown` (a variable namespace: resolve it by reading the script). Message lines (`echo`, `printf`, `die "… helm upgrade …"`) are dropped.
- **3** lists Applications without `selfHeal: true`, then any OutOfSync alert source in the repo; the alert usually lives in a platform repo, so "none found" is a question, not a finding.
- **routed** rows are listed, never graded.

### Measured (2026-10-10)

| Tree | Result |
|---|---|
| Seeded sample (2 Argo Applications, 1 Flux Kustomization, 2 kustomize build files, a CI workflow, 4 scripts, a runbook in `docs/`, a committed Secret; 7 positives, 6 decoys, 3 routed) | 0.1 s, 0 rg errors; bash 3.2 and zsh identical. **7/7 positives surface**: `kubectl scale` and `kubectl annotate` into the Argo prod namespace (`selfHeal: false`: drift persists), CI `kubectl set image` into a `selfHeal: true` namespace (the controller reverts it), CI `argocd app set --parameter`, `flux suspend` with no resume, `kubectl set env` into the Flux namespace, and NO-SELF-HEAL with no OutOfSync alert. Decoys: the controller bootstrap (3 lines, `controller-ns`), a kind dev cluster (`unmanaged`), the kustomize build files (no CD row) and the `docs/` runbook (excluded). Routed: `allowEmpty: true` + `prune: true`, Flux `prune: true` → infrastructure; the base64 Secret → security |
| `benchmarks/fixtures/*` (16) | 0 CD targets, 0 imperative lines, 0 rg errors: every § `N/A (no GitOps controller)`. obs-defects' kustomize `Kustomization` prints no row |
| Real NestJS + React monorepo (read-only, `git status` clean before and after) | 0.1 s. No controller: two kustomize `Kustomization` build files and a KEDA ScaledObject print no CD row. 11 imperative lines in deploy scripts are counted and left to `deploy-safety-scan` (its UNIT rows read them). Before the N/A gate existed, 3 of the 11 were message lines (`printf` of the command, `die "helm upgrade … failed"`) — the message filter drops them on a controller-managed repo |

## The 3,000-hit path

1. **Intersect** with `MANAGED` rows: everything else is `controller-ns`, `unmanaged` or `dry-run` and is dismissed with one read each, named in the coverage block.
2. **Group** by script or CI job and by CD target (precedents § 5): one hotfix script with five verbs is one finding.
3. **Rank:** a prod CD target with `selfHeal` off first (the drift persists), then `selfHeal` on (the change is silently reverted), then the rest.
4. **Read the top 30 groups.**
5. **Run the bulk oracle once** on a named controller context: `argocd app list -o wide` settles §2 for every Application, `flux get kustomizations -A` for every Flux object.
6. **Ledger the rest** as `Live, unreviewed (k groups / n rows — <continuing command>)`. Never mark it `checked`.

## Scans for

| § | Classes | Default severity |
|---|---|---|
| 1 | Out-of-band mutation: an imperative `kubectl`/`oc`/`helm` verb, `argocd app set/patch/sync --local`, or `flux suspend` against a namespace a controller owns | H on a prod CD target, M otherwise |
| 2 | Live drift: a CD target OutOfSync or Degraded, the diff naming fields the spec does not ignore | M (H on prod when the field changes behaviour) |
| 3 | Drift nobody sees: `selfHeal` off or manual sync, and no OutOfSync alert | M |

### 1. Out-of-band mutation

```
BAD:   scripts/scale-up.sh kubectl scale deploy/api -n shop-prod --replicas=6     (Application api-prod owns shop-prod, selfHeal: false)
       cd.yml              kubectl set image deployment/web … -n shop-web          (selfHeal: true — reverted on the next reconcile)
       cd.yml              argocd app set api-prod --parameter image.tag=…          (an override that lives in the Application, not git)
       pause-workers.sh    flux suspend kustomization workers                       (no resume anywhere)
GOOD:  commit the change (an image bump, a replica patch) and let the controller sync it · `argocd app sync` with no --local/--revision
```
**Read the code:**
- Does the verb touch an object the CD target renders (same kind and name in its render)? A one-off `kubectl create job --from=cronjob/…` or a `kubectl debug` creates an untracked object: Hardening.
- Is it the controller's own install or upgrade (`controller-ns`)? That is how Argo or Flux gets there: not a finding.
- What does the sync policy make of it: `selfHeal: false` (git stops describing prod) or `true` (the change disappears)? Both are findings; the fix differs.
- For a variable namespace (`-n "$NS"`), which value does the prod invocation pass? For `flux suspend`, does the same script resume, on every exit path?
- Is this a GitOps CI that only commits manifests (precedents § 23)? Then it is the intended path.

**Finding when** a verb that writes runs against an object a controller owns, outside git. **Proof:** S — the verb's line and the CD target's line (namespace, sync policy); L — on a scratch cluster with the controller installed (isolated `--kubeconfig=<scratch>`), run the verb and read `argocd app diff` / `flux diff kustomization`: the object is OutOfSync (selfHeal off) or reverted within the reconcile interval (on). Without a scratch controller, `NO-DATA(controller)` and the row is `[report-flagged]`.

### 2. Live drift

**Read the code:** Which fields does the diff name? A field an autoscaler, VPA or cert-manager owns is the controller spec's question (infrastructure `k8s-render-scan` §4a, §4d), not drift. Did a §1 line cause it? **Finding when** a prod CD target is OutOfSync or Degraded on a field that changes behaviour, with the controller's own diff as evidence. "Probably drifted" is never a finding. **Proof:** L — `argocd app diff <app>` / `flux diff kustomization <n> --path <dir>` on the controller context the user names, read-only; without it `NO-DATA(controller)`.

### 3. Drift nobody sees

**Read the code:** Is the Application deliberately manual-sync (a prod gate a human clicks), with an alert on OutOfSync? Is the alert in a platform repo or the controller's Helm values (`argocd-notifications` triggers, a PrometheusRule on `argocd_app_info{sync_status="OutOfSync"}`, a Flux `Alert` [K?])? Do not recommend turning `selfHeal` on for an Application that is OutOfSync now: reconcile first, or self-heal enforces the wrong state. **Finding when** drift on a prod target can persist with no one told. **Proof:** S — the Application line and the alert search; L — `argocd app get <app>` sync status and the notifications config on the named context.

## Proof

**Scope: scratch kind clusters with the controller installed, through an isolated `--kubeconfig=<scratch>`, and read-only commands on a controller context the user names — never the default kube context, never a write to the user's cluster.**

| § | Oracle | Tier | V |
|---|---|---|---|
| 1 | Static trace (verb line + CD target line); controller diff on a scratch cluster after the verb | S + L | V290 |
| 2 | The controller's own diff on the named context | L | — |
| 3 | Application sync policy + alert search; sync status on the named context | S + L | — |

## Output

```
gitops-audit — lanes: argo-cd (2 Applications), flux (1 Kustomization) · controller context: none named (§2 NO-DATA) · infrastructure: installed

Findings: 2 · Unconfirmed: 4

1. scripts/scale-up.sh:4                                                  [report-with-fix]   high
   §1 — `kubectl scale deploy/api -n shop-prod --replicas=6`; Application api-prod (deploy/argocd/app-api.yaml:2)
   owns shop-prod with selfHeal: false, so git stops describing prod. Proof: static trace (S). Fix: a replica
   patch in deploy/k8s/overlays/prod committed and synced; delete the script line.

2. .github/workflows/cd.yml:11                                            [report-flagged]    high
   §1 — `kubectl set image … -n shop-web` while web-prod has selfHeal: true: the controller reverts every CI
   deploy. Unproven link: no scratch controller. Settling test: verb + `argocd app diff web-prod` on kind.

Verification: 11 candidates → 2 findings · 4 unconfirmed · 1 hardening · 0 pre-existing · 4 refuted (self-verified)

Class coverage:
  §1 out-of-band mutation   checked (10 imperative lines → 6 MANAGED; 3 controller-ns + 1 unmanaged refuted)
  §2 live drift             NO-DATA(controller) — argocd app list -o wide --server <named>
  §3 unseen drift           checked (2 Applications → 1 NO-SELF-HEAL; alerting: none in repo → Unconfirmed)
  routed                    allowEmpty + prune ×2 → infrastructure k8s-render-scan §4 · kind: Secret ×1 → security iac-scan §3
```

`[report-with-fix]`: the verb, the CD target, the sync policy and the static trace are in hand, and the fix is a commit. `[report-flagged]`: one link is unproven — the controller diff, a variable namespace, the alert in another repo. The coverage block lists all three §s on every run, with `N/A (no GitOps controller)`, `NO-DATA(controller)`, `blocked (<reason>)` or `Live, unreviewed (k groups / n rows)` as they apply.

## False positives / precedents

The verifier reads [`precedents/devops.md`](../../../../snippets/precedents/devops.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4:
- **§ 23** a GitOps CI that only commits manifests is the intended path. **§ 24** preview and ephemeral environments. **§ 5** one finding per script, job or CD target. **§ 4** pre-existing lines on a diff run never block. **§ 41** a tool that errored is NOT-RUN.

Read rules (sample and real repo, 2026-10-10): the controller's own install into `argocd` / `flux-system` is not out-of-band; a kustomize `Kustomization` is not a Flux object; an `ExternalSecret` or `SealedSecret` holds no secret; drift on an autoscaler-owned field is the spec's question, not this skill's.

Rationalizations to reject: "it was an emergency" (commit the hotfix, or it vanishes or lingers); "selfHeal will fix it" (it also erases the hotfix); "we only suspend for a minute" (show the resume on every exit path).

## When to run

- On any diff touching an Argo or Flux object, or a `kubectl`/`helm`/`argocd`/`flux` line in a script, Makefile or CI file.
- After an incident where prod changed and no commit explains it (with a named controller context for §2).
- On every whole-repo `/devops-audit`, reporting all three §s.

## Halt conditions

- **Do not report a critical or high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it; it applies [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/devops.md`. Under `/devops-audit` that is its verification phase; standalone, run the protocol as a second pass and tag those rows `self-verified`. List the rest as Unconfirmed, Hardening, Pre-existing or Refuted; never drop them.
- **No drift claim without the controller's own diff** (§2). No §1 row without the CD target that owns the namespace.
- **Never run a cluster command without an isolated or user-named context**; never a write. Without one, `NO-DATA(controller)` with the command written out.
- **No proposed fix may weaken reconciliation to clear a row:** no `selfHeal: false`, no `ignoreDifferences` widened, no suspended controller.
- **Do not grade the controller spec or a Secret** (§ Boundaries); list them as routed.

## Related

- `/devops-audit` dispatches this skill on an Argo or Flux object or an imperative line in a script; `/devops-fix` closes §1 rows with a commit and the controller diff.
- `@deployment-engineer` judges these rows; `deploy-safety-scan` owns imperative deploys outside GitOps; `@ci-reviewer` and `/add-ci` own the pipeline up to publish.
- Infrastructure `k8s-render-scan` §4 (controller spec), `iac-state-scan` §3 (unpinned controllers), `admission-policy`; security `iac-scan` §3 and `secret-scan-method` — each when its pack is installed.

## Sources

Scope from the batch-4 devops eval (kept-skill scope: §1–§3; spec classes to infrastructure, Secrets to security) and the infrastructure render contract (`k8s-render-scan` §4). Argo CD and Flux field semantics are from the controllers' documentation as the infrastructure research read it (2026-10-10); `allowEmpty` polarity from Argo CD's automated-sync documentation. Rows tagged `[K?]` are settled on a scratch controller before a fix relies on them. Paraphrased; no text reproduced beyond identifiers.

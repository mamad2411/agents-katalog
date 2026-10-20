---
name: fairwinds-polaris-and-goldilocks
description: >
  Guides using Fairwinds Polaris to validate and score Kubernetes
  workload configuration (resource requests/limits, security context,
  health checks, image tags) and Fairwinds Goldilocks (VPA-backed) to
  generate right-sizing recommendations. Use when the user asks to
  "score our workloads against Kubernetes best practices", "check our
  manifests for missing resource limits or health checks", "find
  over/under-provisioned pods", "set up Goldilocks recommendations",
  "add a lightweight config linter before we write custom OPA/Kyverno
  policies", or "why is Polaris flagging this deployment".
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: policy-and-governance-tooling
  maturity: stable
---

# Fairwinds Polaris and Goldilocks

## Purpose

Not every Kubernetes configuration problem needs a custom-authored policy
engine. Fairwinds **Polaris** ships a curated, opinionated set of
best-practice checks (resource requests/limits set, security context
hardened, liveness/readiness probes present, image tags not `latest`,
no host network/PID namespace, etc.) as a ready-made scoring tool and
optional admission webhook — no Rego or YAML rule-authoring required to
get useful coverage on day one. Fairwinds **Goldilocks** solves an
adjacent but different problem: it runs a Vertical Pod Autoscaler (VPA)
in `recommendation` mode (never auto-applying changes) per namespace and
surfaces a dashboard of suggested CPU/memory requests based on observed
usage, so teams can right-size workloads instead of guessing at limits or
copy-pasting defaults. Together they cover "is this workload configured
according to baseline best practice" (Polaris) and "are this workload's
resource requests/limits actually sized correctly for what it uses"
(Goldilocks) — both lower-effort, narrower-scope tools than standing up
OPA/Gatekeeper or Kyverno from scratch, and a reasonable first step before
investing in custom policy authoring for gaps neither tool covers.

## When to use

- The user wants a fast, low-effort baseline check of workload
  configuration (resource limits, security context, probes) without
  writing custom Rego or Kyverno rules first.
- The user is auditing an existing cluster and wants a scored report of
  which workloads violate common Kubernetes best practices, to prioritize
  remediation.
- The user wants Polaris running as an **admission webhook** to block (or
  warn on) new workloads that don't meet the baseline, as a lighter-weight
  alternative or complement to Gatekeeper/Kyverno for this specific class
  of check.
- The user has workloads with resource requests/limits that were guessed
  or copy-pasted, and wants data-driven right-sizing recommendations
  instead.
- The user is deciding whether Polaris's built-in checks are sufficient or
  whether they need custom OPA/Kyverno policies for organization-specific
  rules Polaris doesn't cover (e.g. custom label requirements, internal
  registry allowlists).
- The user asks why a specific Deployment is scoring poorly in Polaris and
  wants to interpret and fix specific check failures.

## Prerequisites & environment

- A Kubernetes cluster (Polaris and Goldilocks both work against any
  conformant 1.2x+ cluster) with access to install via Helm or the CLI.
- **Polaris** — install as a one-off CLI scan (no cluster install
  required, works against local YAML or a live cluster context) or as an
  in-cluster dashboard + optional admission webhook. The CLI is the
  fastest way to get a first report; the webhook is only needed for
  enforcement, not just scoring/visibility.
- **Goldilocks** requires the **Vertical Pod Autoscaler (VPA)** CRDs and
  controller installed first (`vertical-pod-autoscaler` from the
  `kubernetes/autoscaler` project) — Goldilocks is a UI/controller layer
  on top of VPA's `recommender` component, not a replacement for it.
  Install VPA in recommendation-only mode; do not enable VPA's
  auto-update mode as a side effect of installing Goldilocks, since that
  would let VPA evict and resize pods automatically rather than merely
  recommend.
- Both tools are read/report-focused by default (dashboard, CLI exit
  code) — enforcement (blocking a deploy) requires deliberately enabling
  Polaris's admission webhook, which follows the same audit-before-enforce
  discipline as any other admission control.
- Helm 3.x if installing via the Fairwinds Helm charts (`fairwinds-stable`
  repo) — check chart version compatibility notes since Polaris's default
  check set and severity levels have changed across major versions.

## Step-by-step guidance

1. **Run a one-off Polaris scan** against a live cluster or local
   manifests to get a baseline score before installing anything
   persistent:
   ```bash
   polaris audit --format=pretty
   # or against local YAML without a cluster:
   polaris audit --audit-path ./k8s-manifests/ --format=json > polaris-report.json
   ```

2. **Review the score and per-check breakdown** — Polaris groups checks
   into categories (`Security`, `Reliability`, `Efficiency`) and each
   check into `danger`, `warning`, or pass. Prioritize `danger`-level
   findings first (e.g. privileged containers, missing memory limits
   that risk OOM-killing the node) over `warning`-level style issues.

3. **Customize the check set with a config file** — Polaris ships broad
   defaults, but every organization should tune severities and exclusions
   rather than accepting the defaults uncritically:
   ```yaml
   # polaris-config.yaml
   checks:
     cpuRequestsMissing: warning
     memoryRequestsMissing: danger
     memoryLimitsMissing: danger
     readinessProbeMissing: warning
     livenessProbeMissing: warning
     runAsRootAllowed: danger
     notReadOnlyRootFilesystem: warning
     tagNotSpecified: danger
     hostNetworkSet: danger
   exemptions:
     - controllerNames:
         - legacy-batch-job
       rules:
         - readinessProbeMissing   # batch job has no HTTP endpoint to probe
   ```
   ```bash
   polaris audit --config polaris-config.yaml --format=pretty
   ```

4. **Install the in-cluster dashboard** for ongoing visibility rather
   than only ad hoc CLI runs:
   ```bash
   helm repo add fairwinds-stable https://charts.fairwinds.com/stable
   helm install polaris fairwinds-stable/polaris \
     --namespace polaris --create-namespace \
     -f polaris-config.yaml
   ```

5. **Only after reviewing dashboard results, consider enabling the
   admission webhook** to block new non-compliant workloads — start with
   it disabled/warn-only:
   ```yaml
   # values.yaml for the polaris helm chart
   webhook:
     enable: true
   config:
     checks:
       memoryLimitsMissing: danger
   ```
   > **Warning — destructive action risk:** enabling Polaris's admission
   > webhook with checks set to `danger` blocks matching create/update
   > requests **cluster-wide** for every workload that fails, the same
   > way a Gatekeeper `deny` Constraint does. Review the CLI/dashboard
   > report for a full deploy cycle first, and confirm a rollback path
   > (`helm upgrade polaris --set webhook.enable=false`, or deleting the
   > webhook configuration) before enabling it against a production
   > cluster.

6. **Install VPA, then Goldilocks, for right-sizing** — Goldilocks needs
   VPA's recommender already running:
   ```bash
   # VPA (recommender only — do not enable the updater/admission components
   # unless auto-resizing is explicitly wanted)
   kubectl apply -f https://github.com/kubernetes/autoscaler/releases/latest/download/vpa-recommender.yaml

   helm install goldilocks fairwinds-stable/goldilocks --namespace goldilocks --create-namespace
   ```

7. **Opt namespaces in explicitly** — Goldilocks only generates
   recommendations for labeled namespaces, so nothing is auto-enrolled:
   ```bash
   kubectl label namespace payments goldilocks.fairwinds.com/enabled=true
   ```

8. **Read recommendations from the dashboard or CLI**, and treat them as
   a starting point for a manual change, not an auto-applied resize —
   Goldilocks' underlying VPA objects are created in `updateMode: "Off"`
   (recommend-only) so nothing changes without a human editing the
   Deployment/StatefulSet:
   ```bash
   kubectl get vpa -n payments
   kubectl describe vpa payments-api -n payments
   ```

9. **Apply the recommended values manually** (or via a reviewed PR to the
   manifest/Helm values), then re-check with Polaris to confirm the
   resource-limit checks now pass:
   ```yaml
   resources:
     requests:
       cpu: 150m       # from Goldilocks target recommendation
       memory: 256Mi
     limits:
       memory: 512Mi
   ```

10. **Re-run both tools periodically** (weekly dashboard review is
    reasonable) since usage patterns and best-practice adherence drift as
    workloads change — this isn't a one-time audit.

## Best practices

- Treat Polaris as the fast first pass for well-known Kubernetes
  configuration hygiene (limits, probes, security context, image tags),
  and reserve custom OPA/Kyverno policy authoring
  ([opa-gatekeeper-policy-authoring](../opa-gatekeeper-policy-authoring/SKILL.md),
  [kyverno-policy-management](../kyverno-policy-management/SKILL.md)) for
  organization-specific rules Polaris doesn't have a built-in check for
  (custom label schemas, internal registry allowlists, business-specific
  constraints) — don't reimplement Polaris's own checks in Rego/Kyverno
  from scratch.
- Customize severities and add documented exemptions rather than running
  with Polaris's raw defaults — a batch Job with no HTTP endpoint will
  legitimately fail `readinessProbeMissing` forever unless exempted, and
  an unreviewed default config trains teams to ignore the dashboard.
- Never enable Goldilocks' underlying VPA in `Auto`/`Recreate` update mode
  as a shortcut to "automatic" right-sizing — that lets VPA evict and
  restart pods with new resource values without a human review step,
  which is a meaningfully different (and riskier) blast radius than the
  recommend-only mode this skill assumes.
- Use Goldilocks recommendations as informed starting points, then
  monitor actual behavior (OOMKills, CPU throttling) after applying them
  — VPA recommendations are based on historical usage and can miss
  workload-specific spikes (e.g. a batch job that briefly needs much more
  memory once a day).
- Enable the Polaris admission webhook only after a warn/dashboard-only
  period, exactly like the audit-before-enforce discipline for
  Gatekeeper/Kyverno — Polaris enforcement is still a cluster-wide
  blocking gate, just with a different rule engine underneath.
- Label namespaces into Goldilocks deliberately and incrementally (start
  with a few teams) rather than cluster-wide on day one, so the
  dashboard's recommendation volume stays reviewable.

## Common pitfalls

- **Symptom:** The Polaris admission webhook is enabled with default
  severities and immediately blocks deploys for workloads that
  legitimately don't need a readiness probe (e.g. CronJobs, batch Jobs),
  causing an unplanned incident.
  **Fix:** Run Polaris in CLI/dashboard-only (report) mode first, add
  `exemptions` for controller types/names that legitimately fail specific
  checks, and only enable the webhook once the exemption list reflects
  real cluster workloads — the same audit-first discipline used for
  Gatekeeper/Kyverno enforcement.

- **Symptom:** A team installs Goldilocks, sees VPA objects appear, and
  assumes resource requests/limits are now being adjusted automatically —
  then is confused when nothing changes on its own.
  **Fix:** Confirm the VPA `updateMode` is `"Off"` (Goldilocks' default) —
  this is intentional; Goldilocks only recommends. Values must be applied
  manually to the workload's own manifest/Helm values, then verified with
  `kubectl describe vpa` and a follow-up Polaris scan.

- **Symptom:** A workload is resized to Goldilocks' exact recommended CPU
  request, and shortly after starts getting CPU-throttled during a daily
  batch spike that wasn't represented in the VPA's observation window.
  **Fix:** Goldilocks/VPA recommendations reflect historical usage over
  their configured window — for workloads with known periodic spikes, pad
  the recommendation or size for the p95/p99 usage rather than the mean,
  and validate post-change behavior (throttling metrics, OOMKills) rather
  than trusting the recommendation as final.

- **Symptom:** Polaris score looks good (high percentage), but the team
  still gets paged for issues the score gave no visibility into (e.g. an
  internal-only compliance rule about required annotations).
  **Fix:** Polaris's check set is a curated, generic best-practices list —
  it is not a substitute for organization-specific policy. Use
  [opa-gatekeeper-policy-authoring](../opa-gatekeeper-policy-authoring/SKILL.md)
  or [kyverno-policy-management](../kyverno-policy-management/SKILL.md)
  to add custom checks for anything specific to your org that Polaris
  doesn't cover, rather than treating a good Polaris score as full policy
  coverage.

- **Symptom:** Goldilocks is labeled onto every namespace cluster-wide on
  day one, producing hundreds of recommendation deltas that nobody
  reviews, and the dashboard becomes noise nobody looks at.
  **Fix:** Opt namespaces in incrementally (a few teams/services first),
  establish a review cadence (e.g. one namespace batch per sprint), and
  only expand coverage as teams demonstrate they're actually acting on
  recommendations.

## Worked example

A platform team wants a fast baseline audit before investing in custom
Kyverno policies, plus right-sizing data for one overprovisioned service.

`polaris-config.yaml`:
```yaml
checks:
  cpuRequestsMissing: warning
  memoryRequestsMissing: danger
  memoryLimitsMissing: danger
  readinessProbeMissing: warning
  livenessProbeMissing: warning
  runAsRootAllowed: danger
  tagNotSpecified: danger
exemptions:
  - controllerNames:
      - nightly-report-job
    rules:
      - readinessProbeMissing
      - livenessProbeMissing
```

CLI scan in CI (report-only, non-blocking initially):
```bash
polaris audit --audit-path ./k8s/ --config polaris-config.yaml --format=json \
  > polaris-report.json
python3 -c "
import json, sys
r = json.load(open('polaris-report.json'))
score = r['ClusterInfo'].get('Version', 'n/a')
print('Polaris scan complete — see polaris-report.json for full detail')
"
```

Sample finding surfaced against a Deployment missing memory limits:
```
danger  Deployment/payments-api   memoryLimitsMissing
        Memory limits should be set (container "api")
```
Fix applied to the manifest:
```yaml
resources:
  requests:
    memory: 256Mi
  limits:
    memory: 512Mi
```

Separately, Goldilocks is enabled for the same namespace to get an
evidence-based value instead of a guessed one:
```bash
kubectl label namespace payments goldilocks.fairwinds.com/enabled=true
kubectl get vpa payments-api -n payments -o jsonpath='{.status.recommendation}'
```
Output shows a target recommendation of `cpu: 120m, memory: 340Mi` based
on two weeks of observed usage — noticeably lower than the
previously-guessed `cpu: 500m, memory: 1Gi` the team had copy-pasted from
another service. The team updates the manifest to the recommended values,
re-runs `polaris audit`, and confirms `memoryLimitsMissing` and
`cpuRequestsMissing` both now pass.

## Cross-references

- [opa-gatekeeper-policy-authoring](../opa-gatekeeper-policy-authoring/SKILL.md) —
  for organization-specific rules Polaris's built-in checks don't cover,
  authored as Rego ConstraintTemplates.
- [kyverno-policy-management](../kyverno-policy-management/SKILL.md) — a
  YAML-native alternative for the same class of custom policy, without
  Rego.
- [policy-as-code-guardrails](../../../devsecops/skills/policy-as-code-guardrails/SKILL.md) —
  the broader audit-before-enforce discipline this skill's webhook
  guidance follows.
- [secure-cicd-gates](../../../devsecops/skills/secure-cicd-gates/SKILL.md) —
  where a Polaris CLI scan fits as a PR-time or pre-deploy pipeline stage.

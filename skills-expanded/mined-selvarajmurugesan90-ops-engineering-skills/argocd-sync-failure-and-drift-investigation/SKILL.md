---
name: argocd-sync-failure-and-drift-investigation
description: >
  Troubleshoots Argo CD `Application`s that are stuck or failing —
  `OutOfSync`/`Progressing`/`Degraded` states, `PreSync`/`Sync`/`PostSync`
  hook Jobs that fail or hang, resource-level diffs that are hard to read,
  and distinguishing drift caused by an out-of-band `kubectl edit`/`kubectl
  patch` from genuine configuration drift between Git and the live
  cluster. Use when the user asks to "debug why an Argo CD app is
  OutOfSync," "figure out what's actually different between Git and the
  cluster," "a sync hook is failing/stuck," "someone kubectl edited a
  resource Argo CD manages," or "an Application says Synced but the
  cluster doesn't match Git."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: gitops-argo-ecosystem
  maturity: stable
---

# Argo CD Sync Failure and Drift Investigation

## Purpose

An `Application` reporting `OutOfSync`, stuck `Progressing`, or a failed
sync operation tells you *that* something is wrong but rarely tells you
*why* at a glance — the real cause is buried in a specific resource's
diff, a specific hook Job's pod logs, or the distinction between "Git and
the cluster genuinely disagree" versus "someone changed a live resource
by hand and Argo CD hasn't reconciled it yet." This skill assumes the
`Application` spec itself (sync policy, sync waves, hooks, custom health
checks) is already configured per
[argocd-application-configuration](../argocd-application-configuration/SKILL.md)
and goes deep on the investigative workflow for when that configuration
isn't behaving as expected in a running cluster: reading resource-level
diffs, tracing a failing hook to its root cause, and telling manual
cluster drift apart from real Git/cluster divergence before deciding
whether to sync, patch Git, or leave a resource alone.

## When to use

- An `Application` shows `OutOfSync` and it's not obvious which
  resource(s) differ or why.
- An `Application` is stuck `Progressing` past the point it should
  normally settle, or a sync operation is stuck `Running`/`Terminating`.
- A `PreSync`, `Sync`, or `PostSync` hook Job failed, timed out, or is
  blocking the rest of the sync from proceeding.
- Someone ran `kubectl edit`/`kubectl patch`/`kubectl scale` directly
  against a resource Argo CD manages, and you need to know whether that
  change will be reverted, silently kept, or is masking a real
  discrepancy with Git.
- An `Application` reports `Synced`/`Healthy` but a user insists the
  cluster is doing something different from what's in Git (or vice
  versa).
- Deciding whether an `OutOfSync` diff represents a resource that should
  be synced from Git, or a field that should instead be added to
  `ignoreDifferences` because the live value is legitimately
  controller-managed.

## Prerequisites & environment

- Argo CD ≥ 2.9 with `argocd` CLI access
  (`argocd login <ARGOCD_SERVER>`) and read (at minimum) RBAC on the
  target `Application`/`AppProject`.
- `kubectl` access to the destination cluster for direct inspection —
  the `argocd` CLI's view is derived from the same live state but is
  sometimes stale relative to a fresh `kubectl get`.
- The `Application`'s Git source repo accessible for comparison
  (`git log`, `git blame` on the manifest path) so you can tell whether a
  live-cluster value was ever declared in Git at all.
- Familiarity with the `Application` spec fields this skill diagnoses
  against — see
  [argocd-application-configuration](../argocd-application-configuration/SKILL.md)
  for `syncPolicy`, `ignoreDifferences`, sync waves, and hooks if any of
  those concepts are unfamiliar; this skill does not re-explain them.
- For hook failures: `kubectl logs`/`kubectl describe pod` access in the
  destination namespace to read the failing hook Job's actual pod
  output, not just Argo CD's summary status.

## Step-by-step guidance

1. **Start from the `Application`'s own status, not just the UI's
   red/yellow dot.** Pull the full status block for the actual sync/health
   condition and the specific resource(s) implicated:
   ```bash
   argocd app get payments-api-prod -o json | jq '.status.sync, .status.health, .status.operationState'
   kubectl get application payments-api-prod -n argocd -o jsonpath='{.status.conditions}'
   ```
   `status.sync.status` (`Synced`/`OutOfSync`), `status.health.status`
   (`Healthy`/`Progressing`/`Degraded`/`Missing`/`Unknown`), and
   `status.operationState.phase` (`Succeeded`/`Failed`/`Error`/`Running`)
   are three **independent** signals — a `Synced` + `Degraded`
   `Application` and an `OutOfSync` + `Healthy` one are different
   problems requiring different fixes, so don't collapse them into one
   "is it broken" question.

2. **Get the resource-level diff, not the app-level summary.** `argocd
   app diff` shows exactly which fields differ, per resource, between
   the Git-rendered manifest and the live object:
   ```bash
   argocd app diff payments-api-prod
   ```
   Read the diff output as `< live cluster` / `> Git desired` (or the
   reverse depending on CLI version — confirm with `--help` if unsure).
   A diff limited to one or two fields on one resource (e.g. `replicas`,
   an injected annotation) is a very different problem from a diff
   spanning many resources (usually a bad merge, a botched Kustomize
   overlay, or the wrong `targetRevision`).

3. **Narrow to the specific resource when the app has many.** `argocd
   app resources` lists every managed resource with its own sync/health
   status so you're not diffing the whole app to find one bad
   Deployment:
   ```bash
   argocd app resources payments-api-prod
   argocd app diff payments-api-prod --resource apps:Deployment:payments-prod/payments-api
   ```

4. **Distinguish manual drift from genuine Git/cluster divergence** —
   this is the crux of most confusing `OutOfSync` reports:
   - Check whether the differing field is **declared in Git at all**:
     `git show <targetRevision>:<path>` (or `argocd app manifests
     payments-api-prod` for the fully-rendered desired state). If the
     field isn't in the Git-rendered manifest, its live value came from
     somewhere else — a mutating webhook, an HPA, a defaulting
     controller, or a manual edit — not from Git diverging.
   - If the field *is* in Git and the live value differs, check
     `kubectl get <resource> -o yaml` for
     `metadata.managedFields` (`kubectl get deploy payments-api -n
     payments-prod --show-managed-fields -o yaml`) to see which field
     manager last wrote that field and when — `argocd-controller` means
     Argo CD itself made the last write (so the diff is likely transient
     or a race), while `kubectl-edit`/`kubectl-patch`/a human's kubeconfig
     user means someone changed it out-of-band.
   - Cross-check `argocd app history payments-api-prod` against the
     timing of the suspected manual change — if the last successful sync
     predates when the manual edit was made, the live cluster and the
     sync history simply haven't caught up yet; that's expected, not a
     bug.
   - If `selfHeal` is enabled and the field still shows as different
     *after* a completed sync, the manual edit is being fought and
     re-applied continuously — that's the sync-loop pitfall, and the fix
     is `ignoreDifferences`, not disabling `selfHeal` (see
     [argocd-application-configuration](../argocd-application-configuration/SKILL.md)
     Common pitfalls).

5. **Investigate a stuck/failing sync hook by going straight to the
   hook's own Job/Pod, not the Application's summary.** Argo CD's
   `operationState` reports which hook is blocking, but the actual error
   is in the pod:
   ```bash
   argocd app get payments-api-prod -o json | jq '.status.operationState.syncResult.resources[] | select(.hookType != null)'
   kubectl get jobs -n payments-prod -l argocd.argoproj.io/hook-type
   kubectl logs job/payments-api-migrate -n payments-prod
   kubectl describe pod -l job-name=payments-api-migrate -n payments-prod
   ```
   Common root causes at this point: the hook container's command
   exited non-zero (application-level bug in the migration/script — read
   the actual log line), the pod never scheduled (resource
   requests/limits or a missing image pull secret — check `kubectl
   describe pod` events), or the hook Job hit its own `activeDeadlineSeconds`
   / Argo CD's operation timeout before finishing.

6. **If a hook is stuck because a previous failed run's Job object still
   exists**, confirm the `hook-delete-policy` and clean up manually if
   needed rather than waiting indefinitely:
   ```bash
   kubectl get jobs -n payments-prod -l argocd.argoproj.io/hook-type=PreSync
   kubectl delete job payments-api-migrate -n payments-prod   # only if hook-delete-policy is missing/insufficient
   argocd app sync payments-api-prod
   ```
   Prefer fixing `hook-delete-policy: HookSucceeded,HookFailed` in Git
   (see
   [argocd-application-configuration](../argocd-application-configuration/SKILL.md))
   over repeatedly deleting stuck Jobs by hand — the manual delete is a
   one-time unblock, not a fix for the recurring cause.

7. **When a `Degraded`/stuck `Progressing` resource is a custom CRD**,
   confirm whether Argo CD has real health-check logic for that kind
   before trusting its verdict:
   ```bash
   kubectl get application payments-api-prod -n argocd -o jsonpath='{.status.resources[?(@.kind=="DatabaseClaim")]}'
   kubectl get databaseclaim payments-api-db -n payments-prod -o yaml
   ```
   If `kubectl` shows the resource genuinely healthy but Argo CD reports
   `Progressing`/`Unknown` indefinitely, this is a missing custom health
   check, not a real problem with the resource — see
   [argocd-application-configuration](../argocd-application-configuration/SKILL.md)
   step 5 for adding one, rather than treating the app as actually
   broken.

8. **Before forcing a resolution, run a dry-run to see exactly what a
   real sync would change:**
   ```bash
   argocd app sync payments-api-prod --dry-run
   argocd app sync payments-api-prod --resource apps:Deployment:payments-prod/payments-api --dry-run
   ```
   Only escalate to `argocd app sync --force` (replace semantics) or
   `argocd app terminate-op` (abort a stuck operation) once the dry-run
   diff and the hook logs make the root cause unambiguous — both are
   stronger, riskier actions than a normal sync (see Common pitfalls).

## Best practices

- Always check `status.sync`, `status.health`, and
  `status.operationState` as three separate signals before deciding what
  "broken" means for a given `Application` — conflating them leads to
  fixing the wrong thing.
- Diff at the resource level (`argocd app diff --resource ...`) as soon
  as an app manages more than a handful of resources — an app-wide diff
  on a large `Application` buries the one relevant field in noise.
- Treat `managedFields`/field-manager inspection as the standard way to
  tell "Argo CD wrote this last" from "a human/other controller wrote
  this last" — don't guess based on how the diff *looks*.
- Fix recurring manual-drift fields with `ignoreDifferences` (if the
  field is legitimately externally managed) or a written runbook telling
  humans to change it in Git, not `kubectl`, going forward — treat
  repeated manual drift on the same field as a process gap, not a
  one-off to silently re-sync away each time.
- Read the hook's actual pod logs before assuming a hook "just needs a
  retry" — a hook Job that fails the same way every time has a real bug,
  and re-running it without a fix just delays the same failure.
- Prefer `argocd app sync --dry-run` and `--resource`-scoped syncs over a
  full `--force` sync when the cause is still unclear — narrow the blast
  radius while you're still diagnosing, not after.
- Keep a lightweight incident note (which resource, what the diff showed,
  what was manually changed, what fix was applied) for any drift incident
  involving a manual out-of-band edit — repeated manual edits to the same
  resource are a signal worth raising with
  [incident-investigation-using-metrics-logs-traces](../../../observability-and-platform-extras/skills/incident-investigation-using-metrics-logs-traces/SKILL.md)-style
  root-cause tracking if they correlate with incidents.

## Common pitfalls

- **Symptom:** `argocd app diff` shows no meaningful difference, yet the
  `Application` still reports `OutOfSync`.
  **Fix:** The diff is likely in a field Argo CD compares but doesn't
  render clearly in the default diff view (e.g. an annotation ordering
  difference, or a field under a `status` subresource being compared when
  it shouldn't be). Run `argocd app diff --hard-refresh` to bypass any
  cached comparison and force a fresh live-state fetch before concluding
  the diff tool itself is wrong.

- **Symptom:** A resource keeps flipping between `Synced` and `OutOfSync`
  every reconciliation loop, and each `argocd app diff` shows the same
  field toggling.
  **Fix:** This is a live sync loop, not intermittent drift — a mutating
  admission webhook, HPA, or defaulting controller is rewriting the field
  immediately after every sync (`selfHeal` reverts it, the controller sets
  it again). Confirm via `managedFields` timestamps, then add the field
  to `spec.ignoreDifferences` (see
  [argocd-application-configuration](../argocd-application-configuration/SKILL.md))
  instead of repeatedly re-syncing.

- **Symptom:** A `PreSync` hook Job is stuck `Running` far past when it
  should have finished, and the sync operation itself is stuck
  `Running`/never times out.
  **Fix:** Check `kubectl describe pod` for the hook — a common cause is
  the pod never actually scheduled (insufficient node resources, a
  missing/misconfigured image pull secret) so there's no process to time
  out yet. Argo CD's operation-level timeout doesn't fire on a pod that
  never started; fix the scheduling blocker directly, or set
  `activeDeadlineSeconds` on the hook Job spec so it self-terminates
  instead of hanging indefinitely.

- **Symptom:** Someone `kubectl scale`d a Deployment's replicas up during
  an incident, and thirty seconds later it silently reverted back to the
  Git-declared value — the on-call engineer assumes Argo CD is
  "fighting" them and disables sync entirely as a workaround.
  **Fix:** This is `selfHeal` working as designed, not a bug — the
  replica count is declared in Git and Argo CD is correctly reverting
  the out-of-band change. During an active incident where a temporary
  manual scale is intentional, either pause automated sync for that
  specific `Application` (`argocd app set <app> --sync-policy none`) or
  add a temporary `Prune=false`/`ignoreDifferences` entry, and revert the
  workaround once the incident resolves — don't leave sync disabled
  indefinitely as the "fix."

- **Symptom:** `argocd app sync --force` was used to unblock a stuck sync,
  and it deleted and recreated a resource with an immutable field
  (`ClusterIP`, a PVC's storage class), causing unexpected downstream
  breakage.
  **Fix:** `--force` uses replace (delete+create), not patch, semantics —
  reserve it for genuine "the API server rejects a normal patch" cases
  confirmed via the actual error in `operationState.message`, run
  `argocd app diff` first to see what would be replaced, and prefer
  `--resource`-scoped `--force` over an app-wide one so only the resource
  that genuinely needs replacing is affected.

- **Symptom:** A stuck sync operation is aborted with `argocd app
  terminate-op`, but some resources from the partial sync were already
  applied and others weren't, leaving the cluster in a half-migrated
  state.
  **Fix:** `terminate-op` stops the *operation*, not the already-applied
  changes — after terminating, immediately run `argocd app diff` to see
  exactly which resources are now inconsistent, and re-sync deliberately
  (ideally `--dry-run` first) rather than assuming termination reverted
  anything.

## Worked example

**Scenario:** `payments-api-prod` has shown `OutOfSync` for two days.
The team assumed it was "just a flaky sync" and kept clicking "Sync" in
the UI, which briefly clears the status before it returns within
minutes.

1. Pull the three independent status signals:
   ```bash
   argocd app get payments-api-prod -o json | jq '.status.sync.status, .status.health.status, .status.operationState.phase'
   ```
   Result: `"OutOfSync"`, `"Healthy"`, `"Succeeded"` — the app is
   functionally fine (healthy), it's specifically the Git/cluster
   comparison that's mismatched, and the last sync operation itself
   completed without error. This rules out a hook failure entirely.

2. Get the resource-level diff:
   ```bash
   argocd app diff payments-api-prod
   ```
   Output shows a single difference on the `payments-api` Deployment:
   `spec.replicas: live=12, git=3`.

3. Check whether `replicas` is even meaningfully declared in Git as `3`,
   or whether an HPA manages it:
   ```bash
   kubectl get hpa payments-api -n payments-prod -o yaml
   ```
   Confirms an HPA (`payments-api-hpa`) targets this Deployment and had
   scaled it to 12 replicas under load — `replicas` in Git is just the
   HPA's minimum floor, not the live intended value, so this was never
   real drift; it's the well-known HPA-vs-GitOps interaction.

4. Fix at the source rather than re-syncing daily: add `replicas` to
   `ignoreDifferences` in the `Application` spec (per
   [argocd-application-configuration](../argocd-application-configuration/SKILL.md)):
   ```yaml
   spec:
     ignoreDifferences:
       - group: apps
         kind: Deployment
         name: payments-api
         jsonPointers:
           - /spec/replicas
   ```
   After applying, `argocd app get payments-api-prod` reports `Synced`
   permanently (barring an actual Git change), and the team stops
   manually re-syncing an app that was never actually out of sync in any
   meaningful way.

## Cross-references

- [argocd-application-configuration](../argocd-application-configuration/SKILL.md) — where sync policy, sync waves, hooks, and `ignoreDifferences` are configured; this skill diagnoses that configuration's runtime behavior.
- [argocd-applicationset-patterns](../argocd-applicationset-patterns/SKILL.md) — when the same drift/hook issue shows up across many generated `Application`s at once rather than a single app.
- [incident-investigation-using-metrics-logs-traces](../../../observability-and-platform-extras/skills/incident-investigation-using-metrics-logs-traces/SKILL.md) — correlating a sync-hook failure or a bad rollout's `Degraded` state with metrics/logs/traces during a live incident.
- [incident-response-and-on-call-management](../../../site-reliability-engineering/skills/incident-response-and-on-call-management/SKILL.md) — process for handling an intentional out-of-band `kubectl` change made during an active incident without it becoming a confusing drift investigation afterward.

---
name: argocd-application-configuration
description: >
  Configures Argo CD `Application` custom resources — sync policies
  (automated vs. manual, prune, self-heal), sync waves and hooks for
  ordered/multi-phase rollouts, and health checks for custom resource
  types. Use when the user asks to "write an Argo CD Application manifest,"
  "enable auto-sync / self-heal / prune," "order resources with sync
  waves," "add a PreSync/PostSync hook," "fix an Application stuck
  OutOfSync or Progressing," or "define a custom health check for a CRD
  Argo CD doesn't understand natively."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: gitops-argo-ecosystem
  maturity: stable
---

# Argo CD Application Configuration

## Purpose

The Argo CD `Application` custom resource is the unit of reconciliation:
it binds a Git source (repo, revision, path) to a cluster destination and a
sync policy, and everything about how a service actually gets deployed and
kept in sync lives in its `spec`. Getting the `Application` spec right —
sync policy, ordering via sync waves/hooks, and health assessment — is the
difference between a GitOps setup that quietly self-heals drift and one
that either does nothing on its own (manual toil) or auto-prunes resources
nobody meant to delete. This skill assumes you already know *why* GitOps
and Argo CD exist (see
[gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md)) and goes
deep on the mechanics of the `Application` CRD itself: sync policy fields,
sync wave/phase ordering, hooks, and custom health checks.

## When to use

- Writing or reviewing an `Application` manifest from scratch for a new
  service.
- Deciding automated vs. manual sync, and whether `prune`/`selfHeal` should
  be on for a given environment.
- Ordering a multi-resource rollout (e.g., a CRD must exist before the CR
  that uses it, or a DB migration Job must run before the new Deployment)
  using `sync-wave` annotations or `PreSync`/`Sync`/`PostSync` hooks.
- An `Application` is stuck `Progressing` or shows `Unknown`/`Missing`
  health for a resource type Argo CD doesn't have built-in health logic
  for (custom CRDs, some operators).
- Diagnosing why `prune` deleted a resource that was still needed, or why
  `selfHeal` reverted an intentional manual change.
- Tuning `ignoreDifferences` so a legitimately mutated field (e.g., an HPA-
  or webhook-injected field) doesn't show perpetual `OutOfSync`.

## Prerequisites & environment

- Argo CD ≥ 2.9 installed in-cluster (`argocd` namespace) with the
  `argocd` CLI matching the server's major version, and CLI/API access
  (`argocd login <ARGOCD_SERVER>`) with permissions on the target
  `AppProject`.
- The application's manifests already exist in a Git repo Argo CD can
  reach — plain YAML, Kustomize, or Helm; this skill focuses on the
  `Application` resource wrapping any of those, not on templating itself.
- `kubectl` access to the cluster for direct inspection when the
  `argocd` CLI/UI view isn't enough (`kubectl get application -n argocd`,
  `kubectl describe`).
- An `AppProject` already defined (or using `default`) that permits the
  source repo and destination namespace/cluster you're targeting —
  `Application` creation fails silently into a permission error otherwise.

## Step-by-step guidance

1. **Write the base `Application` manifest**, one per deployable unit:
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: payments-api-prod
     namespace: argocd
     finalizers:
       - resources-finalizer.argocd.argoproj.io
   spec:
     project: default
     source:
       repoURL: https://github.com/example/gitops-config.git
       targetRevision: main
       path: apps/payments-api/overlays/prod
     destination:
       server: https://kubernetes.default.svc
       namespace: payments-prod
     syncPolicy:
       syncOptions:
         - CreateNamespace=true
   ```
   The `resources-finalizer.argocd.argoproj.io` finalizer ensures that
   deleting the `Application` object also cascades to delete the managed
   resources (rather than orphaning them) — omit it deliberately if you
   want "delete the Application, leave the workload running" semantics.

2. **Choose the sync policy deliberately, per environment.** Three
   independent knobs, all under `spec.syncPolicy.automated`:
   ```yaml
   syncPolicy:
     automated:
       prune: true        # delete live resources removed from Git
       selfHeal: true      # revert out-of-band (kubectl edit) drift
       allowEmpty: false   # refuse to sync if the source renders 0 resources
     syncOptions:
       - CreateNamespace=true
       - PrunePropagationPolicy=foreground
       - RespectIgnoreDifferences=true
     retry:
       limit: 5
       backoff:
         duration: 5s
         factor: 2
         maxDuration: 3m
   ```
   - Omit `automated` entirely for **manual-only** sync — the common
     choice for production. The `Application` sits `OutOfSync` until an
     operator runs `argocd app sync payments-api-prod`.
   - `prune: true` **without** `selfHeal` still auto-deletes resources
     removed from Git on the next automated sync trigger, but does not
     revert manual in-cluster edits.
   - `selfHeal: true` **without** `prune` reverts drifted fields on
     existing resources but leaves resources manually created out-of-band
     alone (they're simply not tracked, not deleted).

   > **Warning — destructive default:** `prune: true` deletes any live
   > resource that is no longer declared in the Git source, including
   > accidentally-deleted manifests. Never enable it on a production
   > `Application` without `PrunePropagationPolicy` reviewed and, ideally,
   > `argocd app sync --dry-run` exercised first. Combine with
   > `metadata.annotations["argocd.argoproj.io/sync-options"]:
   > Prune=false` on any specific *resource* (not just the whole
   > Application) that must never be auto-deleted, such as a
   > `PersistentVolumeClaim` holding production data.

3. **Order multi-resource rollouts with sync waves.** Resources sync in
   ascending `sync-wave` order (default wave is `0`); resources within the
   same wave sync in parallel and must all reach a healthy state before
   the next wave begins.
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: payments-api
     annotations:
       argocd.argoproj.io/sync-wave: "1"   # after wave 0 (e.g., a CRD/ConfigMap)
   ---
   apiVersion: batch/v1
   kind: Job
   metadata:
     name: payments-api-db-migrate
     annotations:
       argocd.argoproj.io/sync-wave: "0"   # runs, and must succeed, before wave 1
   ```
   Use negative waves (e.g., `"-1"`) for prerequisites like Namespaces or
   CRDs that must exist before anything else applies.

4. **Use lifecycle hooks for one-shot actions that aren't ordinary
   reconciled resources** (migrations, cache warms, notifications):
   ```yaml
   apiVersion: batch/v1
   kind: Job
   metadata:
     name: payments-api-migrate
     annotations:
       argocd.argoproj.io/hook: PreSync
       argocd.argoproj.io/hook-delete-policy: HookSucceeded
   spec:
     template:
       spec:
         restartPolicy: Never
         containers:
           - name: migrate
             image: ghcr.io/example/payments-api-migrate:1.4.2
             command: ["./migrate", "up"]
   ```
   - `PreSync` runs before the sync applies the rest of the manifests;
     `Sync` runs interleaved with normal resources at the same wave;
     `PostSync` runs once everything is synced and healthy.
   - `hook-delete-policy: HookSucceeded` removes the Job automatically on
     success so re-runs on the next sync don't collide with a name already
     in use; `HookFailed` (add both) also cleans up failed attempts once
     inspected.
   - Sync waves and hooks combine: hooks respect wave ordering relative to
     normal resources and each other.

5. **Add custom health checks for CRDs Argo CD doesn't understand
   natively.** Argo CD reports `Progressing`/`Healthy`/`Degraded` using
   built-in logic for common kinds (Deployment, StatefulSet, Ingress,
   etc.); unknown CRDs default to `Healthy` as soon as they exist, which
   hides real failures. Configure a Lua health check in the
   `argocd-cm` ConfigMap:
   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: argocd-cm
     namespace: argocd
   data:
     resource.customizations.health.example.com_DatabaseClaim: |
       hs = {}
       if obj.status ~= nil and obj.status.phase ~= nil then
         if obj.status.phase == "Ready" then
           hs.status = "Healthy"
           hs.message = "Database claim is ready"
           return hs
         end
         if obj.status.phase == "Failed" then
           hs.status = "Degraded"
           hs.message = obj.status.message or "Database claim failed"
           return hs
         end
       end
       hs.status = "Progressing"
       hs.message = "Waiting for database claim"
       return hs
   ```

6. **Tune diffing so legitimate mutation isn't perpetual drift.** Fields
   mutated by admission webhooks, HPAs, or defaulting controllers
   (`replicas` under an HPA, injected sidecar fields) will otherwise show
   as permanent `OutOfSync`:
   ```yaml
   spec:
     ignoreDifferences:
       - group: apps
         kind: Deployment
         jsonPointers:
           - /spec/replicas
       - group: ""
         kind: Service
         jqPathExpressions:
           - .spec.clusterIP
   ```

7. **Apply and verify:**
   ```bash
   kubectl apply -f payments-api-prod-application.yaml
   argocd app get payments-api-prod
   argocd app sync payments-api-prod --dry-run   # preview before a real sync
   argocd app sync payments-api-prod
   argocd app wait payments-api-prod --health --timeout 300
   ```
   `argocd app sync --dry-run` (client-side diff, not a real `--dry-run`
   apply) shows what would change without applying — always run it before
   the first sync of a risky change, and before ever running `argocd app
   sync <app> --force` (which replaces resources instead of patching,
   useful for unrecoverable field conflicts but a stronger action —
   confirm the diff first).

## Best practices

- Default new `Application`s to **manual sync** and only promote to
  `automated` once the team trusts the pipeline feeding the config repo —
  it's much safer to tighten from manual→automated deliberately per
  environment than to discover `prune: true` was live in prod by accident.
- Put `Prune=false`/`Replace=false` sync-option annotations directly on
  any individual resource that must survive being removed from Git
  temporarily (e.g., a PVC), rather than disabling `prune` for the whole
  `Application` and losing its benefit everywhere else.
- Keep sync-wave numbers sparse (`-10`, `0`, `10`, `20`) rather than
  sequential (`0,1,2,3`) so inserting a new ordering step later doesn't
  require renumbering everything downstream.
- Prefer `PreSync` hooks with `hook-delete-policy: HookSucceeded,
  HookFailed` over sync waves for genuinely one-shot actions (migrations)
  — hooks are explicitly one-shot semantics; sync waves are for ordering
  *reconciled* resources, and abusing waves for one-shot Jobs risks the
  Job being treated as a resource to keep converging.
- Write custom health checks for every CRD your `Application`s manage that
  isn't in Argo CD's built-in list — an `Application` reporting `Healthy`
  the instant a custom resource is created (because Argo CD doesn't know
  how to check it) hides real provisioning failures from dashboards and
  alerts.
- Set `retry.limit` and `backoff` explicitly on sync policy rather than
  leaving Argo CD to retry indefinitely against a resource that will never
  succeed (e.g., a bad manifest) — bound the noise.

## Common pitfalls

- **Symptom:** An `Application` continuously reports `OutOfSync` even
  though nothing in Git changed and no one touched the cluster; each
  `argocd app diff` shows the same one or two fields flipping back and
  forth.
  **Fix:** This is a sync loop caused by a mutating admission
  webhook/controller (HPA setting `replicas`, a service mesh sidecar
  injector adding annotations, a cert-manager-managed field) fighting with
  `selfHeal` reverting it. Add the field to `spec.ignoreDifferences`
  rather than disabling `selfHeal` for the whole Application.

- **Symptom:** After removing a Deployment from the Git overlay (thinking
  it was unused), the PVC it depended on was also deleted on the next
  automated sync, taking data with it.
  **Fix:** This is `prune: true` doing exactly what it's configured to do
  — anything no longer in Git is deleted. Before removing manifests for
  stateful resources, either move them to a separate `Application` with
  manual sync, or annotate the specific resource with
  `argocd.argoproj.io/sync-options: Prune=false` so it survives removal
  from Git until deliberately deleted via `kubectl`.

- **Symptom:** An `Application` is stuck `Progressing` indefinitely for a
  custom resource (e.g., a `DatabaseClaim` CRD from an internal operator)
  even though `kubectl get` shows the resource's `status.phase: Ready`.
  **Fix:** Argo CD has no built-in health logic for that CRD and defaults
  unknown types to a generic `Progressing`/`Healthy` guess based on
  presence, not actual status. Add a `resource.customizations.health.*`
  Lua script to `argocd-cm` (step 5 above) that reads the CRD's actual
  status fields.

- **Symptom:** A `PreSync` migration Job fails once, is fixed, and re-run
  by triggering another sync — but the sync fails immediately with
  "Job already exists" before the new Job even runs.
  **Fix:** The failed Job wasn't cleaned up because
  `hook-delete-policy` was set to only `HookSucceeded`. Set it to
  `HookSucceeded,HookFailed` (or `BeforeHookCreation`) so a failed hook
  Job is removed before the next attempt, rather than manually
  `kubectl delete job` every time.

- **Symptom:** `argocd app sync --force` was run to clear a stuck sync,
  and it turned out to delete and recreate a Service, causing a brief
  `ClusterIP` change that broke a hardcoded downstream reference.
  **Fix:** `--force` uses replace (delete+create) semantics instead of a
  patch, which can change immutable fields like `ClusterIP` on
  recreation. Reserve `--force` for genuine "normal patch/apply is
  rejected by the API server" cases, run `argocd app diff` first, and
  never treat it as an interchangeable stronger version of an ordinary
  sync.

## Worked example

**Scenario:** `payments-api` needs a `PreSync` DB migration, custom health
checking for an internal `DatabaseClaim` CRD it depends on, and safe
production sync settings (no auto-prune of its PVC).

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: payments-api-prod
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/example/gitops-config.git
    targetRevision: main
    path: apps/payments-api/overlays/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: payments-prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
    retry:
      limit: 5
      backoff: { duration: 5s, factor: 2, maxDuration: 3m }
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers: ["/spec/replicas"]
```

Overlay-side resources include:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: payments-api-migrate
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded,HookFailed
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - { name: migrate, image: ghcr.io/example/payments-api-migrate:1.4.2 }
---
apiVersion: storage.example.com/v1
kind: DatabaseClaim
metadata:
  name: payments-api-db
  annotations:
    argocd.argoproj.io/sync-options: Prune=false
spec:
  storageClassRef: fast-ssd
```

And `argocd-cm` gets a health check for `DatabaseClaim` (step 5 above).
Result: on each sync, the migration Job runs and must succeed before the
Deployment applies; `DatabaseClaim` health reflects its real
`status.phase`, not just its existence; and even if `payments-api-db` is
ever removed from the overlay by mistake, `Prune=false` prevents automated
deletion of the live claim.

## Cross-references

- [argocd-applicationset-patterns](../argocd-applicationset-patterns/SKILL.md)
- [argo-rollouts-progressive-delivery](../argo-rollouts-progressive-delivery/SKILL.md)
- [gitops-multi-cluster-management](../gitops-multi-cluster-management/SKILL.md)
- [gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md)

---
name: flux-cd-configuration-validation
description: >
  Validates Flux CD `Kustomization`s and `HelmRelease`s with build/diff/
  dry-run tooling (`flux diff kustomization`, `kustomize build`,
  `helm template`) before they reconcile against a live cluster, and
  interprets `flux get`/status conditions to distinguish a genuinely
  healthy reconciliation from one that merely applied without error.
  Use when a user asks to "dry-run a Flux Kustomization before merging,"
  "validate a HelmRelease's values before it deploys," "check what a
  Flux change will actually do before it reconciles," "why is my
  Kustomization Ready but the cluster looks wrong," or "add a CI gate
  for Flux manifest changes."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Flux CD Configuration Validation

## Purpose

Because Flux reconciles automatically and continuously, a bad
`Kustomization` path, a malformed Kustomize overlay, or a `HelmRelease`
values change with a typo doesn't wait for a deliberate "deploy" action
the way a manually-triggered pipeline would — it reconciles against the
live cluster on the next poll interval whether or not anyone reviewed
what it would actually do. Validating a change *before* it merges (dry
running the Kustomize build, diffing against the live cluster, rendering
Helm values) is therefore not optional polish for Flux the way it might
be for a slower, human-gated deploy process — it's the only checkpoint
between "a PR merged" and "the cluster changed." This skill covers that
pre-reconciliation validation workflow, layered on top of
[flux-cd-configuration-and-reconciliation](../flux-cd-configuration-and-reconciliation/SKILL.md)'s
CRD configuration, and on interpreting Flux's own status output
correctly once something has reconciled (or failed to).

## When to use

- Adding a CI gate that validates Kustomize/Helm manifest changes in a
  `gitops-config` repo before merge, so problems surface in a PR check
  rather than after Flux reconciles them.
- Reviewing a PR that changes a `Kustomization`'s path, a Kustomize
  overlay, or a `HelmRelease`'s chart version/values, and wanting to
  see the actual resulting diff against the live cluster before
  approving.
- A `Kustomization`/`HelmRelease` reports `Ready: True` but something
  about the resulting cluster state looks wrong, and it's unclear
  whether that's a validation gap or a genuine bug.
- Testing a `prune: true` Kustomization's refactor (moved/renamed
  resources) for unintended deletions before merging.
- Debugging a `Kustomization` stuck `Ready: False` to determine whether
  the failure is a build-time error (bad YAML/Kustomize syntax) or a
  cluster-side apply error (RBAC, admission webhook rejection, CRD not
  yet installed).

## Prerequisites & environment

- Flux CLI ≥ v2.3 with `flux diff kustomization` support, plus
  `kubectl` access to the target cluster context for diffing (the diff
  command needs to read live cluster state to compare against).
- `kustomize` ≥ 5.0 and `helm` ≥ 3.x installed for standalone
  build/template validation independent of the Flux CLI, useful in CI
  where a full cluster connection isn't available or desired for
  read-only structural checks.
- The `Kustomization`/`HelmRelease` CRDs already defined per
  [flux-cd-configuration-and-reconciliation](../flux-cd-configuration-and-reconciliation/SKILL.md)
  — this skill validates changes to what those CRDs point at, not how
  to define the CRDs themselves.
- For CI-based validation: a runner with network access to the Git
  repo and (for live-diff checks specifically) the target cluster —
  note that a live diff against production from an untrusted CI runner
  has its own credential-scoping considerations, covered in Best
  practices below.

## Step-by-step guidance

1. **Validate Kustomize build output structurally, independent of any
   cluster**, as the fastest, lowest-cost first check — this catches
   syntax errors, broken resource references, and invalid overlay
   patches before anything cluster-aware runs:
   ```bash
   kustomize build apps/payments-api/overlays/prod > /tmp/rendered.yaml
   kubectl apply --dry-run=client -f /tmp/rendered.yaml
   ```
   `--dry-run=client` catches malformed Kubernetes object syntax
   without needing real cluster credentials at all — run this in CI on
   every PR touching a Kustomize path, regardless of whether a live
   cluster diff is also performed.

2. **Validate against the API server's actual schema/admission chain**
   with a server-side dry run, which catches problems `--dry-run=client`
   can't (CRD schema validation, admission webhook rejections, RBAC):
   ```bash
   kubectl apply --dry-run=server -f /tmp/rendered.yaml
   ```
   This requires real (even if read-only-equivalent) cluster
   credentials and talks to the live API server's validation/admission
   pipeline without actually persisting the change — a meaningfully
   stronger check than client-side validation alone, and the natural
   next step before a full live diff.

3. **Diff the rendered manifests against live cluster state directly**
   with Flux's own diff command, which reproduces exactly what a real
   reconcile would apply:
   ```bash
   flux diff kustomization payments-api-prod --path ./apps/payments-api/overlays/prod
   ```
   Run this against a checked-out branch/PR locally, or wire it into
   CI comparing the PR's branch content against the live cluster
   `flux diff kustomization` is pointed at — it surfaces the same class
   of "additive vs. destructive" distinction that reviewing a
   `terraform plan` does in
   [infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md):
   a diff showing only new/changed fields is a different risk profile
   than one showing resources being removed (relevant for
   `prune: true` Kustomizations especially).

4. **Render and validate `HelmRelease` values changes with `helm
   template` before merging**, using the same chart version and values
   the `HelmRelease` declares:
   ```bash
   helm template redis bitnami/redis --version 19.x -f values-prod.yaml > /tmp/redis-rendered.yaml
   kubectl apply --dry-run=server -f /tmp/redis-rendered.yaml
   ```
   Extract `values-prod.yaml` from the `HelmRelease.spec.values` block
   (or `valuesFrom` ConfigMap/Secret references, resolved manually for
   the check) so what's rendered matches exactly what Flux's
   `helm-controller` will actually apply — validating against
   different values than what's really configured gives a false sense
   of safety.

5. **Wire structural and server-dry-run checks into CI as a required PR
   check**, so a broken manifest never reaches the point of being
   merged and picked up by Flux's next poll:
   ```yaml
   # GitHub Actions example
   - name: Kustomize build validation
     run: |
       for overlay in $(find apps -maxdepth 3 -type d -name prod); do
         kustomize build "$overlay" | kubectl apply --dry-run=server -f -
       done
   ```
   Fail the PR check on any error rather than merging first and finding
   out from a `Kustomization`'s `Ready: False` status after the fact.

6. **Interpret `flux get` status output correctly** once something has
   reconciled — the same "applied successfully" vs. "actually correct"
   distinction that matters for
   [argocd-sync-failure-and-drift-investigation](../../../gitops-argo-ecosystem/skills/argocd-sync-failure-and-drift-investigation/SKILL.md)
   applies here:
   ```bash
   flux get kustomizations payments-api-prod
   flux get helmreleases -n payments-prod
   kubectl get kustomization payments-api-prod -n flux-system -o jsonpath='{.status.conditions}'
   ```
   `Ready: True` reflects the last reconcile attempt applying without
   an API-level error; it does not by itself confirm the resulting
   workload is healthy unless `wait: true` with `healthChecks` was
   configured (see
   [flux-cd-configuration-and-reconciliation](../flux-cd-configuration-and-reconciliation/SKILL.md)) —
   treat `Ready: True` with no health checks configured as "applied,"
   not "verified healthy."

7. **For a `Kustomization` stuck `Ready: False`, distinguish a
   build-time failure from a cluster-side apply failure** before
   investigating further, since the fix differs entirely:
   ```bash
   kubectl describe kustomization payments-api-prod -n flux-system
   ```
   A message referencing a Kustomize build error (bad patch, missing
   base resource) means the problem is fixable by re-running step 1
   locally against the exact failing path; a message referencing an
   apply/admission error (RBAC denial, webhook rejection, CRD not
   found) means the problem is cluster-side and the manifest itself may
   be syntactically fine — check `kustomize-controller`'s own RBAC and
   whether a `dependsOn` (installing the missing CRD first) is needed.

8. **Validate a `prune: true` refactor specifically for unintended
   deletions** before merging a change that moves/renames resources
   within a pruning-enabled Kustomization's path:
   ```bash
   flux diff kustomization payments-api-prod --path ./apps/payments-api/overlays/prod
   ```
   Read the diff specifically for resources marked for deletion that
   weren't intentionally removed — a renamed base file or a Kustomize
   `nameSuffix` change can look like "delete old resource, create new
   one" even when the intent was just a rename, and `prune: true`
   will genuinely delete the "old" one on the next reconcile.

## Best practices

- Treat `kustomize build` + `kubectl apply --dry-run=server` as a
  mandatory, fast CI check on every PR touching a Flux-managed path —
  it's cheap, requires no risky cluster-write credentials, and catches
  the majority of structural errors before a human even reviews the
  diff.
- Scope any CI credentials used for `flux diff`/server-side dry-run to
  read-only cluster access — a diff/dry-run operation should never
  need write permissions, and granting write access "just in case" to
  a CI runner defeats the credential-scoping benefit GitOps is supposed
  to provide in the first place (see
  [gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md)).
- Render `HelmRelease` values from the actual source the `HelmRelease`
  references (the real chart version, the real values block/
  ConfigMap/Secret) rather than a hand-maintained copy that can drift
  from what's really configured over time.
- Review `flux diff kustomization` output specifically for deletions on
  any `prune: true` Kustomization before approving a refactor PR — a
  diff that's "just renames" in the author's head can be a real
  destructive delete+create in Flux's eyes.
- Don't conflate `Ready: True` with "verified healthy" in dashboards or
  runbooks — pair status monitoring with the `healthChecks`/`wait`
  configuration from
  [flux-cd-configuration-and-reconciliation](../flux-cd-configuration-and-reconciliation/SKILL.md)
  so `Ready: True` actually means what an on-call engineer will assume
  it means at 3am.
- Validate `HelmRelease` upgrades against the exact target chart
  version pinned in Git, not `latest` or a floating range resolved at
  validation time — a floating version constraint can mean CI validated
  a different chart release than what actually reconciles later.

## Common pitfalls

- **Symptom:** A PR passes `kustomize build` validation cleanly in CI,
  but the `Kustomization` still fails to reconcile once merged.
  **Fix:** `kustomize build` alone doesn't catch cluster-side apply
  failures (RBAC denial, an admission webhook rejecting the resource,
  a referenced CRD not yet installed) — add a server-side dry run
  (`kubectl apply --dry-run=server`) against a representative cluster
  in the same CI check, since client-side build validation and
  server-side admission are genuinely different failure surfaces.

- **Symptom:** `flux diff kustomization` run locally shows a clean,
  expected diff, but the actual reconciliation in the cluster produces
  a different result.
  **Fix:** Confirm the diff was run against the same `GitRepository`
  ref/commit and the same cluster context Flux is actually reconciling
  — a diff run against a stale local checkout, or against the wrong
  cluster context, is comparing against the wrong baseline and its
  "clean" result doesn't reflect what will really happen.

- **Symptom:** A `HelmRelease` values change was reviewed and approved
  based on a hand-written `values-prod.yaml` in the PR description, but
  the actual deployed configuration differs.
  **Fix:** The reviewed values file didn't match what's actually
  referenced in `HelmRelease.spec.values`/`valuesFrom` — always
  validate by rendering from the real CRD spec's value sources (step
  4), not a summary or a separately-maintained copy that can silently
  diverge from the source of truth.

- **Symptom:** A refactor PR that renames a Kustomize base directory
  merges cleanly, and the next reconciliation deletes a resource that
  was still needed.
  **Fix:** This was a `prune: true` refactor validated only by
  `kustomize build` (which shows the new state) without a `flux diff`
  against the *live* cluster (which would have shown the old resource
  being deleted, not just the new one being created) — always run the
  live diff, not just a build check, before merging any change that
  restructures paths inside a pruning-enabled Kustomization.

- **Symptom:** Someone runs `flux diff kustomization` or a server-side
  dry run using a CI credential that also has cluster-admin write
  access, and later that same credential is used (intentionally or by
  a compromised pipeline step) to apply changes directly to the
  cluster, bypassing Flux's own reconciliation and audit trail.
  **Fix:** This defeats the credential-scoping purpose of GitOps
  entirely — validation/diff tooling should run with read-only cluster
  credentials only; if a CI runner needs write access for some other
  legitimate reason, use a separate, narrowly-scoped credential for
  that purpose rather than reusing the broad one for diffing.

## Worked example

**Scenario:** A PR bumps the `redis` `HelmRelease`'s chart version and
renames the `apps/payments-api/overlays/prod` base's `deployment.yaml`
to `deployment-v2.yaml` as part of a cleanup, on a repo where
`payments-api-prod`'s `Kustomization` has `prune: true`.

1. CI's structural check runs first and passes cleanly:
   ```bash
   kustomize build apps/payments-api/overlays/prod | kubectl apply --dry-run=server -f -
   ```
   No errors — the rename didn't break the Kustomize build itself.

2. A reviewer, aware that `prune: true` makes renames risky, runs the
   live diff locally against the PR branch before approving:
   ```bash
   git fetch origin pull/482/head:pr-482 && git checkout pr-482
   flux diff kustomization payments-api-prod --path ./apps/payments-api/overlays/prod
   ```
   Output shows `Deployment/payments-prod/payments-api` marked for
   **deletion** and a *new* `Deployment/payments-prod/payments-api`
   being created — because the rename changed the underlying resource
   identity Kustomize generates, `prune: true` would delete the
   "old" Deployment (briefly dropping the running workload) before
   recreating it, rather than performing a clean in-place update.

3. The reviewer requests a change: keep the file name stable, or add a
   `moved`-equivalent handling (in Flux/Kustomize's case, ensuring the
   resource's `metadata.name` doesn't change) so the diff shows an
   update, not a delete+create.

4. Separately, the `HelmRelease` chart version bump is validated by
   rendering the exact target version and current values:
   ```bash
   helm template redis bitnami/redis --version 19.4.2 -f <(kubectl get helmrelease redis -n payments-prod -o jsonpath='{.spec.values}' | yq -P) \
     | kubectl apply --dry-run=server -f -
   ```
   This passes cleanly, so only the Kustomize rename needs rework
   before the PR merges — catching a would-be brief production outage
   in review instead of during an unattended reconcile.

## Cross-references

- [flux-cd-configuration-and-reconciliation](../flux-cd-configuration-and-reconciliation/SKILL.md) — the `Kustomization`/`HelmRelease` CRD configuration this skill validates before it reconciles.
- [gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md) — vendor-neutral GitOps principles (credential scoping, PR-gated changes) this validation workflow implements concretely for Flux.
- [infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md) — the `terraform plan`-review discipline this skill's `flux diff`/dry-run workflow mirrors for Kubernetes manifests instead of cloud infrastructure.
- [argocd-sync-failure-and-drift-investigation](../../../gitops-argo-ecosystem/skills/argocd-sync-failure-and-drift-investigation/SKILL.md) — the equivalent "status looks fine but isn't" investigative discipline on Argo CD, useful for contrast when a team runs both.
- [kustomize-overlay-management](../kustomize-overlay-management/SKILL.md) — structuring the overlays being built/diffed here.

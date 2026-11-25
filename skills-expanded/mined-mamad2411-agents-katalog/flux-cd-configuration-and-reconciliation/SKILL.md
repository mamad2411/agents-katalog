---
name: flux-cd-configuration-and-reconciliation
description: >
  Configures Flux CD's GitOps toolkit CRDs — `GitRepository` /
  `OCIRepository` sources, `Kustomization` and `HelmRelease` reconcilers,
  and the reconciliation loop's interval/dependency/health-check
  behavior — as the other major CNCF GitOps operator alongside Argo CD.
  Use when a user asks to "set up Flux CD," "configure a Flux
  GitRepository/Kustomization," "deploy a Helm chart via Flux
  HelmRelease," "set Flux reconciliation dependencies between
  Kustomizations," "debug why Flux isn't reconciling," or "choose Flux
  vs. Argo CD."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Flux CD Configuration and Reconciliation

## Purpose

Flux CD implements the same GitOps pull-based reconciliation model
covered generically in
[gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md) —
Git as source of truth, an in-cluster controller converging live state
toward it — but with its own distinct CRD-based architecture: a
`GitRepository`/`OCIRepository`/`HelmRepository` source object declares
*where* desired state comes from, and a `Kustomization` or `HelmRelease`
object declares *what* to reconcile from that source and how (interval,
dependencies, health checks, pruning). This is architecturally different
enough from Argo CD's single `Application` CRD that the two aren't
interchangeable one-for-one, and Flux's source/reconciler split is what
lets one `GitRepository` back multiple independent `Kustomization`s
reconciling at different paths and intervals. This skill goes deep on
Flux's specific CRDs and reconciliation behavior; for GitOps concepts
that apply to both Flux and Argo CD (repo topology, secrets handling,
rollback-by-revert), see
[gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md)
rather than expecting them repeated here.

## When to use

- Standing up Flux CD on a new cluster and deciding source/Kustomization
  structure.
- Deploying a Helm chart declaratively via `HelmRelease` rather than an
  imperative `helm install`/`helm upgrade`.
- Sequencing reconciliation across multiple `Kustomization`s that depend
  on each other (e.g. a CRD-installing Kustomization must reconcile
  before one that creates instances of that CRD).
- Tuning reconciliation interval, pruning behavior, or health-check
  timeout for a specific `Kustomization`/`HelmRelease`.
- Diagnosing a `Kustomization` or `HelmRelease` stuck `False` on
  `Ready`, or one that reconciles successfully but the cluster still
  doesn't match Git.
- Choosing Flux over Argo CD (or the reverse) for a new GitOps rollout.

## Prerequisites & environment

- A Kubernetes cluster ≥ 1.26 and the Flux CLI/controllers ≥ v2.3
  (Flux v1 is end-of-life — do not start a new deployment on it; see
  [gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md)'s
  Prerequisites for the same warning stated generically).
- `flux` CLI installed and cluster-admin (or sufficiently scoped)
  access for the initial bootstrap; ongoing operation only needs
  namespace-scoped RBAC matching what each `Kustomization`/`HelmRelease`
  actually manages.
- A Git repository (or OCI registry, for `OCIRepository` sources) Flux
  can authenticate to — a deploy key or a token stored as a Kubernetes
  `Secret`, never embedded in a CRD spec.
- Kustomize ≥ 5.0 (bundled into the `kustomize-controller`) or Helm ≥
  3.x (for `HelmRelease`) knowledge — this skill assumes familiarity
  with Kustomize overlays as covered in
  [kustomize-overlay-management](../kustomize-overlay-management/SKILL.md)
  and Helm chart structure as covered in
  [helm-chart-authoring](../helm-chart-authoring/SKILL.md).
- A secrets strategy decided before rollout (SOPS with age/GPG,
  External Secrets Operator, Sealed Secrets) — Flux integrates
  particularly well with SOPS via native decryption support in
  `kustomize-controller`, but the underlying rule ("never commit
  plaintext Secrets") is unchanged from
  [gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md).

## Step-by-step guidance

1. **Bootstrap Flux onto the cluster**, which installs the controllers
   and commits their manifests back into the target repo (so Flux's
   own installation is itself GitOps-managed):
   ```bash
   flux bootstrap github \
     --owner=example-org \
     --repository=gitops-config \
     --branch=main \
     --path=clusters/prod \
     --personal=false
   ```
   This creates a deploy key (or uses a provided token) for repo
   access, and writes Flux's own component manifests plus a root
   `Kustomization` under `clusters/prod/flux-system/` — future Flux
   upgrades happen by re-running bootstrap, not manual `kubectl apply`.

2. **Define a `GitRepository` source** pointing at the config repo,
   pinned to a branch or (for stricter environments) a tag:
   ```yaml
   apiVersion: source.toolkit.fluxcd.io/v1
   kind: GitRepository
   metadata:
     name: gitops-config
     namespace: flux-system
   spec:
     interval: 1m
     url: https://github.com/example-org/gitops-config
     ref:
       branch: main
     secretRef:
       name: gitops-config-auth
   ```
   `interval` controls how often Flux polls the source for new
   commits — shorter intervals mean faster propagation but more load
   on the Git provider; 1-5 minutes is a reasonable default for most
   teams.

3. **Define a `Kustomization` reconciling a specific path** from that
   source into the cluster:
   ```yaml
   apiVersion: kustomize.toolkit.fluxcd.io/v1
   kind: Kustomization
   metadata:
     name: payments-api-prod
     namespace: flux-system
   spec:
     interval: 5m
     sourceRef:
       kind: GitRepository
       name: gitops-config
     path: "./apps/payments-api/overlays/prod"
     prune: true
     wait: true
     timeout: 3m
     healthChecks:
       - apiVersion: apps/v1
         kind: Deployment
         name: payments-api
         namespace: payments-prod
   ```
   `prune: true` deletes cluster resources whose manifest was removed
   from the path — powerful and, as in Argo CD, worth enabling
   deliberately rather than by default without thinking about it (see
   [gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md)
   Best practices for the same caution). `wait: true` plus
   `healthChecks` makes the `Kustomization` block on the Deployment
   actually becoming healthy, not just on the apply succeeding.

4. **Sequence dependent `Kustomization`s explicitly** with
   `dependsOn` rather than relying on interval timing to happen to work
   out — critical when one Kustomization installs CRDs/namespaces
   another depends on:
   ```yaml
   apiVersion: kustomize.toolkit.fluxcd.io/v1
   kind: Kustomization
   metadata:
     name: payments-api-prod
     namespace: flux-system
   spec:
     dependsOn:
       - name: infra-crds-prod
       - name: payments-namespace-prod
     # ...(interval, sourceRef, path unchanged)
   ```
   `payments-api-prod` will not attempt to reconcile until both listed
   Kustomizations report `Ready: True` — this replaces guesswork about
   which interval "usually" finishes first with an explicit ordering
   guarantee.

5. **Deploy a Helm chart declaratively via `HelmRelease`**, backed by a
   `HelmRepository` (or `GitRepository`/`OCIRepository`) source:
   ```yaml
   apiVersion: source.toolkit.fluxcd.io/v1
   kind: HelmRepository
   metadata:
     name: bitnami
     namespace: flux-system
   spec:
     interval: 1h
     url: https://charts.bitnami.com/bitnami
   ---
   apiVersion: helm.toolkit.fluxcd.io/v2
   kind: HelmRelease
   metadata:
     name: redis
     namespace: payments-prod
   spec:
     interval: 10m
     chart:
       spec:
         chart: redis
         version: "19.x"
         sourceRef:
           kind: HelmRepository
           name: bitnami
           namespace: flux-system
     values:
       architecture: replication
       auth:
         existingSecret: redis-auth
     install:
       remediation:
         retries: 3
     upgrade:
       remediation:
         remediateLastFailure: true
   ```
   `install.remediation.retries` and
   `upgrade.remediation.remediateLastFailure` give `HelmRelease`
   automatic rollback-on-failure behavior that a plain `helm upgrade`
   in a CI pipeline doesn't have by default.

6. **Wire CI to update the config repo, not the cluster** — the same
   core GitOps inversion as
   [gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md)
   describes generically: application CI bumps an image tag or chart
   version in the `gitops-config` repo; `source-controller` and
   `kustomize-controller`/`helm-controller` perform the actual cluster
   apply, never the CI pipeline directly.

7. **Force an immediate reconciliation** when waiting for the next
   poll interval isn't acceptable (e.g. right after merging an urgent
   fix):
   ```bash
   flux reconcile source git gitops-config
   flux reconcile kustomization payments-api-prod --with-source
   ```
   `--with-source` reconciles the `GitRepository` first, then the
   `Kustomization`, in one command — otherwise the `Kustomization`
   might reconcile against a source that hasn't picked up the latest
   commit yet.

8. **Roll back by reverting Git**, exactly as in the vendor-neutral
   workflow, then confirm via Flux's own status rather than assuming:
   ```bash
   git revert <bad-commit-sha> && git push
   flux reconcile kustomization payments-api-prod --with-source
   flux get kustomizations payments-api-prod
   ```

## Best practices

- Keep `GitRepository`/`Kustomization`/`HelmRelease` reconciliation
  intervals deliberate, not uniformly as fast as possible — a very
  short interval on a large fleet of Kustomizations adds meaningful
  polling load to the Git provider/registry; 1-5 minutes for sources,
  5-10 minutes for Kustomizations/HelmReleases is a reasonable default
  absent a specific need for faster propagation.
- Use `dependsOn` for any real ordering requirement (CRDs before
  instances, namespaces before workloads) instead of tuning intervals
  to "usually" land in the right order — interval-based ordering is
  a race condition waiting to surface during an incident.
- Set `wait: true` with `healthChecks` on `Kustomization`s whose
  success genuinely depends on the workload becoming healthy, not just
  on the API server accepting the manifest — an apply that "succeeds"
  against a Deployment that then crash-loops is not a successful
  rollout.
- Prefer `HelmRelease`'s built-in remediation
  (`install.remediation`/`upgrade.remediation`) over a bespoke CI
  rollback script for Helm-based deploys — it's Flux-native, applies
  consistently across every `HelmRelease`, and doesn't require the CI
  pipeline to hold cluster-apply credentials.
- Use SOPS-encrypted Secrets committed directly to the config repo
  (Flux's `kustomize-controller` supports native decryption via a
  configured age/GPG key) as a lower-friction alternative to Sealed
  Secrets when the team is already comfortable with SOPS — either is
  acceptable per the secrets guidance in
  [gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md);
  don't invent a third, ad hoc mechanism.
- Structure one `Kustomization` per logically-independent unit of
  change (per app per environment, generally), not one giant
  `Kustomization` reconciling the entire repo — smaller units mean a
  failure in one doesn't block reconciliation of everything else, and
  `flux get kustomizations` gives a meaningful per-unit status.

## Common pitfalls

- **Symptom:** A `Kustomization` reports `Ready: False` with a vague
  "kustomization path not found" or build error.
  **Fix:** Check `spec.path` against the source's actual directory
  structure at the pinned `ref` — a path that exists on a different
  branch than the one `GitRepository.spec.ref.branch` points to, or a
  typo in the path, fails at the kustomize-build step before any apply
  is attempted. `flux get kustomizations payments-api-prod` and
  `kubectl describe kustomization payments-api-prod -n flux-system`
  surface the specific build error, not just a generic failure.

- **Symptom:** A `Kustomization` shows `Ready: True` and the reconcile
  "succeeded," but the cluster's actual state doesn't match what's in
  Git.
  **Fix:** `Ready: True` means the last reconcile attempt applied
  without an API error — it does not mean the applied manifests
  produced a healthy workload unless `wait: true` with `healthChecks`
  is configured. Add explicit health checks for anything where
  "applied" and "actually working" can diverge (most Deployments,
  StatefulSets, and any custom resource with its own readiness
  semantics).

- **Symptom:** Two `Kustomization`s reconciling the same resources (or
  a resource that references a CRD from another Kustomization) produce
  intermittent apply failures that "usually" work but sometimes don't.
  **Fix:** This is a missing `dependsOn` — whichever Kustomization
  currently happens to reconcile first via timing luck is masking a
  real ordering dependency. Add explicit `dependsOn` so ordering is
  deterministic rather than interval-timing-dependent, and re-test by
  forcing a simultaneous reconcile of both (`flux reconcile
  kustomization <a> <b>` back-to-back) to confirm it's now reliably
  correct.

- **Symptom:** A `HelmRelease` gets stuck in a failed state after a bad
  chart values change, and every subsequent reconcile attempt fails the
  same way.
  **Fix:** Check `upgrade.remediation.remediateLastFailure` is set —
  without it, Flux may not automatically roll back a failed upgrade,
  leaving the release in a broken intermediate state that blocks future
  upgrades until manually resolved
  (`flux suspend helmrelease redis -n payments-prod`, fix the
  underlying values, `flux resume helmrelease redis -n payments-prod`).

- **Symptom:** `prune: true` on a `Kustomization` unexpectedly deletes a
  resource that was still needed, because it was removed from the
  Kustomize path during a refactor rather than an intentional removal.
  **Fix:** This is the destructive side of `prune: true` working
  exactly as configured, not a bug — treat any restructuring of a
  pruning-enabled Kustomization's path (moving a resource to a
  different overlay, renaming a base) as a change requiring the same
  care as an intentional deletion, and consider `flux diff kustomization`
  (or a CI-based dry-run per
  [flux-cd-configuration-validation](../flux-cd-configuration-validation/SKILL.md))
  before merging a refactor that touches a pruning-enabled path.

## Worked example

**Scenario:** Deploy `payments-api` to production via Flux, where the
app's manifests depend on a CRD installed by a separate infra
Kustomization, and a Redis `HelmRelease` the app also depends on.

```bash
flux bootstrap github --owner=example-org --repository=gitops-config --branch=main --path=clusters/prod
```

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata: { name: gitops-config, namespace: flux-system }
spec:
  interval: 1m
  url: https://github.com/example-org/gitops-config
  ref: { branch: main }
```

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata: { name: infra-crds-prod, namespace: flux-system }
spec:
  interval: 10m
  sourceRef: { kind: GitRepository, name: gitops-config }
  path: "./infra/crds/prod"
  prune: true
  wait: true
```

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata: { name: redis, namespace: payments-prod }
spec:
  interval: 10m
  chart:
    spec:
      chart: redis
      version: "19.x"
      sourceRef: { kind: HelmRepository, name: bitnami, namespace: flux-system }
  install: { remediation: { retries: 3 } }
```

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata: { name: payments-api-prod, namespace: flux-system }
spec:
  interval: 5m
  sourceRef: { kind: GitRepository, name: gitops-config }
  path: "./apps/payments-api/overlays/prod"
  prune: true
  wait: true
  timeout: 3m
  dependsOn:
    - name: infra-crds-prod
  healthChecks:
    - { apiVersion: apps/v1, kind: Deployment, name: payments-api, namespace: payments-prod }
```

`payments-api-prod` waits for `infra-crds-prod` to report `Ready` before
attempting its own reconcile, so a fresh cluster bootstrap always
installs CRDs before anything tries to use them — no interval-timing
race. After merging a version bump, `flux reconcile kustomization
payments-api-prod --with-source` confirms the new version rolls out
immediately, and `flux get kustomizations` shows all three resources
`Ready: True` with their last-applied revision matching the latest
commit SHA.

## Cross-references

- [gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md) — vendor-neutral GitOps concepts (repo topology, secrets strategy, rollback-by-revert) this skill implements in Flux-specific terms; read that first if new to GitOps generally.
- [flux-cd-configuration-validation](../flux-cd-configuration-validation/SKILL.md) — dry-run/diff validation of Kustomizations and HelmReleases before they reconcile against a live cluster.
- [kustomize-overlay-management](../kustomize-overlay-management/SKILL.md) — designing the overlay structure Flux's `Kustomization` `path` points at.
- [helm-chart-authoring](../helm-chart-authoring/SKILL.md) — authoring the charts a `HelmRelease` deploys.
- [argocd-application-configuration](../../../gitops-argo-ecosystem/skills/argocd-application-configuration/SKILL.md) — the equivalent CRD-level configuration on the other major GitOps operator, for comparison when choosing between the two.

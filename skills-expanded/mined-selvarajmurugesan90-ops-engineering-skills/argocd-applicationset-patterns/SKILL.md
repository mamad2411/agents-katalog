---
name: argocd-applicationset-patterns
description: >
  Designs Argo CD `ApplicationSet` resources that template many
  `Application` objects from a single source using generators — List,
  Cluster, Git directory/file, and Matrix (combined generators). Use when
  the user asks to "generate an Application per cluster/environment/
  directory," "avoid copy-pasting Argo CD Applications," "roll out a
  service to a fleet of clusters," "combine a cluster generator with a Git
  generator," or "debug an ApplicationSet producing unexpected or missing
  Applications."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: gitops-argo-ecosystem
  maturity: stable
---

# Argo CD ApplicationSet Patterns

## Purpose

Hand-maintaining one `Application` manifest per service-per-environment or
per-cluster does not scale: N services × M environments quickly becomes
hundreds of near-duplicate YAML files that drift from each other in subtle
ways. `ApplicationSet` solves this by templating `Application` objects from
one or more **generators** — a list, a cluster registry, a Git repo's
directory/file structure, or a combination — so that adding a new
environment, cluster, or service directory automatically produces (and
later, automatically removes) the corresponding `Application`, with no
manual manifest authored per instance. This matters operationally because
it turns fleet-wide rollout consistency from a copy-paste discipline
problem into a generator-configuration problem, and it's the mechanism
that makes [gitops-multi-cluster-management](../gitops-multi-cluster-management/SKILL.md)'s
hub-and-spoke topology actually maintainable at scale.

## When to use

- More than a handful of near-identical `Application`s exist (same
  service, different environment/cluster/region) and are maintained by
  hand-copying and editing one field at a time.
- Onboarding a new cluster or environment should automatically produce the
  right set of `Application`s, not require someone to author new YAML.
  See also
  [argocd-application-configuration](../argocd-application-configuration/SKILL.md)
  for what goes inside each generated `Application`.
- A monorepo has one directory per microservice and each should become its
  own `Application` without per-service boilerplate.
- Rolling a service out to every registered cluster (fleet-wide) or a
  filtered subset of clusters by label.
- Debugging why an `ApplicationSet` produced Applications for directories
  or clusters that shouldn't have matched, or silently stopped generating
  one that should have.

## Prerequisites & environment

- Argo CD ≥ 2.9 with the `ApplicationSet` controller enabled (bundled by
  default in the standard install manifests since Argo CD 2.x; verify with
  `kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-applicationset-controller`).
- For the Cluster generator: target clusters already registered with Argo
  CD (`argocd cluster add <CONTEXT>` or a `Secret` labeled
  `argocd.argoproj.io/secret-type: cluster` in the `argocd` namespace).
- For the Git generator: read access to the config repo already
  configured as an Argo CD repository credential.
- Familiarity with Go template syntax (`{{.field}}`) or, for newer
  installs, the `Fasttemplate`/Sprig-enabled template engine
  (`ApplicationsSyncPolicy` and `goTemplate: true` at the
  `ApplicationSet` spec level) — pick one templating mode per
  `ApplicationSet` and don't mix syntaxes.

## Step-by-step guidance

1. **List generator** — smallest building block, an explicit inline set
   of parameters, most useful for a small fixed set of environments:
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: ApplicationSet
   metadata:
     name: payments-api-envs
     namespace: argocd
   spec:
     goTemplate: true
     goTemplateOptions: ["missingkey=error"]
     generators:
       - list:
           elements:
             - env: staging
               namespace: payments-staging
               replicas: "2"
             - env: prod
               namespace: payments-prod
               replicas: "10"
     template:
       metadata:
         name: "payments-api-{{.env}}"
       spec:
         project: default
         source:
           repoURL: https://github.com/example/gitops-config.git
           targetRevision: main
           path: "apps/payments-api/overlays/{{.env}}"
         destination:
           server: https://kubernetes.default.svc
           namespace: "{{.namespace}}"
         syncPolicy:
           automated: { prune: true, selfHeal: true }
   ```

2. **Cluster generator** — one `Application` per registered cluster,
   the core of fleet-wide rollout:
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: ApplicationSet
   metadata:
     name: platform-agent-fleet
     namespace: argocd
   spec:
     goTemplate: true
     generators:
       - clusters:
           selector:
             matchLabels:
               tier: production   # only clusters registered with this label
     template:
       metadata:
         name: "platform-agent-{{.name}}"
       spec:
         project: default
         source:
           repoURL: https://github.com/example/gitops-config.git
           targetRevision: main
           path: apps/platform-agent/base
         destination:
           server: "{{.server}}"
           namespace: platform-system
         syncPolicy:
           automated: { prune: true, selfHeal: true }
   ```
   `{{.name}}` and `{{.server}}` come from the cluster `Secret`'s labels
   and `server` field automatically; add custom labels
   (`argocd.argoproj.io/secret-type: cluster` Secrets support arbitrary
   labels) to filter which clusters this `ApplicationSet` targets, and
   custom `values.*` fields in the Secret to pass per-cluster parameters
   into the template — this is the mechanism
   [gitops-multi-cluster-management](../gitops-multi-cluster-management/SKILL.md)
   builds on for hub-and-spoke fleet rollout.

3. **Git directory generator** — one `Application` per matching directory,
   for monorepos with one folder per service or environment:
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: ApplicationSet
   metadata:
     name: all-services
     namespace: argocd
   spec:
     goTemplate: true
     generators:
       - git:
           repoURL: https://github.com/example/gitops-config.git
           revision: main
           directories:
             - path: "apps/*/overlays/prod"
             - path: "apps/legacy-billing/overlays/prod"
               exclude: true   # explicitly exclude a matched path
     template:
       metadata:
         name: "{{.path.basenameNormalized}}-prod"
       spec:
         project: default
         source:
           repoURL: https://github.com/example/gitops-config.git
           targetRevision: main
           path: "{{.path.path}}"
         destination:
           server: https://kubernetes.default.svc
           namespace: "{{.path.basenameNormalized}}-prod"
         syncPolicy:
           automated: { prune: true, selfHeal: true }
   ```
   `{{.path.path}}` is the full matched path; `{{.path.basename}}` and
   `{{.path.basenameNormalized}}` (DNS-safe, lowercase) are derived
   convenience fields — new service directories under `apps/*/overlays/prod`
   are picked up on the next generator refresh with zero manifest changes.

4. **Git file generator** — one `Application` per JSON/YAML file matching
   a glob, useful when parameters (not directory structure) drive
   templating:
   ```yaml
   generators:
     - git:
         repoURL: https://github.com/example/gitops-config.git
         revision: main
         files:
           - path: "clusters/*/config.yaml"
   ```
   where each `clusters/<name>/config.yaml` contains structured fields
   (`cluster`, `region`, `tier`) consumed as `{{.cluster}}`, `{{.region}}`,
   etc. in the template — preferred over the directory generator when you
   need more structured metadata per instance than a directory path alone
   encodes.

5. **Matrix generator** — combine two generators so their outputs form a
   cross-product, the pattern for "every service × every cluster" or
   "every service × every environment":
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: ApplicationSet
   metadata:
     name: services-x-clusters
     namespace: argocd
   spec:
     goTemplate: true
     generators:
       - matrix:
           generators:
             - git:
                 repoURL: https://github.com/example/gitops-config.git
                 revision: main
                 directories:
                   - path: "apps/*"
             - clusters:
                 selector:
                   matchLabels: { tier: production }
     template:
       metadata:
         name: "{{.path.basenameNormalized}}-{{.name}}"
       spec:
         project: default
         source:
           repoURL: https://github.com/example/gitops-config.git
           targetRevision: main
           path: "{{.path.path}}/overlays/{{.metadata.labels.tier}}"
         destination:
           server: "{{.server}}"
           namespace: "{{.path.basenameNormalized}}"
         syncPolicy:
           automated: { prune: true, selfHeal: true }
   ```
   Every service directory is crossed with every matching cluster,
   producing `service × cluster` Applications automatically — this is
   what makes fleet-wide multi-service rollout tractable, but see the
   pitfall below on unbounded cross-products.

6. **Preview before trusting `prune` at the `ApplicationSet` level.**
   `ApplicationSet`'s own `syncPolicy.applicationsSync` controls whether
   removed generator matches actually delete their generated
   `Application` (and, transitively, its managed resources if that
   `Application`'s own `syncPolicy.automated.prune` is also on):
   ```yaml
   spec:
     syncPolicy:
       preserveResourcesOnDeletion: true   # keep live resources if the
                                            # generated Application is removed
   ```
   > **Warning — destructive default:** without
   > `preserveResourcesOnDeletion: true`, removing a cluster/directory from
   > the generator's matches deletes the generated `Application`, and — if
   > that Application's `syncPolicy.automated.prune` is enabled — cascades
   > to delete its live workload too. Set
   > `preserveResourcesOnDeletion: true` for any fleet where a generator
   > match briefly disappearing (a flaky cluster Secret, a transient Git
   > API error) must not translate into deleting production workloads.

7. **Verify what a change to a generator will produce before merging:**
   ```bash
   argocd appset generate applicationset.yaml   # dry-run: list what would be generated
   kubectl get applicationset payments-api-envs -n argocd -o yaml   # inspect .status.conditions
   kubectl get applications -n argocd -l argocd.argoproj.io/application-set-name=payments-api-envs
   ```

## Best practices

- Pick `goTemplate: true` for any new `ApplicationSet` (Go template
  syntax, dot-notation) rather than the legacy Fasttemplate `{{field}}`
  syntax — mixing the two across an org's `ApplicationSet`s is a
  persistent source of copy-paste template bugs.
- Use `matchLabels`/`matchExpressions` selectors on the Cluster generator
  rather than targeting "all clusters" implicitly — an unlabeled or
  mislabeled cluster Secret should not silently receive a fleet-wide
  rollout it wasn't meant to get.
- For the Matrix generator, put the generator with the smaller, more
  controlled output first conceptually and always cap scope with
  selectors/directory globs on both sides — the cross-product grows
  multiplicatively, and an accidental match on one side multiplies across
  every match on the other.
- Set `goTemplateOptions: ["missingkey=error"]` so a typo'd template field
  fails loudly at generation time instead of silently rendering an empty
  string into a manifest.
- Name generated `Application`s with a deterministic, collision-free
  pattern (`{{.path.basenameNormalized}}-{{.name}}`) — two generator
  branches producing the same rendered name will overwrite each other's
  `Application` object.
- Set `preserveResourcesOnDeletion: true` for any production fleet
  `ApplicationSet` where generator flakiness (cluster Secret transiently
  missing, Git API rate limit) is a real risk relative to the cost of an
  accidental fleet-wide deletion.

## Common pitfalls

- **Symptom:** A new cluster was registered but no `Application` was
  generated for it.
  **Fix:** Check the cluster Secret's labels against the generator's
  `selector.matchLabels` — the most common cause is the new cluster
  Secret missing the label the `ApplicationSet` filters on. Confirm with
  `kubectl get secret -n argocd -l argocd.argoproj.io/secret-type=cluster --show-labels`.

- **Symptom:** A Matrix generator combining a Git directory generator (50
  service directories) with a Cluster generator (20 clusters) suddenly
  produced 1,000 Applications and overwhelmed the Argo CD controller /
  API server, spiking reconciliation latency across the whole instance.
  **Fix:** This is the cross-product growing exactly as configured but
  larger than intended — add tighter selectors on one or both sides
  (label-select a subset of clusters, glob a subset of directories) or
  split into multiple narrower `ApplicationSet`s rather than one
  all-services-by-all-clusters matrix.

- **Symptom:** Removing a directory from the Git generator's match (a
  service was deprecated and its overlay folder deleted) also deleted the
  live Kubernetes resources for that service immediately, with no
  warning, in production.
  **Fix:** This is expected `ApplicationSet` behavior without
  `preserveResourcesOnDeletion: true` combined with the generated
  Application's own `prune: true` — restore from the last known-good Git
  state if this was unintended, then set
  `syncPolicy.preserveResourcesOnDeletion: true` (or move deprecation to a
  two-step process: disable automated sync first, delete the directory
  second) before it happens again.

- **Symptom:** Two different generator branches (e.g., a List generator
  entry and a Git directory match) both render to the same `Application`
  name, and one silently overwrites/interferes with the other's spec on
  each reconcile.
  **Fix:** Template names must be unique across everything the
  `ApplicationSet` generates. Include a discriminating field
  (environment, cluster name) in the name template, and check
  `kubectl get applications -n argocd -l argocd.argoproj.io/application-set-name=<name>`
  for unexpected duplicates or count mismatches versus expected generator
  matches.

- **Symptom:** A template field renders as an empty string instead of
  failing, producing an `Application` with a blank `namespace` or `path`
  that then fails to sync with a confusing downstream error.
  **Fix:** Set `goTemplateOptions: ["missingkey=error"]` so a
  misspelled or missing template variable fails `ApplicationSet`
  generation loudly instead of silently rendering empty — check
  `kubectl describe applicationset <name> -n argocd` for the resulting
  condition/error once this is set.

## Worked example

**Scenario:** Roll `platform-agent` out to every cluster labeled
`tier: production` in the cluster registry, and separately generate one
`Application` per service directory under `apps/*/overlays/prod` in the
config repo — while ensuring neither an accidental cluster deregistration
nor a deleted directory can silently wipe production workloads.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: platform-agent-fleet
  namespace: argocd
spec:
  goTemplate: true
  goTemplateOptions: ["missingkey=error"]
  generators:
    - clusters:
        selector:
          matchLabels: { tier: production }
  template:
    metadata:
      name: "platform-agent-{{.name}}"
    spec:
      project: default
      source:
        repoURL: https://github.com/example/gitops-config.git
        targetRevision: main
        path: apps/platform-agent/base
      destination:
        server: "{{.server}}"
        namespace: platform-system
      syncPolicy:
        automated: { prune: true, selfHeal: true }
  syncPolicy:
    preserveResourcesOnDeletion: true
---
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: all-services-prod
  namespace: argocd
spec:
  goTemplate: true
  goTemplateOptions: ["missingkey=error"]
  generators:
    - git:
        repoURL: https://github.com/example/gitops-config.git
        revision: main
        directories:
          - path: "apps/*/overlays/prod"
  template:
    metadata:
      name: "{{.path.basenameNormalized}}-prod"
    spec:
      project: default
      source:
        repoURL: https://github.com/example/gitops-config.git
        targetRevision: main
        path: "{{.path.path}}"
      destination:
        server: https://kubernetes.default.svc
        namespace: "{{.path.basenameNormalized}}-prod"
      syncPolicy:
        automated: { prune: true, selfHeal: true }
  syncPolicy:
    preserveResourcesOnDeletion: true
```

Verify: `argocd appset generate platform-agent-fleet.yaml` before
applying shows exactly N Applications for N production-labeled clusters;
after applying, `kubectl get applications -n argocd -l
argocd.argoproj.io/application-set-name=platform-agent-fleet` confirms the
count matches the cluster registry, and a subsequent deregistration of one
cluster leaves that cluster's workload running (rather than deleted)
because of `preserveResourcesOnDeletion: true`, pending deliberate cleanup.

## Cross-references

- [argocd-application-configuration](../argocd-application-configuration/SKILL.md)
- [gitops-multi-cluster-management](../gitops-multi-cluster-management/SKILL.md)
- [argo-rollouts-progressive-delivery](../argo-rollouts-progressive-delivery/SKILL.md)
- [environment-promotion-strategy](../../../devops/skills/environment-promotion-strategy/SKILL.md)

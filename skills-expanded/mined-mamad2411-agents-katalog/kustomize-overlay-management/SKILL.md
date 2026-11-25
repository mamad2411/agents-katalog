---
name: kustomize-overlay-management
description: >
  Guides structuring Kustomize bases and environment overlays, writing
  strategic-merge and JSON6902 patches, using generators (ConfigMap/Secret
  with hash suffixes, image/replica transformers), and deciding when to
  use Kustomize vs. Helm vs. both together. Use when a user asks to
  "set up a Kustomize base and overlays," "patch a Deployment for
  staging vs. prod," "avoid duplicating YAML across environments,"
  "generate a ConfigMap with kustomize," or "should I use Helm or
  Kustomize."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Kustomize Overlay Management

## Purpose

Kustomize solves the "same app, different environment" problem without a
templating language: a `base` holds the common, plain-YAML manifests, and
per-environment `overlays` apply structural patches (not string
substitution) on top. Done well, this eliminates copy-pasted,
drift-prone per-environment YAML trees. Done poorly — patches that
target the wrong resource, generators whose hash suffixes break
references, bases that aren't actually environment-agnostic — it
produces the same drift problem it was meant to solve, just spread
across more files. This skill covers structuring bases/overlays
correctly and knowing when Kustomize is the right tool versus Helm.

## When to use

- Structuring a repo so `base/` manifests are shared and
  `overlays/{dev,staging,prod}/` hold only the environment-specific
  differences.
- Writing a strategic-merge patch or JSON6902 patch to change a
  Deployment's replica count, resource limits, or env vars per
  environment without duplicating the whole manifest.
- Generating ConfigMaps/Secrets from files or literals with an automatic
  content-hash suffix so pods roll on config change.
- Overriding container image tags per environment
  (`images:` transformer) without touching the base Deployment YAML.
- Deciding whether a given repo/team should use Kustomize, Helm, or
  Kustomize-post-processing a Helm chart's rendered output.
- Debugging `kubectl apply -k` output that doesn't match what was
  expected from the overlay.

## Prerequisites & environment

- Kustomize is built into `kubectl` (`kubectl kustomize` / `kubectl apply -k`)
  since `kubectl` 1.14, but the bundled version often lags the standalone
  `kustomize` CLI — for current features (e.g. `replacements`,
  `components`), install the standalone binary (`kustomize` ≥ 5.0) and
  use `kustomize build | kubectl apply -f -` in CI rather than relying on
  `kubectl`'s embedded version.
- `kustomize edit` subcommands (`kustomize edit set image`, `kustomize
  edit set replicas`) for scripting overlay changes without hand-editing
  YAML — useful in CI to set an image tag from a build pipeline.
- A repo layout convention agreed with the team (`base/` +
  `overlays/<env>/` is the most common; `components/` for optional,
  mixable feature patches introduced in Kustomize v3+).
- If GitOps-managed (Argo CD, Flux), confirm the controller's supported
  Kustomize version — Argo CD bundles its own kustomize binary version
  per release and can lag behind the latest CLI features.

## Step-by-step guidance

1. **Structure the repo** with a clear base/overlay split:
   ```
   k8s/
   ├── base/
   │   ├── kustomization.yaml
   │   ├── deployment.yaml
   │   ├── service.yaml
   │   └── configmap.yaml
   └── overlays/
       ├── dev/
       │   ├── kustomization.yaml
       │   └── patch-replicas.yaml
       ├── staging/
       │   └── kustomization.yaml
       └── prod/
           ├── kustomization.yaml
           ├── patch-resources.yaml
           └── patch-replicas.yaml
   ```

2. **Write the base as a fully valid, environment-agnostic manifest set**
   — it should be deployable on its own with sane (usually minimal/dev-
   like) defaults:
   ```yaml
   # base/kustomization.yaml
   apiVersion: kustomize.config.k8s.io/v1beta1
   kind: Kustomization
   resources:
     - deployment.yaml
     - service.yaml
     - configmap.yaml
   commonLabels:
     app.kubernetes.io/name: payments-api
   ```

3. **Reference the base from each overlay** and layer patches/generators
   on top:
   ```yaml
   # overlays/prod/kustomization.yaml
   apiVersion: kustomize.config.k8s.io/v1beta1
   kind: Kustomization
   namespace: payments-prod
   resources:
     - ../../base
   patches:
     - path: patch-replicas.yaml
       target: { kind: Deployment, name: payments-api }
     - path: patch-resources.yaml
       target: { kind: Deployment, name: payments-api }
   images:
     - name: ghcr.io/example/payments-api
       newTag: "1.4.2"
   ```

4. **Prefer strategic-merge patches for structural changes**, JSON6902
   for precise/positional changes (e.g. removing an array element or
   patching a field strategic-merge can't target unambiguously):
   ```yaml
   # overlays/prod/patch-replicas.yaml (strategic merge)
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: payments-api
   spec:
     replicas: 6
   ```
   ```yaml
   # JSON6902 example: remove a debug env var only in prod
   - op: remove
     path: /spec/template/spec/containers/0/env/2
   ```
   JSON6902 patches are positional — a base change that reorders the
   `env` array silently breaks the patch without an error. Prefer
   strategic-merge or named-key patches wherever the field allows it.

5. **Use generators instead of hand-maintained ConfigMaps/Secrets** so
   content changes automatically produce a new resource name (forcing a
   pod roll) rather than silently patching a Secret in place:
   ```yaml
   configMapGenerator:
     - name: payments-api-config
       literals:
         - LOG_LEVEL=info
       files:
         - config/app.yaml
   ```
   Kustomize appends a content hash to the generated name
   (`payments-api-config-8f7d6c4b2a`) and automatically updates every
   reference to that ConfigMap in the rendered output — do not hardcode
   the generated name elsewhere.

6. **Use `components/` for optional, mixable capability** (e.g. a
   "debug logging" or "canary" component an overlay can opt into)
   instead of duplicating an entire overlay for one toggle:
   ```yaml
   # components/debug-logging/kustomization.yaml
   apiVersion: kustomize.config.k8s.io/v1alpha1
   kind: Component
   patches:
     - path: patch-loglevel.yaml
   ```
   ```yaml
   # overlays/staging/kustomization.yaml
   components:
     - ../../components/debug-logging
   ```

7. **Render and diff before applying**:
   ```bash
   kustomize build overlays/prod > /tmp/rendered-prod.yaml
   kubectl diff -k overlays/prod
   kubectl apply -k overlays/prod
   ```
   `kubectl diff` against the live cluster is the single most valuable
   step before applying to a shared environment — it surfaces drift
   introduced by manual `kubectl edit`s as well as overlay mistakes.

8. **Decide Kustomize vs. Helm vs. both**:
   - Pure Kustomize: best when there is no need to distribute the
     manifests to third parties, values are structural (patches) not
     deeply parameterized, and the team wants to avoid a templating
     language.
   - Pure Helm: best when packaging for reuse/distribution (a chart
     others `helm install`), when non-YAML-shaped parameterization is
     needed (loops, conditionals across many values), or when a
     version/release model (`helm history`, `helm rollback`) is wanted.
     See [helm-chart-authoring](../helm-chart-authoring/SKILL.md).
   - Both: run `helm template` to render a vendor chart, then feed the
     output through Kustomize as a resource to apply organization-
     specific patches the chart's values don't expose:
     ```yaml
     # overlays/prod/kustomization.yaml
     resources:
       - rendered-chart.yaml   # output of: helm template ... > rendered-chart.yaml
     patches:
       - path: patch-extra-annotation.yaml
     ```
     Kustomize's native `helmCharts:` field can also invoke `helm
     template` inline during `kustomize build`, avoiding a separate
     render step, at the cost of requiring `helm` on the build machine
     and `--enable-helm` on older Kustomize versions.

## Best practices

- Keep the base deployable and testable in isolation
  (`kustomize build base | kubectl apply --dry-run=server -f -`); if it
  only works after an overlay patch, it isn't a real base.
- Name overlays after environments/purposes, not after teams — overlays
  should track deployment targets, and ownership belongs in CODEOWNERS,
  not directory names.
- Set `namePrefix`/`nameSuffix` or `namespace` at the overlay level, not
  the base, so the base stays reusable across namespaces/clusters.
- Commit the rendered output of `kustomize build` for at least the prod
  overlay in CI as a diffable artifact/PR comment — reviewers approving
  a patch YAML rarely trace through what it produces by eye.
- Avoid patching the same field from two different patch files in one
  overlay; last-applied-wins ordering is easy to get backwards and hard
  to spot in review. Consolidate into one patch per target resource.
- Treat `commonLabels`/`commonAnnotations` changes as blast-radius-wide —
  they rewrite every matching resource's labels, which can break
  selectors on Services/NetworkPolicies if applied inconsistently across
  base and overlay.

## Common pitfalls

- **Symptom:** `kustomize build` succeeds, but the applied Service no
  longer selects any Pods after adding a `commonLabels` entry to an
  overlay.
  **Fix:** `commonLabels` rewrites both the resource's labels *and*
  matching `spec.selector` fields where Kustomize recognizes the
  reference (e.g. Deployment `matchLabels`), but hand-written Service
  `selector` blocks written as fixed maps rather than templated may not
  get the same rewrite in every Kustomize version — inspect the
  rendered output (`kustomize build`) and confirm selectors match labels
  exactly rather than trusting it silently worked.

- **Symptom:** A ConfigMap/Secret generated via `configMapGenerator`
  still references its content by a name that no longer exists after a
  config change ("configmap not found").
  **Fix:** Something outside the Kustomize-managed resource tree
  (a manually written manifest, a script, or a Helm chart in a `both`
  setup) is referencing the ConfigMap by its unsuffixed base name
  instead of going through Kustomize's reference rewriting. Only
  resources listed in the same `kustomization.yaml` tree get their
  references automatically updated to the hashed name.

- **Symptom:** A JSON6902 patch that removed an env var worked last
  release but now errors with "index out of range" or silently patches
  the wrong element.
  **Fix:** JSON6902 array operations are positional. A base-level change
  that added/reordered/removed an earlier array element shifts every
  later index. Switch to a strategic-merge patch keyed by `name` for
  named array elements (env vars, containers, volumes) instead of a
  positional path wherever the resource kind supports it.

- **Symptom:** `kubectl apply -k` behaves differently in CI than on a
  developer's laptop for the same overlay.
  **Fix:** `kubectl`'s embedded Kustomize version is pinned to that
  `kubectl` release and commonly lags the standalone `kustomize` CLI by
  several minor versions, so newer fields (`replacements`, `components`)
  silently no-op or error under the old built-in version. Standardize on
  a pinned standalone `kustomize` binary version in both CI and local
  tooling (`kustomize build | kubectl apply -f -`) rather than `kubectl
  apply -k`.

## Worked example

**Scenario:** `payments-api` needs three environments differing only in
replica count, resource limits, image tag, and (in prod only) an
Ingress host — everything else is identical.

```
k8s/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   └── service.yaml
└── overlays/
    ├── dev/kustomization.yaml
    ├── staging/kustomization.yaml
    └── prod/
        ├── kustomization.yaml
        ├── patch-replicas.yaml
        ├── patch-resources.yaml
        └── ingress.yaml
```

```yaml
# overlays/prod/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: payments-prod
resources:
  - ../../base
  - ingress.yaml
patches:
  - path: patch-replicas.yaml
    target: { kind: Deployment, name: payments-api }
  - path: patch-resources.yaml
    target: { kind: Deployment, name: payments-api }
images:
  - name: ghcr.io/example/payments-api
    newTag: "1.4.2"
configMapGenerator:
  - name: payments-api-config
    behavior: merge
    literals:
      - LOG_LEVEL=warn
```

```bash
kustomize build overlays/prod | kubectl apply --dry-run=server -f -
kubectl diff -k overlays/prod
kubectl apply -k overlays/prod
```

The rendered output shows the base Deployment with `replicas: 6`,
prod-sized resource limits, the pinned image tag, a merged (not
replaced) generated ConfigMap, and the prod-only Ingress — all without a
single duplicated line of the base manifest.

## Cross-references

- [helm-chart-authoring](../helm-chart-authoring/SKILL.md) — when to package as a distributable Helm chart instead of (or alongside) Kustomize overlays.
- [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md) — the Ingress resource and annotations patched per-overlay in the worked example above.

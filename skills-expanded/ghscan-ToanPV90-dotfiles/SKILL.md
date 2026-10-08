---
name: kustomize-generator
description: Use when creating, scaffolding, or generating Kustomize base/overlay directory structures, kustomization.yaml files, patches, configmap/secret generators, or converting raw Kubernetes manifests into a Kustomize-managed layout.
---

# Kustomize Generator

## Overview

Generate production-ready Kustomize configurations with deterministic base/overlay layouts, strategic merge patches, JSON patches, configmap generators, and environment-specific overlays. Built for `kubectl kustomize` (v1.14+) and standalone `kustomize` CLI.

## When to Use This Skill

| Use kustomize-generator | Use OTHER skill |
|-------------------------|-----------------|
| Scaffold a new base + overlay structure | **kustomize-validator**: Validate/lint existing Kustomize configs |
| Convert raw K8s manifests to Kustomize | **k8s-yaml-generator**: Raw K8s YAML (no Kustomize) |
| Add a new environment overlay | **helm-generator**: Helm charts (template-based parameterization) |
| Create configmap/secret generators | **k8s-yaml-validator**: Validate individual K8s manifests |

## Execution Flow

Follow these stages in order. Do not skip required stages.

### Stage 1: Gather Requirements (Required)

Collect:

- Resources: which K8s manifests to manage (Deployment, Service, ConfigMap, etc.)
- Environments: which overlays to create (e.g., `dev`, `staging`, `prod`)
- Patches: what differs per environment (replicas, image tags, resource limits, config values)
- ConfigMaps / Secrets: whether to generate from files or literals
- Namespace: whether to set per-overlay or in base
- Labels/annotations: common labels to add across all resources

Do not silently assume environment names or patch targets.

| Missing Information | Question to Ask |
|---------------------|-----------------|
| Target environments | "Which environments do you need overlays for? (e.g., dev, staging, prod)" |
| Image tag strategy | "Should image tags be patched per overlay, or managed via a separate tool like Flux?" |
| Replica differences | "Do replica counts differ per environment?" |
| Config values | "Are there config values (env vars, flags) that differ per environment?" |
| Namespace strategy | "Should each overlay deploy to a different namespace?" |

### Stage 2: Scaffold Directory Structure (Required)

Use this canonical layout:

```text
<app-name>/
├── base/
│   ├── kustomization.yaml      # Base kustomization: lists all resources
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml          # Base config (non-sensitive values)
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml  # Extends base; applies dev patches
    │   └── patch-replicas.yaml
    ├── staging/
    │   ├── kustomization.yaml
    │   └── patch-resources.yaml
    └── prod/
        ├── kustomization.yaml
        ├── patch-replicas.yaml
        └── patch-resources.yaml
```

For simpler setups with a single overlay, the base directory can be omitted and resources placed directly at the root.

### Stage 3: Write Base kustomization.yaml (Required)

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

commonLabels:
  app.kubernetes.io/managed-by: kustomize
  app.kubernetes.io/name: <app-name>

resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml
```

Rules:

- Always include `apiVersion` and `kind` — required since kustomize v4
- List resources in dependency order (ConfigMap before Deployment)
- Use `commonLabels` for standard K8s labels; prefer `labels.includeSelectors: false` if adding labels to existing resources without changing selectors

### Stage 4: Write Overlay kustomization.yaml (Required for each overlay)

```yaml
# overlays/prod/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: <app>-prod

bases:                         # deprecated syntax — use 'resources' instead
resources:
  - ../../base

namePrefix: prod-              # optional: prefix all resource names

patches:
  - path: patch-replicas.yaml
    target:
      kind: Deployment
      name: <app-name>
  - path: patch-resources.yaml
    target:
      kind: Deployment
      name: <app-name>

images:
  - name: <image-repo>/<app>
    newTag: "1.2.3"
```

Use `resources:` not the deprecated `bases:` key.

### Stage 5: Write Patches (Required when environments differ)

**Strategic merge patch** (for simple field overrides):

```yaml
# patch-replicas.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: <app-name>
spec:
  replicas: 3
```

**JSON 6902 patch** (for precise array operations or path-level control):

```yaml
# patch-resources.yaml — JSON 6902 patch format
- op: replace
  path: /spec/template/spec/containers/0/resources/limits/memory
  value: "2Gi"
- op: replace
  path: /spec/template/spec/containers/0/resources/requests/memory
  value: "1Gi"
```

Use strategic merge patches for most cases. Use JSON 6902 patches when targeting specific array indices or when the strategic merge behavior is ambiguous.

### Stage 6: ConfigMap and Secret Generators (When applicable)

```yaml
# In kustomization.yaml
configMapGenerator:
  - name: app-config
    literals:
      - LOG_LEVEL=info
      - MAX_CONNECTIONS=100
    options:
      disableNameSuffixHash: true   # set to true if other resources reference this configmap by name

secretGenerator:
  - name: app-secrets
    envs:
      - secrets.env                 # .env file with KEY=VALUE; never commit this file
    options:
      disableNameSuffixHash: true
```

Rules for generators:
- By default kustomize appends a content hash suffix to generated names (e.g., `app-config-k8t5m7g3f6`). Set `disableNameSuffixHash: true` only when Deployments reference the ConfigMap by a fixed name.
- Secret generator source files must be listed in `.gitignore`.

### Stage 7: Validate

Preferred path: run the `kustomize-validator` skill.

If skill invocation is unavailable, run locally:

```bash
kustomize build overlays/<env>
# or
kubectl kustomize overlays/<env>
```

Re-run after any fixes.

## Common Mistakes

- **Using `bases:` instead of `resources:`** — `bases:` is deprecated since kustomize v4; always use `resources:` to reference parent bases
- **Missing `apiVersion` and `kind` in kustomization.yaml** — required since kustomize v4; omitting them produces a warning and may fail in strict mode
- **Forgetting `disableNameSuffixHash: true`** — when a Deployment references a ConfigMap by fixed name, the auto-generated hash suffix breaks the reference; add this option or use `envFrom` with a generated name
- **Committing secret source files** — `.env` files used as `secretGenerator` inputs must be in `.gitignore`
- **Strategic merge patch on array fields** — strategic merge on container arrays replaces by `name`; if the container name does not match exactly, the patch creates a new container instead of modifying the existing one
- **Applying JSON 6902 patches to non-existent paths** — the patch will error; verify the exact path in the base resource first with `kustomize build base`

## Scaffold Success Criteria

Mark complete only when all checks pass:

- [ ] `base/kustomization.yaml` has `apiVersion`, `kind`, and lists all resources
- [ ] Each overlay has its own `kustomization.yaml` referencing `../../base` via `resources:`
- [ ] All patches reference resources by correct `kind` and `name`
- [ ] ConfigMap/Secret generator source files are listed in `.gitignore`
- [ ] `kustomize build overlays/<env>` exits 0 for each overlay
- [ ] Rendered output validated (via `kustomize-validator` or `kubeconform` directly)

## Integration with kustomize-validator

After generating the configuration, invoke `kustomize-validator` and close the loop:

1. Generate base + overlays
2. Run `kustomize-validator` (or `kustomize build` fallback)
3. Fix identified issues
4. Re-validate until passing

---
name: helm-procedures
description: Use this skill when the agent is authoring or running a Helm upgrade, previewing chart changes with helm diff, rolling back a release, inspecting release history, or managing values files for a Helm chart — for Helm procedures covering helm diff (via helm-diff plugin), atomic upgrade with --atomic and --wait, helm install / upgrade / rollback, release history, and values-file conventions. Loaded by `/infra-change` and other Kubernetes deployment workflows; not a workflow itself.
disable-model-invocation: true
---

# Helm Procedures — diff, atomic upgrade, rollback

Knowledge reference for Helm operations used by infrastructure-change workflows. Covers chart linting, diff preview via the `helm-diff` plugin, the safe upgrade pattern (`--atomic` + `--wait`), rollback, and inspection of release state.

## Inspect current release state

```
helm list -n <namespace>
helm get values <release-name> -n <namespace>
helm history <release-name> -n <namespace>
```

Record current image tags, replica counts, and values-file diffs as the rollback baseline before any upgrade.

## Lint the chart

Before any diff or upgrade, lint:

```
helm lint <chart-path>
```

Lint failures should block the workflow.

## Diff preview — helm-diff plugin

The `helm-diff` plugin is the recommended tool for previewing chart changes before upgrade. Install once:

```
helm plugin install https://github.com/databus23/helm-diff
```

Then preview:

```
helm diff upgrade <release> <chart-path> -n <namespace> -f <values-file>
```

### Diff summary format

When presenting a diff for review, summarise as:

```
## Helm Diff Summary
| Object | Action | Key Changes |
|--------|--------|-------------|
| Deployment/X | changed | replicas: 1->2, image: v1->v2 |
| Service/Y | added | port 8080 |
| Secret/Z | changed | keys modified |

WARNING — Critical changes:
- [deployment restart expected]
- [secret reference changed]

Downtime risk: [yes/no]
```

## Atomic upgrade — the safe default

```
helm upgrade <release> <chart-path> -n <namespace> -f <values-file> \
  --atomic --timeout 5m --wait
```

Flag rationale:

- `--atomic` — auto-rolls back on failure (recommended for production). If any resource fails to reach Ready within `--timeout`, Helm reverts the entire release to the prior revision.
- `--timeout 5m` — should match the application's readiness-probe budget, with headroom for image pull and init containers. Tune per environment.
- `--wait` — blocks until all resources reach Ready. Without `--wait`, the upgrade command returns immediately after the API server accepts the manifests, hiding rollout failures from the operator.

### Install vs upgrade

```
helm install <release> <chart-path> -n <namespace> -f <values-file> \
  --atomic --timeout 5m --wait
```

For idempotent flows, prefer `helm upgrade --install` which installs if missing and upgrades if present.

## Rollback

```
helm rollback <release> <previous-revision> -n <namespace>
```

Use `helm history` to find the target revision number. Rollback creates a new revision (it does not delete the failed one), so the release history grows monotonically.

For releases deployed with `--atomic`, an automatic rollback already executed on failure — manual rollback is needed only for issues detected after the upgrade reports success.

## Values-file conventions

Common values-file layouts:

- `values.yaml` — chart defaults, checked into the chart repo
- `values-<env>.yaml` (e.g., `values-prod.yaml`, `values-staging.yaml`) — per-environment overrides
- `values-secrets.yaml` — encrypted with SOPS or sealed-secrets, never committed in plaintext

Pass multiple values files in precedence order (later wins):

```
helm upgrade <release> <chart-path> -n <namespace> \
  -f values.yaml -f values-prod.yaml -f values-secrets.yaml \
  --atomic --timeout 5m --wait
```

## When this applies

| Phase | Apply this knowledge |
|---|---|
| Step 3 — Review current state | `helm list`, `helm get values`, `helm history` |
| Step 4 — Implement | Modify `values.yaml` / templates; `helm lint <chart-path>` |
| Step 5 — Plan review | `helm diff upgrade` and diff-summary format |
| Step 6 — Apply | `helm upgrade ... --atomic --timeout 5m --wait` |
| Step 8 — Rollback | `helm rollback <release> <revision>` |

## Integration

- **Used by**: `/infra-change` (Steps 3, 4, 5, 6, 8 — Helm release lifecycle), `/deploy-production`, `/deploy-staging` (when charts are the deploy unit)
- **Companion knowledge**: `@deployment-procedures` (rolling/canary/blue-green strategy choice), `@gitops-detection` (Argo CD / Flux own the apply gate when GitOps is in use)
- **External references**: [Helm docs](https://helm.sh/docs/), [helm-diff plugin](https://github.com/databus23/helm-diff), [Helm upgrade flags](https://helm.sh/docs/helm/helm_upgrade/)

---
name: helm-conventions
description: Write safe, reusable Helm charts with secure defaults and consistent values structure.
---

# Helm conventions

Unsafe chart defaults (plaintext secrets, `privileged: true`, missing `required` guards) ship straight to whoever installs the chart, and `helm upgrade --force` can delete data-holding resources mid-upgrade. Gate installs with `helm lint` in CI.

## Chart structure

- Follow standard layout: `Chart.yaml`, `values.yaml`, `templates/`, `templates/_helpers.tpl`.
- Keep `Chart.yaml` version (`version`) and application version (`appVersion`) in sync with releases.
- Document all values in `values.yaml` with comments explaining purpose, type, and defaults.
- Use `templates/_helpers.tpl` for shared labels, selectors, and name helpers — never duplicate them across templates.

## Values safety

- All `values.yaml` defaults must be safe for production: no empty passwords, no `IfNotPresent` with floating tags, no `privileged: true`.
- Use `required "message"` in templates for values that have no safe default and must be set explicitly.
- Use `.Values.global` for values shared across subcharts.
- Never put secrets in `values.yaml`; reference external secret managers or use `existingSecret` pattern.

## Template patterns

- Use `toYaml | nindent N` for rendering nested config blocks.
- Guard all optional blocks with `if .Values.feature.enabled`.
- Annotate all managed resources with `helm.sh/resource-policy: keep` when they hold data (PVCs, Secrets).
- Use `helm.sh/chart` and `app.kubernetes.io/managed-by: Helm` labels in `_helpers.tpl`.

## Release discipline

- Lint with `helm lint` before every install or upgrade.
- Diff with `helm diff upgrade` (plugin) before applying to production.
- Never use `helm upgrade --force`; it deletes and recreates the resource.
- Set `atomic: true` and `cleanup-on-fail: true` for production installs.
- Pin chart dependencies in `Chart.lock`; run `helm dependency update` after adding dependencies.

## Examples

```yaml
# BAD — values.yaml: privileged default, secret in plain text, no required guard
replicaCount: 1
securityContext:
  privileged: true
database:
  password: "supersecret"

# GOOD — safe defaults, required guard for mandatory values, existingSecret pattern
replicaCount: 1
# securityContext.privileged must never be set to true
securityContext:
  runAsNonRoot: true
  readOnlyRootFilesystem: true
database:
  # Supply via --set or an external secret; never commit a real value
  existingSecret: ""
  existingSecretKey: "password"
```

```yaml
# templates/deployment.yaml — required guard for mandatory value
image:
  repository: {{ required "image.repository is required" .Values.image.repository }}
  tag: {{ .Values.image.tag | quote }}
```

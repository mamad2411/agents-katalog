---
name: helm-chart-authoring
description: Builds Helm charts with a small, documented values file, clean templates and a tested install, upgrade and rollback path.
---

# Helm chart authoring

Design the values first, then the templates. Prove the upgrade path before you call it done.

## Steps

1. Run `helm create` only if there is no chart. Delete the sample files you will not use.
2. Write `values.yaml` for the user: few keys, sensible defaults, a `# --` comment on each, and nested groups such as `image`, `service`, `resources`, `ingress`. Add `values.schema.json` for types and required keys.
3. Keep templates plain. Put names and labels in `_helpers.tpl` and use the standard `app.kubernetes.io/*` labels. Use `include` and `nindent` correctly; avoid logic deeper than two levels of `if`.
4. Use `required` for settings with no safe default, and `toYaml` with `nindent` for passthrough blocks such as `resources`.
5. Add a checksum annotation of ConfigMaps and Secrets to the pod template so config changes roll the pods.
6. Verify:
   - `helm lint --strict`
   - `helm template` with defaults and with each example values file, then check the output with `kubeconform`
   - if a cluster exists (kind or minikube): `helm install`, `helm upgrade` with changed values, `helm rollback`, then `helm test`

## Rules

- Never hardcode namespaces; use `.Release.Namespace`.
- Never put secrets in default values.
- Do not change selector labels after a release; it breaks upgrades.

## Report

Chart layout, the values users should set, and the commands you ran with their results.

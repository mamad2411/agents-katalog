---
name: gateway-pairs-chart-authoring
description: >
  Use when adding features, fixing bugs, or extending the eg-crds or eg-pair
  Helm charts. Covers chart structure, values conventions, template helpers,
  resource ownership model, and the PoC-to-production gap items.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [helm, envoy-gateway, charts, gateway-namespace-mode, rbac]
    related_skills: [gateway-pairs-e2e]
---

# gateway-pairs Chart Authoring

Use this skill when modifying `charts/eg-crds` or `charts/eg-pair`, adding new
Helm values, or closing gaps between the PoC and a production-ready release.

## Repo chart layout

```
charts/
  eg-crds/           -- CRD lifecycle (install once per cluster)
    Chart.yaml
    values.yaml
    templates/
      version-cm.yaml   -- ConfigMap tracking install metadata in kube-system
      NOTES.txt
  eg-pair/           -- one release per controller+dataplane pair
    Chart.yaml
    values.yaml
    templates/
      _helpers.tpl         -- derives names from pair.index
      namespaces.yaml      -- tr-system-{i}, tr-dataplane-{i}
      serviceaccount.yaml  -- envoy-gateway SA in system namespace
      rbac.yaml            -- tokenreviews ClusterRole/Binding + infra-manager Role/Binding
      controller-rbac.yaml -- leader-election Role + cluster-wide gateway-controller ClusterRole
      config.yaml          -- EnvoyGateway ConfigMap (Gateway Namespace mode, watch list)
      deployment.yaml      -- EG controller Deployment
      service.yaml         -- EG xDS + metrics Service
      envoyproxy.yaml      -- EnvoyProxy CR (parametersRef target for GatewayClass)
      gatewayclass.yaml    -- GatewayClass tr-{i}
      gateway.yaml         -- Gateway with allowedRoutes
      NOTES.txt
```

## Name derivation (_helpers.tpl)

All resource names derive from `pair.index`. Never hardcode pair-specific names
in templates; always call the helper:

```
{{ include "eg-pair.systemNamespace" . }}    -> tr-system-{i}
{{ include "eg-pair.dataplaneNamespace" . }} -> tr-dataplane-{i}
{{ include "eg-pair.gatewayClassName" . }}   -> tr-{i}
{{ include "eg-pair.prefix" . }}             -> eg-pair-{i}  (for cluster-scoped names)
```

## Resource ownership model

Each `helm uninstall eg-pair-{i}` must cleanly remove ALL resources the chart
created, including cluster-scoped ones (Namespaces, GatewayClass, ClusterRole,
ClusterRoleBinding). Helm tracks these in the release secret in the system
namespace. This works correctly as long as cluster-scoped resources are created
by the chart (not by a pre-install Job or out-of-band script).

Do NOT create cluster-scoped resources outside the chart templates. If a
pre-install Job is needed (for CRD checks etc.), use a `helm.sh/hook: pre-install`
Job that only reads, never writes.

## eg-crds chart: PoC gap

The current eg-crds chart only drops a tracking ConfigMap. CRD bytes are applied
by `hack/install-crds.sh` outside the Helm lifecycle. This is intentional for the
PoC (avoids the 1 MB annotation limit).

To close the gap for production:
1. Add a `helm.sh/hook: pre-install,pre-upgrade` Job that runs
   `kubectl apply --server-side -f <crd-url>` inside the cluster.
2. OR depend on `oci://docker.io/envoyproxy/gateway-crds-helm` as a subchart
   and set `gateway-crds-helm.crds.gatewayAPI.enabled` from the parent values.
   Note: subchart approach still hits the annotation limit if crds are large --
   test before shipping.
3. The `hack/install-crds.sh` approach is the most reliable for raw operations.
   Document which path is used clearly in the chart NOTES.txt.

## eg-pair values conventions

- `pair.index` is an integer. Cast explicitly in templates: `{{ .Values.pair.index | int }}`.
- All derived names use `printf` in the helper, not string concatenation.
- New optional features should default off (`enabled: false`) unless the PoC
  already exercises them.

## Known PoC gaps (next PRs)

These items are not implemented and should be tracked as issues:

1. `watch.mode: NamespaceSelector` path -- the config.yaml template has a
   `{{- fail }}` guard. Implementing it requires a ClusterRole for
   infra-manager (instead of the namespace-scoped Role) because EG needs
   cross-namespace resource management when namespaces are dynamic.

2. `rbac.sharedTokenreviewsClusterRole` -- the values key exists but the
   ClusterRole template only creates a per-pair ClusterRole. Add:
   ```
   {{- if not .Values.rbac.sharedTokenreviewsClusterRole }}
   ... create ClusterRole ...
   {{- end }}
   ```
   The ClusterRoleBinding already references the shared name when set.

3. EG controller RBAC completeness -- `controller-rbac.yaml` mirrors the
   upstream `gateway-helm` shape but may be missing resources as EG evolves.
   When upgrading EG version, diff against the upstream chart's ClusterRole
   and add any missing resource/verb pairs.

4. Test07 assertion fragility -- the dataplane proxy label selector
   (`eg-pair={i},eg-role=dataplane`) relies on `EnvoyProxy.spec.provider
   .kubernetes.envoyDeployment.pod.labels` flowing through to the generated
   Deployment. Verify this with EG v1.8 before trusting the assertion;
   if EG does not propagate arbitrary labels, switch to watching for any
   Deployment in the dataplane namespace instead.

5. Multi-pair shared ClusterRole cleanup -- when N pairs all create their own
   `eg-pair-{i}-gateway-controller` ClusterRole with identical rules, this is
   wasteful. Consider a single shared ClusterRole created by eg-crds (which
   already installs once) and per-pair ClusterRoleBindings only.

## RBAC shape reference

infra-manager Role (in tr-dataplane-{i}):
- `""` / serviceaccounts, services, configmaps: create get list watch delete deletecollection patch update
- `apps` / deployments, daemonsets: same
- `autoscaling` / horizontalpodautoscalers: same
- `policy` / poddisruptionbudgets: same
- `certificates.k8s.io` / clustertrustbundles: get list watch

tokenreviews ClusterRole:
- `authentication.k8s.io` / tokenreviews: create

gateway-controller ClusterRole (cluster-wide Gateway API watch + status update):
- `gateway.networking.k8s.io` / gatewayclasses,gateways,httproutes,...: get list watch
- `gateway.networking.k8s.io` / */status: update patch
- `gateway.envoyproxy.io` / *: get list watch update patch
- `""` / secrets,configmaps,namespaces,services,serviceaccounts,endpoints,nodes: get list watch
- `apps` / deployments,daemonsets: get list watch
- `discovery.k8s.io` / endpointslices: get list watch
- `autoscaling` / horizontalpodautoscalers: get list watch
- `policy` / poddisruptionbudgets: get list watch

If a controller starts with RBAC errors, compare against the upstream
`gateway-helm` ClusterRole. EG may have added new resources in newer versions.

## allowedRoutes selector

The Gateway listener uses `kubernetes.io/metadata.name` which Kubernetes sets
automatically on every namespace. The chart derives the value from
`eg-pair.dataplaneNamespace`:

```yaml
selector:
  matchLabels:
    kubernetes.io/metadata.name: {{ include "eg-pair.dataplaneNamespace" . }}
```

This is the correct pattern. Do NOT add a separate label to the dataplane
namespace for this purpose -- the built-in label is sufficient and immutable.

## Adding a new listener protocol

Edit `charts/eg-pair/values.yaml` `gateway.listeners` and the `gateway.yaml`
template's `allowedRoutes` block. Each listener gets its own `allowedRoutes`
pointing at the same dataplane namespace. The template range already handles
multiple listeners; only add `allowedRoutes` fields inside the range if they
differ per listener. For the common case (all listeners allow the dataplane NS),
the current structure is correct.

## Helm lint

```bash
make helm-lint
```

Both charts must lint clean (0 failures) before any commit. INFO lines about
missing icons are acceptable.

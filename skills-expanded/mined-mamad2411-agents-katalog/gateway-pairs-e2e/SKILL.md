---
name: gateway-pairs-e2e
description: >
  Use when running, debugging, or extending the gateway-pairs k3d e2e suite.
  Covers cluster lifecycle, CRD install strategy, chart install order, pair
  isolation verification, and the full debug sequence for Gateway Namespace mode.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [envoy-gateway, k3d, helm, e2e, gateway-namespace-mode, gateway-api]
    related_skills: [gateway-pairs-chart-authoring]
---

# gateway-pairs E2E

Use this skill when running or debugging integration tests in the
`gateway-pairs` repo. It covers everything from cluster creation to Gateway
Programmed status verification.

All e2e work must happen outside any sandbox. kubectl, helm, k3d, Docker, and
`go test -tags=e2e` commands all require a real container runtime and kubeconfig.

## Shape of the suite

The harness lives in `e2e/` as a testify/suite gated behind `//go:build e2e`.
Entry point: `TestGatewayPairs` in `e2e/pairs_test.go`.
Base suite (lifecycle + helpers): `e2e/suite_test.go`.

Tests run in order -- testify/suite methods are sorted by name, so the numeric
prefix 01-07 is intentional. Do not rename them without adjusting the sequence.

| Test | What it proves |
|---|---|
| 01_InstallCRDs | Gateway API + EG CRDs present after `hack/install-crds.sh` |
| 02_InstallPair1 | `eg-pair-1` Helm release healthy, controller Deployment Available |
| 03_InstallPair2 | `eg-pair-2` Helm release healthy, controller Deployment Available |
| 04_VerifyIsolation | Each controller has its own replica; no cross-pair bleed |
| 05_VerifyGatewayClasses | GatewayClass tr-1 and tr-2 both Accepted |
| 06_VerifyGateways | Gateway eg in each system namespace reaches Programmed=True |
| 07_VerifyDataplaneProxies | Envoy proxy Deployment available in each dataplane namespace |

## k3d cluster

```
k3d cluster create gw-pairs-e2e
  --agents 0
  --image rancher/k3s:v1.32.2-k3s1
  --k3s-arg --disable=traefik@server:*
  --k3s-arg --kubelet-arg=allowed-unsafe-sysctls=net.ipv4.ip_unprivileged_port_start@server:*
```

Always pin kubectl and helm commands to the k3d context:

```
kubectl --context k3d-gw-pairs-e2e ...
helm --kube-context k3d-gw-pairs-e2e ...
```

The Go helpers in `suite_test.go` enforce this. Reuse the pattern in any
new test helpers you add.

## CRD install (critical path)

Never install CRDs with plain `helm install` -- Helm's 1 MB release secret
limit breaks on large CRD bundles. The correct path:

```bash
# auto-detects provider-managed Gateway API and skips those CRDs
KTX=k3d-gw-pairs-e2e EG_VERSION=v1.8.0 ./hack/install-crds.sh
```

The script uses `gateway-crds-helm` for both Gateway API and EG CRDs.
Do NOT pin `GATEWAY_API_VERSION` separately -- `gateway-crds-helm` at
`EG_VERSION` ships the exact co-tested pair (EG v1.8.0 -> Gateway API v1.5.1).

Provider-managed detection uses `managedFields[*].manager`, not the
`bundle-version` annotation. `bundle-version` is set by ANY install path
and is not a reliable provider-ownership signal.

Or via Make:

```bash
make crds-install
```

Detection logic in the script: if `gateways.gateway.networking.k8s.io` carries
a `gateway.networking.k8s.io/bundle-version` annotation, the provider manages
it -- skip Gateway API CRDs, install only EG CRDs via `gateway-crds-helm`.

Verify after install:

```bash
kubectl --context k3d-gw-pairs-e2e get crd   gatewayclasses.gateway.networking.k8s.io   gateways.gateway.networking.k8s.io   httproutes.gateway.networking.k8s.io   envoyproxies.gateway.envoyproxy.io   envoypatchpolicies.gateway.envoyproxy.io
```

## Pair install

```bash
make pair-install PAIR=1
make pair-install PAIR=2
```

Equivalent helm command (useful for debugging values):

```bash
helm --kube-context k3d-gw-pairs-e2e upgrade --install eg-pair-1 ./charts/eg-pair   --namespace tr-system-1 --create-namespace   --set pair.index=1   --skip-crds   --wait --timeout 120s
```

Post-install readiness check order:

1. `kubectl rollout status deployment/envoy-gateway -n tr-system-1 --timeout=120s`
2. `kubectl wait deployment/envoy-gateway -n tr-system-1 --for=condition=Available --timeout=120s`
3. Check GatewayClass: `kubectl get gatewayclass tr-1 -o jsonpath='{.status.conditions[?(@.type=="Accepted")].status}'`
4. Check Gateway: `kubectl get gateway eg -n tr-system-1 -o jsonpath='{.status.conditions[?(@.type=="Programmed")].status}'`
5. Check dataplane proxy: `kubectl get deployments -n tr-dataplane-1 -l eg-pair=1,eg-role=dataplane`

## Run the full e2e suite

```bash
# suite handles cluster create + CRD install + pair install + teardown
make e2e

# keep cluster after run for debugging
KEEP_CLUSTER=1 make e2e

# reuse an already-running cluster (skip cluster create)
REUSE_CLUSTER=1 make e2e
```

Direct go test form:

```bash
cd e2e
RUN_PAIRS_E2E=1 go test -v -count=1 -tags=e2e -run TestGatewayPairs ./...
```

Always use `-count=1`. Cached test results skip the real cluster run.

## Watch list rule -- most common failure

The EnvoyGateway config must list BOTH namespaces in the watch list.
Omitting the system namespace means EG cannot read its own TLS secret.
Symptom: Gateway shows Accepted=True but Programmed=False, EG logs show
certificate errors.

```yaml
watch:
  type: Namespaces
  namespaces:
  - tr-system-1    # MUST be present
  - tr-dataplane-1
```

This is hardcoded correctly in `charts/eg-pair/templates/config.yaml`. If you
see Accepted-but-not-Programmed, verify the ConfigMap in the system namespace:

```bash
kubectl --context k3d-gw-pairs-e2e get configmap envoy-gateway-config   -n tr-system-1 -o jsonpath='{.data.envoy-gateway\.yaml}'
```

## tokenreviews forbidden

Symptom: Envoy proxy pods exist in `tr-dataplane-{i}` but stay unready.
EG logs contain `tokenreviews.authentication.k8s.io is forbidden`.

Fix: the ClusterRole + ClusterRoleBinding for tokenreviews was not created
or does not bind the correct ServiceAccount. Check:

```bash
kubectl --context k3d-gw-pairs-e2e get clusterrolebinding eg-pair-1-tokenreviews   -o jsonpath='{.subjects}'
```

Should reference `serviceAccountName=envoy-gateway, namespace=tr-system-1`.

## allowedRoutes wiring

HTTPRoutes in `tr-dataplane-{i}` attach to the Gateway in `tr-system-{i}` via:

```yaml
# Gateway listener (managed by chart):
allowedRoutes:
  namespaces:
    from: Selector
    selector:
      matchLabels:
        kubernetes.io/metadata.name: tr-dataplane-1

# HTTPRoute (tenant-managed):
parentRefs:
- namespace: tr-system-1
  name: eg
```

`kubernetes.io/metadata.name` is auto-set by Kubernetes. No labeling step needed.
The chart derives the selector from `pair.index` -- do not override it manually.

## Debug sequence

When a test fails after pair install:

1. Check Gateway and HTTPRoute status (`kubectl get gateway,httproute -A`).
2. Check EG controller logs: `kubectl logs -n tr-system-{i} deploy/envoy-gateway`.
3. Check EnvoyProxy and GatewayClass status.
4. Check dataplane namespace for generated resources:
   `kubectl get all -n tr-dataplane-{i}`.
5. If proxy pods exist but unready: check `tokenreviews` ClusterRoleBinding.
6. If Gateway is Accepted but not Programmed: check watch list in ConfigMap.
7. Keep cluster with `KEEP_CLUSTER=1` for interactive debugging.

## Make targets reference

| Target | Effect |
|---|---|
| `make cluster` | Create k3d cluster |
| `make cluster-delete` | Delete k3d cluster |
| `make crds-install` | Install CRDs via `hack/install-crds.sh` |
| `make pair-install PAIR=N` | Install eg-pair-N (default N=1) |
| `make pair-delete PAIR=N` | Uninstall eg-pair-N |
| `make e2e` | Full suite: create cluster, CRDs, pairs, verify, teardown |
| `make helm-lint` | Lint both charts |

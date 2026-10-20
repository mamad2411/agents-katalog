---
name: eg-namespace-pairs
description: >
  Deploy Envoy Gateway as isolated controller+dataplane pairs inside a single
  cluster using Gateway Namespace mode. Covers the two-chart Helm architecture
  (eg-crds + eg-pair), RBAC requirements, CRD conflict strategy, allowedRoutes
  wiring, and k3d e2e harness. Reference implementation: github.com/dio/gateway-pairs.
metadata:
  hermes:
    tags: [envoy-gateway, gateway-namespace-mode, helm, k8s, rbac, multi-tenancy, k3d]
    related_skills: [envoy-gateway-namespace-mode, transit-k3d-envoy-gateway-e2e]
---

# Envoy Gateway Namespace Pairs

## When to load this skill

- Designing or extending the `eg-crds` / `eg-pair` Helm charts
- Deploying EG with `deploy.type: GatewayNamespace` and N controller+dataplane pairs
- Debugging a pair where Gateway is Accepted but not Programmed
- Writing k3d e2e tests for multi-pair infra
- Answering CRD conflict questions (provider-managed Gateway API, channel mismatch)
- Checking whether a pair is already installed (pre-install conflict detection)
- Designing pair identifiers (string id vs numeric index)

## Architecture

One Helm release of `eg-pair` = one isolated pair using **two namespaces**:

```
tr-release-{i}     -- Helm release Secret only; created by --create-namespace
tr-system-{i}      -- everything: EG controller, proxy, Gateway, tenant HTTPRoutes
GatewayClass tr-{i} -- cluster-scoped, points to EnvoyProxy in tr-system-{i}
```

**There is no separate dataplane namespace.** In GatewayNamespace mode EG
places the Envoy proxy in the Gateway's namespace. The Gateway is declared in
`tr-system-{i}`, so the proxy lands there alongside the controller. Tenant
HTTPRoutes also go in `tr-system-{i}` -- the Gateway `allowedRoutes` uses
`from: Same` (no cross-namespace attachment needed).

The `tr-dataplane-{i}` namespace concept was a naming mistake. It implied a
separation that doesn't match GatewayNamespace mode behavior. Do not create it.

The two-namespace split (release + system) is required to avoid Helm ownership
conflicts. Helm creates `tr-release-{i}` via `--create-namespace` without
ownership annotations. If the chart also declares a `Namespace` resource with
the same name as the release namespace, Helm rejects re-installs with:
`invalid ownership metadata; label validation error: missing key "app.kubernetes.io/managed-by"`

Resource ownership by scope:

| Resource | Scope | Owner |
|---|---|---|
| Namespace tr-release-{i} | cluster | Helm --create-namespace |
| Namespace tr-system-{i} | cluster | eg-pair chart (pre-install hook, weight -5) |
| GatewayClass tr-{i} | cluster | eg-pair chart |
| ClusterRole tokenreviews | cluster | eg-pair chart |
| ClusterRoleBinding tokenreviews | cluster | eg-pair chart |
| ClusterRole gateway-controller | cluster | eg-pair chart |
| ClusterRoleBinding gateway-controller | cluster | eg-pair chart |
| EG controller Deployment | tr-system-{i} | eg-pair chart |
| EnvoyGateway ConfigMap | tr-system-{i} | eg-pair chart |
| EnvoyProxy CR | tr-system-{i} | eg-pair chart |
| Gateway | tr-system-{i} | eg-pair chart |
| Role infra-manager | tr-system-{i} | eg-pair chart |
| RoleBinding infra-manager | tr-system-{i} | eg-pair chart |
| Envoy proxy Deployment | tr-system-{i} | EG controller (generated) |
| Envoy proxy Service | tr-system-{i} | EG controller (generated) |
| HTTPRoute | tr-system-{i} | **tenant-managed** |

## Chart split

**`eg-crds`** -- install once per cluster, upgrade carefully.
- Ships `hack/install-crds.sh` for the `helm template | kubectl apply --server-side` CRD install dance (required: Helm 1 MB release-secret limit breaks direct CRD install).
- Only creates a version-tracking ConfigMap via Helm; actual CRD bytes go through the script.
- Values: `crds.gatewayAPI.{enabled,channel}`, `crds.envoyGateway.enabled`.

**`eg-pair`** -- one release per pair, installed into `tr-release-{i}`.
- Single required value: `pair.index`. All names derived via `_helpers.tpl`.
- `--skip-crds` always -- `eg-crds` owns the CRD lifecycle.
- `--create-namespace` creates `tr-release-{i}` (release-tracking namespace only).
- `tr-system-{i}` is created as a **pre-install hook at weight -5** so it exists when the certgen Job (weight -1) runs.
- Values: `pair.{index,namePrefix,nameSuffix}`, `controller.{image,replicas,resources,topologyInjector}`, `watch.mode`, `gateway.{name,listeners}`, `rbac.{tokenreviews,infraManager,sharedTokenreviewsClusterRole}`.

### Flexible naming (namePrefix / nameSuffix)

`_helpers.tpl` derives all names from `pair.namePrefix`, `pair.index`, and `pair.nameSuffix`:
- `namePrefix`: auto-appends `-` if non-empty and not already ending with `-`.
- `nameSuffix`: coerced to string (Helm `--set` passes bare numbers as int64, use `| toString` in templates).
- When `nameSuffix` is empty and `index > 0`: suffix defaults to `-{index}`.
- When `nameSuffix` is empty and `index == 0`: no suffix (single/unnamed pair).

Examples:
```
namePrefix=tr,   index=1, nameSuffix=""   → tr-system-1, tr-1
namePrefix=tr, index=1, nameSuffix=""   → tr-system-1, tr-1
namePrefix=tr, index=0, nameSuffix=""   → tr-system, tr
namePrefix=tr, index=1, nameSuffix=1    → tr-system1, tr1
namePrefix="",   index=1, nameSuffix=""   → system-1
```

## certgen Job (EG v1.8+, REQUIRED)

EG v1.8 requires a TLS cert at `/certs/tls.crt` for its webhook server. Without
it, the controller crashes on startup: `open /certs/tls.crt: no such file or directory`.

The upstream `gateway-helm` chart runs `envoy-gateway certgen` as a pre-install
Job. The `eg-pair` chart must do the same. Key details:

**Hook ordering (critical):** certgen runs as `helm.sh/hook: pre-install,pre-upgrade`
at weight `-1`. The system namespace must exist first -- it is created as a hook
at weight `-5` (lower weight = runs first). Plain chart resources are created
AFTER all hooks complete, so declaring the system namespace as a plain resource
and relying on `--create-namespace` for a different namespace is wrong.

**Topology injector:** certgen also patches a `MutatingWebhookConfiguration`
for the topology injector (pod topology spread). In multi-pair mode this MUST
be disabled: each pair would register a cluster-scoped webhook that watches all
proxy pods cluster-wide, interfering with other pairs' proxies.

```yaml
# In eg-pair values.yaml:
controller:
  topologyInjector: false  # default; disable for all multi-pair deployments
```

```yaml
# certgen container command:
- envoy-gateway
- certgen
{{- if not .Values.controller.topologyInjector }}
- --disable-topology-injector
{{- end }}
```

certgen writes a Secret named `envoy-gateway` into the system namespace.
The controller Deployment mounts it at `/certs`:

```yaml
volumeMounts:
- name: certs
  mountPath: /certs
  readOnly: true
volumes:
- name: certs
  secret:
    secretName: envoy-gateway
```

## RBAC requirements (all required)

### 0. Certgen RBAC (pre-install hooks)

The certgen Job needs a Role in the system namespace (secret create/update)
and a ClusterRole for the MutatingWebhookConfiguration (even when topology
injector is disabled -- certgen still tries to GET it and fails otherwise).
Use `helm.sh/hook-delete-policy: before-hook-creation,hook-succeeded` to
clean up after each run. Namespace SA needs `hook-delete-policy: before-hook-creation`
only (the namespace must persist).

### 1. tokenreviews ClusterRole + ClusterRoleBinding

Gateway Namespace mode uses JWT (not mTLS) for xDS auth. EG validates proxy
JWT tokens via TokenReview. Without this, proxy pods start but stay Unready:
`tokenreviews.authentication.k8s.io is forbidden`.

```yaml
rules:
- apiGroups: ["authentication.k8s.io"]
  resources: ["tokenreviews"]
  verbs: ["create"]
```

For N pairs sharing a cluster: create one shared ClusterRole, one
ClusterRoleBinding per pair. Use `rbac.sharedTokenreviewsClusterRole` value
to bind to an existing role instead of creating a new one.

### 2. infra-manager Role in BOTH system AND dataplane namespaces

EG creates/manages resources in TWO namespaces in GatewayNamespace mode:
- **System namespace:** generates a ServiceAccount (`eg`) for the proxy to use
- **Dataplane namespace (or Gateway's NS):** generates Envoy Deployment, Service, etc.

The infra-manager Role must exist in both. A common mistake is only creating
it in the dataplane namespace -- the controller then fails with:
`serviceaccounts "eg" is forbidden: cannot patch resource "serviceaccounts" in tr-system-1`

The Role rules are identical for both namespaces:

```yaml
rules:
- apiGroups: [""]
  resources: [serviceaccounts, services, configmaps]
  verbs: [create, get, list, watch, delete, deletecollection, patch, update]
- apiGroups: [apps]
  resources: [deployments, daemonsets]
  verbs: [create, get, list, watch, delete, deletecollection, patch, update]
- apiGroups: [autoscaling]
  resources: [horizontalpodautoscalers]
  verbs: [create, get, list, watch, delete, deletecollection, patch, update]
- apiGroups: [policy]
  resources: [poddisruptionbudgets]
  verbs: [create, get, list, watch, delete, deletecollection, patch, update]
- apiGroups: [certificates.k8s.io]
  resources: [clustertrustbundles]
  verbs: [get, list, watch]
```

### 3. gateway-controller ClusterRole + ClusterRoleBinding

Mirror the upstream `gateway-helm` ClusterRole exactly. Missing resources
cause the controller to start but fail to reconcile. Known missing items that
cause health check failures:

- `listenersets` (Gateway API v1.5, shipped with EG v1.8)
- `pods`, `pods/binding` (topology-related watch)
- `serviceaccounts` (cluster-wide watch for proxy SA creation)
- `multicluster.x-k8s.io/serviceimports`
- All `gateway.envoyproxy.io` status subresources

Full ClusterRole rules (verbatim from `gateway-helm v1.8.0`):

```yaml
rules:
- apiGroups: [""]
  resources: [nodes, namespaces]
  verbs: [get, list, watch]
- apiGroups: [""]
  resources: [configmaps, secrets, services, serviceaccounts]
  verbs: [get, list, watch]
- apiGroups: [""]
  resources: [pods, "pods/binding"]
  verbs: [get, list, patch, update, watch]
- apiGroups: [apps]
  resources: [deployments, daemonsets]
  verbs: [get, list, watch]
- apiGroups: [discovery.k8s.io]
  resources: [endpointslices]
  verbs: [get, list, watch]
- apiGroups: [multicluster.x-k8s.io]
  resources: [serviceimports]
  verbs: [get, list, watch]
- apiGroups: [gateway.networking.k8s.io]
  resources: [gatewayclasses]
  verbs: [get, list, patch, update, watch]
- apiGroups: [gateway.networking.k8s.io]
  resources: [gatewayclasses/status]
  verbs: [update]
- apiGroups: [gateway.networking.k8s.io]
  resources: [gateways, listenersets, grpcroutes, httproutes, referencegrants,
              tcproutes, tlsroutes, udproutes, backendtlspolicies]
  verbs: [get, list, watch]
- apiGroups: [gateway.networking.k8s.io]
  resources: [gateways/status, listenersets/status, grpcroutes/status,
              httproutes/status, tcproutes/status, tlsroutes/status,
              udproutes/status, backendtlspolicies/status]
  verbs: [update]
- apiGroups: [gateway.envoyproxy.io]
  resources: [envoyproxies, envoypatchpolicies, clienttrafficpolicies,
              backendtrafficpolicies, securitypolicies, envoyextensionpolicies,
              backends, httproutefilters]
  verbs: [get, list, watch]
- apiGroups: [gateway.envoyproxy.io]
  resources: [envoypatchpolicies/status, clienttrafficpolicies/status,
              backendtrafficpolicies/status, securitypolicies/status,
              envoyextensionpolicies/status, backends/status]
  verbs: [update]
```

**Tip:** when in doubt, diff your ClusterRole against `gateway-helm` output:
```bash
helm template eg oci://docker.io/envoyproxy/gateway-helm \
  --version v1.8.0 --namespace envoy-gateway-system 2>&1 \
  | sed -n '/envoy-gateway-rbac.yaml/,/^---/p'
```

## Watch list

Only `tr-system-{i}` needs to be in the watch list. There is no separate
dataplane namespace to watch:

```yaml
provider:
  kubernetes:
    deploy:
      type: GatewayNamespace
    watch:
      type: Namespaces
      namespaces:
      - tr-system-1     # only namespace needed
```

All EG-managed resources -- controller, proxy, Gateway, HTTPRoutes -- live in
the system namespace. No `tr-dataplane-{i}` exists.

## allowedRoutes wiring

Gateway and HTTPRoutes both live in `tr-system-{i}`. Use `from: Same` -- no
cross-namespace attachment, no selector, no extra labels:

```yaml
listeners:
- name: http
  port: 80
  protocol: HTTP
  allowedRoutes:
    namespaces:
      from: Same
```

HTTPRoute `parentRefs` need only the gateway name (namespace defaults to Same):

```yaml
parentRefs:
- name: eg
```

**Do NOT use `from: Selector` pointing at a separate `tr-dataplane-{i}`.**
There is no dataplane namespace in the current model. The proxy, Gateway, and
tenant resources all share `tr-system-{i}`.

## Provider-managed Gateway API: compatibility check

When a cluster provides its own Gateway API CRDs (GKE, AKS), the skip-or-install
decision is not binary. The provider version may be too old for the EG version
being installed.

**EG v1.8.0 bundled Gateway API: v1.5.1.** A provider at v1.2.x is missing:
- `ListenerSet` (added v1.5) -- EG logs warning, continues
- `.spec.infrastructure` on Gateway (added v1.3) -- EG cannot set infrastructure; hard functional gap
- Several status subresource fields (added v1.3-v1.4) -- EG cannot update status; operators fly blind

**Detection flow for `gwp preflight`:**

1. Check `bundle-version` annotation -- non-empty means installed by someone.
2. Check `managedFields[*].manager` for known provider managers.
3. If provider-managed: compare installed version against the bundled version.
4. Report: required CRDs present/absent, required fields present/absent.
5. Hard block if required fields are missing. Soft warn for optional CRDs.

**`--force-gateway-api-crds` on provider-managed clusters is dangerous.** The
provider's control plane may reconcile CRDs back on the next node pool upgrade
or maintenance window, silently reverting EG to a broken state. Document this
prominently and recommend using a newer provider channel instead (GKE rapid, AKS
preview) rather than fighting the provider.

**CRD conflict strategy (continued from above):

Four scenarios:

| Scenario | Action |
|---|---|
| Fresh k3d cluster | install Gateway API + EG CRDs both via `gateway-crds-helm` |
| Provider-managed (GKE autopilot, AKS, GKE Standard with Gateway API add-on) | skip Gateway API CRDs, install EG CRDs only |
| User-installed Gateway API, unmanaged | server-side apply upgrades cleanly |
| Wrong channel (experimental vs standard) | block: check live objects before downgrade |

**Single version pin rule:** always use `gateway-crds-helm` for BOTH Gateway
API and EG CRDs. Do not pull Gateway API CRDs from a separate
`kubernetes-sigs/gateway-api` release URL -- the versions will drift.
`gateway-crds-helm v1.8.0` ships Gateway API **v1.5.1**, not v1.2.1.

**Provider-managed detection:** use `managedFields[*].manager`, NOT the
`bundle-version` annotation. `bundle-version` is written by any install path
(kubectl, helm, GKE, AKS) and is not a provider-ownership signal.

Known provider manager names:
- `gke-networking-controller`, `gke-gateway-api` -- GKE Standard / Autopilot
- `aks-gateway-api-controller` -- AKS
- `addon-manager` -- GKE addon-manager pattern

```bash
# Is it installed?
kubectl get crd gateways.gateway.networking.k8s.io \
  -o jsonpath='{.metadata.annotations.gateway\.networking\.k8s\.io/bundle-version}' 2>/dev/null
# Empty = not installed. Non-empty = installed by someone (check managedFields next).

# Is it provider-managed?
kubectl get crd gateways.gateway.networking.k8s.io \
  -o jsonpath='{.metadata.managedFields[*].manager}' 2>/dev/null
# Contains a known provider manager = skip Gateway API CRDs.
```

Install script: `hack/install-crds.sh` in `dio/gateway-pairs` implements this
detection. See `references/crd-conflict-strategy.md` for full scenarios and
verify commands. Always use `--server-side` on `kubectl apply` for CRDs.

## Pair identity: string id vs numeric index

The current chart uses `pair.index` (integer) which defaults suffix to `-{index}`.
This works for numbered pairs but breaks down for environment/team/region namespacing.

**Planned evolution:** replace `pair.index` with `pair.id` (string). Numeric ids
(`id: "1"`) continue to work. Arbitrary ids (`id: "prod"`, `id: "team-a"`,
`id: "eu-west"`) become natural. The suffix IS the id -- no auto-hyphen arithmetic.

Until `pair.id` lands, use `pair.nameSuffix` to override: `pair.nameSuffix=prod`
gives `tr-system-prod`, `tr-dataplane-prod`, `tr-prod` (GatewayClass).

Keep `pair.index` as a deprecated alias that sets `pair.id` when `pair.id` is unset.

## Already-installed pre-install check

Before installing a pair, three distinct conflict types must be checked:

**Type 1: Helm release already exists**
```bash
helm --kube-context $KTX status eg-pair-{id} -n {prefix}-release-{id}
```
- `status: deployed` → pair is healthy; use `gwp pair status {id}` to inspect or `gwp pair install {id}` to upgrade
- `status: failed` → previous install failed midway; `helm upgrade --install` recovers
- Not found → safe to install

**Type 2: GatewayClass name conflict without matching Helm release**
`tr-{id}` exists but has no `meta.helm.sh/release-name` annotation pointing at `eg-pair-{id}`.
This is a hard block. Options: choose a different id, delete the orphaned GatewayClass,
or use `gwp pair delete {id} --force-cleanup` to remove stale cluster-scoped resources.

**Type 3: Namespace exists without matching Helm release**
`tr-system-{id}` exists but no release secret in `tr-release-{id}`. Helm refuses
to install: "Namespace exists and cannot be imported into the current release: invalid
ownership metadata". Fix: delete the orphaned namespace, OR annotate it for Helm
ownership before installing:
```bash
kubectl annotate namespace tr-system-{id} \
  meta.helm.sh/release-name=eg-pair-{id} \
  meta.helm.sh/release-namespace=tr-release-{id}
kubectl label namespace tr-system-{id} \
  app.kubernetes.io/managed-by=Helm
```
This is the `--adopt-namespaces` pattern (future CLI flag).

## GatewayClass naming for N pairs

GatewayClass is cluster-scoped. Each pair must have a unique name. Convention:
`tr-{index}`. The `eg-pair` chart derives it from `pair.index`.

Multiple pairs sharing a cluster each get their own GatewayClass, ClusterRoleBinding,
and infra-manager RoleBinding. They share the same `gateway-controller`
ClusterRole (per-pair ClusterRoleBinding bound to each pair's ServiceAccount).

## CRITICAL: unique controllerName per pair

Every EG controller watches all GatewayClasses cluster-wide (they are cluster-scoped).
If multiple EG instances share the same `gateway.controllerName`, each one tries
to reconcile ALL GatewayClasses in the cluster. An instance for pair 1 will try
to find the EnvoyProxy for pair 2's GatewayClass in its own watched namespaces
(`tr-system-1`, `tr-dataplane-1`) and fail:

```
failed to process ParametersRef for GatewayClass
error: "failed to find envoyproxy tr-system-2/eg for GatewayClass tr-2:
unable to get: tr-system-2/eg because of unknown namespace for the cache"
```

This causes GatewayClasses to oscillate between Accepted and Unknown, and
controllers to log constant reconcile failures even when their own pair is healthy.

**Fix: each pair's `controllerName` must be unique:**

```yaml
# EnvoyGateway ConfigMap:
gateway:
  controllerName: gateway.envoyproxy.io/tr-1   # derived from gatewayClassName

# GatewayClass:
spec:
  controllerName: gateway.envoyproxy.io/tr-1   # must match exactly
```

In `_helpers.tpl` the `controllerName` is derived as:
`gateway.envoyproxy.io/{{ include "eg-pair.gatewayClassName" . }}`

Both `config.yaml` (EnvoyGateway ConfigMap) and `gatewayclass.yaml` must use
the same helper so they stay in sync. If they diverge, the GatewayClass will
never be reconciled by any controller.

The upstream `gateway-helm` chart uses a single shared controller name because
it manages only one GatewayClass. The multi-pair architecture requires unique
names -- this is a deliberate divergence from upstream.

## k3d e2e harness shape

See `references/e2e-harness-shape.md` for the full testify/suite pattern.
Key points:
- Build tag `//go:build e2e` gates the suite, gated by env var `RUN_PAIRS_E2E=1`.
- All kubectl/helm calls pinned to `k3d-{cluster}` context; reject non-k3d contexts unless `UNSAFE_CONTEXT=1`.
- Test order: CRD install (via hack/install-crds.sh inside the test) → pair 1,2,3 install → isolation check → GatewayClass Accepted → Gateway Programmed → proxy Deployment ready → delete pair 2 → verify pairs 1+3 unaffected → reinstall pair 2.
- Wait for `deployment/envoy-gateway` rollout with both `rollout status` and `wait --for=condition=Available`, not pod-label waits (stale ReplicaSet pods).
- Gateway Programmed status: use jsonpath range `{range .status.conditions[*]}{.type}={.status} {end}` and `strings.Contains(out, "Programmed=True")`. Filter expressions `?(@.type=='Programmed')` have quoting issues across kubectl versions -- do not use.

**`installPair` must wait for Gateway listener Programmed, not just controller Available.**
Returning as soon as the controller Deployment is Available is not enough. The
GatewayClass may not be Accepted yet, and subsequent tests that assume
Accepted=True will fail. The correct gate is listener-level `Programmed=True`
(use eventually with 5m timeout). Once installPair guarantees this, VerifyGatewayClasses
and VerifyGateways become fast sanity assertions (no polling).

**ClusterIP gateways never show top-level Programmed=True.** EG in GatewayNamespace
mode creates the proxy Service as `ClusterIP` (no external IP). The top-level
`Gateway.status.conditions[type=Programmed]` stays `False` with reason
`AddressNotAssigned` even when xDS is fully wired and routing works. Use the
**listener-level conditions** instead:

```go
// CORRECT: listener-level Programmed
out, err := kubectl("get", "gateway", "eg", "-n", sysNS,
    "-o", "jsonpath={range .status.listeners[*]}{range .conditions[*]}{.type}={.status} {end}{end}")
// contains "Programmed=True" when proxy is connected

// WRONG: top-level for ClusterIP services
out, err := kubectl("get", "gateway", "eg", "-n", sysNS,
    "-o", "jsonpath={range .status.conditions[*]}{.type}={.status} {end}")
// never contains "Programmed=True" for ClusterIP gateways (AddressNotAssigned)
```

This was the root cause of persistent `installPair` timeouts in e2e tests even
when the cluster was healthy.

**Namespace stuck Terminating after helm uninstall.** When EG generates proxy
resources in the system namespace (GatewayNamespace mode puts proxy in the
Gateway's namespace), the proxy Deployment has Kubernetes finalizers. If you
run `helm uninstall` without first deleting the Gateway, the controller is torn
down before it can remove proxy finalizers. The namespace hangs in Terminating
indefinitely.

Fix: delete the Gateway FIRST, then uninstall:

```bash
kubectl delete gateway eg -n tr-system-{i}  # EG deprovisions proxy cleanly
helm uninstall eg-pair-{i} -n tr-release-{i}
kubectl delete namespace tr-release-{i} tr-system-{i} tr-dataplane-{i} \
  --ignore-not-found --wait=false
```

Without the Gateway deletion step, the proxy pod lingers, the namespace waits
for pod finalizers, and the pod never terminates because its owner (controller)
is gone. The `gwp pair delete` command must implement this sequence.

**Release namespace (tr-release-{i}) is NOT tracked by Helm for uninstall.**
Created by `--create-namespace` without Helm ownership annotations. After
uninstall, explicitly delete `tr-release-{i}` or the next install will fail
with an ownership conflict on the release namespace.

**helm uninstall --wait does NOT wait for namespace termination.** Chart-declared
namespaces (tr-system-{i}, tr-dataplane-{i}) may still be Terminating after
`helm uninstall --wait` returns. If you try to install before they finish
terminating, helm fails: `namespaces "tr-system-1" already exists`. Poll:

```go
deadline := time.Now().Add(2 * time.Minute)
for _, pfx := range []string{"tr-release", "tr-system", "tr-dataplane"} {
    ns := fmt.Sprintf("%s-%d", pfx, index)
    for time.Now().Before(deadline) {
        out, err := kubectl("get", "namespace", ns)
        if err != nil || !strings.Contains(out, ns) {
            break
        }
        time.Sleep(2 * time.Second)
    }
}
```

**k3d must use `--agents 1` for 3-pair e2e.** A single-node k3d cluster
(`--agents 0`) cannot handle 3 concurrent EG controllers + 3 Envoy proxies +
3 certgen Jobs under typical laptop constraints. Each install step times out at
the slower pair (usually pair 2, scheduled last). Use `--agents 1` to give the
cluster 2 nodes -- pairs spread across server and agent, reducing contention.

```bash
k3d cluster create gw-pairs-e2e \
  --agents 1 \
  --image rancher/k3s:v1.32.2-k3s1 \
  --k3s-arg --disable=traefik@server:*
# wait for both nodes
kubectl wait nodes/k3d-gw-pairs-e2e-server-0 --for=condition=Ready --timeout=120s
kubectl wait nodes/k3d-gw-pairs-e2e-agent-0  --for=condition=Ready --timeout=120s
```

**Remote e2e via `make e2e-remote` (Orbstack on mac mini or similar).**
If the laptop is resource-constrained, offload the e2e to a remote machine
with Orbstack installed. Pattern:

```makefile
e2e-remote:
    git add -A && git diff --cached --quiet || git commit -m "wip: sync for remote e2e"
    git push
    ssh dio@mini 'export PATH="/opt/homebrew/bin:$$HOME/.orbstack/bin:$$PATH" && \
      cd ~/src/dio/gateway-pairs && git pull --ff-only && \
      DOCKER_HOST=unix://$$HOME/.orbstack/run/docker.sock \
      PAIR_PREFIX=$(PAIR_PREFIX) make e2e'
```

Requirements on remote: `k3d`, `helm`, `go >= 1.24`, Docker (Orbstack).

**PITFALL: `e2e-remote` requires a commit for every intermediate fix.**
The round-trip (local fix → commit → push → ssh pull → run → see failure)
forces a commit on every iteration, polluting the log with `wip:` entries
and slowing down debugging. Prefer running e2e locally (`--agents 1` gives
enough headroom for 3 pairs on a modern laptop). Use `e2e-remote` only for
final green-run validation or when the local machine is genuinely resource-
constrained and no faster iteration path exists.

Use `e2e-remote-dirty` for fast iteration without git commits -- rsync syncs
the working tree directly:

```makefile
e2e-remote-dirty:
	rsync -az --delete \
	  --exclude='.git/' --exclude='bin/' --exclude='dist/' \
	  --exclude='charts/crds/*.yaml' \
	  ~/src/dio/gateway-pairs/ \
	  dio@mini:~/src/dio/gateway-pairs-wip/
	ssh dio@mini 'export PATH="/opt/homebrew/bin:$$HOME/.orbstack/bin:$$PATH" && \
	  cd ~/src/dio/gateway-pairs-wip && \
	  DOCKER_HOST=unix://$$HOME/.orbstack/run/docker.sock \
	  PAIR_PREFIX=$(PAIR_PREFIX) make e2e'
```

`charts/crds/*.yaml` is excluded from rsync -- those are generated and gitignored.
Mini must run `make generate-crds` once to populate them. For e2e runs this is
fine since the e2e uses `hack/install-crds.sh` not the embedded bytes.
Workflow: iterate with `e2e-remote-dirty` → once green run `e2e-remote` to push
a clean commit and share.

**Helm release namespace vs chart-declared namespaces:** use `helm upgrade
--install ... --namespace tr-release-{i} --create-namespace`. The system
and dataplane namespaces are chart-declared resources. The release namespace
holds only the Helm release Secret. Never declare the release namespace in
chart templates -- Helm's `--create-namespace` creates it without ownership
annotations, and the chart then fails on re-install with an ownership conflict.

**CRD install in e2e test:** call `hack/install-crds.sh` via `exec.CommandContext`
with the k3d context set in env. The test sets `REUSE_CLUSTER=1` to skip
cluster creation on repeated runs -- but the script detects already-installed
CRDs and skips Gateway API if present (via the self-managed/provider-managed
detection), so it is safe to call repeatedly.

## Debugging sequence

When a controller crashes on startup (`CrashLoopBackOff`):
1. Check for TLS cert error: `open /certs/tls.crt: no such file or directory` -- certgen Job missing or failed.
2. Check certgen Job logs in system namespace: `kubectl logs -n tr-system-1 -l app=certgen`.
3. If certgen failed on webhook patch: verify `--disable-topology-injector` flag is set (for multi-pair deployments).
4. If certgen succeeded but cert not mounted: verify Deployment has `/certs` volume + mount from `envoy-gateway` Secret.

When controller is Running but healthz check fails (`healthz check failed` in logs):
1. Check for RBAC watch errors: `kubectl logs -n tr-system-1 deploy/envoy-gateway | grep forbidden`.
2. Common missing permissions: `serviceaccounts` (needs cluster-wide get/list/watch AND namespace-scoped create/patch in BOTH system and dataplane NS), `listenersets`, `pods/binding`.
3. Compare your ClusterRole against upstream: `helm template eg oci://docker.io/envoyproxy/gateway-helm --version v1.8.0 --namespace envoy-gateway-system | sed -n '/envoy-gateway-rbac.yaml/,/^---/p'`.
4. RBAC changes take effect after pod restart -- apply the updated ClusterRole then `kubectl rollout restart deployment/envoy-gateway -n tr-system-1`.

When a Gateway is Accepted but not Programmed:
1. Check watch list -- system namespace missing is the most common cause.
2. Check tokenreviews permission: `kubectl logs deploy/envoy-gateway -n tr-system-1 | grep tokenreviews`.
3. Check infra-manager Role in BOTH system and dataplane namespace.
4. Check gateway-controller ClusterRole covers all resources above.
5. Port-forward Envoy admin (if pod exists) and inspect `/config_dump`.
6. Check EnvoyProxy CR status in tr-system-{i}.

## Multi-tier proxies within one pair (L1/L2 model for transit integrations)

One `eg-pair` can host multiple Envoy proxy tiers (e.g. L1 edge + L2 backend)
within the same pair by declaring multiple Gateways, each backed by its own
`EnvoyProxy` CR. EG places each tier's proxy Deployment in the Gateway's
namespace (the system namespace).

**Mechanism: Gateway-level EnvoyProxy override.** EG v1.1+ supports
`Gateway.spec.infrastructure.parametersRef → EnvoyProxy`. This overrides the
GatewayClass-level `parametersRef` for that specific Gateway only.

```yaml
# GatewayClass: points at baseline EnvoyProxy
spec:
  controllerName: gateway.envoyproxy.io/tr-1
  parametersRef:
    group: gateway.envoyproxy.io
    kind: EnvoyProxy
    name: default   # baseline: image, resource limits

# Gateway/l1: overrides with l1-specific EnvoyProxy
spec:
  gatewayClassName: tr-1
  infrastructure:
    parametersRef:
      group: gateway.envoyproxy.io
      kind: EnvoyProxy
      name: l1   # custom image with l1 dynamic module, 2 replicas

# Gateway/l2: overrides with l2-specific EnvoyProxy
spec:
  gatewayClassName: tr-1
  infrastructure:
    parametersRef:
      group: gateway.envoyproxy.io
      kind: EnvoyProxy
      name: l2   # shared proxy image, different upstream cluster config
```

Generated proxy names: `envoy-{namespace}-{gateway-name}-{hash}`. L1 and L2
proxies are independently addressable, rollable, and patchable via EnvoyPatchPolicy.

**EnvoyPatchPolicy targeting per tier:**

```yaml
spec:
  targetRef:
    group: gateway.networking.k8s.io
    kind: Gateway
    name: l1   # targets ONLY l1's proxy, not l2
```

**Helm `tiers` list (planned chart evolution).** The current `eg-pair` chart
creates exactly one Gateway + one EnvoyProxy. The roadmap evolution is a `tiers`
list in values that generates one Gateway + one EnvoyProxy per tier with a range
loop, falling back to the current single-tier behavior when `tiers` is unset.

**Scope:** L1 and L2 live in the same system namespace under one controller.
One `eg-pair` per logical isolation boundary. If tiered-router-eg and
cluster-router-eg are separate integrations that should not share fate, they
each get their own `eg-pair`. Within a single integration, `tiers` handles
L1/L2 as distinct proxies under one controller.

## Helm namespace hook leak problem (current PoC limitation)

The system namespace `tr-system-{i}` is created as a `pre-install` hook
(weight -5) so it exists before the certgen Job (weight -1) runs. **Hook
resources are NOT tracked in the Helm release manifest for deletion.** Helm
only deletes hook resources when `hook-delete-policy` includes `hook-succeeded`
-- which we cannot use for a namespace (it would delete the namespace after
certgen succeeds, before workloads are deployed).

Consequence: `helm uninstall` leaves `tr-system-{i}` behind. Operators who
run raw `helm uninstall` (without `gwp pair delete`) get a leaked namespace.
Re-install fails if the namespace is Terminating.

**The root cause: using a hook for namespace creation is wrong.** The hook
exists solely to work around Helm's `--create-namespace` ownership conflict --
if we declare the namespace as a normal chart resource AND use it as the release
namespace, Helm rejects re-install with ownership validation errors.

**Options evaluated:**

1. Hook + normal resource (namespace in both): Helm tries to create it twice.
   The hook creates without ownership annotations; the normal template fails.
   Does not work.

2. Post-delete hook Job that deletes the namespace: requires a SA/RBAC in the
   release namespace, runs after the controller is already gone, still has the
   proxy finalizer problem. Complex and fragile.

3. `--create-namespace` with explicit `gwp pair delete` cleanup: current
   approach. Works, but `helm uninstall` alone is incomplete. Documented
   limitation.

4. **Subchart migration (planned, correct fix):** see next section.

## Subchart migration plan (next PR)

The clean fix for the namespace hook leak AND the RBAC maintenance burden:
make `gateway-helm` a Helm subchart dependency of `eg-pair`. This eliminates
maintaining certgen, RBAC, and the controller Deployment by hand.

### What changes

**Delete from `eg-pair` templates:**
- `certgen.yaml` -- upstream provides
- `controller-rbac.yaml` -- upstream provides
- `serviceaccount.yaml` -- upstream provides
- `deployment.yaml` -- upstream provides
- `service.yaml` -- upstream provides
- `config.yaml` -- upstream provides (we pass values)
- tokenreviews + infra-manager parts of `rbac.yaml` -- upstream provides

**Keep in `eg-pair` templates:**
- `namespaces.yaml` (but as a NORMAL chart resource, not a hook -- see below)
- `gatewayclass.yaml` -- cluster-scoped, unique per pair
- `envoyproxy.yaml` -- parametersRef target
- `gateway.yaml` -- with `allowedRoutes: from: Same`
- `_helpers.tpl` -- naming derivation

### Namespace model simplification

With `gateway-helm` as a subchart, use `tr-system-{i}` as BOTH the release
namespace AND the workload namespace (drop `tr-release-{i}` entirely):

```
tr-system-{i}   Helm release Secret + all workloads (mirror of envoy-gateway-system)
```

`helm upgrade --install eg-pair-{i} ... --namespace tr-system-{i} --create-namespace`

`--create-namespace` creates `tr-system-{i}`. `gateway-helm` deploys certgen +
controller there. Our chart adds GatewayClass, EnvoyProxy, Gateway. All tracked
in one release. `helm uninstall eg-pair-{i} -n tr-system-{i}` removes everything
including the namespace.

The proxy finalizer problem remains -- `gwp pair delete` still needs to delete
the Gateway before uninstalling. But after step 3 (helm uninstall) the namespace
terminates cleanly because no orphan resources remain.

### controllerName injection challenge

`gateway-helm` exposes `config.envoyGateway.gateway.controllerName` as a plain
string. It cannot be set from a template expression inside `Chart.yaml` dependencies.

Solution: the CLI (`gwp pair install`) computes the controllerName string from
the pair id and passes it as a `--set` flag:

```bash
gwp pair install prod \
  --set "gateway-helm.config.envoyGateway.gateway.controllerName=gateway.envoyproxy.io/tr-prod"
```

The chart has `controllerName: ""` as a placeholder. The CLI is the smart layer.
Chart is dumb about naming; CLI provides the computed values.

### Chart.yaml dependency

```yaml
dependencies:
- name: gateway-helm
  version: "v1.8.0"
  repository: "oci://docker.io/envoyproxy"
  condition: gatewayHelm.enabled
```

`helm dependency update` fetches `gateway-helm-v1.8.0.tgz` into `charts/`.
The `generate-crds` Makefile target also needs `helm dependency update`.
Add `charts/gateway-helm-v1.8.0.tgz` to `.gitignore` OR commit it
(small binary, acceptable to commit for reproducible builds).

When EG releases v1.9.0, bump `EG_VERSION` in the Makefile. `helm dependency
update` + `make generate-crds` fetches the new chart and CRDs. Our chart
becomes a pure configuration/extension layer.

## Embedded assets and release pipeline

When building `gwp` as a released CLI tool:

**Chart embedding:** put `embed.go` directly inside `charts/` so the
`//go:embed` directive resolves against sibling directories with no copy step:

```go
// charts/embed.go
package charts

//go:embed eg-crds eg-pair all:crds
var fs_ embed.FS
```

Use `all:crds` (not `crds`) so `.gitkeep` (a hidden file) is included. Without
`all:`, the embed directive fails if only `.gitkeep` is present (no non-hidden
files). Committed `.gitkeep` in `charts/crds/` ensures the directive compiles
on a clean checkout before `generate-crds` has run.

**Do NOT put `embed.go` in `internal/assets/`.** The correct location is inside
the directory being embedded. `charts/embed.go` with `//go:embed eg-crds eg-pair all:crds`
resolves directly against sibling dirs with zero copy step. A separate
`internal/assets/` package requires a build-time `cp -r` to populate it,
breaks single-source-of-truth, and generates gitignored copies -- all avoidable.

**goreleaser has no native Helm chart publishing stanza** (confirmed in v2 schema).
Use a separate `publish-charts` job after the goreleaser job:

```yaml
publish-charts:
  needs: goreleaser
  permissions:
    packages: write
  steps:
  - uses: azure/setup-helm@...
  - run: echo "${{ secrets.GITHUB_TOKEN }}" | helm registry login ghcr.io ...
  - run: |
      VERSION="${GITHUB_REF_NAME#v}"   # strip leading v
      for chart in eg-crds eg-pair; do
        helm package "charts/${chart}" --version "${VERSION}" --app-version "${EG_VERSION}"
        helm push "${chart}-${VERSION}.tgz" "oci://ghcr.io/OWNER/REPO/charts"
      done
```

Chart `version:` in `Chart.yaml` should be set to `0.0.0-dev` sentinel and
injected by `helm package --version` at release time. Never bump manually.

**`EG_VERSION` lives in the release workflow env block**, not in `.goreleaser.yml`.
Single bump point:

```yaml
# .github/workflows/release.yml
env:
  EG_VERSION: v1.8.0
```

goreleaser accesses it as `{{ .Env.EG_VERSION }}` in `before.hooks` and `ldflags`.
goreleaser `before.hooks` must run `make generate-crds` before Go compilation
so embed dirs exist when the compiler is invoked.

**`gwp pair install`** extracts the embedded chart to `os.MkdirTemp`, passes
the path to `helm upgrade --install`, defers `os.RemoveAll`. Helm release
tracking is preserved (history, uninstall, upgrade all work).

See `references/goreleaser-homebrew-pattern.md` for the full `.goreleaser.yml`,
release workflow, Makefile targets, pinned Action SHAs, and pitfalls.

## Reference files

- `references/e2e-harness-shape.md` -- full testify/suite template for multi-pair k3d tests
- `references/crd-conflict-strategy.md` -- provider detection (managedFields heuristic), single-version-pin rule, four scenarios with exact commands
- `references/gwp-cli-design.md` -- `gwp` CLI subcommand tree, embedded asset design, goreleaser integration, implementation constraints, exit codes, key diagnostic flows
- `references/goreleaser-homebrew-pattern.md` -- reusable goreleaser + homebrew-tap pattern for dio CLI repos; pinned Action SHAs
- `references/eg-v1.8-certgen-and-rbac.md` -- certgen Job template, full upstream ClusterRole rules, topology injector multi-pair conflict, proxy placement behavior
- `references/provider-gateway-api-compat.md` -- version floor table by EG version, what is missing at each gap, detection algorithm, `--force-gateway-api-crds` risks on provider-managed clusters, GKE channel → Gateway API version mapping

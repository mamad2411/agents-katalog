---
name: envoy-gateway-namespace-mode
description: >
  Use when deploying, configuring, or debugging Envoy Gateway in Gateway Namespace
  Mode -- where proxy Deployments, Services, and ServiceAccounts are created in
  each Gateway's namespace instead of the controller namespace. Covers Helm config,
  RBAC shape, JWT vs mTLS auth shift, watch mode options, allowedRoutes wiring,
  known footguns, and the multi-pair isolation model.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [envoy-gateway, gateway-namespace-mode, k8s, helm, rbac, jwt, xds, multi-tenancy]
    related_skills: [transit-k3d-envoy-gateway-e2e]
---

# Envoy Gateway -- Gateway Namespace Mode

## Overview

In standard (Controller Namespace) mode EG creates all data-plane resources
(Deployments, Services, ServiceAccounts) in the controller namespace, typically
`envoy-gateway-system`. This co-locates control plane and data plane and requires
minimal RBAC.

**Gateway Namespace Mode** places the generated Envoy proxy Deployment, Service,
and ServiceAccount in the **Gateway object's namespace** instead. This gives
stronger isolation: each tenant's proxy lives in their namespace, RBAC can be
scoped per namespace, and a compromised proxy cannot trivially affect other tenants.

The cost: the EG controller needs cluster-wide RBAC to create and manage resources
in arbitrary namespaces, and authentication between proxy and controller shifts
from mTLS to JWT.

## Authentication shift: mTLS → JWT

This is the most important difference to understand.

| Mode | Auth mechanism |
|---|---|
| Controller Namespace (default) | mTLS -- mutual TLS, client + server both present certificates |
| Gateway Namespace Mode | Server-side TLS + JWT token validation |

In Gateway Namespace Mode:
- **Proxy pods** (in Gateway namespaces) authenticate using **projected ServiceAccount JWT tokens**. These are short-lived, audience-specific, automatically mounted.
- **EG controller** (in controller namespace) validates those JWT tokens via `TokenReview` API.
- Only the **CA certificate** is present in proxy pod namespaces. No client certificates.
- The proxy uses the CA certificate to validate the controller's server certificate.

Consequence: the EG ServiceAccount needs `tokenreviews/create` at cluster scope. Without it proxies cannot authenticate to xDS and stay unready. The error in EG logs is:
```
tokenreviews.authentication.k8s.io is forbidden
```

## Helm configuration

Minimal values to enable Gateway Namespace Mode:

```yaml
config:
  envoyGateway:
    provider:
      type: Kubernetes
      kubernetes:
        deploy:
          type: GatewayNamespace
```

One-liner install:
```shell
helm install \
  --set config.envoyGateway.provider.kubernetes.deploy.type=GatewayNamespace \
  eg oci://docker.io/envoyproxy/gateway-helm \
  --version v1.8.0 -n envoy-gateway-system --create-namespace
```

## RBAC created by the Helm chart

The upstream `gateway-helm` chart automatically creates these when
`deploy.type: GatewayNamespace` is set:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: gateway-helm-cluster-infra-manager
rules:
- apiGroups: [""]
  resources: ["serviceaccounts", "services", "configmaps"]
  verbs: ["create", "get", "delete", "deletecollection", "patch"]
- apiGroups: ["apps"]
  resources: ["deployments", "daemonsets"]
  verbs: ["create", "get", "delete", "deletecollection", "patch"]
- apiGroups: ["autoscaling", "policy"]
  resources: ["horizontalpodautoscalers", "poddisruptionbudgets"]
  verbs: ["create", "get", "delete", "deletecollection", "patch"]
- apiGroups: ["authentication.k8s.io"]
  resources: ["tokenreviews"]
  verbs: ["create"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: gateway-helm-cluster-infra-manager
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: 'gateway-helm-cluster-infra-manager'
subjects:
- kind: ServiceAccount
  name: 'envoy-gateway'
  namespace: 'envoy-gateway-system'
```

Note: `tokenreviews/create` at cluster scope is load-bearing. Without it the JWT
auth validation fails and proxies cannot connect to xDS.

## Watch mode configuration

EG can be told which namespaces to watch. Two options:

### Explicit namespace list

Watches only named namespaces. Creates **namespace-scoped Roles** in each listed
namespace (narrower permissions, good for known static tenants).

```yaml
envoyGateway:
  provider:
    type: Kubernetes
    kubernetes:
      deploy:
        type: GatewayNamespace
      watch:
        type: Namespaces
        namespaces:
          - team-a
          - team-b
```

### Namespace selector

Watches all namespaces matching a label selector. Uses a **ClusterRole** for infra
management (required since target namespaces are dynamic at runtime).

```yaml
envoyGateway:
  provider:
    type: Kubernetes
    kubernetes:
      deploy:
        type: GatewayNamespace
      watch:
        type: NamespaceSelector
        namespaceSelector:
          matchLabels:
            gateway: enabled
```

## Critical: watch list must include the controller namespace

If the watch list only covers tenant/Gateway namespaces but omits the controller
namespace, EG cannot read its own TLS secret. Symptom:

```
Gateway shows Accepted=True but Programmed=False
```

Always include the controller namespace in the explicit list:

```yaml
watch:
  type: Namespaces
  namespaces:
  - envoy-gateway-system   # REQUIRED: controller reads its own TLS secret here
  - team-a
  - team-b
```

Failing to include the controller namespace is the most common misconfiguration.

## Where proxies land

In Gateway Namespace Mode, EG places all data-plane resources in the **Gateway
object's namespace**. If your Gateway is in `team-a`, the proxy Deployment and
Service land in `team-a`.

```shell
kubectl get pods -n team-a
# envoy-team-a-gateway-a-b65c6264-d56f5d989-6dv5s   2/2   Running
# team-a-backend-6f786fb76f-nx26p                    1/1   Running

kubectl get services -n team-a
# envoy-team-a-gateway-a-b65c6264  LoadBalancer  172.18.0.200  8080:30999/TCP
```

Generated resource names follow the pattern:
`envoy-{namespace}-{gateway-name}-{hash}`

## HTTPRoutes -- same namespace as Gateway (from: Same)

Since proxy and Gateway both land in the same namespace, HTTPRoutes should also
live in that namespace. Use `allowedRoutes: from: Same`:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: gateway-a
  namespace: team-a
spec:
  gatewayClassName: eg
  listeners:
  - name: http
    port: 80
    protocol: HTTP
    allowedRoutes:
      namespaces:
        from: Same
```

HTTPRoute in the same namespace, no `parentRefs.namespace` needed:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: team-a-route
  namespace: team-a
spec:
  parentRefs:
  - name: gateway-a
  hostnames: ["www.team-a.com"]
  rules:
  - backendRefs:
    - name: team-a-backend
      port: 3000
```

If you need cross-namespace route attachment use `from: Selector` with
`kubernetes.io/metadata.name` label selector (auto-set by Kubernetes):

```yaml
allowedRoutes:
  namespaces:
    from: Selector
    selector:
      matchLabels:
        kubernetes.io/metadata.name: team-a-routes
```

## Uninstall / namespace termination gotcha

When `helm uninstall` removes the EG controller Deployment, the controller is gone.
Any proxy pods that still exist have a finalizer
(`gateway-exists-finalizer.gateway.networking.k8s.io`) that only the controller can
remove. If the controller is gone the finalizer is never cleared, and the namespace
sticks in `Terminating` indefinitely.

**Correct delete sequence:**
1. Delete the Gateway resource -- EG controller sees this, deprovisions the proxy,
   and clears the finalizer while the controller is still alive.
2. Wait for the proxy Deployment to be gone.
3. Then run `helm uninstall`.
4. Namespace terminates cleanly.

```shell
kubectl delete gateway my-gateway -n team-a --wait=true --timeout=60s
kubectl wait --for=delete deployment -l gateway.envoyproxy.io/owning-gateway-name=my-gateway \
  -n team-a --timeout=60s
helm uninstall eg -n envoy-gateway-system
```

## Incompatibility: Merged Gateways

**Gateway Namespace Mode is not supported with Merged Gateways deployments.**
These two features are mutually exclusive. If `mergeGateways: true` is set,
`deploy.type: GatewayNamespace` will not work correctly.

## Verification checklist

After installing with Gateway Namespace Mode:

```shell
# Gateway is Programmed (not just Accepted)
kubectl get gateway my-gateway -n team-a
# NAME        CLASS   ADDRESS        PROGRAMMED   AGE
# my-gateway  eg      172.18.0.200   True         67s

# Proxy pod running in Gateway namespace (not in envoy-gateway-system)
kubectl get pods -n team-a -l 'app.kubernetes.io/component=proxy'

# No tokenreviews errors in EG controller
kubectl logs -n envoy-gateway-system deploy/envoy-gateway | grep -i token
```

If Gateway is `Accepted=True` but `Programmed=False`:
1. Check watch list includes controller namespace.
2. Check `tokenreviews` ClusterRole/Binding exists and binds the right SA.
3. Check EG controller logs for cert or cache errors.

## Debug sequence

```
1. kubectl get gateway -A               -- check Accepted + Programmed
2. kubectl logs -n envoy-gateway-system deploy/envoy-gateway | tail -30
3. kubectl get clusterrolebinding | grep infra-manager  -- RBAC present?
4. kubectl get clusterrolebinding | grep tokenreviews   -- JWT auth RBAC?
5. kubectl get configmap envoy-gateway-config -n envoy-gateway-system -o yaml
   -- verify deploy.type=GatewayNamespace + watch list has controller NS
6. kubectl get pods -n <gateway-namespace>              -- proxy running?
7. kubectl describe pod <proxy-pod> -n <gateway-namespace>  -- any failures?
```

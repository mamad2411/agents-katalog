---
name: service-mesh-istio
description: >
  Guides installing and operating Istio service mesh — choosing an
  install profile, configuring traffic management with VirtualService
  and DestinationRule, enforcing mutual TLS (mTLS), and wiring up
  mesh observability (metrics, distributed tracing, access logs). Use
  when a user asks to "install Istio," "set up canary/traffic-split
  routing," "enforce mTLS between services," "debug a 503 from the
  Istio sidecar," "add retries/timeouts/circuit breaking," or "reduce
  Istio's resource overhead."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Service Mesh (Istio)

## Purpose

Istio moves cross-cutting network concerns — mTLS, retries, timeouts,
traffic splitting, fine-grained observability — out of application code
and into a sidecar proxy (Envoy) that every service call passes through.
That power comes with real operational cost: sidecars add latency and
resource overhead, misconfigured `VirtualService`/`DestinationRule`
pairs silently blackhole traffic, and mTLS misconfiguration can either
leave traffic unencrypted or break all cross-namespace calls at once.
This skill covers installing Istio deliberately (not "install
everything") and configuring traffic management and mTLS in a way that
fails safely.

## When to use

- Deciding which Istio install profile to use and whether the mesh is
  actually warranted versus a simpler Ingress-only setup.
- Configuring canary/blue-green traffic splitting between two service
  versions with `VirtualService` weighted routing.
- Enforcing mTLS mesh-wide or per-namespace, including migration from
  permissive to strict mode without an outage.
- Adding retries, timeouts, or circuit breaking (outlier detection) to a
  service-to-service call path.
- Debugging sidecar-related `503 UC`/`503 NR` errors or unexpected
  timeout behavior.
- Wiring up Istio's built-in metrics/tracing so request-level latency
  and error rate are visible per service, independent of application
  instrumentation.

## Prerequisites & environment

- Istio ≥ 1.21 (ambient mesh mode — sidecar-less data plane via ztunnel
  — reached general availability in 1.24; sidecar mode remains the
  default and more mature option for most production installs as of
  this writing). Confirm your chosen minor version's supported
  Kubernetes version range in Istio's release notes before installing —
  Istio typically supports the last 3–4 Kubernetes minor versions.
- `istioctl` matching (or within one minor version of) the control
  plane version being installed.
- A Kubernetes cluster with a CNI that permits Istio's `istio-init`/CNI
  plugin to set up pod-level iptables redirection, or Istio's CNI plugin
  installed in place of the init-container approach (required on
  clusters, like OpenShift, that restrict privileged init containers).
- Enough node capacity for sidecar overhead: budget roughly 50–150m CPU
  and 64–128Mi memory per sidecar at idle as a starting point, scaling
  with traffic — validate against your own workloads rather than
  assuming these figures hold at scale.
- If also running an Ingress controller, decide up front whether Istio's
  ingress gateway replaces it or the two coexist (see
  [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md)).

## Step-by-step guidance

1. **Choose an install profile deliberately** rather than defaulting to
   `default`:
   ```bash
   istioctl profile list
   istioctl install --set profile=minimal -y     # control plane only, no ingress/egress gateway
   istioctl install --set profile=default -y     # control plane + ingress gateway (most common start)
   ```
   Use `demo` only for local learning/testing — it enables verbose
   tracing and permissive settings not appropriate for production.

2. **Verify the install** before enabling injection anywhere:
   ```bash
   istioctl verify-install
   kubectl get pods -n istio-system
   ```

3. **Enable sidecar injection per namespace, not cluster-wide**, so
   rollout is deliberate and reversible per team/service:
   ```bash
   kubectl label namespace payments istio-injection=enabled
   ```
   Existing pods in that namespace need a rollout restart to actually
   pick up the sidecar — labeling alone doesn't inject into already-
   running pods:
   ```bash
   kubectl rollout restart deployment -n payments
   ```

4. **Configure traffic splitting** with a `DestinationRule` (defines
   subsets) and a `VirtualService` (routes traffic to them):
   ```yaml
   apiVersion: networking.istio.io/v1
   kind: DestinationRule
   metadata:
     name: payments-api
   spec:
     host: payments-api.payments.svc.cluster.local
     subsets:
       - name: v1
         labels: { version: v1 }
       - name: v2
         labels: { version: v2 }
   ---
   apiVersion: networking.istio.io/v1
   kind: VirtualService
   metadata:
     name: payments-api
   spec:
     hosts: ["payments-api.payments.svc.cluster.local"]
     http:
       - route:
           - destination: { host: payments-api.payments.svc.cluster.local, subset: v1 }
             weight: 90
           - destination: { host: payments-api.payments.svc.cluster.local, subset: v2 }
             weight: 10
   ```
   Shift weight incrementally (90/10 → 50/50 → 0/100) while watching
   error rate and latency for the `v2` subset before removing `v1`.

5. **Add resilience policies** (timeout, retries, outlier detection) on
   the same `VirtualService`/`DestinationRule` pair:
   ```yaml
   spec:
     hosts: ["payments-api.payments.svc.cluster.local"]
     http:
       - timeout: 3s
         retries:
           attempts: 2
           perTryTimeout: 1s
           retryOn: 5xx,reset,connect-failure
         route:
           - destination: { host: payments-api.payments.svc.cluster.local, subset: v1 }
   ```
   ```yaml
   # DestinationRule outlier detection (circuit breaking)
   spec:
     host: payments-api.payments.svc.cluster.local
     trafficPolicy:
       outlierDetection:
         consecutive5xxErrors: 5
         interval: 30s
         baseEjectionTime: 30s
         maxEjectionPercent: 50
   ```
   Retries combined with a short per-try timeout can amplify load on an
   already-struggling backend — cap `attempts` and `maxEjectionPercent`
   deliberately rather than defaulting to aggressive retry settings.

6. **Enable mTLS incrementally, starting permissive**, so mixed
   mesh/non-mesh traffic doesn't break during rollout:
   ```yaml
   apiVersion: security.istio.io/v1
   kind: PeerAuthentication
   metadata:
     name: default
     namespace: payments
   spec:
     mtls:
       mode: PERMISSIVE   # accepts both plaintext and mTLS
   ```
   Once all callers into the namespace are confirmed to be in-mesh
   (check via `istioctl x describe` or mesh metrics for plaintext
   connections), tighten to strict:
   ```yaml
   spec:
     mtls:
       mode: STRICT
   ```
   > **Warning:** flipping directly to `STRICT` mesh-wide before every
   > caller is sidecar-injected breaks any non-meshed client (a cron Job
   > without injection, an external health checker hitting the pod IP
   > directly) instantly and cluster-wide. Roll out namespace-by-namespace
   > and confirm via traffic metrics first.

7. **Enable observability**: Istio emits Prometheus metrics
   (`istio_requests_total`, `istio_request_duration_milliseconds`) and
   propagates trace headers automatically once the app forwards
   `traceparent`/`x-b3-*` headers on outbound calls it makes. Install
   the observability addons (Prometheus, Grafana, Kiali, Jaeger/Tempo)
   or point Istio's telemetry at existing infra via a `Telemetry`
   resource rather than assuming a default sink exists:
   ```yaml
   apiVersion: telemetry.istio.io/v1
   kind: Telemetry
   metadata:
     name: mesh-default
     namespace: istio-system
   spec:
     tracing:
       - randomSamplingPercentage: 5.0
   ```

8. **Validate configuration before it reaches production**:
   ```bash
   istioctl analyze -n payments
   istioctl proxy-config routes deploy/payments-api -n payments
   ```
   `istioctl analyze` catches the most common misconfigurations
   (a `VirtualService` referencing a `DestinationRule` subset that
   doesn't exist, a host mismatch) before they cause a live 503.

## Best practices

- Start with the `minimal` or `default` profile and add gateways/features
  as a specific need arises — every enabled component is more attack
  surface and more upgrade coordination.
- Pin `VirtualService` hosts to the fully-qualified service name
  (`<svc>.<ns>.svc.cluster.local`) to avoid ambiguity when multiple
  namespaces have same-named services.
- Set an explicit `trafficPolicy` default in every `DestinationRule`
  (connection pool limits, outlier detection) rather than relying on
  Envoy's defaults, which are tuned for generic workloads, not yours.
- Treat `istioctl upgrade`/control-plane version bumps as a change with
  real blast radius — use `istioctl x precheck` and, for multi-revision
  clusters, canary the control plane with revision tags before
  migrating all namespaces.
- Keep the number of `PeerAuthentication`/`AuthorizationPolicy`
  resources per namespace small and centrally reviewed — authorization
  policy sprawl across many narrowly-scoped resources is hard to reason
  about holistically and easy to leave a gap in.
- If most traffic is north-south through one Ingress and mTLS/circuit-
  breaking isn't needed east-west, weigh whether a full mesh is
  justified versus [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md)
  alone — a mesh installed "because it's best practice" without a
  specific east-west requirement is often not worth its operational
  cost.

## Common pitfalls

- **Symptom:** Calls between two services return `503 UC` (upstream
  connection termination) intermittently after enabling the mesh.
  **Fix:** Usually a `DestinationRule` connection-pool limit
  (`maxConnections`/`http1MaxPendingRequests`) that's too low for actual
  traffic, or outlier detection ejecting healthy instances too
  aggressively. Check `istioctl proxy-config cluster <pod>` for the
  effective connection-pool settings and outlier-detection state before
  assuming it's an application bug.

- **Symptom:** `503 NR` ("no route") appears after applying a new
  `VirtualService`.
  **Fix:** The `VirtualService` host doesn't match any route Envoy
  knows about — often a namespace-qualification mismatch, or the
  `DestinationRule` subset referenced doesn't exist. Run `istioctl
  analyze` first; it catches this class of error before it reaches
  traffic.

- **Symptom:** After enabling `PeerAuthentication` in `STRICT` mode
  cluster-wide, a batch Job or an external monitoring probe that talks
  directly to pod IPs starts failing entirely.
  **Fix:** Non-sidecar-injected clients cannot participate in mTLS.
  Either inject sidecars into that workload too, exempt the specific
  port via `PeerAuthentication` `portLevelMtls`, or route the probe
  through a path that doesn't require mTLS — never flip to `STRICT`
  mesh-wide without first inventorying every non-meshed caller.

- **Symptom:** Sidecar injection was enabled on a namespace but existing
  pods show no `istio-proxy` container.
  **Fix:** The `istio-injection=enabled` label only affects *new* pod
  admissions via the mutating webhook; existing pods must be recreated
  (`kubectl rollout restart deployment -n <ns>`) to pick up the sidecar.

- **Symptom:** Upgrading the Istio control plane breaks data-plane
  compatibility for workloads not yet restarted.
  **Fix:** Envoy sidecars from an old control-plane version can be
  incompatible with a newer `istiod`'s xDS config beyond a couple of
  minor versions ("N-2" support window varies by release). Use revision
  tags (`istioctl install --set revision=1-24`) to run old and new
  control planes side by side, migrate namespaces gradually, and
  restart workloads to pick up matching sidecar versions before
  decommissioning the old revision.

## Worked example

**Scenario:** Canary a new version of `payments-api` (v2) behind mTLS,
starting at 10% traffic, with a 3s timeout and bounded retries, in the
`payments` namespace.

```bash
kubectl label namespace payments istio-injection=enabled
kubectl rollout restart deployment -n payments
```

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata: { name: default, namespace: payments }
spec:
  mtls: { mode: PERMISSIVE }
---
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata: { name: payments-api, namespace: payments }
spec:
  host: payments-api.payments.svc.cluster.local
  subsets:
    - name: v1
      labels: { version: v1 }
    - name: v2
      labels: { version: v2 }
  trafficPolicy:
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
---
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata: { name: payments-api, namespace: payments }
spec:
  hosts: ["payments-api.payments.svc.cluster.local"]
  http:
    - timeout: 3s
      retries: { attempts: 2, perTryTimeout: 1s, retryOn: 5xx,connect-failure }
      route:
        - destination: { host: payments-api.payments.svc.cluster.local, subset: v1 }
          weight: 90
        - destination: { host: payments-api.payments.svc.cluster.local, subset: v2 }
          weight: 10
```

```bash
istioctl analyze -n payments
kubectl apply -f canary.yaml
watch -n5 'kubectl exec deploy/payments-api-v2 -n payments -c istio-proxy -- pilot-agent request GET stats | grep 5xx'
```

Once `v2` shows a healthy error rate at 10% for a soak period, shift to
`50/50`, then `0/100`, before removing the `v1` subset and (separately,
once no plaintext callers remain) tightening `PeerAuthentication` to
`STRICT`.

## Cross-references

- [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md) — comparing/coexisting with a dedicated Ingress controller for north-south traffic versus Istio's ingress gateway.
- [cert-manager-tls-automation](../cert-manager-tls-automation/SKILL.md) — issuing and rotating the TLS certificates used at the Istio ingress gateway (separate from mesh-internal mTLS, which Istio manages itself via its own CA).
- [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md) — how Istio's sidecar traffic interception interacts with the underlying CNI and Kubernetes `NetworkPolicy` enforcement.

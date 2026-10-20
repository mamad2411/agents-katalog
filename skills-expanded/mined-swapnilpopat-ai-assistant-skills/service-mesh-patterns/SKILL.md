---
name: service-mesh-patterns
description: Apply service mesh (Istio ambient, Linkerd, Cilium) for mTLS, traffic policy, and observability across microservices. Use when service-to-service security, resilience, or telemetry must be uniform and out of application code.
---

# Service Mesh Patterns

Move cross-cutting network concerns - identity, mTLS, retries, traffic shaping, telemetry - out of services and into a mesh data plane managed by a single control plane. Done well, it shrinks application code and standardizes zero-trust posture.

## Stack Baseline (2026)

| Concern | Recommended |
| --- | --- |
| Mesh runtime | Istio 1.24 ambient mode (ztunnel + waypoint), Linkerd 2.16, Cilium Service Mesh 1.16 (eBPF) |
| Identity | SPIFFE / SPIRE workload identity; SVIDs rotated < 24h |
| Ingress / egress | Istio Gateway API, Envoy Gateway, Cilium Gateway API (Gateway API 1.2) |
| Policy | AuthorizationPolicy, Kyverno / OPA Gatekeeper, NetworkPolicy + CiliumNetworkPolicy |
| Observability | OpenTelemetry 1.x, Prometheus, Tempo / Jaeger, Kiali, Hubble for eBPF flows |
| Progressive delivery | Argo Rollouts or Flagger driving Istio VirtualService weights |
| Multi-cluster | Istio multi-primary, Linkerd multi-cluster gateways, Cilium Cluster Mesh |

## When to Use
- Tens or more services need consistent mTLS, retries, and traffic policy.
- Zero-trust mandate requires per-workload identity and authorization beyond NetworkPolicy.
- Progressive delivery (canary, shadow, A/B) must be uniform across languages and runtimes.
- Compliance demands signed, attested workload identity and audit-quality access logs.

## Prerequisites
- Kubernetes 1.30+ with CNI supporting your chosen mesh; cluster autoscaling stable.
- Centralized telemetry backend (Prometheus + OTel collector + tracing store).
- Platform team that owns mesh upgrades, CRDs, and policies.
- A documented service catalog with owners, SLOs, and dependency graph.

## Instructions

1. **Decide if you actually need a mesh**: For < 10 services with simple needs, a Gateway API + library-level retries may be cheaper. Pick mesh when at least two of: zero-trust mTLS, multi-language fleet, multi-cluster, or platform-wide progressive delivery apply.

2. **Choose data plane mode**: Prefer ambient (Istio ztunnel) or eBPF (Cilium) over per-pod sidecars to cut memory and tail latency. Reserve sidecars for L7 features only where needed via waypoint proxies.

   ```mermaid
   flowchart LR
       C[Client] --> GW[Gateway API]
       GW --> ZT1[ztunnel L4 mTLS]
       ZT1 --> WP[Waypoint L7<br/>auth, retry, route]
       WP --> SVC[Service Pod]
       SVC --> ZT2[ztunnel] --> DEP[Dependency]
   ```

3. **Bootstrap workload identity**: Issue SPIFFE IDs (`spiffe://cluster.local/ns/payments/sa/checkout`) per ServiceAccount; require mTLS STRICT in every namespace; deny plaintext egress at namespace boundary.

4. **Define traffic policy as code**: Encode timeouts, retries, outlier detection, and canary weights in Gateway API and mesh CRDs; review like any other infra change.

   ```yaml
   apiVersion: networking.istio.io/v1
   kind: VirtualService
   metadata: { name: checkout }
   spec:
     hosts: [checkout]
     http:
     - route:
       - destination: { host: checkout, subset: stable }
         weight: 95
       - destination: { host: checkout, subset: canary }
         weight: 5
       timeout: 2s
       retries: { attempts: 2, perTryTimeout: 800ms, retryOn: 5xx,reset,connect-failure }
   ```

5. **Author authorization policies**: Default-deny per namespace; allow explicit `from.principals` (SPIFFE IDs) on specific paths and methods. Test with negative cases in CI.

6. **Wire telemetry**: Export RED metrics, access logs (with `trace_id`), and traces via OTel; build per-service SLO dashboards and burn-rate alerts before enabling new features.

7. **Plan rollout and upgrades**: Roll out one namespace at a time; pin mesh version; subscribe to CVE feeds; rehearse control-plane upgrades in a non-prod cluster.

## Common Pitfalls

| Pitfall | Why it bites | Mitigation |
| --- | --- | --- |
| Sidecar everywhere by default | Memory, CPU, and tail-latency tax across the fleet | Use ambient / eBPF; add waypoints only where L7 features are required |
| mTLS PERMISSIVE left on forever | Silent plaintext traffic, false sense of zero-trust | Move to STRICT per namespace with a tracked deadline; alert on plaintext |
| App-level retries plus mesh retries | Retry storms and amplified outages | Disable client retries when mesh handles them; tune budgets centrally |
| AuthorizationPolicy without negative tests | Overly permissive rules ship unnoticed | CI tests assert allowed and denied calls per service identity |
| Mesh upgrades skipped | CVEs accumulate; eventual forced jump breaks APIs | Quarterly upgrade cadence; canary control plane in staging |
| No egress control | Data exfiltration and shadow dependencies | Egress gateway + allowlisted external hosts per namespace |

## Output Format

Deliver a mesh design doc with: rationale and chosen runtime/mode, identity scheme (SPIFFE namespacing), Gateway API and mesh CRDs as YAML, authorization matrix, observability schema, rollout plan per namespace, upgrade and incident runbooks, and SLOs for the mesh itself.

## Authoritative References

- [Istio Ambient Mesh](https://istio.io/latest/docs/ambient/)
- [Linkerd Documentation](https://linkerd.io/2/overview/)
- [Cilium Service Mesh](https://docs.cilium.io/en/stable/network/servicemesh/)
- [Kubernetes Gateway API](https://gateway-api.sigs.k8s.io/)
- [SPIFFE / SPIRE](https://spiffe.io/docs/latest/spiffe-about/overview/)
- [CNCF Zero Trust whitepaper](https://www.cncf.io/blog/2022/05/24/cncf-zero-trust-white-paper/)
- [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/)

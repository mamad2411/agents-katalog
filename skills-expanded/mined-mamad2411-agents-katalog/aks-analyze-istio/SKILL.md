---
name: aks-analyze-istio
description: Analyze Istio service-mesh behavior on AKS including sidecar injection, VirtualService, DestinationRule, Gateway, subsets, retries, timeouts, mTLS, routing, and proxy-related failures. Use for mesh routing, 503/504, mTLS, retry, traffic-split, or sidecar issues.
---

# Analyze Istio

1. Confirm whether the namespace/workload uses Istio injection.
2. Inspect relevant Gateway, VirtualService, DestinationRule, ServiceEntry, PeerAuthentication, and AuthorizationPolicy resources when applicable.
3. Verify hosts, routes, subsets, ports, retries, timeouts, and traffic weights.
4. Inspect Envoy sidecar state and proxy-related evidence.
5. Distinguish application failure from Kubernetes Service failure and mesh-policy/routing failure.
6. Never alter traffic weights, mTLS, or authorization policy unless explicitly authorized.

## Output
- Mesh Topology
- Routing/Policy Findings
- Sidecar/Proxy Evidence
- Failure Layer
- Recommended Action

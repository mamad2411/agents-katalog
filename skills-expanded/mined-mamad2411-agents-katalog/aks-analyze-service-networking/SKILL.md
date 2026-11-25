---
name: aks-analyze-service-networking
description: Analyze AKS Kubernetes Services, endpoints, DNS, ingress/gateway routing, ports, selectors, network policies, and service-to-service connectivity. Use for connection failures, unreachable services, wrong ports/selectors, DNS issues, or request routing problems.
---

# Analyze Service Networking

1. Resolve the source service, destination service, namespace, and expected port/protocol.
2. Inspect Service selectors, endpoints, target ports, DNS names, ingress/gateway resources, and applicable network policies.
3. Compare declared dependency metadata with live routing.
4. If Istio is enabled, route mesh-specific checks to `aks-analyze-istio`.
5. Distinguish no-endpoint, DNS, policy, port, application, and mesh failures.
6. Do not change network policy or routing unless explicitly authorized.

## Output
- Service/Endpoint State
- Routing Findings
- Connectivity Evidence
- Failure Layer
- Recommended Next Skill

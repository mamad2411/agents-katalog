---
name: aks-inspect-sidecars
description: Inspect sidecar containers in AKS pods, including Istio/Envoy, logging, security, proxy, or platform sidecars, and determine their effect on application startup, readiness, resources, networking, and termination. Use when sidecars may block or degrade application pods.
---

# Inspect Sidecars

1. Identify all non-primary containers in the target pod.
2. Determine each sidecar purpose and lifecycle relationship to the application container.
3. Inspect readiness, restarts, logs, resources, ports, mounts, and termination behavior.
4. Correlate sidecar failures with application readiness, networking, and resource pressure.
5. Route Istio-specific behavior to `aks-analyze-istio`.
6. Do not assume the primary application caused a pod failure when a sidecar is unhealthy.

## Output
- Sidecar Inventory
- Sidecar Health
- Application Impact
- Supporting Evidence
- Recommended Next Skill

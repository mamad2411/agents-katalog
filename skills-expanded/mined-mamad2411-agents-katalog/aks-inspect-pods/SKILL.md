---
name: aks-inspect-pods
description: Inspect AKS pods and containers for readiness, liveness, restarts, CrashLoopBackOff, pending scheduling, logs, termination reasons, resource pressure, probes, init containers, and container state. Use for pod-level runtime failures and service health investigations.
---

# Inspect Pods

1. Resolve cluster, namespace, deployment, and target pods.
2. Inspect pod phase, conditions, restarts, container states, termination reasons, probes, events, CPU/memory pressure, and scheduling.
3. Inspect init containers and sidecars separately from the primary application container.
4. Retrieve logs for the relevant container and time window.
5. Correlate pod failure timing with rollout, image, startup-job, and DataDog evidence.
6. Avoid treating a restarted pod as root cause without supporting evidence.

## Output
- Pod State
- Container Findings
- Events/Logs Evidence
- Resource/Probe Findings
- Recommended Next Skill

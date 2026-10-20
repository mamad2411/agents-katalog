---
name: aks-inspect-namespace
description: Inspect Kubernetes namespace state in AKS, including workloads, quotas, limits, events, service accounts, policies, and namespace-scoped failures. Use when a service issue may be isolated to a namespace or when resolving environment-to-namespace context.
---

# Inspect Namespace

1. Resolve cluster and namespace from `.digital-platform-ai/aks.yaml`.
2. Inspect namespace workloads, events, quotas, limit ranges, service accounts, and relevant policies.
3. Identify failed, pending, restarting, or unscheduled workloads.
4. Correlate namespace events with deployment and pod timelines.
5. Route to deployment, pod, storage, networking, or Istio skills based on evidence.

## Output
- Namespace State
- Workload Summary
- Relevant Events
- Constraints/Policies
- Recommended Next Skill

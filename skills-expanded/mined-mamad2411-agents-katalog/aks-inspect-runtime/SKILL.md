---
name: aks-inspect-runtime
description: Route AKS runtime investigations to the appropriate focused skill across clusters, namespaces, deployments, pods, storage, services/networking, blue-green, Istio, images, sidecars, startup jobs, Argo CD, Terraform, and rollout diagnosis. Use as the general AKS entry point when the failure domain is not yet known.
---

# Inspect Runtime

1. Read `.digital-platform-ai/aks.yaml`, service metadata, dependencies, environment metadata, and relevant service instructions.
2. Resolve environment, cluster, namespace, workload, and ops repository.
3. Determine the investigation domain from available evidence.
4. Route to one or more focused AKS skills:
   - `aks-inspect-cluster`
   - `aks-inspect-namespace`
   - `aks-analyze-deployment`
   - `aks-inspect-pods`
   - `aks-analyze-storage`
   - `aks-analyze-service-networking`
   - `aks-analyze-blue-green`
   - `aks-analyze-istio`
   - `aks-inspect-container-images`
   - `aks-inspect-sidecars`
   - `aks-inspect-startup-jobs`
   - `aks-inspect-argocd`
   - `aks-inspect-terraform`
   - `aks-diagnose-rollout`
5. Run independent evidence gathering in parallel.
6. Continue until evidence identifies the failing layer or remaining unknowns.

## Output
- Resolved AKS Context
- Investigation Domains
- Evidence Summary
- Failing Layer
- Recommended Next Action

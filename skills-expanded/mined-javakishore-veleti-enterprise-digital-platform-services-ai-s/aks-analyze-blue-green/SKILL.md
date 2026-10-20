---
name: aks-analyze-blue-green
description: Analyze blue-green deployment topology on AKS, including active/preview workloads, services, labels/selectors, traffic switching, image versions, health, and rollback readiness. Use during blue-green releases, cutover failures, version mismatch, or traffic-routing incidents.
---

# Analyze Blue-Green Deployment

1. Read rollout metadata from `.digital-platform-ai/aks.yaml` and the `-ops` repository.
2. Identify blue and green deployments, active and preview services, labels/selectors, images, replica health, and traffic target.
3. Verify the live traffic path points to the intended color/version.
4. Compare health and runtime evidence between blue and green.
5. Check whether startup jobs, Istio routing, or ArgoCD sync state affected cutover.
6. Never switch production traffic unless explicitly authorized.

## Output
- Active/Preview State
- Version Comparison
- Traffic Target
- Cutover Evidence
- Rollback Readiness

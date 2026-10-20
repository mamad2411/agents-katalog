---
name: aks-analyze-deployment
description: Analyze Kubernetes Deployment, ReplicaSet, manifest, rollout strategy, desired/current replicas, probes, environment references, and deployment descriptors for an AKS-hosted application. Use for rollout failures, replica mismatch, deployment drift, manifest problems, or application deployment investigation.
---

# Analyze Deployment

1. Read service and AKS metadata plus the corresponding `-ops` repository.
2. Identify deployment descriptors, overlays/templates, desired image, replica count, probes, env/config references, volumes, and rollout strategy.
3. Compare desired configuration with live Deployment and ReplicaSet state.
4. Identify drift, failed revisions, unavailable replicas, probe failures, or configuration mismatch.
5. Inspect pods when the live deployment is unhealthy.
6. Do not modify manifests or live resources unless explicitly authorized.

## Output
- Desired vs Live State
- Deployment Findings
- Revision/Rollout Evidence
- Configuration Drift
- Recommended Action

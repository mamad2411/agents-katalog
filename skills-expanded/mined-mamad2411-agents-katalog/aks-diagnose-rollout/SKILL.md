---
name: aks-diagnose-rollout
description: Diagnose AKS application rollout failures end-to-end across deployment descriptors, Argo CD, startup jobs, images, pods, probes, sidecars, Istio routing, blue-green state, and runtime evidence. Use when a release is stuck, degraded, partially deployed, or failing after deployment.
---

# Diagnose Rollout

1. Read `.digital-platform-ai/aks.yaml`, service metadata, and the `-ops` repository.
2. Establish rollout timeline and target version.
3. Inspect independent signals in parallel:
   - ArgoCD sync/health
   - deployment/ReplicaSet state
   - startup jobs/init containers
   - image pull/version
   - pod readiness/restarts
   - sidecars
   - service/Istio routing
   - blue-green state when applicable
4. Correlate the first failure in time rather than the loudest downstream symptom.
5. Separate deployment failure, runtime failure, networking/mesh failure, and application failure.
6. Do not rollback or promote traffic unless explicitly authorized.

## Output
- Rollout Timeline
- First Confirmed Failure
- Supporting Evidence
- Current Traffic/Version State
- Safe Recommended Action

---
name: aks-inspect-container-images
description: Inspect container images used by AKS workloads, including image repository, tag/digest, pull policy, registry reference, rollout version, ImagePullBackOff, and version drift. Use for image pull failures, wrong-version deployments, registry issues, or release verification.
---

# Inspect Container Images

1. Read expected image metadata from deployment descriptors and service context.
2. Inspect live pod image references, resolved digests, pull policies, and pull failures.
3. Compare expected and running image versions/digests.
4. Identify ImagePullBackOff, authentication, missing image, architecture, or stale-tag issues.
5. Correlate image changes with rollout and application failures.
6. Do not expose registry credentials.

## Output
- Expected Image
- Running Image/Digest
- Pull/Registry Findings
- Version Drift
- Recommended Action

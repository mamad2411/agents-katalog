---
name: kubeblocks-engine-generic
version: "0.1.0"
description: Generic create-time fallback for KubeBlocks engines that do not yet have a dedicated kubeblocks-engine-* entry. Use this only after kubeblocks-preflight and only when the engine is not locked into the Tier-1 dedicated set. The legacy kubeblocks-create-cluster skill remains only as a compatibility shim.
---

# Generic Engine Fallback

Use this only when all three statements are true:

- [kubeblocks-preflight](../kubeblocks-preflight/SKILL.md) has already produced a recommendation bundle.
- `references/coverage/engine-tier-map.yaml` does **not** place the target engine in the Tier-1 dedicated set.
- `references/routing/route-matrix.yaml` allows the request to continue through `kubeblocks-engine-generic`.

## What This Entry Must Decide

Before applying any generic Cluster manifest, make the following explicit:

1. `clusterDef` and `topology`
2. `serviceVersion`
3. `storageClassName` and any topology-aware storage requirement from preflight
4. sizing profile
5. connection / verification plan
6. next-hop operations and observability path

## Generic Workflow

1. Confirm the engine really belongs to the generic fallback.
2. Gather `clusterDef`, `topology`, and component names from the live environment.
3. Fill the preserved generic Cluster template in [legacy reference.md](../kubeblocks-create-cluster/references/reference.md).
4. Validate with `kubectl apply --dry-run=server`.
5. Apply and verify the cluster reaches `Running`.

Never use this as the default path for any Tier-1 engine.

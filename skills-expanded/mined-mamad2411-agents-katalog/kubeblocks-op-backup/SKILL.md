---
name: kubeblocks-op-backup
version: "0.1.0"
description: Primary Day-2 backup entry for KubeBlocks-managed database clusters. Use this for backup workflows on existing clusters. Confirm support in the ops capability matrix when available. The legacy kubeblocks-backup skill remains only as a compatibility shim.
---

# Backup Ops Entry

Use this as the primary Day-2 entry for backup workflows on existing clusters.

## Entry Contract

- Confirm support in [ops-capability-matrix](../../references/coverage/ops-capability-matrix.yaml) before acting.
- Keep create-time provisioning questions on the engine-entry side.
- If support is `unsupported` or `partial`, say that explicitly before you act.
- Route monitoring asks to [kubeblocks-observability-router](../kubeblocks-observability-router/SKILL.md) and broken-state diagnosis to [kubeblocks-troubleshoot](../kubeblocks-troubleshoot/SKILL.md).

## Day-2 Checklist

1. Identify the cluster, engine, and requested action.
2. Confirm the matrix row for that engine and capability.
3. Follow the preserved detailed workflow below when the capability is supported.
4. Verify post-change health and capture the rollback boundary.

## Preserved Detailed Reference

For preserved OpsRequest examples and older command snippets, see [legacy reference](../kubeblocks-backup/references/reference.md).
Do not recommend [kubeblocks-backup](../kubeblocks-backup/SKILL.md) as the primary entry once this `kubeblocks-op-*` entry exists.

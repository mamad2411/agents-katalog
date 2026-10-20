---
name: msk-analyze-storage
description: Analyze Amazon MSK storage for Provisioned clusters including EBS utilization, storage scaling, retention pressure, partition growth, and tiered storage where supported. Use for disk pressure, retention, storage scaling, or cost investigations.
---

# Analyze Storage

1. Identify broker/storage model, current capacity, retention, and topic growth.
2. Inspect storage utilization and growth by broker/topic where evidence is available.
3. Evaluate elastic storage behavior and scaling requirements.
4. Inspect tiered-storage usage only when supported by the cluster/broker configuration.
5. Distinguish retention-driven growth from partition imbalance.
6. Do not reduce retention or delete data without explicit authorization.

## Output
- Storage Model
- Utilization/Growth
- Retention/Partition Findings
- Tiering Assessment
- Recommended Action

---
name: msk-analyze-capacity
description: Analyze Amazon MSK capacity across Provisioned Standard or Express brokers and MSK Serverless, including broker sizing, partition density, throughput, scaling, quotas, and workload growth. Use for sizing, throttling, saturation, or capacity planning.
---

# Analyze Capacity

1. Identify cluster type and applicable capacity model.
2. Inspect ingress/egress, CPU where applicable, partition counts, traffic distribution, and workload peaks.
3. For Provisioned clusters, evaluate broker class/count and scaling options.
4. For Serverless, evaluate workload behavior and service quotas rather than broker sizing.
5. Distinguish cluster capacity from partition skew or slow consumers.
6. Do not resize production capacity unless explicitly authorized.

## Output
- Capacity Model
- Workload Evidence
- Saturation/Quota Findings
- Scaling Options
- Recommended Action

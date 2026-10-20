---
name: kms-analyze-eks-integration
description: Analyze AWS KMS integration with Amazon EKS, including Kubernetes secrets envelope encryption, KMS provider configuration, IAM, CSI/Secrets Store patterns, and pod/runtime access. Use for EKS-hosted workloads that depend on KMS-protected secrets or encryption.
---

# Analyze EKS Integration

1. Identify EKS cluster, region, KMS key, and whether the use case is Kubernetes secrets encryption or external secret retrieval.
2. Inspect cluster encryption configuration and key permissions where applicable.
3. For Secrets Store CSI/external secrets patterns, inspect pod identity/IRSA and secret-provider integration.
4. Correlate pod failures with IAM/KMS/network evidence.
5. Distinguish EKS control-plane encryption from application runtime secret access.
6. Never print secret values or tokens.

## Output
- EKS/KMS Topology
- IAM/Key Findings
- Runtime/CSI Findings
- Failure Layer
- Recommended Action

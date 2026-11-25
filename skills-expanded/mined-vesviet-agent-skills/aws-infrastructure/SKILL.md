---
name: aws-infrastructure
description: Provision, configure, and optimize AWS cloud infrastructure via OpenTofu state KMS encryption, Crossplane Go compositions, Bottlerocket distroless EKS nodes, and IAM Zero-Trust. Use when provisioning VPCs, EKS, RDS, S3, Bedrock, or specialized silicon; authoring EKS Pod Identity roles and SCPs; or enforcing FinOps cost tags.
version: 2.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# AWS Infrastructure

Use this skill when designing, provisioning, or operating AWS cloud infrastructure using OpenTofu v1.13+ with client-side KMS state encryption, Crossplane v2.4+ Go compositions, Bottlerocket distroless EKS nodes, AWS IAM Zero-Trust, Karpenter v1.x autoscaling (or managed EKS Auto Mode), Graviton5/Trainium3/Inferentia2 compute, and Amazon Bedrock PrivateLink isolation.

## When to Use

- provisioning VPCs, Bottlerocket EKS clusters, Aurora/RDS, or S3 storage via OpenTofu or Crossplane
- authoring IAM roles with EKS Pod Identity (v1.31+) or Control Tower Service Control Policies (SCPs)
- deploying sidecarless service networking via AWS VPC Lattice (Gateway API) and IAM SigV4 auth
- configuring Karpenter v1.x declarative autoscaling (EKS Auto Mode as the managed default) with Graviton5 (c9g, m9g, r9g) and Spot fleets
- provisioning Amazon Bedrock PrivateLink VPC endpoints with Guardrails v2 (contextual grounding >= 0.7)
- enforcing FinOps cost allocation tags (`team`, `service`, `environment`, `cost-center`) at apply time
- emitting the `aws-infra-spec.json` machine handoff for downstream DevOps or System Engineers

## Example (OpenTofu KMS & Bottlerocket EKS)

```hcl
terraform {
  encryption {
    key_provider "aws_kms" "primary" {
      kms_key_id = "arn:aws:kms:us-east-1:123456789012:key/state-key-uuid"
      region     = "us-east-1"
      key_spec   = "AES_256"
    }
    method "aes_gcm" "state_encryption" {
      keys = key_provider.aws_kms.primary
    }
    state {
      method   = method.aes_gcm.state_encryption
      enforced = true
    }
    plan {
      method   = method.aes_gcm.state_encryption
      enforced = true
    }
  }
}
```

## Core Rules

- **OPENTOFU-KMS-LOCK**: All IaC state and plans must be client-side encrypted in-memory via OpenTofu v1.13+ using AWS KMS (AES-GCM) with `enforced = true`; unencrypted remote state in S3 is prohibited.
- **CROSSPLANE-COMPOSITION-LOCK**: Universal cloud control planes must use Crossplane v2.4+ Compositions powered by compiled Go functions (`function-go-templating`) or KCL; unstructured YAML patch-and-transform is banned.
- **BOTTLEROCKET-LOCK**: EKS node pools must run AWS Bottlerocket distroless container OS (`amiFamily: Bottlerocket` in `EC2NodeClass`) with SELinux enforcing and dm-verity integrity; general-purpose Linux with shells is prohibited.
- **AWS-IAM-ZERO-TRUST-LOCK**: Enforce IAM Identity Center for humans and EKS Pod Identity (v1.31+) with `pods.eks.amazonaws.com` for workloads; ban static IAM users and long-lived AKIA keys via root SCP.
- **KARPENTER-AUTOSCALING-LOCK**: Compute autoscaling must use EKS Auto Mode (managed Karpenter, default for new clusters) or self-managed Karpenter v1.x `NodePool` manifests with `WhenEmptyOrUnderutilized` consolidation and disruption budgets; static node groups are prohibited.
- **GRAVITON5-FIRST-LOCK**: Default compute to AWS Graviton5 (c9g, m9g, r9g — all GA by 2026-08; Graviton4 only where a Graviton5 family lacks regional availability); Trainium3 (trn3) for AI training and Inferentia2 (inf2) for inference; enforce multi-architecture images (`linux/arm64,linux/amd64`) in CI/CD.
- **VPC-LATTICE-LOCK**: Cross-VPC and cross-account service networking must route through AWS VPC Lattice via Gateway API (`amazon-vpc-lattice`) with IAM SigV4 auth; proxy sidecars are prohibited.
- **BEDROCK-ISOLATION-LOCK**: Bedrock endpoints must route exclusively through PrivateLink VPC endpoints; enforce Guardrails v2 with contextual grounding >= 0.7 and token-level cost attribution.
- **FINOPS-LOCK**: Apply mandatory cost allocation tags (`team`, `service`, `environment`, `cost-center`) enforced via SCP at creation time; review Compute Optimizer rightsizing monthly.
- **GITOPS-LOCK**: All infrastructure state changes must be committed and reviewed before apply; zero console click-ops.

## Suggested Process

### Step 1: Collect Architecture & FinOps Requirements
Ingest system topology from System Engineer (`system-design-spec.json`), security mandates, compliance constraints, and cost allocation tags (`team`, `service`, `environment`, `cost-center`).

### Step 2: Establish Network, Identity & Governance Foundations
Configure multi-account landing zone SCPs, IAM Identity Center, VPC subnets, PrivateLink endpoints, and AWS VPC Lattice Service Network with IAM SigV4 authorization policies.

### Step 3: Author IAM Roles & Workload Federation
Author customer-managed IAM roles with EKS Pod Identity trust policies (`pods.eks.amazonaws.com`). Submit IAM definitions to Security Engineer and validate with IAM Access Analyzer.

### Step 4: Provision Compute, Storage & Managed AI via IaC
Deploy OpenTofu v1.13+ modules with KMS state encryption or Crossplane Go compositions. Configure Bottlerocket EKS clusters, Karpenter Graviton4 NodePools, Aurora Multi-AZ, and Bedrock PrivateLink endpoints.

### Step 5: Validate, Verify & Emit Machine Contract
Verify CIS benchmarks via AWS Config and telemetry via ADOT/CloudWatch. Emit `contracts/schemas/aws-infra-spec.json` for downstream DevOps Engineer consumption.

## Checklist

- [ ] OpenTofu client-side state KMS encryption configured with `enforced = true` on state and plan.
- [ ] Crossplane Compositions authoring with compiled Go functions (`function-go-templating`) or KCL.
- [ ] EKS worker nodes run Bottlerocket distroless OS with SELinux enforcing and dm-verity active.
- [ ] Zero static AKIA access keys; workload credentials federated via EKS Pod Identity (v1.31+).
- [ ] Karpenter v1.x autoscaling (or EKS Auto Mode) configured with Graviton5 and `WhenEmptyOrUnderutilized` consolidation.
- [ ] VPC Lattice Gateway API configured with IAM SigV4 authorization; zero proxy sidecars.
- [ ] Bedrock accessed exclusively via PrivateLink; Guardrails v2 configured with grounding >= 0.7.
- [ ] Mandatory cost allocation tags (`team`, `service`, `environment`, `cost-center`) enforced by SCP.
- [ ] `contracts/schemas/aws-infra-spec.json` emitted and validated against schema.

## Output Contracts

When provisioning or updating AWS cloud infrastructure as part of a multi-role delivery, emit:

- **`contracts/schemas/aws-infra-spec.json`** — Emitted upon IaC specification and staging verification to document provisioned cloud resources, endpoints, IAM roles, and FinOps cost allocation tags. Set `produced_by_role: aws-engineer`.
- **`contracts/schemas/deployment-plan.json`** — Emitted when infrastructure modifications require an ordered rollout plan, documenting infrastructure changes, configuration updates, and validation runs.

Skip emission for local sandbox experimentation where no cloud resources are provisioned.

## Failure Modes

- **Unencrypted State in S3**: IaC state stored unencrypted. Mitigation: Enforce `OPENTOFU-KMS-LOCK` with AES-GCM client-side encryption and S3 bucket policy denying unencrypted uploads.
- **Drift in Control Planes**: Cloud resources drift out-of-band. Mitigation: Enforce `CROSSPLANE-COMPOSITION-LOCK` with closed-loop reconciliation and compiled Go functions.
- **Host Compromise on Worker Nodes**: SSH or shell injection into host. Mitigation: Enforce `BOTTLEROCKET-LOCK`; distroless root filesystem with dm-verity halts modified nodes.
- **Leaked Long-Lived Credentials**: AKIA key compromised. Mitigation: Enforce `AWS-IAM-ZERO-TRUST-LOCK`; root SCP denies `iam:CreateAccessKey`; use IAM Identity Center and EKS Pod Identity.
- **Ungrounded LLM Responses**: AI hallucination or prompt injection. Mitigation: Enforce `BEDROCK-ISOLATION-LOCK` with Guardrails v2 contextual grounding >= 0.7 and PrivateLink.
- **Unattributed Cloud Spending**: Resources created without tags. Mitigation: Enforce `FINOPS-LOCK`; SCP denies resource creation missing `team`, `service`, `environment`, or `cost-center`.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: Enforce EKS Pod Identity and IAM Identity Center; reject wildcard permissions; run IAM Access Analyzer before apply.
- **ASI04 Agentic Supply Chain**: Mandate Bottlerocket distroless AMI and ECR immutable KMS-encrypted repositories; verify Bedrock PrivateLink isolation.
- **ASI05 Unexpected Code Execution**: Never execute unvalidated scripts on EC2 hosts; manage Bottlerocket via transactional `apiclient` API without interactive shells.
- **ASI07 Insecure Inter-Agent Communication**: Treat `aws-infra-spec.json` as authoritative contract; validate schema before handing off to DevOps Engineer.
- **ASI09 Human-Agent Trust Exploitation**: Always surface wildcard permissions and unencrypted endpoints honestly; do not claim compliance without verification.

## Related Skills

- **setup-deployment**: For deploying application workloads and GitOps pipelines on top of provisioned AWS infrastructure.
- **add-telemetry-instrumentation**: For configuring ADOT collectors, CloudWatch Application Signals, and X-Ray tracing.
- **manage-secrets**: For configuring AWS Secrets Manager and External Secrets Operator (ESO) integration.
- **security-audit**: For auditing IAM policies, SCPs, and CIS AWS Foundations benchmarks.
- **system-design**: For cross-cloud architecture and hardware capacity modeling.
- Companion reference: `references/opentofu-aws-zero-trust-and-irsa.md`
- Companion example: `examples/opentofu-eks-pod-identity-vpc.tf`

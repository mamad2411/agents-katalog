---
name: aws-core
description: Apply AWS Well-Architected defaults for the most-used services (IAM, VPC, S3, EC2/ECS/Lambda, RDS, DynamoDB, KMS, CloudWatch). Use when designing or reviewing AWS workloads, hardening accounts, or selecting between compute, storage, and data services.
source: self
date_added: 2026-04-30
---

# AWS Core

Default configurations and decision guides for the AWS services that underpin most workloads. Pair with [landing-zones](../landing-zones/) for org/account baseline and [finops](../finops/) for cost control.

## When to Use

- Designing a new service on AWS or reviewing an existing one.
- Picking between compute (Lambda vs ECS vs EKS vs EC2) or data services (RDS vs Aurora vs DynamoDB).
- Hardening IAM, VPC, encryption, and logging defaults.
- Triaging cost, latency, or reliability issues on AWS.

## IAM Defaults

- **Root account**: hardware MFA, no access keys, alarms on use.
- **No long-lived user credentials in workloads** — use IAM Roles via instance profile, ECS task role, Lambda execution role, IRSA on EKS, or **IAM Identity Center** for humans.
- **Least privilege**: start from AWS-managed policies, then trim with Access Analyzer; deny `iam:*` and `kms:*` broadly.
- **SCPs at the org** prevent disabling CloudTrail, GuardDuty, Config; restrict regions; block public S3 ACLs.
- **Permission boundaries** on developer-creatable roles.
- Rotate any unavoidable access keys < 90 days; prefer **IAM Roles Anywhere** for on-prem.

## VPC Defaults

- Three AZs minimum for prod. Private subnets for workloads, public only for ALB/NAT.
- **VPC endpoints** (Gateway for S3/DynamoDB; Interface for STS, KMS, Secrets Manager, ECR, logs) to avoid NAT cost and keep traffic on the AWS network.
- Security groups by role (`sg-app`, `sg-db`); reference SGs by ID, not CIDRs.
- **VPC Flow Logs** on; **AWS Network Firewall** or third-party for egress filtering when required.
- IPv6 dual-stack for new VPCs where supported.

## Compute Decision Guide

| Workload | Pick |
| --- | --- |
| Event-driven, spiky, <15 min, no warm cache need | **Lambda** |
| Long-running container, predictable load, want simple | **ECS on Fargate** |
| Many services, K8s ecosystem, multi-tenant platform | **EKS** (with managed node groups or Fargate) |
| Need GPUs, custom kernel, or specialized AMI | **EC2** (or EKS with node groups) |
| Batch jobs | **AWS Batch** on Fargate/EC2 |

Defaults: ARM (Graviton) instances unless a binary forces x86. Spot for batch and stateless tiers.

## Data Services

| Need | Pick |
| --- | --- |
| Transactional RDBMS | **Aurora PostgreSQL** (or RDS PG); MySQL only if required |
| Single-digit-ms key/value, predictable scale, multi-region | **DynamoDB** with on-demand or provisioned + auto-scaling |
| Object storage | **S3** (Intelligent-Tiering by default) |
| Analytics/lakehouse | **S3 + Iceberg + Athena**, or Redshift Serverless for BI |
| Cache | **ElastiCache for Valkey/Redis** (multi-AZ) |
| Search | **OpenSearch Serverless** (or self-managed for cost at scale) |
| Streaming | **MSK** (Kafka) or **Kinesis Data Streams** |
| Files (POSIX) | **EFS** (general) or **FSx** (specialized) |

Aurora: enable Storage Auto Scaling, Performance Insights, automated backups (>=14d), Blue/Green deploys for upgrades. DynamoDB: design partition key for uniform access; PITR on; use Streams for change capture.

## Storage Defaults (S3)

- Block Public Access at account + bucket.
- SSE-KMS with customer-managed keys for sensitive data; bucket key on.
- Versioning + lifecycle rules (transition + expire noncurrent).
- Object Lock for compliance/WORM.
- Access logs to a separate logging account bucket.
- Use **S3 Access Points** for multi-tenant access patterns.

## Encryption & Secrets

- KMS CMKs per data domain; key rotation enabled; key policies grant by role, not user.
- Secrets in **Secrets Manager** (auto-rotation for RDS) or **SSM Parameter Store** (SecureString) for simpler config.
- TLS 1.2+ enforced on ALB/CloudFront; ACM for certs (auto-renew).

## Networking & Edge

- Public APIs behind **CloudFront + WAF** (managed rule sets + rate-based rules).
- Private inter-VPC traffic via **Transit Gateway** or **VPC Peering**; **PrivateLink** for SaaS-style exposure.
- Route 53 health checks + failover for multi-region.

## Observability

- **CloudWatch Logs** with retention set per log group (no infinite default).
- **CloudWatch Metrics + Alarms**, **Container Insights** on ECS/EKS.
- **AWS X-Ray** or OpenTelemetry via ADOT collector for traces.
- **CloudTrail** org-wide to a logging account; **Config** + conformance packs.
- **GuardDuty**, **Security Hub**, **Inspector** on across the org.

## Cost Defaults

- Required tags: `app`, `env`, `owner`, `cost-center` enforced via SCP/Config.
- **Compute Savings Plans** for stable baseline; Spot for flex.
- S3 Intelligent-Tiering; lifecycle to Glacier Deep Archive for cold backups.
- Budget alerts per account/team.

## Anti-Patterns

- IAM users with `AdministratorAccess` for CI/CD instead of OIDC federation (`aws-actions/configure-aws-credentials`).
- Single-AZ RDS in production; backups disabled; no read replicas.
- NAT Gateway in every AZ for traffic that could go through a VPC endpoint.
- DynamoDB scans on hot paths.
- CloudWatch Logs without retention (silent cost growth).
- Region-pinning to `us-east-1` for global users without CloudFront.
- Hand-clicked changes in console — use IaC (Terraform/CDK).

## Quality Gates

- IaC for all production resources; drift detection on.
- Org-wide CloudTrail, Config, GuardDuty enabled and logged centrally.
- Backups + restore rehearsed (RDS, DynamoDB PITR, S3 versioning).
- WAF + CloudFront in front of public origins.
- Cost anomaly detection and per-team budgets.

## References

- AWS Well-Architected Framework (six pillars)
- AWS Prescriptive Guidance
- AWS Security Reference Architecture

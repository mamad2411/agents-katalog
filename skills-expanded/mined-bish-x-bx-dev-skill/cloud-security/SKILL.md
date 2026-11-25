---
name: "cloud-security"
description: "Use when assessing cloud infrastructure for security misconfigurations, IAM privilege escalation paths, S3 public exposure, open security group rules, or IaC security gaps. Covers AWS, Azure, and GCP posture assessment with MITRE ATT&CK mapping."
---

# Cloud Security

Cloud security posture assessment skill for detecting IAM privilege escalation, public storage exposure, network configuration risks, and infrastructure-as-code misconfigurations. This is NOT active cloud compromise response or application vulnerability scanning (see security-pentest in review-qa/) — this is about systematic cloud configuration analysis to prevent exploitation.

---

## Table of Contents

- [Overview](#overview)
- [Manual Cloud Posture Review](#manual-cloud-posture-review)
- [IAM Policy Analysis](#iam-policy-analysis)
- [S3 Exposure Assessment](#s3-exposure-assessment)
- [Security Group Analysis](#security-group-analysis)
- [IaC Security Review](#iac-security-review)
- [Cloud Provider Coverage Matrix](#cloud-provider-coverage-matrix)
- [Workflows](#workflows)
- [Anti-Patterns](#anti-patterns)
- [Cross-References](#cross-references)

---

## Overview

### What This Skill Does

This skill provides the methodology and tooling for **cloud security posture management (CSPM)** — systematically checking cloud configurations for misconfigurations that create exploitable attack surface. It covers IAM privilege escalation paths, storage public exposure, network over-permissioning, and infrastructure code security.

### Distinction from Other Security Skills

| Skill | Focus | Approach |
|-------|-------|----------|
| **cloud-security** (this) | Cloud configuration risk | Preventive — assess before exploitation |
| Incident response process | Active cloud incidents | Reactive — triage confirmed cloud compromise |
| threat-detection | Behavioral anomalies | Proactive — hunt for attacker activity in cloud logs |
| security-pen-testing | Application vulnerabilities | Offensive — actively exploit found weaknesses |

### Prerequisites

Read access to IAM policy documents, S3 bucket configurations, and security group rules in JSON format. For continuous monitoring, integrate with cloud provider APIs (AWS Config, Azure Policy, GCP Security Command Center).

---

## Manual Cloud Posture Review

This public skill does not bundle an executable posture checker. Export cloud configuration as JSON or IaC, then review it against the IAM, storage, network, and IaC matrices below and the expanded `references/cspm-checks.md` reference.

Recommended inputs:

| Input | Review focus |
|-------|--------------|
| IAM policy documents and trust policies | Privilege escalation combinations, wildcard actions, public principals |
| S3 or object-storage bucket configs | Public access, ACLs, bucket policies, encryption |
| Security group / NSG / firewall rules | Internet exposure, admin ports, database ports |
| Terraform, CloudFormation, Bicep, or Kubernetes manifests | Misconfigurations before deployment |
| Cloud context | Internet-facing and regulated-data workloads need higher severity |

Critical findings require immediate remediation. If evidence suggests active exploitation, hand off to the organization's incident response process.

---

## IAM Policy Analysis

IAM analysis detects privilege escalation paths, overprivileged grants, public principal exposure, and data exfiltration risk.

### Privilege Escalation Patterns

| Pattern | Severity | Key Action Combination | MITRE |
|---------|----------|------------------------|-------|
| Lambda PassRole escalation | Critical | iam:PassRole + lambda:CreateFunction | T1078.004 |
| EC2 instance profile abuse | Critical | iam:PassRole + ec2:RunInstances | T1078.004 |
| CloudFormation PassRole | Critical | iam:PassRole + cloudformation:CreateStack | T1078.004 |
| Self-attach policy escalation | Critical | iam:AttachUserPolicy + sts:GetCallerIdentity | T1484.001 |
| Inline policy self-escalation | Critical | iam:PutUserPolicy + sts:GetCallerIdentity | T1484.001 |
| Policy version backdoor | Critical | iam:CreatePolicyVersion + iam:ListPolicies | T1484.001 |
| Credential harvesting | High | iam:CreateAccessKey + iam:ListUsers | T1098.001 |
| Group membership escalation | High | iam:AddUserToGroup + iam:ListGroups | T1098 |
| Password reset attack | High | iam:UpdateLoginProfile + iam:ListUsers | T1098 |
| Service-level wildcard | High | iam:* or s3:* or ec2:* | T1078.004 |

### IAM Finding Severity Guide

| Finding Type | Condition | Severity |
|-------------|-----------|----------|
| Full admin wildcard | Action=* Resource=* | Critical |
| Public principal | Principal: '*' | Critical |
| Dangerous action combo | Two-action escalation path | Critical |
| Individual priv-esc actions | On wildcard resource | High |
| Data exfiltration actions | s3:GetObject, secretsmanager:GetSecretValue on * | High |
| Service wildcard | service:* action | High |
| Data actions on named resource | Appropriate scope | Low/Clean |

### Least Privilege Recommendations

For every critical or high finding, the tool outputs a `least_privilege_suggestion` field with specific remediation guidance:
- Replace `Action: *` with a named list of required actions
- Replace `Resource: *` with specific ARN patterns
- Use AWS Access Analyzer to identify actually-used permissions
- Separate dangerous action combinations into different roles with distinct trust policies

---

## S3 Exposure Assessment

S3 assessment checks four dimensions: public access block configuration, bucket ACL, bucket policy principal exposure, and default encryption.

### S3 Configuration Check Matrix

| Check | Finding Condition | Severity |
|-------|------------------|----------|
| Public access block | Any of four flags missing/false | High |
| Bucket ACL | public-read-write | Critical |
| Bucket ACL | public-read or authenticated-read | High |
| Bucket policy Principal | "Principal": "*" with Allow | Critical |
| Default encryption | No ServerSideEncryptionConfiguration | High |
| Default encryption | Non-standard SSEAlgorithm | Medium |
| No PublicAccessBlockConfiguration | Status unknown | Medium |

### Recommended S3 Baseline Configuration

```json
{
  "PublicAccessBlockConfiguration": {
    "BlockPublicAcls": true,
    "BlockPublicPolicy": true,
    "IgnorePublicAcls": true,
    "RestrictPublicBuckets": true
  },
  "ServerSideEncryptionConfiguration": {
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "aws:kms",
        "KMSMasterKeyID": "arn:aws:kms:region:account:key/key-id"
      },
      "BucketKeyEnabled": true
    }]
  },
  "ACL": "private"
}
```

All four public access block settings must be enabled at both the bucket level and the AWS account level. Account-level settings can be overridden by bucket-level settings if not both enforced.

---

## Security Group Analysis

Security group analysis flags inbound rules that expose admin ports, database ports, or all traffic to internet CIDRs (0.0.0.0/0, ::/0).

### Critical Port Exposure Rules

| Port | Service | Finding Severity | Remediation |
|------|---------|-----------------|-------------|
| 22 | SSH | Critical | Restrict to VPN CIDR or use AWS Systems Manager Session Manager |
| 3389 | RDP | Critical | Restrict to VPN CIDR or use AWS Fleet Manager |
| 0–65535 (all) | All traffic | Critical | Remove rule; add specific required ports only |

### High-Risk Database Port Rules

| Port | Service | Finding Severity | Remediation |
|------|---------|-----------------|-------------|
| 1433 | MSSQL | High | Allow from application tier SG only — move to private subnet |
| 3306 | MySQL | High | Allow from application tier SG only — move to private subnet |
| 5432 | PostgreSQL | High | Allow from application tier SG only — move to private subnet |
| 27017 | MongoDB | High | Allow from application tier SG only — move to private subnet |
| 6379 | Redis | High | Allow from application tier SG only — move to private subnet |
| 9200 | Elasticsearch | High | Allow from application tier SG only — move to private subnet |

### Severity Modifiers

Use `--severity-modifier internet-facing` when the assessed resource is directly internet-accessible (load balancer, API gateway, public EC2). Use `--severity-modifier regulated-data` when the resource handles PCI, HIPAA, or GDPR-regulated data. Both modifiers bump each finding's severity by one level.

---

## IaC Security Review

Infrastructure-as-code review catches configuration issues at definition time, before deployment.

### IaC Check Matrix

| Tool | Check Types | When to Run |
|------|-------------|-------------|
| Terraform | Resource-level checks (aws_s3_bucket_acl, aws_security_group, aws_iam_policy_document) | Pre-plan, pre-apply, PR gate |
| CloudFormation | Template property validation (PublicAccessBlockConfiguration, SecurityGroupIngress) | Template lint, deploy gate |
| Kubernetes manifests | Container privileges, network policies, secret exposure | PR gate, admission controller |
| Helm charts | Same as Kubernetes | PR gate |

### Terraform IAM Policy Example — Finding vs. Clean

```hcl
# BAD: Will generate critical findings
resource "aws_iam_policy" "bad_policy" {
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}

# GOOD: Least privilege
resource "aws_iam_policy" "good_policy" {
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject", "s3:PutObject"]
      Resource = "arn:aws:s3:::my-specific-bucket/*"
    }]
  })
}
```

Full CSPM check reference: `references/cspm-checks.md`

---

## Cloud Provider Coverage Matrix

| Check Type | AWS | Azure | GCP |
|-----------|-----|-------|-----|
| IAM privilege escalation | Full (IAM policies, trust policies, ESCALATION_COMBOS) | Partial (RBAC assignments, service principal risks) | Partial (IAM bindings, workload identity) |
| Storage public access | Full (S3 bucket policies, ACLs, public access block) | Partial (Blob SAS tokens, container access levels) | Partial (GCS bucket IAM, uniform bucket-level access) |
| Network exposure | Full (Security Groups, NACLs, port-level analysis) | Partial (NSG rules, inbound port analysis) | Partial (Firewall rules, VPC firewall) |
| IaC scanning | Full (Terraform, CloudFormation) | Partial (ARM templates, Bicep) | Partial (Deployment Manager) |

---

## Workflows

### Workflow 1: Quick Posture Check (20 Minutes)

For a newly provisioned resource or pre-deployment review:

```bash
# 1. Export IAM policy document
aws iam get-policy-version --policy-arn ARN --version-id v1 | \
  jq '.PolicyVersion.Document' > policy.json
# Review policy.json against the IAM privilege escalation matrix.

# 2. Check S3 bucket configuration
aws s3api get-bucket-acl --bucket my-bucket > acl.json
aws s3api get-public-access-block --bucket my-bucket >> bucket.json
# Review acl.json and bucket.json against the S3 exposure matrix.

# 3. Review security groups for open admin ports
aws ec2 describe-security-groups --group-ids sg-123456 | \
  jq '.SecurityGroups[0]' > sg.json
# Review sg.json against the security group analysis tables.
```

**Decision**: Critical findings block deployment and require remediation. High findings should be remediated within 24 hours or formally accepted with owner and expiry.

### Workflow 2: Full Cloud Security Assessment (Multi-Day)

**Day 1 — IAM and Identity:**
1. Export all IAM policies attached to production roles
2. Review each policy against the IAM privilege escalation and severity guide tables
3. Map all privilege escalation paths found
4. Identify overprivileged service accounts and roles
5. Review cross-account trust policies

**Day 2 — Storage and Network:**
1. Enumerate all S3 buckets and export configurations
2. Apply regulated-data severity modifiers for data buckets
3. Export security group configurations for all VPCs
4. Apply internet-facing severity modifiers for public resources
5. Review NACL rules for network segmentation gaps

**Day 3 — IaC and Continuous Integration:**
1. Review Terraform/CloudFormation templates in version control
2. Check CI/CD pipeline for IaC security gates
3. Validate findings against `references/cspm-checks.md`
4. Produce remediation plan with priority ordering (Critical → High → Medium)

### Workflow 3: CI/CD Security Gate

Integrate posture checks into deployment pipelines to prevent misconfigured resources reaching production:

```bash
# Validate IaC before terraform apply
terraform show -json plan.json | \
  jq '[.resource_changes[].change.after | select(. != null)]' > resources.json
# Review resources.json with the matrices in this skill or the repo's configured IaC scanner.
# Block deployment on critical cloud security findings.

# Validate existing S3 bucket before modifying
aws s3api get-bucket-policy --bucket "${BUCKET}" | jq '.Policy | fromjson' > bucket-policy.json
# Review bucket-policy.json for public principals and regulated-data exposure.
```

---

## Anti-Patterns

1. **Running IAM analysis without checking escalation combos** — Individual high-risk actions in isolation may appear low-risk. The danger is in combinations: `iam:PassRole` alone is not critical, but `iam:PassRole + lambda:CreateFunction` is a confirmed privilege escalation path. Always analyze the full statement, not individual actions.
2. **Enabling only bucket-level public access block** — AWS S3 has both account-level and bucket-level public access block settings. A bucket-level setting can override an account-level setting. Both must be configured. Account-level block alone is insufficient if any bucket has explicit overrides.
3. **Treating `--severity-modifier internet-facing` as optional for public resources** — Internet-facing resources have significantly higher exposure than internal resources. High findings on internet-facing infrastructure should be treated as critical. Always apply `--severity-modifier internet-facing` for DMZ, load balancer, and API gateway configurations.
4. **Checking only administrator policies** — Privilege escalation paths frequently originate from non-administrator policies that combine innocuous-looking permissions. All policies attached to production identities must be checked, not just policies with obvious elevated access.
5. **Remediating findings without root cause analysis** — Removing a dangerous permission without understanding why it was granted will result in re-addition. Document the business justification for every high-risk permission before removing it, to prevent silent re-introduction.
6. **Ignoring service account over-permissioning** — Service accounts are often over-provisioned during development and never trimmed for production. Every service account in production must be audited against AWS Access Analyzer or equivalent to identify and remove unused permissions.
7. **Not applying severity modifiers for regulated data workloads** — A high finding in a general-purpose S3 bucket is different from the same finding in a bucket containing PHI or cardholder data. Always use `--severity-modifier regulated-data` when assessing resources in regulated data environments.

---

## Cross-References

| Skill | Relationship |
|-------|-------------|
| Incident response process | Critical findings such as public sensitive storage or active privilege escalation may trigger incident classification |
| [threat-detection](../threat-detection/SKILL.md) | Cloud posture findings create hunting targets — over-permissioned roles are likely lateral movement destinations |
| Red team exercises | Controlled adversarial exercises can test exploitability of cloud misconfigurations found in posture assessment |
| security-pentest (in review-qa/) | Cloud posture findings feed into the infrastructure security section of pen test assessments |

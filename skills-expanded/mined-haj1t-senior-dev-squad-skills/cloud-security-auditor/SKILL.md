---
name: cloud-security-auditor
description: "AWS, GCP, Azure security auditing, IaC scanning, IAM analysis, network security, compliance mapping. Use when auditing cloud infrastructure for security gaps."
---

# Cloud Security Auditor

## Overview

This skill audits Infrastructure as Code (IaC) templates (Terraform, CloudFormation, Pulumi) and active cloud configurations (AWS, GCP, Azure) for security vulnerabilities. It analyzes IaC configurations for misconfigurations (e.g., public S3 buckets, open security groups, unencrypted volumes), checks IAM rules for over-privileged roles, unused permissions, and privilege escalation paths, audits network security settings (VPC setups, security groups, NACLs), and verifies data protection policies (encryption at rest/transit, KMS key rotation, bucket policies). The objective is to provide a measurable assessment of cloud security alignment using CIS Benchmarks and NIST CSF frameworks.

**Core principle:** Insecure by default. Anything that is not explicitly authorized is forbidden, particularly in cloud environments.

## The Iron Law

```
NO IaC TEMPLATE CAN BE DEPLOYED TO PRODUCTION WITHOUT UNDERGOING SECURITY SCANNING AND BEING AUDITED AGAINST AT LEAST ONE CIS BENCHMARK CONTROL.
```

Any resource deployed without static configuration scanning is assumed to be insecure.

## When to Use

**Use this when:**
- An Infrastructure as Code (Terraform, CloudFormation, Pulumi) template is created and requires pre-deployment scanning.
- You need to audit the security posture of an active cloud environment (AWS Account, GCP Project, Azure Subscription).
- Reviewing IAM roles and policies to detect over-privileged access, unused permissions, or privilege escalation paths.
- Verifying network security configurations (VPC subnets, security group rules, network ACLs).
- Confirming data protection configurations (encryption, KMS key rotation, bucket policies).
- Preparing for a CIS Benchmark or NIST CSF compliance audit.

**Use this ESPECIALLY when:**
- Hearing "this is just a development environment, security is secondary" — development environments are critical if they can access production data or host source code.
- Setting up a new cloud account to verify that root access and initial resources conform to baseline security requirements.
- Migrating configurations between cloud providers, where the underlying security models and terminology differ.

**Don't skip when:**
- No cloud resources have been written or declared yet — draft the initial IaC templates first, then execute the scans.
- You lack read permissions or access keys to inspect the cloud environment.

## Phase 1: IaC Security Scanning (Terraform / CloudFormation / Pulumi)

**BEFORE proceeding:**

Collect all IaC configuration files into a target directory. If using remote backends (e.g., S3 tfstate), ensure you have read access to the state files.

1. **Trigger automated scans** using Checkov, Terrascan, or tfsec across all template directories.
2. **Map findings to CIS Benchmark IDs** (e.g., CKV_AWS_53 mapping to S3 bucket public access).
3. **Analyze findings for false positives** through manual verification of the configuration files.
4. **Scan state and variables** for hardcoded secrets or plain-text credentials.

```bash
# Terraform security scan
cd terraform/
checkov -d . --framework terraform --output cli
# or
tfsec . --no-color --format json > tfsec-report.json

# CloudFormation security scan
cfn_nag_scan --input-path ./cloudformation/
```

```yaml
# Checkov findings entry example with CIS mapping
- file: "main.tf:123"
  resource: "aws_s3_bucket.assets"
  check: "CKV_AWS_53"
  severity: "CRITICAL"
  # CIS AWS Foundations Benchmark 2.1.1
  description: "S3 Bucket allows public ACL settings"
  recommendation: "Attach an aws_s3_bucket_public_access_block resource"
  status: "FAILED"
```

## Phase 2: IAM Audit — Roles, Policies, and Privilege Escalation

**BEFORE proceeding:**

Ensure the IaC scanning phase is completed and IAM resources (users, groups, roles, and policies) are cataloged.

1. **Locate over-privileged definitions:**
   - Roles assigned the `AdministratorAccess` policy.
   - Statements using `*` or wildcard actions.
   - Resource statements defined as `*`.
2. **Check for unused permissions** (e.g., credentials or access keys that have not logged API activity in over 90 days).
3. **Audit privilege escalation paths:**
   - `iam:PassRole` combined with `ec2:RunInstances` permissions.
   - `lambda:CreateFunction` paired with `iam:PassRole` permissions.
   - `iam:CreateAccessKey` permissions assigned to non-admin identities.
4. **Verify MFA status** for console users, flagging any human accounts without active MFA.
5. **Inspect trust policies for service roles** to confirm external ID enforcement on cross-account roles.

```terraform
# INSECURE IAM policy definition (will be caught during the scan)
resource "aws_iam_policy" "too_broad" {
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = ["s3:*", "ec2:*", "iam:*"]     # Overly broad actions
        Effect = "Allow"
        Resource = "*"                           # Wildcard resource
      }
    ]
  })
}

# SECURE ALTERNATIVE:
# - Implement least privilege principles
# - Restrict resources to specific ARNs
# - Apply conditions (e.g., IP range restrictions)
```

## Phase 3: Network Security Audit (VPC, Security Groups, NACLs)

**BEFORE proceeding:**

Confirm that VPC configuration files (subnets, security groups, network ACLs) are present in the IaC configuration or active cloud inventory.

1. **Audit Security Group rules:**
   - Open ports (`0.0.0.0/0` or `::/0`) pointing to management interfaces or databases: 22 (SSH), 3389 (RDP), 3306 (MySQL), 5432 (PostgreSQL), 6379 (Redis), 9200 (Elasticsearch).
   - Inbound rules configured for all ports (port ranges 0-65535).
2. **Audit Network ACLs:**
   - Verify that default ingress rules have been hardened.
   - Ensure ephemeral port rules (1024-65535) are configured correctly.
3. **Verify VPC Flow Logs** status to confirm they are enabled and publishing logs to S3 or CloudWatch.
4. **Locate public-facing resources** (e.g., database instances or cache clusters running in public subnets with public IP addresses).
5. **Verify routing policies** on VPC peering links, VPN tunnels, and Direct Connect connections for encryption status.

```bash
# Querying open security groups via AWS CLI
aws ec2 describe-security-groups \
  --query "SecurityGroups[?IpPermissions[?contains(IpRanges[].CidrIp, '0.0.0.0/0')]]" \
  --output table | grep -E "(GroupName|FromPort|CidrIp)"
```

```yaml
network_findings:
  public_port_22:
    resource: "aws_security_group.bastion_sg"
    port: 22
    cidr: "0.0.0.0/0"
    severity: "HIGH"
    # CIS AWS Foundations Benchmark 4.1
    remediation: "Restrict SSH access to specified corporate CIDR ranges only."
  
  rds_public:
    resource: "aws_db_instance.production_db"
    publicly_accessible: true
    severity: "CRITICAL"
    remediation: "Set publicly_accessible to false and move RDS to a private subnet."
```

## Phase 4: Data Protection Audit

**BEFORE proceeding:**

Compile a listing of all active storage resources (buckets, database instances, key management stores, block storage volumes).

1. **Verify encryption at rest:**
   - Confirm EBS/block storage volumes have encryption enabled.
   - Check RDS instances and DynamoDB tables for encryption status.
   - Ensure S3/GCS buckets have default encryption configurations active (AES-256 or custom KMS keys).
2. **Verify encryption in transit:**
   - Audit SSL/TLS configurations on load balancers, CDNs, and API gateways.
   - Confirm database connections enforce TLS (e.g., checking `force_ssl` parameters).
   - Verify S3 bucket policies contain statements denying non-HTTPS traffic.
3. **Verify KMS configuration:**
   - Check if KMS key rotation is enabled (minimum of annual rotation).
   - Audit cross-account access configurations on key policies.
   - Ensure customer-managed keys (CMKs) are applied to sensitive datastores instead of default AWS-managed keys.
4. **Audit bucket access policies:**
   - Search for policies containing wildcard `Principal: "*"` rules.
   - Ensure access control lists (ACLs) are configured to block public reading and writing of objects.

```python
# S3 Bucket encryption audit checklist
s3_buckets_checked = [
    {"bucket": "prod-logs", "encryption": "AES256", "public_block": True, "status": "OK"},
    {"bucket": "backup-data", "encryption": "NONE", "public_block": True, "status": "FAIL"},
    {"bucket": "old-company-data", "encryption": "NONE", "public_block": False, "status": "CRITICAL"},
]

# KMS Key rotation checklist
kms_keys = [
    {"key_id": "arn:aws:kms:us-east-1:xxx:key/yyy", "rotation": True, "auto_rotate": True},
    {"key_id": "arn:aws:kms:us-east-1:xxx:key/zzz", "rotation": False, "auto_rotate": False},
]
```

## Phase 5: Compliance Mapping and Remediation

**BEFORE proceeding:**

Consolidate findings from the IaC scan, IAM audit, network security check, and data protection review.

1. **Map each security finding to a CIS Benchmark ID:**
   - CIS AWS Foundations Benchmark (or relevant GCP/Azure equivalent).
2. **Assign the corresponding NIST CSF subcategory:**
   - Public bucket → PR.DS-1 (Data Security).
   - Over-privileged IAM → PR.AC-1 (Identity and Access Management).
   - Open security group → PR.AC-3 (Network Security).
   - Flow logs disabled → DE.CM-1 (Security Monitoring).
3. **Prioritize remediation** (Critical > High > Medium > Low).
4. **Draft executable remediation code** (e.g., providing corrected Terraform block syntax rather than abstract advice).

```yaml
compliance_mapping:
  finding: "S3 Bucket allows public access"
  cis_id: "CIS AWS 2.1.1"
  nist_csf: "PR.DS-1"
  severity: "CRITICAL"
  remediation: |
    resource "aws_s3_bucket_public_access_block" "this" {
      bucket                  = aws_s3_bucket.this.id
      block_public_acls       = true
      block_public_policy     = true
      ignore_public_acls      = true
      restrict_public_buckets = true
    }
```

## Final Verification Check:

- [ ] Have all IaC templates been scanned using tfsec, Checkov, or equivalent automated linters?
- [ ] Are IAM policies and role configurations verified against least privilege baselines?
- [ ] Are all security groups audited for ingress rules configured to 0.0.0.0/0?
- [ ] Is encryption at rest validated on all storage volumes, database hosts, and bucket stores?
- [ ] Is key rotation enabled on all customer-managed KMS keys?
- [ ] Has every critical and high vulnerability been mapped to a CIS Benchmark check?
- [ ] Is every vulnerability mapped to its corresponding NIST CSF subcategory?
- [ ] Have executable remediation blocks been written for all reported findings?
- [ ] Are confirmed false positives documented with justifications?
- [ ] Does the audit report include both technical code modifications and an executive summary?

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "This dev environment can be relaxed; it does not require production security controls" — **Dev environments are target access routes; audit dev environments with the same rigor as production.**
- "This bucket must be public since it hosts static web assets" — **Enforce bucket policies restricting access to designated CDN origins instead of opening public ACLs.**
- "The IAM statement contains wildcards, but only trusted operators can assume the role" — **Wildcards invite credential reuse; refactor to include specific target resources.**
- "We opened port 22 to all IPs temporarily for debugging; we will close it later" — **Temporary configurations persist; use IaC code pull requests to track and revoke changes.**
- "The CIS rules are too stringent for our setup; we can skip them" — **CIS Benchmarks represent foundational security postures; align to the baseline controls.**

**ALL OF THESE MEAN: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Why didn't you flag this S3 bucket as public?" — You missed auditing S3 ACLs or block public access settings.
- "You missed this privilege escalation path in the IAM roles" — Re-analyze policies for `iam:PassRole` permissions.
- "This CIS Benchmark mapping is incorrect" — Verify check metadata against the selected framework version.
- "VPC Flow Logs are disabled here; did you check that?" — You skipped verifying logging configurations.
- "The remediation plan is missing the IaC configuration blocks" — Provide deployable code blocks instead of text descriptions.
- "This finding is a true positive, not a false positive" — Validate local state and policy configurations.

**When you see these:** STOP. Return to the relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "IaC scans are redundant for dev environments." | Vulnerabilities in dev configurations propagate to production via templates. Scan every stage. |
| "A public bucket is fine for static frontend code." | Open write access allows code injection. Use Origin Access Control (OAC) with a CDN. |
| "We will refactor the wildcard IAM policies later." | Legacy wildcards are rarely audited post-deployment. Enforce least privilege immediately. |
| "CIS rules are too complex for our organization." | Apply the Tier 1 baseline checks first to mitigate common cloud misconfigurations. |
| "The security group is protected because the subnet is private." | Subnet boundaries do not prevent lateral movement if hosts are compromised. Apply ingress filters. |
| "MFA is only necessary for production console logins." | Compromised credentials on any account can lead to data leaks or billing exploits. |

## Related Skills

- **nist-csf-scanner** — Map Cloud Security Auditor findings to NIST CSF functions (PR, DE, ID).
- **mitre-attack-mapper** — Align cloud misconfigurations to MITRE ATT&CK techniques.

## Self-Review

After completing this process:

1. **Audit Scope:** Have all configuration directories, IAM policies, and VPC structures been scanned?
2. **Benchmark Verification:** Is each high/critical vulnerability assigned a CIS check ID?
3. **Actionability:** Are IaC code snippets provided for all reported remediations?
4. **Iron Law Audit:** Has every target template passed linter scans and CIS benchmark verification?


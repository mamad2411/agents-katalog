---
name: iac-check
description: >
  Enforces IaC security rules (IAC-1 through IAC-5). Loaded by the conductor for
  security audits and review operations on infrastructure-as-code files. Detects
  public storage buckets, containers running as root, missing encryption-at-rest,
  wildcard IAM policies, and exposed ports in security groups. Supports Terraform
  HCL, CloudFormation YAML/JSON, and Kubernetes manifests; other dialects are
  skipped gracefully.
version: "1.0.0"
last-reviewed: "2026-04-03"
languages: [terraform, yaml, json]
changelog: "../../CHANGELOG.md"
tools: Read, Grep, Bash
model: claude-sonnet-4.6
permissionMode: default
---

# IaC Check — Infrastructure-as-Code Security Enforcement

**Precedence**: **SEC-* (BLOCK)** → TDD → ARCH/TYPE → **IAC-* (BLOCK)** → all quality checks.

**Supported dialects**:
- Terraform HCL (`.tf` files)
- CloudFormation YAML/JSON (`.yaml`, `.json` with `AWSTemplateFormatVersion` or `Resources:` key)
- Kubernetes manifests (`.yaml` with `apiVersion:` and `kind:` keys)
- **Unsupported**: Pulumi, CDK, Bicep — skip with a note, do not false-positive

---

## Rules

### IAC-1 — Public Storage Bucket
**Severity**: BLOCK | **Languages**: terraform, yaml, json | **Source**: CCC

**What it prohibits**: S3 buckets, GCS buckets, or Azure blobs with public
read/write ACL or bucket policy allowing `*` principal.

**Detection**:
1. Look for `acl = "public-read"`, `acl = "public-read-write"` in Terraform resources
2. Look for `"Principal": "*"` in bucket policies (CloudFormation or Terraform JSON)
3. Look for `spec.accessModes: [ReadWriteMany]` without access control on Kubernetes PVCs
4. Check for `PublicAccessBlockConfiguration` set to `false` or absent on S3 resources

**agent_action**:
1. Cite: `IAC-1 (BLOCK): Public storage bucket at {file}:{line} — resource '{resource_name}' allows public access.`
2. **STOP ALL WORK** on this resource until resolved.
3. Remediation:
   - Set bucket ACL to `private`
   - Use IAM-based access policies instead of public ACLs
   - Enable Block Public Access settings (`block_public_acls = true`, `block_public_policy = true`)

---

### IAC-2 — Container Running as Root
**Severity**: BLOCK | **Languages**: yaml, json | **Source**: CCC

**What it prohibits**: Container or pod running with UID 0 or without a
non-root security context.

**Detection**:
1. Missing `securityContext.runAsNonRoot: true` on container or pod spec
2. Explicit `securityContext.runAsUser: 0`
3. Absent `securityContext` entirely on container specs in Deployment, StatefulSet,
   DaemonSet, Job, CronJob, or Pod resources

**agent_action**:
1. Cite: `IAC-2 (BLOCK): Container running as root at {file}:{line} — resource '{resource_name}' has no non-root security context.`
2. **STOP ALL WORK** on this resource until resolved.
3. Remediation:
   - Add `securityContext: { runAsNonRoot: true, runAsUser: 1000 }` to container spec
   - For init containers that genuinely need root: document with a `# WAIVER:` comment

---

### IAC-3 — Missing Encryption at Rest
**Severity**: BLOCK | **Languages**: terraform, yaml, json | **Source**: CCC

**What it prohibits**: Storage resources (S3, RDS, EBS, DynamoDB) without
encryption enabled.

**Detection**:
1. `encrypted = false` or missing `encrypted` on EBS volumes
2. Missing `server_side_encryption_configuration` block on S3 buckets
3. `storage_encrypted = false` or absent on RDS resources
4. Missing `server_side_encryption` on DynamoDB tables
5. CloudFormation `AWS::RDS::DBInstance` without `StorageEncrypted: true`

**agent_action**:
1. Cite: `IAC-3 (BLOCK): Missing encryption at rest at {file}:{line} — resource '{resource_name}' has no encryption configured.`
2. **STOP ALL WORK** on this resource until resolved.
3. Remediation:
   - Set `encrypted = true` on EBS/RDS resources
   - Add `server_side_encryption_configuration` block with KMS key reference
   - Use AWS-managed or customer-managed KMS keys

---

### IAC-4 — Wildcard IAM Policy
**Severity**: BLOCK | **Languages**: terraform, yaml, json | **Source**: CCC

**What it prohibits**: IAM role, policy, or Kubernetes RBAC rule granting `*`
on Actions/resources or `verbs: ["*"]`.

**Detection**:
1. `"Action": "*"` or `"Action": ["*"]` in IAM policy documents
2. `"Resource": "*"` combined with broad Action grants
3. Kubernetes ClusterRole with `resources: ["*"]` and `verbs: ["*"]`
4. Terraform `aws_iam_policy_document` with `actions = ["*"]`

**agent_action**:
1. Cite: `IAC-4 (BLOCK): Wildcard IAM policy at {file}:{line} — resource '{resource_name}' grants unrestricted permissions.`
2. **STOP ALL WORK** on this resource until resolved.
3. Remediation:
   - Replace wildcard with minimum required actions
   - Use least-privilege policy templates (e.g., AWS managed policies scoped to service)
   - For Kubernetes RBAC: enumerate specific resources and verbs

---

### IAC-5 — Exposed Port in Security Group
**Severity**: WARN (22/3389) / BLOCK (0-65535 open) | **Languages**: terraform, yaml, json | **Source**: CCC

**What it prohibits**: Security group ingress rule allowing port 22 (SSH),
3389 (RDP), or 0-65535 from `0.0.0.0/0` or `::/0`.

**Detection**:
1. `cidr_blocks = ["0.0.0.0/0"]` with `from_port = 0, to_port = 65535` → BLOCK
2. `cidr_blocks = ["0.0.0.0/0"]` with `from_port = 22` or `from_port = 3389` → WARN
3. IPv6 equivalent: `ipv6_cidr_blocks = ["::/0"]` with same port patterns
4. CloudFormation `AWS::EC2::SecurityGroup` with `CidrIp: 0.0.0.0/0` and open port ranges

**agent_action**:
1. Cite: `IAC-5 (BLOCK|WARN): Exposed port at {file}:{line} — resource '{resource_name}' allows {port_range} from {cidr}.`
2. If BLOCK (full port range open): **STOP ALL WORK** until resolved.
3. Remediation:
   - Restrict `cidr_blocks` to known IP ranges or VPC CIDR
   - Use bastion host or VPN for SSH/RDP access
   - For 0-65535 open: this is never acceptable — close immediately

---

**Output format per violation**:
```
IAC-N | BLOCK/WARN | <resource name> | <violation description> | Remediation: <guidance>
```

**Activation**:
Loaded by the conductor for `security` and `review` operations when IaC file
types are detected. Signal phrases: "IaC review", "Terraform", "CloudFormation",
"Kubernetes manifest", "infrastructure security", "check my yaml".

Report schema: see `skills/conductor/shared-contracts.md`.

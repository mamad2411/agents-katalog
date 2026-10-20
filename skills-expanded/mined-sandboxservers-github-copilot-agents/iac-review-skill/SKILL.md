---
name: iac-review
description: >-
  Comprehensive safety and best-practices checklist for Terraform, Bicep, and
  CloudFormation infrastructure code. Enforces security, cost optimization,
  maintainability, and operational standards before deployment.
when-to-use: >-
  Invoke when reviewing infrastructure-as-code files (.tf, .bicep, .json
  templates, .yaml for Helm/Kubernetes) before merging. Also invoke when
  designing new infrastructure to catch issues early.
categories:
  - infrastructure
  - security
  - cost-optimization
  - devops
---

# IaC Review Checklist

Use this skill when reviewing Terraform, Bicep, or CloudFormation code. This checklist catches security gaps, cost issues, and operational risks before they reach production.

## Quick Triage

1. **What language?**
   - Terraform (.tf) → Use Terraform section below
   - Bicep (.bicep) → Use Bicep section below
   - CloudFormation (.json, .yaml) → Use CloudFormation section
   - Helm (.yaml in /helm) → Use Kubernetes/Helm section

2. **What's the scope?**
   - New resource? → Check resource-specific subsection
   - Full module? → Run full checklist
   - Refactoring? → Focus on maintainability section

3. **What's the risk level?**
   - Development/test only? → Can skip some security checks
   - Production (any environment)? → All security checks required
   - Sensitive data access? → Security section + Data Protection subsection

---

## Terraform (.tf files)

### Security Checks (Required for production)

- [ ] **Secrets Management**
  - No hardcoded passwords, keys, or connection strings
  - Sensitive variables use `sensitive = true`
  - Database passwords referenced from external vault (AWS Secrets Manager, Azure Key Vault, etc.)
  - No `.tfvars` files with secrets committed (should be in `.gitignore`)

- [ ] **Access Control & IAM**
  - Resources have explicit security group rules (not wide-open `0.0.0.0/0`)
  - IAM roles follow least-privilege principle (no `*` actions)
  - Storage buckets/blobs have restricted public access
  - VPC/network resources have proper subnet isolation

- [ ] **Encryption**
  - Database encryption at rest enabled
  - Storage encryption enabled
  - TLS/SSL enforced for external-facing resources
  - Encrypted transit (e.g., enforce HTTPS, deny HTTP)

- [ ] **Logging & Monitoring**
  - CloudTrail/Activity Log enabled for audit trail
  - VPC Flow Logs enabled
  - Application-level logging configured
  - Alerts configured for security events

- [ ] **Compliance**
  - No public RDP/SSH ports exposed (3389, 22)
  - No unencrypted databases
  - Backup policies defined
  - Disaster recovery plan documented (in PR description)

### Maintainability Checks

- [ ] **Module Structure**
  - Modules are reusable (not one-off scripts)
  - Modules have clear input variables with descriptions
  - Output values expose only necessary data
  - Module nesting is at most 3 levels (avoid complexity)

- [ ] **Variable Design**
  - Variables have `type` declarations (not bare `any`)
  - Sensitive variables marked with `sensitive = true`
  - Defaults are sensible and documented
  - Variable naming is consistent (snake_case)

- [ ] **Resource Naming**
  - Resources follow org naming standard (e.g., `${var.environment}-${var.app}-${resource_type}`)
  - Tags applied to all taggable resources
  - Names are descriptive, not generic

- [ ] **Code Quality**
  - Terraform formatted (`terraform fmt`)
  - No unused variables or outputs
  - Comments explain non-obvious logic (e.g., conditionals, loops)
  - Locals used to reduce duplication

- [ ] **Dependencies**
  - Explicit `depends_on` used only when needed (otherwise use implicit depends)
  - Resource creation order is logical
  - Destroy order is safe (dependencies respected)

### Cost & Performance Checks

- [ ] **Right-Sizing**
  - VM/container sizes match actual workload needs
  - No over-provisioning (e.g., production tier for dev)
  - Auto-scaling policies defined for variable workloads
  - Storage tier appropriate for access pattern

- [ ] **Efficiency**
  - Reserved capacity used for predictable, long-running resources
  - Spot instances used where fault-tolerance exists
  - Multi-AZ redundancy only when needed
  - Temporary resources (dev, testing) have TTLs/auto-cleanup

### Drift & State Management

- [ ] **State Security**
  - Backend encrypted and access-controlled
  - State locking enabled (DynamoDB for AWS, blob storage for Azure)
  - No state files in version control
  - Backup of state taken before major changes

- [ ] **Resource Lock-In**
  - No hard-coded ARNs/IDs (use outputs from other resources)
  - Cross-stack references use data sources, not string interpolation
  - No provider-specific hacks that break portability

---

## Bicep (.bicep files)

### Security Checks (Required for production)

- [ ] **Secrets & Parameters**
  - No hardcoded secrets in parameters or variables
  - Sensitive parameters use `@secure()` decorator
  - Key Vault references for all sensitive values
  - Parameter files excluded from version control

- [ ] **RBAC & Access**
  - RBAC assignments follow least-privilege
  - No wildcard (`*`) scope assignments
  - Managed identities used instead of connection strings
  - API Management/service endpoints have IP restrictions

- [ ] **Encryption**
  - All storage accounts have encryption enabled
  - SQL databases encrypted with CMK (customer-managed keys) for sensitive data
  - Disk encryption enabled on VMs
  - Key Vault has purge protection enabled

- [ ] **Network Isolation**
  - Private endpoints used for sensitive services
  - VNet integration configured
  - No public endpoints for internal-only services
  - Network security groups have explicit allow rules

- [ ] **Compliance**
  - Audit logging enabled
  - Backup policies configured
  - No hardcoded subscriptions or tenants
  - Naming convention applied consistently

### Maintainability Checks

- [ ] **Template Structure**
  - Metadata section documents purpose and usage
  - Parameters section clearly describes each input
  - Variables section encapsulates computed values
  - Outputs section exports necessary resource properties

- [ ] **Modularity**
  - Common patterns extracted to reusable modules
  - Module hierarchy is clear (no circular dependencies)
  - Module defaults are sensible
  - Symbolic links or file references maintain DRY principle

- [ ] **Code Quality**
  - Bicep CLI validation passes (`bicep lint`, `bicep build`)
  - No unused parameters or variables
  - Consistent naming (camelCase for variables, PascalCase for resource names)
  - Comments explain conditional logic

- [ ] **Type Safety**
  - Parameters have explicit types (not `any`)
  - Outputs have type declarations
  - Enum values used for constrained inputs
  - User-defined types used for complex structures

### Deployment Checks

- [ ] **Parameter Validation**
  - Valid parameter combinations are enforced
  - Unsupported region/SKU combinations rejected by conditions
  - Dependency skeletons clear (`dependsOn` syntax correct)

- [ ] **Cost Optimization**
  - Correct tier selected (Basic vs Standard vs Premium)
  - No unnecessary redundancy for dev/test
  - Spot VMs used where applicable
  - Auto-scaling configured for variable workloads

---

## CloudFormation (.json, .yaml templates)

### Security Checks

- [ ] **Secret Management**
  - Secrets Manager used for sensitive values
  - No hardcoded secrets in templates
  - Parameter masking configured
  - Rotation policies defined

- [ ] **IAM Policies**
  - Least-privilege principle applied
  - No wildcard (`*`) actions in policies
  - Resource-level permissions when possible
  - Service-linked roles used where appropriate

- [ ] **Encryption**
  - S3 buckets encrypted by default
  - RDS encryption enabled
  - EBS volumes encrypted
  - KMS key policies properly configured

- [ ] **Logging**
  - CloudTrail enabled
  - S3 access logging
  - VPC Flow Logs enabled
  - Application logs sent to CloudWatch

### Maintainability Checks

- [ ] **Template Organization**
  - AWSTemplateFormatVersion specified
  - Description explains purpose
  - Parameters section is documented
  - Outputs section exports key values

- [ ] **Code Quality**
  - No hardcoded values (use parameters/mappings)
  - Helper scripts validated
  - Metadata section for cfn-init/cfn-signal
  - Consistent naming (PascalCase resources)

### Deployment Checks

- [ ] **Stack Safety**
  - Termination protection enabled for production stacks
  - Update policies configured for rolling updates
  - Rollback on failure enabled
  - Change sets reviewed before execution

---

## Kubernetes / Helm

### Security Checks (for production)

- [ ] **RBAC**
  - Service accounts have minimal permissions
  - Role bindings are specific, not cluster-admin
  - No privileged containers unless absolutely required
  - Network policies restrict traffic

- [ ] **Secrets & ConfigMaps**
  - Sensitive data in Secrets, not ConfigMaps
  - Secret encryption at rest enabled
  - External secrets controller used for vault integration
  - No base64-encoded secrets in manifests

- [ ] **Image Security**
  - Container images from trusted registries
  - Image pull policies set to `Always`
  - Image scanning enabled in CI/CD
  - No `latest` tags in production

- [ ] **Resource Limits**
  - CPU/memory requests and limits set
  - Network policies restrict pod-to-pod traffic
  - Ingress has authentication/authorization
  - Service mesh (Istio) for sensitive workloads

### Maintainability Checks

- [ ] **Manifest Quality**
  - All objects have labels (app, version, environment)
  - Namespace specified explicitly
  - Probes (liveness, readiness) configured
  - Health checks appropriate for application

- [ ] **Helm Values**
  - values.yaml is well-documented
  - Defaults are sensible
  - Environment-specific overrides organized
  - No hardcoded environment-specific data in templates

---

## Decision Tree: When to Fail a Review

| Scenario | Action |
| --- | --- |
| Hardcoded secrets found | **BLOCK** — require re-submission |
| Open security group (0.0.0.0/0) to sensitive port | **BLOCK for production** — allow for dev/test only |
| Unencrypted data at rest | **BLOCK for production** — allow for dev/test only |
| No backup/disaster recovery for stateful resource | **BLOCK for production** — allow for dev/test only |
| IAM policy with wildcard actions | **BLOCK for production** — allow for dev/test only |
| Unused resources/variables | **Request removal** — minor issue |
| Non-standard naming convention | **Request correction** — minor issue |
| Missing comments on complex logic | **Request improvement** — minor issue |

---

## Approval Criteria

✅ **Approve when:**
- All security checks for environment type pass
- Maintainability standards met
- Cost optimization guidelines followed
- Code is well-formatted and tested

❌ **Block when:**
- Hardcoded secrets found
- Production resources unencrypted
- Security group/RBAC allows excessive access
- No logging/audit trail for sensitive operations

⚠️ **Request changes when:**
- Code needs formatting
- Naming convention inconsistent
- Opportunities for cost savings missed
- Comments missing on non-obvious logic

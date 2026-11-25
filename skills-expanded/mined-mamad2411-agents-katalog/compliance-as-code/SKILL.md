---
name: compliance-as-code
version: 1.0.0
min_mindforge_version: 0.1.0
status: stable
triggers: compliance as code, policy engine, OPA rego, automated compliance, audit evidence, SOC2 mapping, HIPAA control, compliance check, policy enforcement, control framework, compliance report, regulatory automation
---

# Skill — Compliance as Code

## When this skill activates
Any task involving automated compliance verification, policy-as-code implementation,
audit evidence generation, regulatory control mapping, or compliance CI integration.

## Mandatory actions when this skill is active

### Before writing any code
1. Identify the compliance framework(s) applicable (SOC2, HIPAA, PCI-DSS, GDPR).
2. Map specific controls to technical policies that can be automated.
3. Define evidence requirements for each control.

### During implementation
- Write policies as code (OPA/Rego, Sentinel, Conftest).
- Integrate policy checks into CI pipeline (fail on violation).
- Generate machine-readable evidence automatically.

### After implementation
- Verify all mapped controls have automated verification.
- Set up continuous compliance dashboard with drift alerts.
- Document policy-to-control mapping in ARCHITECTURE.md.

## Policy Engines

### OPA (Open Policy Agent) with Rego
- General-purpose policy engine.
- Declarative policy language (Rego).
- Use for: infrastructure policies, API authorization, data access control.
- Integrations: Kubernetes (Gatekeeper), Terraform, CI pipelines, API gateways.

```rego
package terraform.aws

deny[msg] {
    resource := input.resource.aws_s3_bucket[name]
    not resource.server_side_encryption_configuration
    msg := sprintf("S3 bucket '%s' must have encryption enabled", [name])
}
```

### HashiCorp Sentinel
- Policy-as-code for Terraform Enterprise/Cloud.
- Enforces infrastructure policies before apply.
- Use for: cost controls, naming conventions, required tags, approved regions.

```hcl
import "tfplan"

main = rule {
    all tfplan.resources.aws_instance as _, instances {
        all instances as _, r {
            r.applied.tags contains "environment"
        }
    }
}
```

### Conftest
- Testing framework for structured configuration data.
- Uses OPA/Rego policies against YAML, JSON, HCL, Dockerfile.
- Use for: Kubernetes manifests, Docker configs, CI pipelines.

```rego
package main

deny[msg] {
    input.kind == "Deployment"
    not input.spec.template.spec.securityContext.runAsNonRoot
    msg := "Containers must run as non-root"
}
```

## Control Framework Mapping

### SOC2 Trust Service Criteria
| Control | Policy | Automated Check |
|---------|--------|-----------------|
| CC6.1 (Logical Access) | IAM least privilege | No wildcard permissions in policies |
| CC6.6 (System Boundaries) | Network segmentation | Security groups restrict ingress |
| CC7.2 (Monitoring) | Log aggregation | All services emit structured logs |
| CC8.1 (Change Management) | PR approval required | Branch protection rules enforced |

### HIPAA Security Rule (164.312)
| Control | Policy | Automated Check |
|---------|--------|-----------------|
| 164.312(a)(1) Access Control | Role-based access | RBAC policies enforced |
| 164.312(a)(2)(iv) Encryption | Data encrypted at rest | All storage encrypted |
| 164.312(b) Audit Controls | Audit logging | All PHI access logged |
| 164.312(e)(1) Transmission Security | TLS required | No HTTP endpoints |

### PCI-DSS
| Requirement | Policy | Automated Check |
|-------------|--------|-----------------|
| 2.2 System hardening | CIS benchmark | Configuration scanner passes |
| 3.4 Data encryption | Encryption at rest | Storage encryption verified |
| 6.5 Secure development | SAST/DAST | No critical findings in scan |
| 10.2 Audit trails | Comprehensive logging | All access events captured |

## Evidence Generation

### Automated Evidence Types
- **Configuration snapshots**: point-in-time state of security configs.
- **Policy evaluation results**: pass/fail with details for each control.
- **Access review reports**: who has access to what, generated automatically.
- **Deployment audit trails**: who deployed what, when, with what approval.

### Evidence Requirements
- Timestamped and immutable (stored in append-only log).
- Machine-readable (JSON/structured format for automated processing).
- Traceable (linked to specific control and policy).
- Continuous (generated on every change, not just at audit time).

### Example Evidence Output
```json
{
  "control": "CC6.1",
  "framework": "SOC2",
  "policy": "no-wildcard-iam-permissions",
  "result": "PASS",
  "timestamp": "2024-01-15T10:30:00Z",
  "resource": "arn:aws:iam::123456:policy/app-service",
  "details": "No wildcard actions found in policy document",
  "evidence_hash": "sha256:abc123..."
}
```

## CI Pipeline Integration

### Pipeline Stage: Policy Check
```yaml
stages:
  - name: compliance-check
    steps:
      - conftest test --policy policies/ deployment.yaml
      - opa eval --data policies/ --input tfplan.json "data.terraform.deny"
    on_failure: block_deployment
```

### Enforcement Levels
- **Advisory**: log warning, don't block (for new policies being rolled out).
- **Soft mandatory**: block with override option (requires approval).
- **Hard mandatory**: block deployment, no override (critical security controls).

### Gradual Rollout of New Policies
1. Deploy policy in advisory mode (2 weeks).
2. Review violations, adjust policy if false positives.
3. Promote to soft mandatory (2 weeks).
4. Promote to hard mandatory after all violations resolved.

## Compliance Dashboard

### Key Metrics
- **Compliance score**: percentage of controls with passing automated checks.
- **Drift count**: controls that passed previously but now fail.
- **Time to remediate**: average time from violation detection to fix.
- **Coverage**: percentage of controls with automated verification.

### Alerting
- Drift detected: immediate alert to security team.
- New violation in PR: block merge, notify developer.
- Compliance score drops below threshold: escalate to CISO.
- Evidence generation failure: alert compliance team.

## Reporting

### Continuous Compliance Report
- Generated on demand or on schedule (weekly/monthly).
- Shows: all controls, current status, evidence links, violation history.
- Format: PDF for auditors, JSON for automated systems.

### Audit Preparation
- Pre-audit checklist: verify all evidence is current and complete.
- Gap analysis: identify controls without automated verification.
- Remediation tracking: SLA for fixing violations.

## Self-check before task completion

Before marking a task done when this skill was active:

- [ ] Did I read the full SKILL.md before starting? (Not just the triggers)
- [ ] Is every control mapped to an automated policy?
- [ ] Are policies integrated into CI (blocking on violation)?
- [ ] Is evidence generated automatically (not manually)?
- [ ] Is there a compliance dashboard with drift alerting?
- [ ] Are enforcement levels appropriate (advisory → soft → hard)?
- [ ] Is the policy-to-control mapping documented?

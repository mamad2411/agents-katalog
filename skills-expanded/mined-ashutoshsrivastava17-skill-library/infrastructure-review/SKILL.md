---
name: infrastructure-review
description: >
  Review infrastructure configurations for reliability, security, cost efficiency,
  and operational best practices across cloud and on-prem environments.
  TRIGGER when: user says /infrastructure-review, "review our infrastructure",
  "audit cloud setup", "infra review", or "check our AWS/GCP/Azure config".
argument-hint: "[cloud provider, service, or IaC files to review]"
user-invocable: true
---

# Infrastructure Review

You are a senior infrastructure engineer performing a comprehensive review. Evaluate against reliability, security, cost, and operational excellence pillars.

## Process

### Step 1: Understand the Environment

| Parameter | Description |
|-----------|-------------|
| Cloud provider(s) | AWS, GCP, Azure, on-prem, hybrid |
| IaC tool | Terraform, CloudFormation, Pulumi, CDK, Ansible |
| Architecture pattern | Microservices, monolith, serverless, event-driven |
| Scale | Traffic volume, data size, team size |
| Compliance requirements | SOC2, HIPAA, PCI-DSS, GDPR |

### Step 2: Review Checklist

#### Reliability

| Check | What to Look For |
|-------|-----------------|
| High availability | Multi-AZ / multi-region, no single points of failure |
| Auto-scaling | Scaling policies configured, min/max instances appropriate |
| Backup & recovery | Automated backups, tested restore, RPO/RTO defined |
| Health checks | LB health checks, container liveness/readiness probes |
| Circuit breakers | Retry policies, timeout configs, fallback mechanisms |

#### Security

| Check | What to Look For |
|-------|-----------------|
| Network segmentation | VPC design, subnet isolation, security groups |
| IAM | Least-privilege roles, no wildcard permissions, MFA enforced |
| Encryption | At-rest (KMS), in-transit (TLS 1.2+), key rotation |
| Secrets management | No hardcoded secrets, using vault/SSM/secrets manager |
| Logging & audit | CloudTrail / audit logs enabled, tamper-proof storage |

#### Cost Efficiency

| Check | What to Look For |
|-------|-----------------|
| Right-sizing | Instances matched to actual utilization |
| Reserved/committed use | Savings plans for predictable workloads |
| Idle resources | Unused volumes, unattached IPs, stopped instances |
| Storage tiering | Lifecycle policies, archive old data |

#### Operational Excellence

| Check | What to Look For |
|-------|-----------------|
| IaC coverage | All resources managed by code, no manual changes |
| Tagging | Consistent tags for cost allocation, ownership, environment |
| Monitoring | Metrics, logs, traces for all critical services |
| Deployment pipeline | CI/CD for infrastructure changes |

## Output Format

```markdown
## Infrastructure Review: [Environment]

### Summary
- Overall health: [Good / Needs Attention / Critical]
- Findings: N critical, N high, N medium, N low

### Findings
#### [SEVERITY]: [Title]
**Resource:** [specific resource or config]
**Pillar:** Reliability | Security | Cost | Operations
**Issue:** [What is wrong]
**Risk:** [What could happen]
**Recommendation:** [What to do]
**Effort:** Low / Medium / High

### Cost Optimization Opportunities
| Opportunity | Estimated Savings | Effort |

### Action Plan
| Priority | Action | Owner | Effort | Impact |
```

## Quality Checklist

- [ ] All four pillars reviewed (reliability, security, cost, operations)
- [ ] Findings reference specific resources or configurations
- [ ] Recommendations are actionable with effort estimates
- [ ] Cost savings are quantified where possible
- [ ] Security findings flagged with appropriate urgency

## Edge Cases

- **Multi-cloud**: Review each provider independently, then assess cross-cloud networking
- **Legacy infrastructure**: Focus on migration path and risk reduction
- **Startup / early stage**: Prioritize security and reliability basics over optimization
- **Regulated industry**: Lead with compliance requirements, map controls to infrastructure

---
name: reviewing-architecture
description: Reviews an existing or proposed architecture against the Well-Architected pillars (operational excellence, security, reliability, performance efficiency, cost optimization, sustainability), producing risks ranked by impact with remediation. Use for architecture reviews, design reviews, production-readiness reviews, cloud workload assessments, or when the user asks "is this architecture good".
metadata:
  role: system-architect
  version: "1.0"
---

# Reviewing architecture

Use the six pillars shared by the AWS Well-Architected Framework (and closely mirrored by Azure and Google Cloud frameworks) as the review lens. Cloud-agnostic: apply the principles, not vendor products.

## Workflow

1. **Scope.** Which workload, which environments, which business-critical flows. Collect: architecture diagrams, ADRs, IaC, runbooks, SLOs, incident history, cost reports.
2. **Verify against reality.** Read the IaC/manifests/code; flag where docs and reality disagree — that is itself a finding.
3. **Walk each pillar** with the questions in [reference/pillars.md](reference/pillars.md). Answer each with evidence (file, dashboard, doc) or "no evidence".
4. **Rate risks**: High (likely to cause outage, breach, data loss, or major cost waste), Medium, Low.
5. **Recommend** the smallest change that removes each High risk; group the rest into an improvement plan.

## Fast red-flag scan

Check these first; each is usually a High risk:
- Single point of failure (one instance, one AZ, one DB without replica/failover)
- No tested backups or restore; RPO/RTO undefined
- No timeouts/retries/circuit breakers on remote calls
- Secrets in code or plaintext config; overly broad IAM (`*:*`)
- Public data stores or admin endpoints
- Manual, undocumented deployments; no rollback path
- No SLOs, alerts, or on-call; logs without correlation IDs
- Unbounded autoscaling or no budgets/alerts on spend
- Shared database written by multiple services

## Output format

```markdown
# Architecture review: <workload> — <date>

## Summary
<verdict, top 3 risks, overall readiness>

## Risks
| # | Pillar | Risk | Evidence | Impact | Likelihood | Rating | Recommendation |
|---|--------|------|----------|--------|------------|--------|----------------|

## Strengths
## Improvement plan (ordered)
## Questions / missing evidence
```

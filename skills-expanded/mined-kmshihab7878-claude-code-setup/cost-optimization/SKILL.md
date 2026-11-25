---
name: cost-optimization
description: Cloud cost optimization with Infracost for Terraform, ccusage for Claude Code tokens, and AWS Cost Explorer patterns
triggers:
  - cost optimization
  - infracost
  - ccusage
  - cloud costs
  - aws costs
  - budget
  - spending
---

# Cost Optimization

Track and optimize costs across infrastructure (AWS/Terraform) and AI tools (Claude Code).

## Claude Code Usage Tracking

```bash
# View usage analytics from local JSONL logs
npx ccusage

# Daily breakdown
npx ccusage --daily

# Monthly summary
npx ccusage --monthly

# Live monitoring of current session
npx ccusage --live
```

## Infracost (Terraform Cost Estimation)

```bash
# Show cost breakdown for current Terraform
infracost breakdown --path terraform/

# Compare cost of changes (in CI)
infracost diff --path terraform/ --compare-to infracost-base.json

# Generate baseline for comparison
infracost breakdown --path terraform/ --format json --out-file infracost-base.json
```

### CI Integration

```yaml
- name: Infracost
  uses: infracost/actions/setup@v3
- run: infracost diff --path terraform/ --format json --compare-to /tmp/base.json --out-file /tmp/diff.json
- uses: infracost/actions/comment@v3
  with:
    path: /tmp/diff.json
    behavior: update
```

## AWS Cost Patterns

### Right-sizing Checklist
- EC2: Check CPU <20% avg -> downsize instance type
- RDS: Check connections <50% -> consider smaller instance or Aurora Serverless
- EKS: Check pod resource requests vs actual usage -> adjust requests/limits
- S3: Enable Intelligent-Tiering for unpredictable access patterns
- Lambda: Optimize memory allocation (use AWS Lambda Power Tuning)

### Budget Alerts

```hcl
resource "aws_budgets_budget" "monthly" {
  name         = "coremind-monthly"
  budget_type  = "COST"
  limit_amount = "500"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  notification {
    comparison_operator = "GREATER_THAN"
    threshold           = 80
    threshold_type      = "PERCENTAGE"
    notification_type   = "ACTUAL"
    subscriber_email_addresses = ["<your-email@example.com>"]
  }
}
```

## Cost Optimization Quick Wins
1. Use Spot instances for non-critical workloads (60-90% savings)
2. Reserved Instances or Savings Plans for steady-state (30-40% savings)
3. S3 lifecycle policies to transition to Glacier after 90 days
4. Delete unattached EBS volumes and unused Elastic IPs
5. Use `opusplan` in Claude Code (Opus for planning, Sonnet for coding)

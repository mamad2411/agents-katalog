---
name: aws-rightsizing
description: |
  Use when working with Aws Rightsizing — analyze EC2, RDS, EBS, and Lambda
  resource utilization to identify right-sizing opportunities. Uses CloudWatch
  metrics with anti-hallucination rules for burstable instances, memory metrics,
  peak vs average analysis, and estimated monthly savings calculations.
connection_type: aws
preload: false
---

# AWS Rightsizing Skill

Analyze resource utilization and identify right-sizing opportunities with anti-hallucination guardrails and reusable CloudWatch functions.

**Relationship to other AWS skills:**

- `aws-rightsizing/` -> "What to resize" (anti-hallucination rules, utilization thresholds, savings estimates)
- `aws/` -> "How to execute" (parallel patterns, CloudWatch statistics syntax, throttling)
- `aws-pricing/` -> "How much things cost" (on-demand pricing via `get_aws_cost`)
- `aws-billing/` -> "Current spend" (billing context, discount detection)

## CRITICAL: Rightsizing Rules (Anti-Hallucination)

**These rules are MANDATORY when analyzing resource utilization. Violating them produces incorrect recommendations that can cause outages.**

### Rule 1: Minimum 14-Day Observation Window

Short observation windows miss weekly patterns (batch jobs, weekend traffic, month-end spikes). Default `--days 14`, allow up to 90.

```
WRONG:  --days 3   -> Misses weekend batch jobs
WRONG:  --days 1   -> Captures only one day's pattern
CORRECT: --days 14 -> Captures at least 2 full weekly cycles
```

The `_rs_parse_days` helper enforces the 14-90 day range.

### Rule 2: Burstable Instances (t-family) Need Credit Balance

A t3.micro at 5% avg CPU may be fine OR may be throttled with 0 credits. A burstable instance running out of CPU credits is effectively capped at baseline performance, causing latency spikes.

**MANDATORY**: For any t-family instance (t2, t3, t3a, t4g), always check `CPUCreditBalance`. If credit balance trends toward 0, the instance is NOT underutilized -- it is credit-starved and may need upsizing.

```
WRONG:  t3.micro avg CPU 5% -> "underutilized, downsize"
CORRECT: t3.micro avg CPU 5%, credit balance 0 -> "credit-starved, consider upsizing"
CORRECT: t3.micro avg CPU 5%, credit balance 144 -> "underutilized, downsize candidate"
```

### Rule 3: Memory Metrics Require CloudWatch Agent

`mem_used_percent` is NOT available by default in CloudWatch. It requires the CloudWatch Agent (CWAgent namespace) to be installed and configured on the instance.

**MANDATORY**: If CWAgent namespace returns no data, report "memory data unavailable" -- do NOT assume memory is fine.

```
WRONG:  No memory data -> "memory is fine"
CORRECT: No memory data -> "memory data unavailable (CWAgent not installed)"
```

### Rule 4: Peak vs Average -- Never Downsize on Average Alone

An instance with avg CPU 10% but max CPU 95% is a bursty workload. Downsizing would cause failures during peaks.

**MANDATORY**: Report BOTH Average AND Maximum statistics. Only flag for downsizing if max < threshold too.

```
WRONG:  avg CPU 10% -> "downsize"
CORRECT: avg CPU 10%, max CPU 22% -> "downsize candidate (both avg and max are low)"
CORRECT: avg CPU 10%, max CPU 95% -> "bursty workload, do NOT downsize"
```

### Rule 5: Savings Estimates Use On-Demand Pricing Only

If the instance has RI/SP coverage, actual savings differ from on-demand-based estimates. Always caveat estimates.

```
WRONG:  "You will save $70/mo by downsizing"
CORRECT: "Estimated savings: $70/mo (based on on-demand rates; actual savings may differ if RI/SP coverage applies)"
```

### Rule 6: Multi-AZ RDS Doubles Compute Cost

A db.r5.large Multi-AZ costs ~$365/mo, not ~$182/mo. The standby replica incurs the same compute charge.

**MANDATORY**: Check `MultiAZ` flag before estimating RDS costs.

```
WRONG:  db.r5.large -> $182/mo
CORRECT: db.r5.large, MultiAZ=true -> $365/mo
CORRECT: db.r5.large, MultiAZ=false -> $182/mo
```

### Rule 7: GP2 vs GP3 Baseline IOPS

GP2 baseline IOPS = max(100, 3 x GB). GP3 baseline = 3000 IOPS at lower cost per GB.

A 100GB GP2 has 300 IOPS baseline. GP3 gives 3000 IOPS at $0.08/GB vs $0.10/GB. Always calculate both when evaluating EBS rightsizing.

```
WRONG:  "GP2 and GP3 have similar performance"
CORRECT: "100GB GP2: 300 IOPS baseline at $10/mo. 100GB GP3: 3000 IOPS baseline at $8/mo (10x IOPS, 20% cheaper)"
```

### Rule 8: Lambda Memory Controls CPU Allocation

Reducing Lambda memory from 1GB to 256MB also cuts CPU by 4x. Duration may increase, negating savings. Check duration trend before recommending memory reduction.

```
WRONG:  "Lambda uses 200MB of 1GB, reduce to 256MB"
CORRECT: "Lambda uses 200MB of 1GB. Check duration: if avg duration is near timeout, reducing memory will increase duration and may increase cost."
```

### Mandatory Pre-Analysis Checklist

**Before writing ANY rightsizing analysis, verify ALL of the following:**

- [ ] Observation window >= 14 days (see Rule 1)
- [ ] Burstable instances (t-family) checked for CPUCreditBalance (see Rule 2)
- [ ] Memory metrics checked via CWAgent namespace with graceful fallback if unavailable (see Rule 3)
- [ ] Both Average AND Maximum statistics reported for all metrics (see Rule 4)
- [ ] Savings caveated as "based on on-demand rates" (see Rule 5)
- [ ] Multi-AZ flag checked for RDS instances (see Rule 6)
- [ ] All cost figures include currency unit (USD)
- [ ] Parallel execution used for all CloudWatch queries (see `aws/SKILL.md`)

---

## Rightsizing Script (`get_rightsizing_aws.sh`)

**DO NOT read or modify the script file.** Only source and call the functions.

**SETUP** (at the start of your script):

```bash
source ./_skills/connections/aws/aws-rightsizing/scripts/get_rightsizing_aws.sh
```

**All functions enforce anti-hallucination rules**: 14-day minimum window, parallel CloudWatch queries, TOON output format.

**FUNCTION REFERENCE**:

| Function | Purpose | Signature |
|----------|---------|-----------|
| `aws_rightsizing_ec2` | EC2 CPU + optional memory analysis, flag under/over-utilized | `[--days N] [--region REGION]` |
| `aws_rightsizing_ec2_savings` | Estimate savings for flagged EC2 instances | `[--days N] [--region REGION]` |
| `aws_rightsizing_rds` | RDS CPU, connections, storage utilization | `[--days N] [--region REGION]` |
| `aws_rightsizing_rds_savings` | Estimate savings for flagged RDS instances | `[--days N] [--region REGION]` |
| `aws_rightsizing_ebs` | EBS IOPS/throughput utilization, GP2->GP3 candidates | `[--days N] [--region REGION]` |
| `aws_rightsizing_lambda` | Lambda memory/duration/invocation analysis | `[--days N] [--region REGION]` |
| `aws_rightsizing_summary` | Run all checks, output unified summary | `[--days N] [--region REGION]` |

**RECOMMENDED WORKFLOW** (every rightsizing analysis):

1. **Always run `aws_rightsizing_ec2` first** -- EC2 is typically the largest compute cost
2. **Run `aws_rightsizing_rds`** for database layer analysis
3. **Run `aws_rightsizing_ebs`** for storage optimization (especially GP2->GP3 migration)
4. **Run `aws_rightsizing_lambda`** if Lambda is a significant cost driver
5. **Or run `aws_rightsizing_summary`** for a unified view across all resource types
6. For savings estimates, run `aws_rightsizing_ec2_savings` and `aws_rightsizing_rds_savings`

**Examples:**

```bash
source ./_skills/connections/aws/aws-rightsizing/scripts/get_rightsizing_aws.sh

# EC2 utilization analysis (14-day default)
aws_rightsizing_ec2

# EC2 analysis with 30-day window in specific region
aws_rightsizing_ec2 --days 30 --region us-west-2

# EC2 savings estimates
aws_rightsizing_ec2_savings --days 30

# RDS utilization
aws_rightsizing_rds --days 14

# RDS savings estimates
aws_rightsizing_rds_savings --days 14

# EBS rightsizing (GP2->GP3 candidates)
aws_rightsizing_ebs --days 14

# Lambda memory/duration analysis
aws_rightsizing_lambda --days 14

# Full summary across all resource types
aws_rightsizing_summary --days 30 --region us-east-1
```

---

## EC2 Instance Family Quick Reference

Approximate monthly on-demand costs in USD (us-east-1). Use to validate savings estimates.

| Family | Size | vCPU | Memory | ~Monthly USD |
|--------|------|------|--------|-------------|
| t3 | micro | 2 | 1 GB | $8 |
| t3 | small | 2 | 2 GB | $15 |
| t3 | medium | 2 | 4 GB | $30 |
| t3 | large | 2 | 8 GB | $61 |
| m5 | large | 2 | 8 GB | $70 |
| m5 | xlarge | 4 | 16 GB | $140 |
| m5 | 2xlarge | 8 | 32 GB | $281 |
| c5 | large | 2 | 4 GB | $62 |
| c5 | xlarge | 4 | 8 GB | $124 |
| c5 | 2xlarge | 8 | 16 GB | $248 |
| r5 | large | 2 | 16 GB | $91 |
| r5 | xlarge | 4 | 32 GB | $182 |

**Downsizing savings:** Moving one size down within a family typically saves ~50% (e.g., m5.xlarge $140 -> m5.large $70 = $70/mo savings).

For instance types or RDS pricing not listed above, use `get_aws_cost` from the `aws-pricing/` skill.

---

## Common Errors

| Error | Cause | Solution |
|-------|-------|---------|
| `InvalidParameterCombination` for CloudWatch | Wrong statistics syntax | Use spaces not commas: `--statistics Average Maximum` |
| No data for `mem_used_percent` | CWAgent not installed | Report "memory data unavailable", don't assume |
| `CPUCreditBalance` returns no data | Not a burstable instance | Only query for t-family instances |
| Savings estimate seems too high | Multi-AZ RDS not accounted for | Check `MultiAZ` flag, double cost if true |
| `InvalidParameterValue` for period | Period too small for date range | Use 3600 (1hr) for <= 15 days, 86400 (1day) for > 15 days |

## Output Format

Present results as a structured report:
```
Aws Rightsizing Report
══════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |


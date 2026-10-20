---
name: aws-idle-resources
description: |
  Use when working with Aws Idle Resources — detect unused and idle AWS
  resources that incur cost without providing value. Covers detached EBS
  volumes, idle load balancers, unused Elastic IPs, stopped EC2 instances, idle
  NAT Gateways, old snapshots, and unused ENIs. Includes estimated monthly waste
  per resource and anti-hallucination rules for safe detection.
connection_type: aws
preload: false
---

# AWS Idle Resources Skill

Detect unused and idle AWS resources with anti-hallucination guardrails and cost waste estimation.

**Relationship to other AWS skills:**

- `aws-idle-resources/` -> "What is wasting money" (idle detection rules, cost estimation, protection tag checks)
- `aws/` -> "How to execute" (parallel patterns, filtering hierarchy, pagination)
- `aws-pricing/` -> "How much things cost" (on-demand pricing via `get_aws_cost`)
- `aws-billing/` -> "Current spend" (billing context, discount detection)

## CRITICAL: Idle Resource Detection Rules (Anti-Hallucination)

**These rules are MANDATORY when detecting idle resources. Violating them produces recommendations that can cause data loss or outages.**

### Rule 1: "Available" EBS != Always Deletable

Detached EBS volumes in "available" state may be intentional (warm standby, manual backups, data archives). Report but NEVER auto-recommend deletion without user context.

```
WRONG:  "vol-abc is detached, delete it"
CORRECT: "vol-abc is detached (available), candidate for review. Created 2025-06-15, 100GB gp3, est. $8/mo"
```

### Rule 2: Stopped EC2 Still Incurs EBS + EIP Costs

When an EC2 instance is stopped, compute charges stop but attached EBS volumes and associated Elastic IPs continue to incur charges.

**MANDATORY**: Report the ongoing cost of stopped instances, not just the compute savings.

```
WRONG:  "i-abc is stopped, no cost"
CORRECT: "i-abc is stopped since 2025-12-01. Ongoing cost: 2x EBS volumes ($24/mo) + 1 EIP ($3.60/mo) = $27.60/mo"
```

### Rule 3: EIP Cost: $0.005/hr ($3.60/mo) Per Public IPv4

Since February 2024, AWS charges $0.005/hr for ALL public IPv4 addresses, including EIPs attached to running instances. An unassociated EIP is pure waste because it costs money AND provides zero value.

```
WRONG:  "EIP attached to running instance is free"
CORRECT: "All EIPs cost $3.60/mo. EIP eipalloc-abc is unassociated -- pure waste at $3.60/mo"
CORRECT: "EIP eipalloc-def is attached to running i-123 -- cost exists but provides value"
```

### Rule 4: NAT Gateway: $0.045/hr ($32.40/mo) Minimum

NAT Gateways have a fixed hourly charge regardless of traffic, plus $0.045/GB data processed. Even idle NAT Gateways cost $32+/mo.

```
WRONG:  "NAT Gateway has low traffic, minimal cost"
CORRECT: "NAT Gateway nat-abc has < 10 active connections/day avg. Fixed cost: $32.40/mo + data processing charges"
```

### Rule 5: Snapshot Cost: $0.05/GB/mo (Standard)

Old snapshots accumulate silently. 1TB of old snapshots = $50/mo. However, some snapshots back AMIs and are required.

**MANDATORY**: Cross-reference with `describe-images --owners self` to exclude snapshots that back active AMIs before flagging.

```
WRONG:  "snap-abc is 90 days old, delete it"
CORRECT: "snap-abc is 90 days old, 200GB, est. $10/mo. NOT backing any AMI. Candidate for review."
CORRECT: "snap-def is 120 days old, 500GB. BACKS AMI ami-xyz -- skipped (required by AMI)."
```

### Rule 6: Never Recommend Deletion -- Only Flag

Always phrase results as "candidate for review" not "should be deleted". Resources may be intentionally idle (DR, staging, warm standby).

```
WRONG:  "Delete these 5 volumes to save $87/mo"
CORRECT: "5 detached volumes identified as candidates for review. Estimated waste: $87/mo if all are unnecessary."
```

### Rule 7: Check Protection Tags Before Flagging

Look for tags like `do-not-delete`, `keep`, `protected`, `backup`, `DoNotDelete`. If found, mark as "protected -- skipped" in the output.

```
WRONG:  "vol-abc (tagged keep) is idle, candidate for deletion"
CORRECT: "vol-abc: PROTECTED (tag: keep) -- skipped"
```

### Mandatory Pre-Detection Checklist

**Before writing ANY idle resource analysis, verify ALL of the following:**

- [ ] Region context established (current or specified via `--region`)
- [ ] Protection tags checked before flagging any resource (see Rule 7)
- [ ] Cost estimates use current on-demand pricing (see pricing table below)
- [ ] Results clearly state "candidates for review" not "should be deleted" (see Rule 6)
- [ ] Each resource shows estimated monthly waste
- [ ] All costs include currency unit (USD)
- [ ] Snapshot-AMI cross-reference performed (see Rule 5)
- [ ] Parallel execution used for all AWS API calls (see `aws/SKILL.md`)

---

## Idle Resources Script (`get_idle_resources_aws.sh`)

**DO NOT read or modify the script file.** Only source and call the functions.

**SETUP** (at the start of your script):

```bash
source ./_skills/connections/aws/aws-idle-resources/scripts/get_idle_resources_aws.sh
```

**All functions enforce anti-hallucination rules**: protection tag checks, cost estimation, "candidate for review" language, TOON output format.

**FUNCTION REFERENCE**:

| Function | Purpose | Signature |
|----------|---------|-----------|
| `aws_idle_ebs` | Detached (available) EBS volumes with cost estimate | `[--region REGION]` |
| `aws_idle_elb` | ALB/NLB with 0 healthy targets or < threshold requests | `[--days N] [--region REGION]` |
| `aws_idle_eip` | Elastic IPs not associated to running instances | `[--region REGION]` |
| `aws_idle_ec2_stopped` | EC2 stopped > N days with attached EBS cost | `[--days N] [--region REGION]` |
| `aws_idle_natgw` | NAT Gateways with minimal/no traffic | `[--days N] [--region REGION]` |
| `aws_idle_snapshots` | EBS snapshots older than N days, not backing AMIs | `[--days N] [--region REGION]` |
| `aws_idle_eni` | Network interfaces in "available" (unattached) state | `[--region REGION]` |
| `aws_idle_summary` | Run all checks, unified waste summary with total | `[--days N] [--region REGION]` |

**RECOMMENDED WORKFLOW** (every idle resource analysis):

1. **Run `aws_idle_summary`** for a unified view of all idle resource types with total waste estimate
2. For deeper analysis of a specific category, run the individual function
3. Always review "PROTECTED" items separately -- they were intentionally tagged

**Examples:**

```bash
source ./_skills/connections/aws/aws-idle-resources/scripts/get_idle_resources_aws.sh

# Full idle resource scan (default region)
aws_idle_summary

# Full scan in specific region
aws_idle_summary --days 30 --region us-west-2

# Detached EBS volumes only
aws_idle_ebs

# Idle load balancers (7-day window)
aws_idle_elb --days 7

# Unused Elastic IPs
aws_idle_eip

# Long-stopped EC2 instances (60-day threshold)
aws_idle_ec2_stopped --days 60

# Idle NAT Gateways
aws_idle_natgw --days 14

# Old snapshots (120-day threshold)
aws_idle_snapshots --days 120

# Unused network interfaces
aws_idle_eni --region eu-west-1
```

---

## Resource Cost Reference

Approximate monthly costs in USD. Use to validate waste estimates.

| Resource | Pricing Model | Typical Monthly Cost |
|----------|--------------|---------------------|
| EBS gp2 | $0.10/GB/mo | 100GB = $10 |
| EBS gp3 | $0.08/GB/mo | 100GB = $8 |
| EBS io1 | $0.125/GB + $0.065/IOPS/mo | 100GB + 3000 IOPS = $207.50 |
| EBS io2 | $0.125/GB + $0.065/IOPS/mo | 100GB + 3000 IOPS = $207.50 |
| EBS st1 | $0.045/GB/mo | 500GB = $22.50 |
| EBS sc1 | $0.015/GB/mo | 500GB = $7.50 |
| Elastic IP (any) | $0.005/hr (all public IPv4) | $3.60 (unassociated = pure waste) |
| NAT Gateway | $0.045/hr + $0.045/GB | $32.40 base |
| EBS Snapshot | $0.05/GB/mo | 100GB = $5 |
| ENI (unused) | Free | $0 (cleanup value only) |

For resources not listed above, use `get_aws_cost` from the `aws-pricing/` skill.

---

## Common Errors

| Error | Cause | Solution |
|-------|-------|---------|
| `InvalidParameterValue` for filters | Wrong filter syntax | Use `Name=status,Values=available` format |
| `describe-images` timeout | Too many AMIs | Add `--owners self` filter |
| EBS cost seems wrong | io1/io2 IOPS cost not included | Add IOPS-based cost for provisioned IOPS volumes |
| Snapshot count very high | Account has many automated backups | Use `--days` to filter by age, cross-ref AMIs |
| NAT Gateway shows as idle but is needed | Used for private subnet egress | Check VPC route tables before flagging |
| EIP shows as unused but is in use | Attached to network interface, not EC2 | Check `NetworkInterfaceId` association |

## Output Format

Present results as a structured report:
```
Aws Idle Resources Report
═════════════════════════
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


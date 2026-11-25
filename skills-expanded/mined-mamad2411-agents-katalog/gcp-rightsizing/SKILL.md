---
name: gcp-rightsizing
description: "Analyze Compute Engine VM, Cloud SQL, Persistent Disk, and serverless (Cloud Functions/Cloud Run) utilization to identify right-sizing opportunities. Uses Cloud Monitoring metrics with anti-hallucination rules for E2 shared-core instances, sole-tenant nodes, preemptible/spot VMs, SUD eligibility, peak vs average analysis, CUD-aware savings, and estimated monthly savings calculations."
connection_type: gcp
preload: false
---

# GCP Rightsizing Skill

Analyze resource utilization and identify right-sizing opportunities with anti-hallucination guardrails and reusable Cloud Monitoring functions.

**Relationship to other GCP skills:**

- `gcp-rightsizing/` -> "What is oversized" (utilization thresholds, downsize recommendations)
- `gcp-idle-resources/` -> "What is wasting money" (idle detection rules, cost estimation)
- `gcp/` -> "How to execute" (parallel patterns, monitoring aligners, billing/pricing scripts)

## CRITICAL: Rightsizing Rules (Anti-Hallucination)

**These rules are MANDATORY when analyzing resource utilization. Violating them produces incorrect recommendations that can cause outages.**

### Rule 1: Minimum 14-Day Observation Window

Short observation windows miss weekly patterns (batch jobs, weekend traffic, month-end spikes). Default `--days 14`, allow up to 90.

```
WRONG:  --days 3   -> Misses weekend batch jobs
WRONG:  --days 1   -> Captures only one day's pattern
CORRECT: --days 14 -> Captures at least 2 full weekly cycles
```

### Rule 2: E2 Shared-Core Instances Have Hard CPU Limits

E2 shared-core VMs (e2-micro, e2-small, e2-medium) have CPU time limits, NOT burstable credits like AWS t-family. An e2-micro gets 2 vCPUs but is capped at 12.5% (0.25 vCPU equivalent) sustained. They cannot exceed their allocation even if idle beforehand.

**MANDATORY**: Do NOT treat E2 shared-core like AWS burstable. High CPU % on shared-core means the workload is hitting its hard cap.

```
WRONG:  e2-micro avg CPU 12% -> "underutilized, this is a 2-vCPU machine at only 12%"
CORRECT: e2-micro avg CPU 12% -> "near cap (12.5% limit). Consider upgrading to e2-small (25% cap)"
CORRECT: e2-small avg CPU 5% -> "using 5% of 25% cap, underutilized"
```

CPU cap reference:

| Machine Type | vCPUs | CPU Cap | Cap as % |
|-------------|-------|---------|----------|
| e2-micro | 2 | 0.25 vCPU | 12.5% |
| e2-small | 2 | 0.50 vCPU | 25% |
| e2-medium | 2 | 1.00 vCPU | 50% |

### Rule 3: Sole-Tenant Nodes -- Report Node Utilization, Not VM

On sole-tenant nodes, VMs share a physical host. Rightsizing individual VMs without considering overall node fill rate is misleading.

**MANDATORY**: Flag sole-tenant VMs separately. The optimization is node fill rate, not individual VM utilization.

```
WRONG:  "vm-abc on sole-tenant node is at 5% CPU, downsize"
CORRECT: "vm-abc is on sole-tenant node node-group-xyz. Individual VM rightsizing deferred -- optimize node fill rate instead."
```

### Rule 4: Peak vs Average -- Never Downsize on Average Alone

An instance with avg CPU 10% but max CPU 95% is a bursty workload. Downsizing would cause failures during peaks.

**MANDATORY**: Report BOTH Average AND Maximum statistics. Only flag for downsizing if max < threshold too.

```
WRONG:  avg CPU 10% -> "downsize"
CORRECT: avg CPU 10%, max CPU 22% -> "downsize candidate (both avg and max are low)"
CORRECT: avg CPU 10%, max CPU 95% -> "bursty workload, do NOT downsize"
```

### Rule 5: Preemptible/Spot VMs -- Skip Rightsizing

Preemptible and Spot VMs already run at 60-91% discount. Rightsizing savings are marginal and the workload is already optimized for cost.

**MANDATORY**: Exclude preemptible/spot VMs from rightsizing analysis.

```
WRONG:  "preemptible vm-abc is underutilized, downsize"
CORRECT: "vm-abc is preemptible/spot -- skipped (already cost-optimized)"
```

### Rule 6: Savings Estimates Must Caveat CUD/SUD Coverage

GCP applies Sustained Use Discounts (SUDs) automatically (up to 30% for N1/N2) and Committed Use Discounts (CUDs) contractually. Downsizing a CUD-covered VM does NOT immediately save money -- the commitment continues.

**MANDATORY**: Caveat all savings estimates. Query CUD coverage when possible.

```
WRONG:  "Downsize to save $70/mo"
CORRECT: "Estimated on-demand savings: $70/mo. Note: if CUD-covered, savings may not apply until commitment expires. SUD automatically adjusts."
```

### Rule 7: Cloud SQL activationPolicy + HA Doubles Compute

Cloud SQL with `availabilityType=REGIONAL` (HA) doubles compute cost (standby replica). A db-custom-4-16384 HA instance costs 2x the single-zone price.

**MANDATORY**: Check `availabilityType` before estimating Cloud SQL costs.

```
WRONG:  db-custom-4-16384 -> $165/mo
CORRECT: db-custom-4-16384, availabilityType=REGIONAL -> $330/mo (HA doubles compute)
CORRECT: db-custom-4-16384, availabilityType=ZONAL -> $165/mo
```

### Rule 8: Persistent Disk Type Migration (pd-standard -> pd-balanced)

pd-standard (HDD) is $0.04/GiB/mo but limited to 0.75 IOPS/GiB. pd-balanced (SSD) is $0.10/GiB/mo with 6 IOPS/GiB baseline. A 200GiB pd-standard has only 150 IOPS baseline.

**MANDATORY**: Compare actual IOPS usage against baseline before recommending type changes.

```
WRONG:  "pd-standard is slower, just switch to pd-balanced"
CORRECT: "200GiB pd-standard: 150 IOPS baseline, actual avg 40 IOPS (27%). Right-sized for IOPS."
CORRECT: "200GiB pd-standard: 150 IOPS baseline, actual avg 140 IOPS (93%). Upgrade to pd-balanced for 1200 IOPS baseline."
```

### Rule 9: Cloud Functions/Cloud Run -- Flag Waste, Don't Prescribe Values

Serverless resource configuration is highly workload-specific. Flag obvious waste (allocated 4GiB, uses 200MiB) but do NOT recommend specific memory/CPU values. Let the user benchmark.

```
WRONG:  "Cloud Function allocates 2GiB, reduce to 256MiB"
CORRECT: "Cloud Function fn-abc allocates 2048MiB but peak memory usage is 180MiB. Candidate for memory reduction (benchmark required)."
```

### Rule 10: SUD Eligibility Varies by Machine Family

N1 and N2 families get automatic SUDs (up to 30%). E2 and T2D do NOT get SUDs. C3 and M3 do NOT get SUDs (use CUDs instead).

**MANDATORY**: Include SUD eligibility when showing savings.

```
WRONG:  "All VMs get 30% sustained use discount"
CORRECT: "n2-standard-4: SUD-eligible (up to 30% automatic discount)"
CORRECT: "e2-standard-4: NOT SUD-eligible (use CUDs for discounts)"
```

### Mandatory Pre-Analysis Checklist

**Before writing ANY rightsizing analysis, verify ALL of the following:**

- [ ] Observation window >= 14 days (see Rule 1)
- [ ] E2 shared-core instances analyzed against their CPU cap, not raw vCPU count (see Rule 2)
- [ ] Sole-tenant VMs identified and handled separately (see Rule 3)
- [ ] Both Average AND Maximum statistics reported for all metrics (see Rule 4)
- [ ] Preemptible/Spot VMs excluded (see Rule 5)
- [ ] Savings caveated as "based on on-demand rates; CUD/SUD may apply" (see Rule 6)
- [ ] Cloud SQL HA flag checked (see Rule 7)
- [ ] All cost figures include currency unit (USD)
- [ ] Parallel execution used for all Cloud Monitoring queries (see `gcp/SKILL.md`)

---

## Rightsizing Script (`get_rightsizing_gcp.sh`)

**DO NOT read or modify the script file.** Only source and call the functions.

**SETUP** (at the start of your script):

```bash
source ./_skills/connections/gcp/gcp-rightsizing/scripts/get_rightsizing_gcp.sh
```

**All functions enforce anti-hallucination rules**: 14-day minimum window, parallel Cloud Monitoring queries, TOON output format.

**FUNCTION REFERENCE**:

| Function | Purpose | Signature |
|----------|---------|-----------|
| `gcp_rightsizing_vms` | Compute Engine VM CPU analysis with shared-core, sole-tenant, preemptible handling | `[--days N] [--project PROJECT]` |
| `gcp_rightsizing_cloudsql` | Cloud SQL CPU + connections with HA cost awareness | `[--days N] [--project PROJECT]` |
| `gcp_rightsizing_disks` | Persistent Disk IOPS/throughput utilization, type migration candidates | `[--days N] [--project PROJECT]` |
| `gcp_rightsizing_serverless` | Cloud Functions + Cloud Run memory/CPU waste detection | `[--days N] [--project PROJECT]` |
| `gcp_rightsizing_summary` | Run all checks, output unified summary | `[--days N] [--project PROJECT]` |

**RECOMMENDED WORKFLOW** (every rightsizing analysis):

1. **Always run `gcp_rightsizing_vms` first** -- Compute Engine is typically the largest compute cost
2. **Run `gcp_rightsizing_cloudsql`** for database layer analysis
3. **Run `gcp_rightsizing_disks`** for storage optimization (pd-standard -> pd-balanced candidates)
4. **Run `gcp_rightsizing_serverless`** if Cloud Functions/Cloud Run is a significant cost driver
5. **Or run `gcp_rightsizing_summary`** for a unified view across all resource types

**Examples:**

```bash
source ./_skills/connections/gcp/gcp-rightsizing/scripts/get_rightsizing_gcp.sh

# VM utilization analysis (14-day default)
gcp_rightsizing_vms

# VM analysis with 30-day window in specific project
gcp_rightsizing_vms --days 30 --project my-project-id

# Cloud SQL utilization
gcp_rightsizing_cloudsql --days 14

# PD rightsizing (type migration candidates)
gcp_rightsizing_disks --days 14

# Cloud Functions + Cloud Run analysis
gcp_rightsizing_serverless --days 14

# Full summary across all resource types
gcp_rightsizing_summary --days 30 --project my-project-id
```

---

## GCP Machine Type Quick Reference

Approximate monthly on-demand costs in USD (us-central1, tax-exclusive). Use to validate savings estimates.

| Family | Machine Type | vCPU | Memory | ~Monthly USD | SUD Eligible |
|--------|-------------|------|--------|-------------|-------------|
| E2 | e2-micro | 2 (shared 0.25) | 1 GB | $6.11 | No |
| E2 | e2-small | 2 (shared 0.50) | 2 GB | $12.23 | No |
| E2 | e2-medium | 2 (shared 1.00) | 4 GB | $24.46 | No |
| E2 | e2-standard-2 | 2 | 8 GB | $48.92 | No |
| E2 | e2-standard-4 | 4 | 16 GB | $97.83 | No |
| E2 | e2-standard-8 | 8 | 32 GB | $195.67 | No |
| N2 | n2-standard-2 | 2 | 8 GB | $56.82 | Yes (up to 30%) |
| N2 | n2-standard-4 | 4 | 16 GB | $113.63 | Yes |
| N2 | n2-standard-8 | 8 | 32 GB | $227.26 | Yes |
| C3 | c3-standard-4 | 4 | 16 GB | $120.37 | No (CUD only) |
| N1 | n1-standard-1 | 1 | 3.75 GB | $24.27 | Yes (up to 30%) |
| N1 | n1-standard-2 | 2 | 7.5 GB | $48.55 | Yes |

**Downsizing savings:** Moving one size down within a family typically saves ~50% (e.g., e2-standard-8 $196 -> e2-standard-4 $98 = $98/mo savings).

For machine types not listed above, use `get_gcp_cost` from the `gcp/` skill.

---

## Cloud SQL Tier Reference

| Tier | vCPU | Memory | ~Monthly USD (Zonal) | ~Monthly USD (HA) |
|------|------|--------|---------------------|-------------------|
| db-f1-micro | shared | 0.6 GB | $10.80 | N/A |
| db-g1-small | shared | 1.7 GB | $36.00 | N/A |
| db-custom-1-3840 | 1 | 3.75 GB | $49.64 | $99.29 |
| db-custom-2-7680 | 2 | 7.5 GB | $99.29 | $198.58 |
| db-custom-4-15360 | 4 | 15 GB | $198.58 | $397.15 |
| db-custom-8-30720 | 8 | 30 GB | $397.15 | $794.30 |

---

## Persistent Disk Performance Reference

| Disk Type | $/GiB/mo | IOPS/GiB | Max IOPS | Throughput/GiB |
|-----------|----------|----------|----------|---------------|
| pd-standard | $0.04 | 0.75 R / 1.5 W | 7,500 | 0.12 MB/s |
| pd-balanced | $0.10 | 6 | 80,000 | 0.28 MB/s |
| pd-ssd | $0.17 | 30 | 100,000 | 0.48 MB/s |
| pd-extreme | $0.125 + IOPS | configurable | 120,000 | 1.2 GB/s |

---

## Cloud Monitoring Metrics Used

| Resource | Metric | Namespace | Aligner |
|----------|--------|-----------|---------|
| VM CPU | `instance/cpu/utilization` | `compute.googleapis.com` | ALIGN_MEAN, ALIGN_MAX |
| Cloud SQL CPU | `database/cpu/utilization` | `cloudsql.googleapis.com` | ALIGN_MEAN, ALIGN_MAX |
| Cloud SQL connections | `database/network/connections` | `cloudsql.googleapis.com` | ALIGN_MEAN |
| PD Read IOPS | `instance/disk/read_ops_count` | `compute.googleapis.com` | ALIGN_RATE |
| PD Write IOPS | `instance/disk/write_ops_count` | `compute.googleapis.com` | ALIGN_RATE |
| Cloud Function executions | `function/execution_count` | `cloudfunctions.googleapis.com` | ALIGN_RATE |
| Cloud Function memory | `function/user_memory_bytes` | `cloudfunctions.googleapis.com` | ALIGN_MAX |
| Cloud Run request count | `request_count` | `run.googleapis.com` | ALIGN_RATE |
| Cloud Run memory util | `container/memory/utilizations` | `run.googleapis.com` | ALIGN_MAX |

**CRITICAL**: `alignment-period` MUST be >= 60 seconds when using aligners other than ALIGN_NONE.

---

## Common Errors

| Error | Cause | Solution |
|-------|-------|---------|
| `PERMISSION_DENIED` on monitoring | Missing `monitoring.timeSeries.list` permission | Check service account roles |
| No data for VM CPU | Instance was recently created or restarted | Extend observation window |
| E2 shared-core appears underutilized | Comparing against 2 vCPUs instead of CPU cap | Use the CPU cap table (Rule 2) |
| Savings estimate seems too high | HA Cloud SQL not accounted for | Check `availabilityType`, double cost if REGIONAL (Rule 7) |
| Preemptible VM flagged for rightsizing | Script didn't filter scheduling policy | Check `scheduling.preemptible` field (Rule 5) |
| Cloud SQL shows as idle but has replicas | Read replicas are separate instances | Check for read replica relationships |
| Cloud Function memory unclear | Memory metric shows allocated, not peak | Use `function/user_memory_bytes` with ALIGN_MAX |

## Output Format

Present results as a structured report:
```
Gcp Rightsizing Report
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


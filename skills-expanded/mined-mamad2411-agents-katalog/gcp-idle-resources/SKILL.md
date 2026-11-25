---
name: gcp-idle-resources
description: |
  Use when working with Gcp Idle Resources — detect unused and idle GCP
  resources that incur cost without providing value. Covers unattached
  Persistent Disks, unused external IPs, stopped VMs, idle Cloud NAT, idle load
  balancers, old snapshots, idle Cloud SQL instances, abandoned GKE node pools,
  unused VPC connectors, and orphaned Filestore instances. Includes estimated
  monthly waste per resource and anti-hallucination rules for safe detection.
connection_type: gcp
preload: false
---

# GCP Idle Resources Skill

Detect unused and idle GCP resources with anti-hallucination guardrails and cost waste estimation.

**Relationship to other GCP skills:**

- `gcp-idle-resources/` -> "What is wasting money" (idle detection rules, cost estimation, protection label checks)
- `gcp/` -> "How to execute" (parallel patterns, filtering, monitoring aligners, billing/pricing scripts)
- `gcp-rightsizing/` -> "What is oversized" (utilization thresholds, downsize recommendations)

## CRITICAL: Idle Resource Detection Rules (Anti-Hallucination)

**These rules are MANDATORY when detecting idle resources. Violating them produces recommendations that can cause data loss or outages.**

### Rule 1: Unattached Persistent Disk != Always Deletable

Detached PDs (no `users` field) may be intentional (warm standby, manual backups, data archives). Report but NEVER auto-recommend deletion without user context.

```
WRONG:  "disk-abc is detached, delete it"
CORRECT: "disk-abc is detached, candidate for review. Created 2025-06-15, 100GiB pd-ssd, est. $17/mo"
```

### Rule 2: Stopped VMs (TERMINATED) Still Incur PD + IP Costs

When a Compute Engine instance is stopped (status=TERMINATED), compute charges stop but attached Persistent Disks and reserved External IPs continue to incur charges.

**MANDATORY**: Report the ongoing cost of stopped instances, not just the compute savings.

```
WRONG:  "vm-abc is stopped, no cost"
CORRECT: "vm-abc is stopped since 2025-12-01. Ongoing cost: 2x PDs ($24/mo) + 1 external IP ($7.20/mo) = $31.20/mo"
```

### Rule 3: External IP Cost: $0.010/hr ($7.20/mo) When Unused

Since February 2024, GCP charges for ALL external IPv4 addresses. Unused reserved IPs (status=RESERVED, not attached to any resource) cost $0.010/hr ($7.20/mo). In-use IPs on standard VMs cost $0.004/hr ($2.88/mo). IPs on forwarding rules are free.

```
WRONG:  "External IP attached to running instance is free"
CORRECT: "All external IPs cost money. IP 35.x.x.x is RESERVED (unattached) -- $7.20/mo pure waste"
```

### Rule 4: Cloud NAT: $0.0014/hr Per VM (Capped at $0.044/hr) + $0.045/GB

Cloud NAT charges per VM instance using the gateway ($0.0014/hr per VM, capped at $0.044/hr for 32+ VMs), plus $0.045/GB data processed. Even idle Cloud NAT gateways with a few VMs incur cost.

```
WRONG:  "Cloud NAT has low traffic, minimal cost"
CORRECT: "Cloud NAT nat-abc serves 5 VMs but < 10 active connections/day avg. Fixed cost: ~$5.04/mo + data processing"
```

### Rule 5: Snapshot Cost: $0.050/GiB/mo (Standard Regional)

Old snapshots accumulate silently. 1TiB of old snapshots = $51.20/mo. Snapshots backing machine images are required.

**MANDATORY**: Cross-reference with `gcloud compute images list` and `gcloud compute machine-images list` to exclude snapshots backing active images before flagging.

```
WRONG:  "snap-abc is 90 days old, delete it"
CORRECT: "snap-abc is 90 days old, 200GiB, est. $10/mo. NOT backing any image. Candidate for review."
CORRECT: "snap-def is 120 days old, 500GiB. BACKS image image-xyz -- skipped (required by image)."
```

### Rule 6: Never Recommend Deletion -- Only Flag

Always phrase results as "candidate for review" not "should be deleted". Resources may be intentionally idle (DR, staging, warm standby).

```
WRONG:  "Delete these 5 disks to save $87/mo"
CORRECT: "5 detached disks identified as candidates for review. Estimated waste: $87/mo if all are unnecessary."
```

### Rule 7: Check Protection Labels Before Flagging

Look for labels like `do-not-delete`, `keep`, `protected`, `backup`. GCP labels are always lowercase with hyphens/underscores. If found, mark as "PROTECTED -- skipped" in the output.

```
WRONG:  "disk-abc (labeled keep) is idle, candidate for deletion"
CORRECT: "disk-abc: PROTECTED (label: keep) -- skipped"
```

### Rule 8: Cloud SQL activationPolicy=NEVER Means Stopped, Not Idle

Cloud SQL instances with `activationPolicy=NEVER` are explicitly stopped by the user. They still incur storage costs. Do NOT confuse stopped Cloud SQL with idle (running but unused) Cloud SQL.

```
WRONG:  "Cloud SQL my-db is idle (activationPolicy=NEVER)"
CORRECT: "Cloud SQL my-db is STOPPED (activationPolicy=NEVER). Storage cost continues: 100GiB SSD = $17/mo"
```

### Rule 9: GKE Node Pools -- Only Flag Zero Nodes + No Autoscaler

A node pool with 0 nodes but autoscaler enabled is intentional (scale-to-zero). Only flag pools with 0 nodes AND autoscaling disabled or absent.

```
WRONG:  "node-pool-abc has 0 nodes, candidate for review"
CORRECT: "node-pool-abc has 0 nodes, autoscaler ENABLED (min=0, max=5) -- intentional, skipped"
CORRECT: "node-pool-def has 0 nodes, autoscaler DISABLED, initial=3. Candidate for review: may be abandoned."
```

### Mandatory Pre-Detection Checklist

**Before writing ANY idle resource analysis, verify ALL of the following:**

- [ ] Project context established (gcloud config or `--project`)
- [ ] Protection labels checked before flagging any resource (see Rule 7)
- [ ] Cost estimates use current on-demand pricing (see pricing table below)
- [ ] Results clearly state "candidates for review" not "should be deleted" (see Rule 6)
- [ ] Each resource shows estimated monthly waste
- [ ] All costs include currency unit (USD, tax-exclusive)
- [ ] Snapshot-image cross-reference performed (see Rule 5)
- [ ] Parallel execution used for all gcloud API calls (see `gcp/SKILL.md`)

---

## Idle Resources Script (`get_idle_resources_gcp.sh`)

**DO NOT read or modify the script file.** Only source and call the functions.

**SETUP** (at the start of your script):

```bash
source ./_skills/connections/gcp/gcp-idle-resources/scripts/get_idle_resources_gcp.sh
```

**All functions enforce anti-hallucination rules**: protection label checks, cost estimation, "candidate for review" language, TOON output format.

**FUNCTION REFERENCE**:

| Function | Purpose | Signature |
|----------|---------|-----------|
| `gcp_idle_disks` | Unattached Persistent Disks with cost estimate | `[--project PROJECT]` |
| `gcp_idle_ips` | External IPs with status RESERVED (unattached) | `[--project PROJECT]` |
| `gcp_idle_vms_stopped` | VMs stopped > N days with attached PD + IP cost | `[--days N] [--project PROJECT]` |
| `gcp_idle_nat` | Cloud NAT gateways with minimal/no traffic | `[--days N] [--project PROJECT]` |
| `gcp_idle_lb` | Forwarding rules with 0 healthy backends | `[--days N] [--project PROJECT]` |
| `gcp_idle_snapshots` | Snapshots older than N days, not backing images | `[--days N] [--project PROJECT]` |
| `gcp_idle_cloudsql` | Cloud SQL instances with very low utilization | `[--days N] [--project PROJECT]` |
| `gcp_idle_gke_nodepools` | GKE node pools with 0 nodes + autoscaler disabled | `[--project PROJECT]` |
| `gcp_idle_vpc_connectors` | VPC connectors with zero throughput | `[--days N] [--project PROJECT]` |
| `gcp_idle_filestore` | Filestore instances with 0 connected clients | `[--days N] [--project PROJECT]` |
| `gcp_idle_summary` | Run all checks, unified waste summary with total | `[--days N] [--project PROJECT]` |

**RECOMMENDED WORKFLOW** (every idle resource analysis):

1. **Run `gcp_idle_summary`** for a unified view of all idle resource types with total waste estimate
2. For deeper analysis of a specific category, run the individual function
3. Always review "PROTECTED" items separately -- they were intentionally labeled

**Examples:**

```bash
source ./_skills/connections/gcp/gcp-idle-resources/scripts/get_idle_resources_gcp.sh

# Full idle resource scan (default project)
gcp_idle_summary

# Full scan in specific project
gcp_idle_summary --days 30 --project my-project-id

# Detached Persistent Disks only
gcp_idle_disks

# Idle Cloud SQL instances (14-day window)
gcp_idle_cloudsql --days 14

# Unused External IPs
gcp_idle_ips

# Long-stopped VMs (60-day threshold)
gcp_idle_vms_stopped --days 60

# Idle Cloud NAT
gcp_idle_nat --days 14

# Old snapshots (120-day threshold)
gcp_idle_snapshots --days 120

# Abandoned GKE node pools
gcp_idle_gke_nodepools

# Unused VPC connectors
gcp_idle_vpc_connectors --days 7

# Orphaned Filestore instances
gcp_idle_filestore --days 14
```

---

## Resource Cost Reference

Approximate monthly costs in USD (tax-exclusive, us-central1). Use to validate waste estimates.

| Resource | Pricing Model | Typical Monthly Cost |
|----------|--------------|---------------------|
| PD standard (pd-standard) | $0.04/GiB/mo | 100GiB = $4 |
| PD balanced (pd-balanced) | $0.10/GiB/mo | 100GiB = $10 |
| PD SSD (pd-ssd) | $0.17/GiB/mo | 100GiB = $17 |
| PD extreme (pd-extreme) | $0.125/GiB/mo + IOPS | 100GiB = $12.50 + IOPS cost |
| External IP (unused/reserved) | $0.010/hr | $7.20/mo (pure waste) |
| External IP (in-use, standard VM) | $0.004/hr | $2.88/mo |
| Cloud NAT | $0.0014/hr/VM (cap $0.044/hr) + $0.045/GB | 5 VMs idle = ~$5.04/mo base |
| Forwarding rule (LB) | $0.025/hr per 5 rules | $18/mo per 5 rules |
| LB data processing | $0.008/GB | variable |
| Snapshot (standard regional) | $0.050/GiB/mo | 100GiB = $5 |
| Snapshot (archive) | $0.019/GiB/mo | 100GiB = $1.90 |
| Cloud SQL vCPU (Enterprise) | $0.0413/hr | ~$30.15/mo per vCPU |
| Cloud SQL memory (Enterprise) | $0.007/GB/hr | ~$5.11/mo per GB |
| Cloud SQL shared-core (db-f1-micro) | ~$0.0150/hr | ~$10.80/mo |
| Cloud SQL shared-core (db-g1-small) | ~$0.0500/hr | ~$36.00/mo |
| Cloud SQL SSD storage | $0.17/GiB/mo | 100GiB = $17 |
| Cloud SQL HDD storage | $0.09/GiB/mo | 100GiB = $9 |
| VPC connector (e2-micro, min 2) | ~$4.28/mo per instance | ~$8.56/mo minimum |
| Filestore Basic HDD | ~$0.20/GiB/mo | 1TiB = ~$204.80/mo |
| Filestore Basic SSD | ~$0.30/GiB/mo | 1TiB = ~$307.20/mo |

**Note:** All prices are TAX-EXCLUSIVE. Console shows tax-inclusive totals. See `gcp/SKILL.md` for VAT/tax handling.

For resources not listed above, use `get_gcp_cost` from the `gcp/` skill.

---

## GCP Detection Commands Reference

Quick reference for the gcloud CLI commands used to detect each idle resource type.

| Resource | Command | Key Filter |
|----------|---------|-----------|
| Unattached PD | `gcloud compute disks list --filter="-users:*"` | No `users` field = unattached |
| Unused External IP | `gcloud compute addresses list --filter="status:RESERVED AND addressType:EXTERNAL"` | RESERVED = unattached |
| Stopped VM | `gcloud compute instances list --filter="status:TERMINATED"` | TERMINATED = stopped |
| Cloud NAT | `gcloud compute routers nats list --router=R --region=REG` | Check via Cloud Monitoring metrics |
| Forwarding rules | `gcloud compute forwarding-rules list` | Check backend health via backend-services |
| Snapshots | `gcloud compute snapshots list` | Age filter + image cross-reference |
| Cloud SQL | `gcloud sql instances list` | CPU utilization via Cloud Monitoring |
| GKE node pools | `gcloud container node-pools list --cluster=C --location=L` | Check `autoscaling.enabled` + node count |
| VPC connectors | `gcloud compute networks vpc-access connectors list --region=R` | Check throughput via Cloud Monitoring |
| Filestore | `gcloud filestore instances list` | Check connected clients via Cloud Monitoring |

---

## Cloud Monitoring Metrics Used

| Resource | Metric | Namespace | Aligner |
|----------|--------|-----------|---------|
| Cloud NAT | `nat/open_connections` | `router.googleapis.com` | ALIGN_MEAN |
| Cloud SQL CPU | `database/cpu/utilization` | `cloudsql.googleapis.com` | ALIGN_MEAN |
| Cloud SQL connections | `database/network/connections` | `cloudsql.googleapis.com` | ALIGN_MEAN |
| VPC connector | `connector/sent_bytes_count` | `vpcaccess.googleapis.com` | ALIGN_RATE |
| Filestore | `nfs/server/connected_client_count` | `file.googleapis.com` | ALIGN_MEAN |
| LB requests | `https/request_count` | `loadbalancing.googleapis.com` | ALIGN_RATE |

**CRITICAL**: `alignment-period` MUST be >= 60 seconds when using aligners other than ALIGN_NONE.

---

## Common Errors

| Error | Cause | Solution |
|-------|-------|---------|
| `PERMISSION_DENIED` on monitoring | Missing `monitoring.timeSeries.list` permission | Check service account roles |
| `NOT_FOUND` for Cloud SQL metrics | Instance is stopped (`activationPolicy=NEVER`) | Report as stopped, not error (Rule 8) |
| Disk cost seems wrong | pd-extreme IOPS cost not included | Add provisioned IOPS cost for pd-extreme |
| Snapshot count very high | Account has many automated backups | Use `--days` to filter by age, cross-ref images |
| Cloud NAT shows as idle but is needed | Used for private subnet egress | Check VPC route tables before flagging |
| GKE node pool false positive | Pool uses autoscaler with min=0 | Check `autoscaling.enabled` before flagging (Rule 9) |
| VPC connector shows 0 throughput | Connector created but service uses Direct VPC Egress | Check Cloud Run/Functions config |

## Output Format

Present results as a structured report:
```
Gcp Idle Resources Report
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


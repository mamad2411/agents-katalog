---
name: cis-inspector-scan
description: Run an AWS Inspector CIS scan on a single EC2 instance, enforce readiness rules, fetch results, and save durable evidence with recovery-aware bash helpers.
---

# CIS Inspector Scan

Run an AWS Inspector CIS scan on a single EC2 instance, enforce readiness rules,
fetch results, and save durable evidence.

## When to use this skill

- Run an Inspector CIS scan on an EC2 instance
- Recover a previous scan by config ARN
- Validate Inspector CIS readiness before scanning
- Fetch and archive failed CIS controls

## Readiness rules (enforced by scripts)

A result is only valid when:
- `status = COMPLETED`
- `totalChecks > 0`

If either condition fails, the scripts exit non-zero. Partial evidence (scan.json)
is saved to help with troubleshooting, but aggregated-checks.json and
failed-controls.json are not created.

## Quick start

**Prerequisites:** The target instance must have a tag `instance_id=<instance-id>`. Add it if missing:

```bash
aws ec2 create-tags \
  --resources <i-xxx> \
  --tags Key=instance_id,Value=<i-xxx> \
  --profile <aws-profile> \
  --region <region>
```

### Single-command pipeline (recommended)

```bash
OUTDIR=~/.AGENTS-temp/<repo>/inspector-$(date +%Y%m%d-%H%M%S)
mkdir -p "$OUTDIR"

bash scripts/inspector_cis_full_pipeline.sh \
  --profile <aws-profile> \
  --region <region> \
  --instance-id <i-xxx> \
  --scan-name my-cis-scan-$(date +%Y%m%d) \
  --output-dir "$OUTDIR"
```

Exits 0 only on valid result. Auto-recovers once on timeout.

### Cleanup before scan (if stale configs exist)

```bash
bash scripts/inspector_cis_cleanup.sh \
  --profile <aws-profile> \
  --region <region> \
  --instance-id <i-xxx>
```

### Manual step-by-step workflow

```bash
OUTDIR=~/.AGENTS-temp/<repo>/inspector-$(date +%Y%m%d-%H%M%S)
mkdir -p "$OUTDIR"

# 1. Preflight
bash scripts/inspector_cis_preflight.sh \
  --profile <aws-profile> \
  --region <region> \
  --instance-id <i-xxx> \
  --output-dir "$OUTDIR"

# 2. Create scan (or recover existing)
bash scripts/inspector_cis_create_or_recover_scan.sh \
  --profile <aws-profile> \
  --region <region> \
  --instance-id <i-xxx> \
  --scan-name my-cis-scan-$(date +%Y%m%d) \
  --security-level LEVEL_2 \
  --output-dir "$OUTDIR"

# Extract the config ARN for next step
SCAN_CONFIG_ARN=$(cat "$OUTDIR/scan-config-arn.txt")

# 3. Fetch results (polls until COMPLETED or failure)
bash scripts/inspector_cis_fetch_results.sh \
  --profile <aws-profile> \
  --region <region> \
  --scan-config-arn "$SCAN_CONFIG_ARN" \
  --output-dir "$OUTDIR"

# 4. Reduce to failed controls only
bash scripts/inspector_cis_reduce_failed_controls.sh \
  --output-dir "$OUTDIR"
```

To recover an existing scan config instead of creating a new one:

```bash
# Skip step 2, use existing ARN directly in step 3
bash scripts/inspector_cis_create_or_recover_scan.sh \
  --profile <aws-profile> \
  --region <region> \
  --scan-config-arn <existing-arn> \
  --output-dir "$OUTDIR"

SCAN_CONFIG_ARN=$(cat "$OUTDIR/scan-config-arn.txt")
# Continue with step 3...
```

## Script flags

| Flag | Scripts | Required |
|---|---|---|
| `--profile` | preflight, create, fetch | yes |
| `--region` | preflight, create, fetch | yes |
| `--instance-id` | preflight, create | yes (create: only if not recovering) |
| `--output-dir` | all | yes |
| `--scan-config-arn` | create (recovery), fetch | conditional |
| `--scan-name` | create | yes (new scan) |
| `--security-level` | create | no (default: LEVEL_2) |

Note: `inspector_cis_reduce_failed_controls.sh` only requires `--output-dir`.

## Evidence saved

| File | Description |
|---|---|
| `preflight.json` | Preflight check results |
| `scan-config.json` | Raw scan configuration from Inspector |
| `scan.json` | Raw scan row (status, counts, ARNs) |
| `aggregated-targets.json` | Raw target aggregation for invalid scans when the diagnostic query succeeds |
| `target-status.json` | Concise status and reason for each target, or a diagnostic error when the query fails |
| `aggregated-checks.json` | Full aggregated check results |
| `failed-controls.json` | Reduced: only checks with failed count > 0 |

## Known failure modes

| Symptom | Likely cause | Resolution |
|---|---|---|
| `totalChecks = 0` | Metadata tags disabled, wrong accountIds, IAM gap, endpoint/DNS issue | Check preflight items in order |
| `Failed to get instance tags from instance metadata` | `InstanceMetadataTags` not enabled | Enable via modify-instance-metadata-options |
| `ConflictException` | Stale scan config from cancelled run | Auto-cleaned by create script (v2) |
| `status = FAILED` | SSM agent unhealthy, IAM missing `AmazonInspector2ManagedCisPolicy` | Fix IAM/SSM, retry |
| Infinite polling loop | (Fixed in v2) | Fetch script now uses list-all + Python filter |

Note: The create script automatically detects and deletes stale scan configs targeting
the same instance before creating a new one. This prevents ConflictException from
cancelled runs. The fetch script uses `list-cis-scans` (all) with Python filtering
instead of `--filter-criteria` to avoid bash quoting issues.

## IAM requirements

Instance profile must include:
- `AmazonSSMManagedInstanceCore`
- `AmazonInspector2ManagedCisPolicy`

## References

- `references/inspector-workflow.md` — step-by-step workflow and polling rules
- `references/source-artifacts.md` — proven scan examples and check counts

## Cleanup

After a scan completes, the scan config remains in Inspector. To avoid config sprawl:

```bash
# List existing configs
aws inspector2 list-cis-scan-configurations \
  --profile <aws-profile> \
  --region <region>

# Delete a config after use
aws inspector2 delete-cis-scan-configuration \
  --scan-configuration-arn <arn> \
  --profile <aws-profile> \
  --region <region>
```

One-time scan configs can be deleted immediately after fetching results.

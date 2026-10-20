---
name: managing-oracle-oci
description: |
  Use when working with Oracle Oci — oracle Cloud Infrastructure management via
  the OCI CLI. Covers compute instances, networking, block storage, databases,
  and IAM. Use when managing Oracle Cloud resources, checking instance health,
  or reviewing OCI infrastructure.
connection_type: oracle-oci
preload: false
---

# Managing Oracle Cloud Infrastructure

Manage Oracle Cloud Infrastructure using the `oci` CLI.

## MANDATORY: Discovery-First Pattern

**Always discover available resources before performing analysis.**

### Phase 1: Discovery

```bash
#!/bin/bash

COMPARTMENT_ID="${OCI_COMPARTMENT_ID:?Set OCI_COMPARTMENT_ID}"

echo "=== Compute Instances ==="
oci compute instance list --compartment-id "$COMPARTMENT_ID" \
    --query 'data[*].{id:id,name:"display-name",state:"lifecycle-state",shape:shape,region:region}' \
    --output table 2>/dev/null | head -30

echo ""
echo "=== VCNs ==="
oci network vcn list --compartment-id "$COMPARTMENT_ID" \
    --query 'data[*].{id:id,name:"display-name",cidr:"cidr-block",state:"lifecycle-state"}' \
    --output table 2>/dev/null | head -20

echo ""
echo "=== Block Volumes ==="
oci bv volume list --compartment-id "$COMPARTMENT_ID" \
    --query 'data[*].{id:id,name:"display-name",size:"size-in-gbs",state:"lifecycle-state"}' \
    --output table 2>/dev/null | head -20

echo ""
echo "=== DB Systems ==="
oci db system list --compartment-id "$COMPARTMENT_ID" \
    --query 'data[*].{id:id,name:"display-name",shape:shape,state:"lifecycle-state"}' \
    --output table 2>/dev/null | head -10

echo ""
echo "=== Autonomous Databases ==="
oci db autonomous-database list --compartment-id "$COMPARTMENT_ID" \
    --query 'data[*].{id:id,name:"display-name",cpus:"cpu-core-count",storage:"data-storage-size-in-tbs",state:"lifecycle-state"}' \
    --output table 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash

COMPARTMENT_ID="${OCI_COMPARTMENT_ID:?Set OCI_COMPARTMENT_ID}"
INSTANCE_ID="${1:?Instance OCID required}"

echo "=== Instance Details ==="
oci compute instance get --instance-id "$INSTANCE_ID" \
    --query 'data.{name:"display-name",state:"lifecycle-state",shape:shape,ocpus:"shape-config"."ocpus",memory:"shape-config"."memory-in-gbs",created:"time-created"}' \
    --output table 2>/dev/null

echo ""
echo "=== VNIC Attachments ==="
oci compute vnic-attachment list --compartment-id "$COMPARTMENT_ID" --instance-id "$INSTANCE_ID" \
    --query 'data[*].{id:"vnic-id",state:"lifecycle-state",subnet:"subnet-id"}' \
    --output table 2>/dev/null | head -10

echo ""
echo "=== Boot Volume ==="
oci compute boot-volume-attachment list --compartment-id "$COMPARTMENT_ID" \
    --availability-domain "$(oci compute instance get --instance-id "$INSTANCE_ID" --query 'data."availability-domain"' --raw-output)" \
    --instance-id "$INSTANCE_ID" \
    --query 'data[*].{id:"boot-volume-id",state:"lifecycle-state"}' \
    --output table 2>/dev/null

echo ""
echo "=== Monitoring Metrics ==="
oci monitoring metric-data summarize-metrics-data --compartment-id "$COMPARTMENT_ID" \
    --namespace oci_computeagent \
    --query-text "CpuUtilization[1h]{resourceId = \"$INSTANCE_ID\"}.mean()" \
    --query 'data[*].{name:name,timestamps:"aggregated-datapoints"[*].timestamp,values:"aggregated-datapoints"[*].value}' \
    --output table 2>/dev/null | head -20
```

## Output Format

```
ID                    NAME       STATE     SHAPE         REGION
ocid1.instance.oc1    web-01     RUNNING   VM.Standard3  us-ashburn-1
ocid1.instance.oc2    db-01      RUNNING   VM.Standard3  us-ashburn-1
```

## Safety Rules
- Use read-only commands: `list`, `get`, `summarize-metrics-data`
- Never run `terminate`, `delete`, `update` without explicit user confirmation
- Always pass `--compartment-id` for resource listing
- Use `--query` and `--output table` for clean output
- Limit output with `| head -N` to stay under 50 lines

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |


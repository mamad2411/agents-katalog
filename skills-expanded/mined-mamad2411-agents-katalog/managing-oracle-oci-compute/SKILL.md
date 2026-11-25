---
name: managing-oracle-oci-compute
description: |
  Use when working with Oracle Oci Compute — oracle OCI Compute deep-dive
  management via the OCI CLI. Covers instances, shapes, images, boot volumes,
  console connections, instance pools, and autoscaling. Use for detailed OCI
  compute analysis.
connection_type: oracle-oci-compute
preload: false
---

# Managing Oracle OCI Compute (Deep Dive)

Deep-dive Oracle OCI Compute management using the `oci compute` CLI commands.

## MANDATORY: Discovery-First Pattern

**Always discover available resources before performing analysis.**

### Phase 1: Discovery

```bash
#!/bin/bash

COMPARTMENT_ID="${OCI_COMPARTMENT_ID:?Set OCI_COMPARTMENT_ID}"
AD="${OCI_AD:-$(oci iam availability-domain list --compartment-id "$COMPARTMENT_ID" --query 'data[0].name' --raw-output 2>/dev/null)}"

echo "=== Instances ==="
oci compute instance list --compartment-id "$COMPARTMENT_ID" \
    --query 'data[*].{id:id,name:"display-name",state:"lifecycle-state",shape:shape,ad:"availability-domain",created:"time-created"}' \
    --output table 2>/dev/null | head -30

echo ""
echo "=== Instance Shapes (Available) ==="
oci compute shape list --compartment-id "$COMPARTMENT_ID" --availability-domain "$AD" \
    --query 'data[*].{shape:shape,ocpus:"ocpus",memory:"memory-in-gbs",gpus:"gpus",network:"networking-bandwidth-in-gbps"}' \
    --output table 2>/dev/null | head -20

echo ""
echo "=== Instance Pools ==="
oci compute-management instance-pool list --compartment-id "$COMPARTMENT_ID" \
    --query 'data[*].{id:id,name:"display-name",state:"lifecycle-state",size:size}' \
    --output table 2>/dev/null | head -10

echo ""
echo "=== Autoscaling Configurations ==="
oci autoscaling configuration list --compartment-id "$COMPARTMENT_ID" \
    --query 'data[*].{id:id,name:"display-name",type:"resource.type",cool_down:"cool-down-in-seconds"}' \
    --output table 2>/dev/null | head -10

echo ""
echo "=== Boot Volumes ==="
oci bv boot-volume list --compartment-id "$COMPARTMENT_ID" --availability-domain "$AD" \
    --query 'data[*].{id:id,name:"display-name",size:"size-in-gbs",state:"lifecycle-state",image:"image-id"}' \
    --output table 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash

COMPARTMENT_ID="${OCI_COMPARTMENT_ID:?Set OCI_COMPARTMENT_ID}"
INSTANCE_ID="${1:?Instance OCID required}"

echo "=== Instance Details ==="
oci compute instance get --instance-id "$INSTANCE_ID" \
    --query 'data.{name:"display-name",state:"lifecycle-state",shape:shape,ocpus:"shape-config".ocpus,memory_gb:"shape-config"."memory-in-gbs",ad:"availability-domain",fd:"fault-domain",created:"time-created",metadata:metadata}' \
    --output table 2>/dev/null

echo ""
echo "=== VNIC Details ==="
for vnic_id in $(oci compute vnic-attachment list --compartment-id "$COMPARTMENT_ID" --instance-id "$INSTANCE_ID" --query 'data[*]."vnic-id"' --raw-output 2>/dev/null | tr -d '[]" ' | tr ',' '\n'); do
    oci network vnic get --vnic-id "$vnic_id" \
        --query 'data.{id:id,private_ip:"private-ip",public_ip:"public-ip",subnet:"subnet-id",hostname:"hostname-label"}' \
        --output table 2>/dev/null
done | head -15

echo ""
echo "=== Boot Volume Attachments ==="
oci compute boot-volume-attachment list --compartment-id "$COMPARTMENT_ID" \
    --availability-domain "$(oci compute instance get --instance-id "$INSTANCE_ID" --query 'data."availability-domain"' --raw-output)" \
    --instance-id "$INSTANCE_ID" \
    --query 'data[*].{boot_volume_id:"boot-volume-id",state:"lifecycle-state",type:"encryption-in-transit-type"}' \
    --output table 2>/dev/null

echo ""
echo "=== Volume Attachments ==="
oci compute volume-attachment list --compartment-id "$COMPARTMENT_ID" --instance-id "$INSTANCE_ID" \
    --query 'data[*].{volume_id:"volume-id",state:"lifecycle-state",type:"attachment-type",device:device}' \
    --output table 2>/dev/null | head -10

echo ""
echo "=== Console History (last entry) ==="
oci compute console-history list --compartment-id "$COMPARTMENT_ID" --instance-id "$INSTANCE_ID" \
    --query 'data[0].{id:id,state:"lifecycle-state",created:"time-created"}' \
    --output table 2>/dev/null

echo ""
echo "=== Instance Monitoring ==="
oci monitoring metric-data summarize-metrics-data --compartment-id "$COMPARTMENT_ID" \
    --namespace oci_computeagent \
    --query-text "CpuUtilization[1h]{resourceId = \"$INSTANCE_ID\"}.mean()" \
    --query 'data[0]."aggregated-datapoints"[-5:]' \
    --output table 2>/dev/null | head -10
```

## Output Format

```
INSTANCE_OCID                         NAME      STATE    SHAPE           OCPUS  MEMORY
ocid1.instance.oc1.iad.abc123        web-01    RUNNING  VM.Standard3    2      32GB
ocid1.instance.oc1.iad.def456        db-01     RUNNING  VM.Standard3    4      64GB
```

## Safety Rules
- Use read-only commands: `list`, `get`, `summarize-metrics-data`
- Never run `terminate`, `stop`, `update` without explicit user confirmation
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


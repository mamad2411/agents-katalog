---
name: managing-ibm-cloud
description: |
  Use when working with Ibm Cloud — iBM Cloud infrastructure management via the
  ibmcloud CLI. Covers VPC instances, Kubernetes clusters, Cloud Foundry apps,
  databases, object storage, and billing. Use when managing IBM Cloud resources
  or reviewing infrastructure health.
connection_type: ibm-cloud
preload: false
---

# Managing IBM Cloud

Manage IBM Cloud infrastructure using the `ibmcloud` CLI.

## MANDATORY: Discovery-First Pattern

**Always discover available resources before performing analysis.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Account Info ==="
ibmcloud account show 2>/dev/null | head -10

echo ""
echo "=== Target Region ==="
ibmcloud target 2>/dev/null

echo ""
echo "=== VPC Instances ==="
ibmcloud is instances --output json 2>/dev/null | jq -r '.[] | "\(.id)\t\(.name)\t\(.zone.name)\t\(.profile.name)\t\(.status)\t\(.primary_network_interface.primary_ipv4_address // "N/A")"' | head -30

echo ""
echo "=== Kubernetes Clusters ==="
ibmcloud ks clusters --output json 2>/dev/null | jq -r '.[] | "\(.id)\t\(.name)\t\(.location)\t\(.state)\t\(.masterKubeVersion)"' | head -10

echo ""
echo "=== Resource Instances (Databases, Services) ==="
ibmcloud resource service-instances --output json 2>/dev/null | jq -r '.[] | "\(.id)\t\(.name)\t\(.region_id)\t\(.state)"' | head -20

echo ""
echo "=== VPCs ==="
ibmcloud is vpcs --output json 2>/dev/null | jq -r '.[] | "\(.id)\t\(.name)\t\(.status)\t\(.default_network_acl.name)"' | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash

INSTANCE_ID="${1:?Instance ID required}"

echo "=== Instance Details ==="
ibmcloud is instance "$INSTANCE_ID" --output json 2>/dev/null | jq '{
    id: .id,
    name: .name,
    status: .status,
    profile: .profile.name,
    zone: .zone.name,
    vcpu: .vcpu.count,
    memory: .memory,
    created: .created_at,
    primary_ip: .primary_network_interface.primary_ipv4_address
}'

echo ""
echo "=== Volume Attachments ==="
ibmcloud is instance-volume-attachments "$INSTANCE_ID" --output json 2>/dev/null | jq -r '.[] | "\(.id)\t\(.volume.name)\t\(.status)\t\(.type)"' | head -10

echo ""
echo "=== Network Interfaces ==="
ibmcloud is instance-network-interfaces "$INSTANCE_ID" --output json 2>/dev/null | jq -r '.[] | "\(.id)\t\(.name)\t\(.primary_ipv4_address)\t\(.subnet.name)"' | head -10

echo ""
echo "=== Billing Summary ==="
ibmcloud billing account-usage --output json 2>/dev/null | jq '{
    month: .month,
    billable_cost: .resources[].billable_cost,
    currency: .currency_code
}' | head -20
```

## Output Format

```
ID                    NAME      ZONE       PROFILE     STATUS   IP
0716-abc123-def456    web-01    us-south-1 bx2-2x8     running  10.0.0.5
0716-abc123-ghi789    db-01     us-south-2 bx2-4x16    running  10.0.1.3
```

## Safety Rules
- Use read-only commands: list, get, show, account-usage
- Never run `delete`, `stop`, `remove` without explicit user confirmation
- Use `--output json` with jq for structured output
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


---
name: managing-azure-dns
description: |
  Use when working with Azure Dns — azure DNS management covering public and
  private DNS zones, record sets, virtual network links, DNSSEC, and alias
  records. Use when managing Azure DNS zones, configuring DNS records, setting
  up private DNS for VNets, managing alias records for Azure resources, or
  troubleshooting DNS resolution.
connection_type: azure
preload: false
---

# Azure DNS Skill

Manage Azure public and private DNS zones, record sets, VNet links, and alias records.

## Core Helper Functions

```bash
#!/bin/bash

# List DNS zones
az_dns_zones() {
    az network dns zone list --output json 2>/dev/null
}

# List private DNS zones
az_private_dns_zones() {
    az network private-dns zone list --output json 2>/dev/null
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Public DNS Zones ==="
az network dns zone list -o json 2>/dev/null | jq -r '
    .[] | "\(.name)\t\(.resourceGroup)\t\(.numberOfRecordSets) records\tNS: \(.nameServers[0])"
' | column -t | head -15

echo ""
echo "=== Private DNS Zones ==="
az network private-dns zone list -o json 2>/dev/null | jq -r '
    .[] | "\(.name)\t\(.resourceGroup)\t\(.numberOfRecordSets) records\t\(.numberOfVirtualNetworkLinks) VNet links"
' | column -t | head -15

echo ""
echo "=== Record Set Summary ==="
for ZONE in $(az network dns zone list --query '[].name' -o tsv 2>/dev/null | head -10); do
    RG=$(az network dns zone list --query "[?name=='$ZONE'].resourceGroup" -o tsv 2>/dev/null)
    COUNTS=$(az network dns record-set list -g "$RG" -z "$ZONE" --query '[].type' -o tsv 2>/dev/null | sed 's|Microsoft.Network/dnszones/||' | sort | uniq -c | sort -rn | tr '\n' '  ')
    echo "$ZONE: $COUNTS"
done | head -10

echo ""
echo "=== VNet Links (Private Zones) ==="
for ZONE in $(az network private-dns zone list --query '[].name' -o tsv 2>/dev/null | head -10); do
    RG=$(az network private-dns zone list --query "[?name=='$ZONE'].resourceGroup" -o tsv 2>/dev/null)
    az network private-dns link vnet list -g "$RG" -z "$ZONE" -o json 2>/dev/null | jq -r --arg z "$ZONE" '
        .[] | "\($z)\t\(.name)\t\(.registrationEnabled)\t\(.provisioningState)"
    '
done | column -t | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
ZONE="${1:?Zone name required}"
RG="${2:?Resource group required}"

echo "=== Zone Details ==="
az network dns zone show -n "$ZONE" -g "$RG" -o json 2>/dev/null | jq '{
    name, resourceGroup, numberOfRecordSets,
    nameServers, zoneType, registrationVirtualNetworks
}'

echo ""
echo "=== Record Sets ==="
az network dns record-set list -g "$RG" -z "$ZONE" -o json 2>/dev/null | jq -r '
    .[] | "\(.type | split("/") | last)\t\(.name)\t\(.ttl)s\t\(.aRecords // .cnameRecord // .txtRecords // .mxRecords // "alias" | tostring | .[0:60])"
' | sort | column -t | head -30

echo ""
echo "=== Alias Records ==="
az network dns record-set list -g "$RG" -z "$ZONE" -o json 2>/dev/null | jq '
    [.[] | select(.targetResource.id != null)] | .[] | {
        name, type: (.type | split("/") | last),
        targetResource: .targetResource.id
    }' | head -15
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `az` CLI with `--output json` and jq for parsing
- Always specify resource group and zone name

## Safety Rules
- **Read-only by default**: Use list/show commands for inspection
- **Never delete record sets** without explicit confirmation
- **VNet link changes** can break private DNS resolution for linked networks
- **Registration-enabled VNet links** auto-create records for VM NICs

## Output Format

Present results as a structured report:
```
Managing Azure Dns Report
═════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

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

## Common Pitfalls
- **Resource group required**: Most commands need `-g` resource group parameter
- **Public vs private**: Different CLI command groups (`dns zone` vs `private-dns zone`)
- **Alias records**: Point to Azure resources (LB, Traffic Manager, CDN) -- no TTL control
- **Zone delegation**: Child zones need NS records in parent zone
- **Private DNS auto-registration**: Creates A records for VMs automatically when enabled

---
name: managing-infoblox
description: |
  Use when working with Infoblox — infoblox DDI (DNS, DHCP, IPAM) management
  covering DNS zones, records, networks, IP address allocation, DHCP scopes, and
  grid health. Use when managing Infoblox DNS/DHCP infrastructure, auditing IP
  address usage, troubleshooting DNS resolution, or analyzing network allocation
  across the Infoblox grid.
connection_type: infoblox
preload: false
---

# Infoblox DDI Skill

Manage Infoblox DNS zones, DHCP, IPAM, network allocation, and grid health.

## Core Helper Functions

```bash
#!/bin/bash

IB_API="https://$INFOBLOX_HOST/wapi/v2.12"

ib_api() {
    local endpoint="$1"
    shift
    curl -s -k -u "$INFOBLOX_USERNAME:$INFOBLOX_PASSWORD" \
         -H "Content-Type: application/json" \
         "$IB_API/$endpoint" "$@"
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Grid Status ==="
ib_api "grid" | jq -r '.[] | "\(.name)\t\(.service_status)"'

echo ""
echo "=== Grid Members ==="
ib_api "member?_return_fields=host_name,platform,service_status,node_info" | jq -r '
    .[] | "\(.host_name)\t\(.platform)\t\(.service_status)"
' | column -t | head -15

echo ""
echo "=== DNS Zones ==="
ib_api "zone_auth?_return_fields=fqdn,view,zone_format,comment&_max_results=50" | jq -r '
    .[] | "\(.fqdn)\t\(.view)\t\(.zone_format)\t\(.comment // "")"
' | column -t | head -20

echo ""
echo "=== Networks (IPAM) ==="
ib_api "network?_return_fields=network,comment,network_view&_max_results=30" | jq -r '
    .[] | "\(.network)\t\(.network_view)\t\(.comment // "")"
' | column -t | head -20

echo ""
echo "=== DHCP Ranges ==="
ib_api "range?_return_fields=network,start_addr,end_addr,comment&_max_results=20" | jq -r '
    .[] | "\(.network)\t\(.start_addr)-\(.end_addr)\t\(.comment // "")"
' | column -t | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash
NETWORK="${1:?Network CIDR required (e.g., 10.0.0.0/24)}"

echo "=== Network Details ==="
ib_api "network?network=$NETWORK&_return_fields=network,comment,members,options,network_view" | jq '
    .[0] | {network, comment, network_view, members, options}
'

echo ""
echo "=== IP Address Utilization ==="
ib_api "network?network=$NETWORK&_return_fields=network,total_hosts,used_hosts" | jq -r '
    .[0] | "Network: \(.network)  Total: \(.total_hosts // "n/a")  Used: \(.used_hosts // "n/a")"
'

echo ""
echo "=== Host Records in Network ==="
ib_api "record:host?ipv4addr~=$NETWORK&_return_fields=name,ipv4addrs,view&_max_results=30" | jq -r '
    .[] | "\(.name)\t\(.ipv4addrs[0].ipv4addr)\t\(.view)"
' | column -t | head -20

echo ""
echo "=== Fixed Addresses (DHCP Reservations) ==="
ib_api "fixedaddress?network=$NETWORK&_return_fields=ipv4addr,mac,name,comment&_max_results=20" | jq -r '
    .[] | "\(.ipv4addr)\t\(.mac)\t\(.name // "")\t\(.comment // "")"
' | column -t | head -15

echo ""
echo "=== DNS Records for Zone ==="
ZONE="${2:-}"
if [ -n "$ZONE" ]; then
    ib_api "allrecords?zone=$ZONE&_return_fields=name,type,address,comment&_max_results=30" | jq -r '
        .[] | "\(.type)\t\(.name)\t\(.address // .canonical // "")\t\(.comment // "")"
    ' | column -t | head -20
fi
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use jq to parse WAPI JSON responses
- Always use `_max_results` to limit response size

## Safety Rules
- **Read-only by default**: Use GET requests for inspection
- **Never delete DNS records or networks** without explicit confirmation
- **DHCP scope changes** can cause IP conflicts or loss of connectivity
- **Grid restarts** affect DNS/DHCP services for all clients

## Output Format

Present results as a structured report:
```
Managing Infoblox Report
════════════════════════
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
- **WAPI versioning**: Use a supported WAPI version matching your Infoblox appliance
- **Self-signed certs**: Most Infoblox grids use self-signed SSL; use `-k` for curl
- **_max_results**: Default limit is 1000; set explicitly to avoid truncation
- **Network views**: Multi-tenancy uses network views; always specify the correct view
- **Extensible attributes**: Custom metadata stored as EA; query with `*EA_Name` syntax

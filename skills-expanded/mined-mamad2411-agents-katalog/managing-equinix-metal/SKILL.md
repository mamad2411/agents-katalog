---
name: managing-equinix-metal
description: |
  Use when working with Equinix Metal — equinix Metal bare metal infrastructure
  management via the metal CLI and Equinix Metal API. Covers devices, projects,
  VLANs, IPs, BGP sessions, and capacity. Use when managing Equinix Metal bare
  metal servers or networking.
connection_type: equinix-metal
preload: false
---

# Managing Equinix Metal

Manage Equinix Metal bare metal infrastructure using the `metal` CLI.

## MANDATORY: Discovery-First Pattern

**Always discover available resources before performing analysis.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Projects ==="
metal project get -o json 2>/dev/null | jq -r '.[] | "\(.id)\t\(.name)\t\(.created_at)"' | head -10

echo ""
echo "=== Devices ==="
metal device get -p "$METAL_PROJECT_ID" -o json 2>/dev/null | jq -r '.[] | "\(.id)\t\(.hostname)\t\(.facility.code)\t\(.plan.slug)\t\(.state)\t\(.ip_addresses[0].address // "N/A")"' | head -30

echo ""
echo "=== VLANs ==="
metal virtual-network get -p "$METAL_PROJECT_ID" -o json 2>/dev/null | jq -r '.virtual_networks[] | "\(.id)\t\(.description)\t\(.vxlan)\t\(.facility_code)"' | head -10

echo ""
echo "=== IP Reservations ==="
metal ip get -p "$METAL_PROJECT_ID" -o json 2>/dev/null | jq -r '.[] | "\(.id)\t\(.address)\t\(.cidr)\t\(.type)\t\(.facility.code)"' | head -10

echo ""
echo "=== SSH Keys ==="
metal ssh-key get -o json 2>/dev/null | jq -r '.[] | "\(.id)\t\(.label)\t\(.fingerprint)"' | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash

DEVICE_ID="${1:?Device ID required}"

echo "=== Device Details ==="
metal device get -i "$DEVICE_ID" -o json 2>/dev/null | jq '{
    id, hostname, state, plan: .plan.slug,
    facility: .facility.code, metro: .metro.code,
    os: .operating_system.slug,
    ip_addresses: [.ip_addresses[] | {address, cidr, address_family, public}],
    created_at, tags
}'

echo ""
echo "=== BGP Sessions ==="
metal device get -i "$DEVICE_ID" -o json 2>/dev/null | jq '[.bgp_sessions[]? | {id, status, learned_routes, default_route}]' | head -10

echo ""
echo "=== Network Ports ==="
metal device get -i "$DEVICE_ID" -o json 2>/dev/null | jq '[.network_ports[] | {id, name, type, bond: .bond?.name, virtual_networks: [.virtual_networks[]?.vxlan]}]' | head -15

echo ""
echo "=== Capacity ==="
metal capacity get -o json 2>/dev/null | jq '[to_entries[:5][] | {facility: .key, plans: [.value | to_entries[:5][] | {plan: .key, available: .value.available}]}]' | head -20

echo ""
echo "=== Events ==="
metal event get -p "$METAL_PROJECT_ID" -o json 2>/dev/null | jq -r '.[] | "\(.created_at)\t\(.type)\t\(.body)"' | head -10
```

## Output Format

```
ID                                    HOSTNAME   FACILITY  PLAN         STATE
abc123-def456-ghi789                  web-01     sv15      c3.small.x86 active
abc123-def456-jkl012                  db-01      sv15      m3.large.x86 active
```

## Safety Rules
- Use read-only commands: `get`, `list`
- Never run `delete`, `destroy`, `power-off` without explicit user confirmation
- Use `-o json` with jq for structured output parsing
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


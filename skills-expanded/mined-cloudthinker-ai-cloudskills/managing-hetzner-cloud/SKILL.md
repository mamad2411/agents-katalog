---
name: managing-hetzner-cloud
description: |
  Use when working with Hetzner Cloud — hetzner Cloud deep-dive management via
  the hcloud CLI. Covers server types, pricing, placement groups, certificates,
  primary IPs, and detailed server metrics. Use for detailed Hetzner Cloud
  analysis beyond basic server listing.
connection_type: hetzner-cloud
preload: false
---

# Managing Hetzner Cloud (Deep Dive)

Deep-dive Hetzner Cloud management using the `hcloud` CLI for detailed analysis.

## MANDATORY: Discovery-First Pattern

**Always discover available resources before performing analysis.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Server Types (Available) ==="
hcloud server-type list -o columns=id,name,description,cores,memory,disk,storage_type 2>/dev/null | head -20

echo ""
echo "=== Placement Groups ==="
hcloud placement-group list -o columns=id,name,type,servers 2>/dev/null | head -10

echo ""
echo "=== Primary IPs ==="
hcloud primary-ip list -o columns=id,name,type,ip,datacenter,assignee_id,auto_delete 2>/dev/null | head -10

echo ""
echo "=== Certificates ==="
hcloud certificate list -o columns=id,name,type,domain_names,not_valid_after 2>/dev/null | head -10

echo ""
echo "=== Images ==="
hcloud image list --type system -o columns=id,name,description,os_flavor,os_version,disk_size 2>/dev/null | head -15

echo ""
echo "=== Snapshots ==="
hcloud image list --type snapshot -o columns=id,description,created,image_size,disk_size 2>/dev/null | head -10

echo ""
echo "=== Backups ==="
hcloud image list --type backup -o columns=id,description,created,image_size,created_from_name 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash

SERVER_ID="${1:?Server ID required}"

echo "=== Server Details ==="
hcloud server describe "$SERVER_ID" -o json 2>/dev/null | jq '{
    id, name, status,
    server_type: .server_type.name,
    cores: .server_type.cores,
    memory: .server_type.memory,
    disk: .server_type.disk,
    datacenter: .datacenter.name,
    location: .datacenter.location.city,
    public_ipv4: .public_net.ipv4.ip,
    public_ipv6: .public_net.ipv6.ip,
    private_nets: [.private_net[] | {network: .network, ip: .ip}],
    image: .image.name,
    iso: .iso,
    rescue_enabled: .rescue_enabled,
    locked: .locked,
    protection: .protection,
    labels: .labels,
    created: .created
}'

echo ""
echo "=== Server Metrics (CPU last 1h) ==="
hcloud server metrics "$SERVER_ID" --type cpu --start "$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" --end "$(date -u +%Y-%m-%dT%H:%M:%SZ)" -o json 2>/dev/null | jq '.metrics.timeseries[] | {name: .labels.mode, values: [.values[-5:][]]}' | head -20

echo ""
echo "=== Server Metrics (Disk I/O last 1h) ==="
hcloud server metrics "$SERVER_ID" --type disk --start "$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" --end "$(date -u +%Y-%m-%dT%H:%M:%SZ)" -o json 2>/dev/null | jq '.metrics.timeseries[] | {name: .labels | to_entries | map(.value) | join("-"), values_tail: [.values[-3:][]]}' | head -15

echo ""
echo "=== Server Metrics (Network last 1h) ==="
hcloud server metrics "$SERVER_ID" --type network --start "$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" --end "$(date -u +%Y-%m-%dT%H:%M:%SZ)" -o json 2>/dev/null | jq '.metrics.timeseries[] | {name: .labels | to_entries | map(.value) | join("-"), values_tail: [.values[-3:][]]}' | head -15
```

## Output Format

```
ID       NAME       STATUS    TYPE    CORES  MEMORY  DATACENTER  IP
123456   web-01     running   cx21    2      4GB     fsn1-dc14   1.2.3.4
```

## Safety Rules
- Use read-only commands: `list`, `describe`, `metrics`
- Never run `delete`, `shutdown`, `rebuild` without explicit user confirmation
- Use `-o json` with jq for detailed output, `-o columns=` for summaries
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


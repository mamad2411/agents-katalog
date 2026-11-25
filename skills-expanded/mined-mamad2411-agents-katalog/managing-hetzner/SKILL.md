---
name: managing-hetzner
description: |
  Use when working with Hetzner — hetzner Cloud and dedicated server management
  via the hcloud CLI and Hetzner API. Covers servers, volumes, networks,
  firewalls, load balancers, and snapshots. Use when managing Hetzner
  infrastructure or checking server health.
connection_type: hetzner
preload: false
---

# Managing Hetzner

Manage Hetzner infrastructure using the `hcloud` CLI and Hetzner Robot API.

## MANDATORY: Discovery-First Pattern

**Always discover available resources before performing analysis.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Hetzner Cloud Servers ==="
hcloud server list -o columns=id,name,status,server_type,datacenter,ipv4,created 2>/dev/null | head -30

echo ""
echo "=== Volumes ==="
hcloud volume list -o columns=id,name,size,server,location,created 2>/dev/null | head -20

echo ""
echo "=== Networks ==="
hcloud network list -o columns=id,name,ip_range,servers 2>/dev/null | head -10

echo ""
echo "=== Firewalls ==="
hcloud firewall list -o columns=id,name,rules_count,applied_to_count 2>/dev/null | head -10

echo ""
echo "=== Load Balancers ==="
hcloud load-balancer list -o columns=id,name,type,location,ipv4 2>/dev/null | head -10

echo ""
echo "=== SSH Keys ==="
hcloud ssh-key list -o columns=id,name,fingerprint 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash

SERVER_ID="${1:?Server ID required}"

echo "=== Server Details ==="
hcloud server describe "$SERVER_ID" 2>/dev/null

echo ""
echo "=== Server Metrics (CPU, Disk, Network) ==="
hcloud server metrics "$SERVER_ID" --type cpu,disk,network --start "$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" --end "$(date -u +%Y-%m-%dT%H:%M:%SZ)" 2>/dev/null | head -30

echo ""
echo "=== Snapshots ==="
hcloud image list --type snapshot -o columns=id,description,created,image_size,disk_size 2>/dev/null | head -10

echo ""
echo "=== Floating IPs ==="
hcloud floating-ip list -o columns=id,type,ip,server,home_location 2>/dev/null | head -10
```

## Output Format

```
ID       NAME       STATUS    TYPE     DATACENTER  IP
123456   web-01     running   cx21     fsn1-dc14   1.2.3.4
123457   db-01      running   cx31     nbg1-dc3    5.6.7.8
```

## Safety Rules
- Use read-only commands: `list`, `describe`, `metrics`
- Never run `delete`, `shutdown`, `reset` without explicit user confirmation
- Use `-o columns=` for clean, targeted output
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


---
name: managing-linode
description: |
  Use when working with Linode — linode (Akamai Cloud) infrastructure management
  via the linode-cli. Covers Linodes, NodeBalancers, volumes, domains,
  databases, and Kubernetes (LKE). Use when managing Linode/Akamai resources or
  checking instance health.
connection_type: linode
preload: false
---

# Managing Linode (Akamai Cloud)

Manage Linode infrastructure using the `linode-cli`.

## MANDATORY: Discovery-First Pattern

**Always discover available resources before performing analysis.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Account Info ==="
linode-cli account view --text --no-headers --format 'email,balance,active_since' 2>/dev/null

echo ""
echo "=== Linodes ==="
linode-cli linodes list --text --no-headers --format 'id,label,region,type,status,ipv4' 2>/dev/null | head -30

echo ""
echo "=== Volumes ==="
linode-cli volumes list --text --no-headers --format 'id,label,size,region,linode_id,status' 2>/dev/null | head -20

echo ""
echo "=== NodeBalancers ==="
linode-cli nodebalancers list --text --no-headers --format 'id,label,region,hostname,client_conn_throttle' 2>/dev/null | head -10

echo ""
echo "=== Databases ==="
linode-cli databases list --text --no-headers --format 'id,label,type,engine,region,status' 2>/dev/null | head -10

echo ""
echo "=== LKE Clusters ==="
linode-cli lke clusters-list --text --no-headers --format 'id,label,region,k8s_version,status' 2>/dev/null | head -10

echo ""
echo "=== Domains ==="
linode-cli domains list --text --no-headers --format 'id,domain,type,status' 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash

LINODE_ID="${1:?Linode ID required}"

echo "=== Linode Details ==="
linode-cli linodes view "$LINODE_ID" --text --no-headers --format 'id,label,region,type,status,ipv4,specs.vcpus,specs.memory,specs.disk,created' 2>/dev/null

echo ""
echo "=== Linode Stats (Last 24h) ==="
linode-cli linodes stats-view "$LINODE_ID" --text 2>/dev/null | head -20

echo ""
echo "=== Disks ==="
linode-cli linodes disks-list "$LINODE_ID" --text --no-headers --format 'id,label,size,filesystem,status' 2>/dev/null

echo ""
echo "=== Networking ==="
linode-cli linodes ips-list "$LINODE_ID" --text --no-headers 2>/dev/null | head -10

echo ""
echo "=== Firewalls ==="
linode-cli firewalls list --text --no-headers --format 'id,label,status,rules.inbound_policy,rules.outbound_policy' 2>/dev/null | head -10

echo ""
echo "=== Transfer Usage ==="
linode-cli linodes transfer-view "$LINODE_ID" --text --no-headers 2>/dev/null
```

## Output Format

```
ID        LABEL     REGION   TYPE         STATUS   IPV4
12345678  web-01    us-east  g6-standard  running  1.2.3.4
12345679  db-01     us-east  g6-dedicated running  5.6.7.8
```

## Safety Rules
- Use read-only commands: `list`, `view`, `stats-view`
- Never run `delete`, `shutdown`, `remove` without explicit user confirmation
- Use `--text --no-headers --format` for clean output
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


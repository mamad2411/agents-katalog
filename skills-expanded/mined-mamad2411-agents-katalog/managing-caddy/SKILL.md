---
name: managing-caddy
description: |
  Use when working with Caddy — caddy web server management, automatic TLS
  certificate handling, reverse proxy configuration, site management, and plugin
  inspection. Covers Caddyfile analysis, admin API usage, access logs, and
  upstream health monitoring. Read this skill before any Caddy operations — it
  enforces discovery-first patterns, anti-hallucination rules, and safety
  constraints.
connection_type: caddy
preload: false
---

# Caddy Management Skill

Monitor, analyze, and manage Caddy web servers safely.

## MANDATORY: Discovery-First Pattern

**Always query the Caddy admin API and current config before making changes. Never guess site names or upstream addresses.**

### Phase 1: Discovery

```bash
#!/bin/bash

CADDY_ADMIN="${CADDY_ADMIN:-http://localhost:2019}"

caddy_api() {
    curl -s "${CADDY_ADMIN}${1}"
}

echo "=== Caddy Version ==="
caddy version 2>/dev/null || caddy_api "/config/" | python3 -c "import sys; print('Admin API reachable')" 2>/dev/null

echo ""
echo "=== Running Configuration ==="
caddy_api "/config/" | python3 -m json.tool 2>/dev/null | head -50

echo ""
echo "=== Loaded Modules ==="
caddy list-modules 2>/dev/null | head -30

echo ""
echo "=== Listening Addresses ==="
caddy_api "/config/apps/http/servers" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for name, srv in data.items():
    listen = srv.get('listen', [])
    print(f'Server: {name} -> {listen}')
" 2>/dev/null

echo ""
echo "=== Process Info ==="
ps aux | grep '[c]addy' | awk '{print $1, $2, $9, $11}'
```

**Phase 1 outputs:** Server names, listen addresses, routes, upstream targets, loaded modules

### Phase 2: Analysis

Only inspect sites and upstreams confirmed in Phase 1 output.

## Anti-Hallucination Rules

- **NEVER assume site addresses** — always parse from running config or Caddyfile
- **NEVER guess upstream targets** — extract from `reverse_proxy` directives
- **NEVER assume certificate paths** — Caddy auto-manages TLS; check via admin API
- **NEVER assume plugin availability** — verify with `caddy list-modules`
- **ALWAYS query admin API** for live state rather than reading Caddyfile alone

## Safety Rules

- **READ-ONLY by default**: Use admin API GET endpoints, `caddy validate`, log reading
- **FORBIDDEN without explicit request**: `caddy stop`, config POST/PUT/DELETE, certificate deletion
- **ALWAYS validate**: Run `caddy validate --config Caddyfile` before applying changes
- **Admin API access**: The admin API is localhost-only by default — never expose it externally
- **Backup Caddyfile**: Always copy before editing

## Core Helper Functions

```bash
#!/bin/bash

CADDY_ADMIN="${CADDY_ADMIN:-http://localhost:2019}"

caddy_api() {
    curl -s "${CADDY_ADMIN}${1}"
}

# List all configured sites
list_sites() {
    caddy_api "/config/apps/http/servers" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for name, srv in data.items():
    for route in srv.get('routes', []):
        for match in route.get('match', [{}]):
            hosts = match.get('host', ['*'])
            print(f'{name}: {hosts}')
" 2>/dev/null
}

# Get reverse proxy upstreams
list_upstreams() {
    caddy_api "/config/" | python3 -c "
import json, sys
def find_upstreams(obj, path=''):
    if isinstance(obj, dict):
        if obj.get('handler') == 'reverse_proxy':
            ups = [u.get('dial','') for u in obj.get('upstreams', [])]
            print(f'{path}: {ups}')
        for k, v in obj.items():
            find_upstreams(v, f'{path}/{k}')
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            find_upstreams(v, f'{path}[{i}]')
find_upstreams(json.load(sys.stdin))
" 2>/dev/null
}
```

## Common Operations

### TLS Certificate Status

```bash
#!/bin/bash
echo "=== Managed Certificates ==="
caddy_api "/config/apps/tls" | python3 -m json.tool 2>/dev/null

echo ""
echo "=== Certificate Storage ==="
CADDY_DATA="${XDG_DATA_HOME:-$HOME/.local/share}/caddy"
if [ -d "$CADDY_DATA/certificates" ]; then
    find "$CADDY_DATA/certificates" -name "*.crt" | while read cert; do
        domain=$(basename "$(dirname "$cert")")
        expiry=$(openssl x509 -enddate -noout -in "$cert" 2>/dev/null | cut -d= -f2)
        echo "$domain -> expires: $expiry"
    done
else
    echo "Certificate storage: $CADDY_DATA (check path)"
fi

echo ""
echo "=== Auto-HTTPS Status ==="
caddy_api "/config/apps/http/servers" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for name, srv in data.items():
    auto = srv.get('automatic_https', {})
    print(f'{name}: auto_https={auto if auto else \"enabled (default)\"}')
" 2>/dev/null
```

### Reverse Proxy Configuration

```bash
#!/bin/bash
echo "=== Reverse Proxy Routes ==="
caddy_api "/config/" | python3 -c "
import json, sys
def find_proxies(obj, path=''):
    if isinstance(obj, dict):
        if obj.get('handler') == 'reverse_proxy':
            upstreams = [u.get('dial','') for u in obj.get('upstreams', [])]
            lb = obj.get('load_balancing', {}).get('selection_policy', {}).get('policy', 'random')
            health = obj.get('health_checks', {})
            print(f'Route: {path}')
            print(f'  Upstreams: {upstreams}')
            print(f'  LB Policy: {lb}')
            if health: print(f'  Health Checks: {json.dumps(health, indent=4)}')
            print()
        for k, v in obj.items():
            find_proxies(v, f'{path}/{k}')
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            find_proxies(v, f'{path}[{i}]')
find_proxies(json.load(sys.stdin))
" 2>/dev/null
```

### Site Management

```bash
#!/bin/bash
echo "=== All Configured Sites ==="
caddy_api "/config/apps/http/servers" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for name, srv in data.items():
    listen = srv.get('listen', [])
    print(f'\nServer: {name} (listen: {listen})')
    for i, route in enumerate(srv.get('routes', [])):
        matches = route.get('match', [{}])
        for m in matches:
            hosts = m.get('host', ['*'])
            path = m.get('path', ['*'])
            print(f'  Route {i}: hosts={hosts} path={path}')
" 2>/dev/null

echo ""
echo "=== Caddyfile Validation ==="
caddy validate --config "${CADDYFILE:-/etc/caddy/Caddyfile}" 2>&1 || echo "Caddyfile path may differ"
```

### Plugin Management

```bash
#!/bin/bash
echo "=== Installed Modules ==="
caddy list-modules --versions 2>/dev/null | head -40

echo ""
echo "=== Standard vs Non-Standard Modules ==="
caddy list-modules 2>/dev/null | awk '
    /^http/ || /^tls/ || /^caddy/ { standard++ }
    /^github/ || /^dns/ { nonstandard++; print "Plugin:", $0 }
    END { print "\nStandard:", standard+0, "Non-standard:", nonstandard+0 }
'
```

## Output Format

Present results as a structured report:
```
Managing Caddy Report
═════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Admin API is powerful**: POST/PUT/DELETE to admin API changes live config instantly — no reload needed but no rollback either
- **Caddyfile vs JSON config**: They are equivalent but transformations can lose comments; always keep source Caddyfile
- **Auto-HTTPS conflicts**: If port 80/443 is occupied, Caddy fails silently on ACME challenges
- **Placeholder syntax**: `{host}` in Caddyfile is a placeholder, not a literal — escape with `\{` if needed
- **`caddy reload` vs `caddy run`**: Reload sends config to running instance; `run` starts a new process
- **Global options block**: Must be the first block in Caddyfile — placing it elsewhere causes parse errors
- **Reverse proxy headers**: Caddy sets `X-Forwarded-For` by default but not `X-Real-IP` — configure `header_up` if needed

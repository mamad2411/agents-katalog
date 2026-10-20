---
name: managing-consul-kv
description: |
  Use when working with Consul Kv — consul KV store management, key namespace
  analysis, session/lock inspection, and watch configuration. Covers KV tree
  structure, key count by prefix, session health, prepared queries, and
  transaction support diagnostics. Read this skill before any Consul KV
  operations.
connection_type: consul
preload: false
---

# Consul KV Management Skill

Monitor, analyze, and optimize Consul KV store operations safely.

## MANDATORY: Discovery-First Pattern

**Always check Consul agent status and list KV prefixes before any key operations. Never assume key paths or session states.**

### Phase 1: Discovery

```bash
#!/bin/bash

CONSUL_ADDR="${CONSUL_HTTP_ADDR:-http://localhost:8500}"
CONSUL_TOKEN="${CONSUL_HTTP_TOKEN:+X-Consul-Token: $CONSUL_HTTP_TOKEN}"

echo "=== Agent Self ==="
curl -s ${CONSUL_TOKEN:+-H "$CONSUL_TOKEN"} "$CONSUL_ADDR/v1/agent/self" | python3 -c "
import sys, json
data = json.load(sys.stdin)
config = data.get('Config', {})
print(f\"Datacenter: {config.get('Datacenter','?')}\")
print(f\"Node: {config.get('NodeName','?')}\")
print(f\"Server: {config.get('Server', False)}\")
print(f\"Version: {config.get('Version','?')}\")
" 2>/dev/null

echo ""
echo "=== Cluster Members ==="
curl -s ${CONSUL_TOKEN:+-H "$CONSUL_TOKEN"} "$CONSUL_ADDR/v1/agent/members" | python3 -c "
import sys, json
for m in json.load(sys.stdin):
    print(f\"  {m['Name']}: {m['Addr']}:{m['Port']} | Status={m['Status']} | Type={'server' if m.get('Tags',{}).get('role')=='consul' else 'client'}\")
" 2>/dev/null

echo ""
echo "=== KV Top-Level Keys ==="
curl -s ${CONSUL_TOKEN:+-H "$CONSUL_TOKEN"} "$CONSUL_ADDR/v1/kv/?keys&separator=/" | python3 -c "
import sys, json
keys = json.load(sys.stdin)
print(f\"Top-level prefixes: {len(keys)}\")
for k in keys[:20]:
    print(f\"  {k}\")
" 2>/dev/null

echo ""
echo "=== Active Sessions ==="
curl -s ${CONSUL_TOKEN:+-H "$CONSUL_TOKEN"} "$CONSUL_ADDR/v1/session/list" | python3 -c "
import sys, json
sessions = json.load(sys.stdin)
print(f\"Active sessions: {len(sessions)}\")
for s in sessions[:10]:
    print(f\"  {s['ID'][:12]}... | Node: {s.get('Node','?')} | TTL: {s.get('TTL','none')} | Behavior: {s.get('Behavior','?')}\")
" 2>/dev/null
```

**Phase 1 outputs:** Datacenter, node info, cluster members, KV namespace tree, active sessions.

### Phase 2: Analysis

```bash
#!/bin/bash

CONSUL_ADDR="${CONSUL_HTTP_ADDR:-http://localhost:8500}"
CONSUL_TOKEN="${CONSUL_HTTP_TOKEN:+X-Consul-Token: $CONSUL_HTTP_TOKEN}"
PREFIX="${1:-}"

echo "=== Key Count by Prefix ==="
curl -s ${CONSUL_TOKEN:+-H "$CONSUL_TOKEN"} "$CONSUL_ADDR/v1/kv/$PREFIX?keys" | python3 -c "
import sys, json
keys = json.load(sys.stdin)
print(f\"Total keys under '{sys.argv[1] if len(sys.argv)>1 else '/'}': {len(keys)}\")
prefixes = {}
for k in keys:
    parts = k.strip('/').split('/')
    if parts:
        prefixes[parts[0]] = prefixes.get(parts[0], 0) + 1
for p, c in sorted(prefixes.items(), key=lambda x: -x[1])[:15]:
    print(f\"  {p}/: {c} keys\")
" "$PREFIX" 2>/dev/null

echo ""
echo "=== Locked Keys ==="
curl -s ${CONSUL_TOKEN:+-H "$CONSUL_TOKEN"} "$CONSUL_ADDR/v1/kv/$PREFIX?recurse" | python3 -c "
import sys, json
data = json.load(sys.stdin)
locked = [kv for kv in data if kv.get('Session')]
print(f\"Locked keys: {len(locked)}\")
for kv in locked[:10]:
    print(f\"  {kv['Key']}: session={kv['Session'][:12]}...\")
" 2>/dev/null || echo "No locked keys"

echo ""
echo "=== Prepared Queries ==="
curl -s ${CONSUL_TOKEN:+-H "$CONSUL_TOKEN"} "$CONSUL_ADDR/v1/query" | python3 -c "
import sys, json
queries = json.load(sys.stdin)
print(f\"Prepared queries: {len(queries)}\")
for q in queries[:5]:
    print(f\"  {q.get('Name','unnamed')}: service={q.get('Service',{}).get('Service','?')}\")
" 2>/dev/null || echo "No prepared queries"
```

## Output Format

```
CONSUL KV ANALYSIS
==================
Datacenter: [dc] | Node: [name] | Members: [count]
KV Prefixes: [count] | Total Keys: [count] | Sessions: [count]

ISSUES FOUND:
- [issue with affected prefix/session]

RECOMMENDATIONS:
- [actionable recommendation]
```

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


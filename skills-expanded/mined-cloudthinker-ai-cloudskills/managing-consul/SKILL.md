---
name: managing-consul
description: |
  Use when working with Consul — hashiCorp Consul service discovery and mesh
  management. Covers service registration, health checks, KV store operations,
  intentions (ACLs), Connect service mesh, datacenter federation, and prepared
  queries. Use when managing service discovery, debugging health checks,
  configuring service mesh intentions, or working with Consul KV store.
connection_type: consul
preload: false
---

# Consul Management Skill

Manage HashiCorp Consul service discovery, KV store, health checks, intentions, and Connect service mesh.

## Core Helper Functions

```bash
#!/bin/bash

# Consul CLI wrapper
consul_cmd() {
    consul "$@" 2>/dev/null
}

# Consul HTTP API helper
consul_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"
    local url="${CONSUL_HTTP_ADDR:-http://127.0.0.1:8500}"

    local auth_header=""
    if [ -n "${CONSUL_HTTP_TOKEN:-}" ]; then
        auth_header="-H \"X-Consul-Token: $CONSUL_HTTP_TOKEN\""
    fi

    if [ -n "$data" ]; then
        eval curl -s -X "$method" $auth_header -H "Content-Type: application/json" "${url}/v1/${endpoint}" -d "'$data'"
    else
        eval curl -s -X "$method" $auth_header "${url}/v1/${endpoint}"
    fi
}
```

## MANDATORY: Discovery-First Pattern

**Always discover cluster members and services before specific queries.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Consul Agent Info ==="
consul_api GET "agent/self" | jq '{
    datacenter: .Config.Datacenter,
    node_name: .Config.NodeName,
    server: .Config.Server,
    version: .Config.Version,
    acl_enabled: .DebugConfig.ACLsEnabled
}'

echo ""
echo "=== Cluster Members ==="
consul_api GET "agent/members" | jq -r '.[] | "\(.Name)\t\(.Addr)\t\(.Status)\t\(.Tags.role // "client")\t\(.Tags.dc)"' | column -t

echo ""
echo "=== Leader ==="
consul_api GET "status/leader"

echo ""
echo "=== Registered Services ==="
consul_api GET "catalog/services" | jq -r 'to_entries[] | "\(.key)\t\(.value | join(","))"' | column -t | head -30

echo ""
echo "=== Health Summary ==="
consul_api GET "health/state/critical" | jq -r '.[] | "\(.ServiceName)\t\(.Node)\t\(.CheckID)\t\(.Output[0:60])"' | column -t | head -15
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use Consul HTTP API with jq for structured output
- Never dump full service definitions -- extract key fields

## Common Operations

### Service Discovery Dashboard

```bash
#!/bin/bash
echo "=== Service Health Overview ==="
for svc in $(consul_api GET "catalog/services" | jq -r 'keys[]' | head -20); do
    TOTAL=$(consul_api GET "health/service/$svc" | jq 'length')
    PASSING=$(consul_api GET "health/service/$svc?passing" | jq 'length')
    echo "$svc: $PASSING/$TOTAL healthy"
done

echo ""
echo "=== Critical Checks ==="
consul_api GET "health/state/critical" | jq -r '
    .[] | "\(.ServiceName // "node-check")\t\(.Node)\t\(.Name)\t\(.Output[0:80])"
' | column -t | head -15

echo ""
echo "=== Warning Checks ==="
consul_api GET "health/state/warning" | jq -r '
    .[] | "\(.ServiceName // "node-check")\t\(.Node)\t\(.Name)"
' | column -t | head -10
```

### Service Detail Inspection

```bash
#!/bin/bash
SERVICE="${1:?Service name required}"

echo "=== Service Instances: $SERVICE ==="
consul_api GET "health/service/$SERVICE" | jq -r '
    .[] | "\(.Node.Node)\t\(.Service.Address):\(.Service.Port)\t\(.Checks | map(.Status) | join(","))\t\(.Service.Tags | join(","))"
' | column -t

echo ""
echo "=== Service Configuration ==="
consul_api GET "agent/service/$SERVICE" | jq '{
    id: .ID,
    service: .Service,
    address: .Address,
    port: .Port,
    tags: .Tags,
    meta: .Meta,
    connect: .Connect
}' 2>/dev/null

echo ""
echo "=== Health Checks ==="
consul_api GET "health/checks/$SERVICE" | jq -r '
    .[] | "\(.CheckID)\t\(.Status)\t\(.Type)\t\(.Notes[0:40])"
' | column -t
```

### KV Store Operations

```bash
#!/bin/bash
echo "=== KV Store Tree (top-level) ==="
consul_api GET "kv/?keys&separator=/" | jq -r '.[]' | head -30

echo ""
echo "=== KV Lookup ==="
KEY="${1:-}"
if [ -n "$KEY" ]; then
    consul_api GET "kv/$KEY" | jq -r '.[0] | {
        key: .Key,
        value: (.Value | @base64d),
        flags: .Flags,
        create_index: .CreateIndex,
        modify_index: .ModifyIndex
    }'
fi

echo ""
echo "=== KV Prefix Listing ==="
PREFIX="${2:-config/}"
consul_api GET "kv/${PREFIX}?recurse&keys" | jq -r '.[]' | head -20
```

### Intentions (Service-to-Service ACL)

```bash
#!/bin/bash
echo "=== All Intentions ==="
consul_api GET "connect/intentions" | jq -r '
    .[] | "\(.SourceName) -> \(.DestinationName)\t\(.Action)\t\(.CreatedAt[0:19])\t\(.Description[0:40])"
' | column -t | head -20

echo ""
echo "=== Denied Intentions ==="
consul_api GET "connect/intentions" | jq -r '
    [.[] | select(.Action == "deny")] | .[] |
    "\(.SourceName) -X-> \(.DestinationName)\t\(.Description[0:50])"
' | column -t

echo ""
echo "=== Check Intention ==="
SRC="${1:-web}"
DST="${2:-api}"
consul_api GET "connect/intentions/check?source=$SRC&destination=$DST" | jq '.Allowed'
```

### Connect Service Mesh Status

```bash
#!/bin/bash
echo "=== Connect CA Configuration ==="
consul_api GET "connect/ca/configuration" | jq '{
    provider: .Provider,
    config: .Config
}'

echo ""
echo "=== Connect Proxy Services ==="
consul_api GET "catalog/services" | jq -r 'to_entries[] | select(.key | test("-sidecar-proxy$")) | .key' | head -15

echo ""
echo "=== Mesh Gateway Status ==="
consul_api GET "catalog/service/mesh-gateway" | jq -r '
    .[]? | "\(.Node)\t\(.Address):\(.ServicePort)\t\(.Checks | map(.Status) | join(","))"
' | column -t

echo ""
echo "=== Datacenter Peers ==="
consul_api GET "catalog/datacenters" | jq -r '.[]'
```

## Safety Rules
- **Read-only by default**: Use GET requests for catalog, health, KV reads
- **Never delete** KV keys or deregister services without explicit user confirmation
- **ACL tokens**: Never expose Consul ACL tokens in output
- **Intention changes**: Modifying intentions can break service connectivity immediately

## Output Format

Present results as a structured report:
```
Managing Consul Report
══════════════════════
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
- **Health check flapping**: Check intervals too short cause flapping -- review check definitions
- **DNS caching**: Consul DNS TTL is 0 by default -- clients may cache stale results
- **KV size limit**: Values are limited to 512KB -- use for config, not bulk data
- **Intention precedence**: More specific intentions override wildcards -- check ordering
- **Connect sidecar ports**: Sidecar proxies bind to different ports than the main service

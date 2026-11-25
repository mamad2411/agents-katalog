---
name: managing-consul-connect
description: |
  Use when working with Consul Connect — hashiCorp Consul Connect service mesh
  management covering service discovery, intentions, sidecar proxies, mesh
  gateways, ingress/terminating gateways, certificate management, and health
  checks. Use when managing Consul Connect mesh, configuring service-to-service
  authorization, debugging proxy connections, or managing mesh gateways for
  multi-datacenter communication.
connection_type: consul
preload: false
---

# Consul Connect Service Mesh Skill

Manage Consul Connect service mesh, intentions, gateways, proxies, and service discovery.

## Core Helper Functions

```bash
#!/bin/bash

CONSUL_HTTP_ADDR="${CONSUL_HTTP_ADDR:-http://localhost:8500}"

consul_api() {
    local endpoint="$1"
    shift
    curl -s -H "X-Consul-Token: $CONSUL_HTTP_TOKEN" \
         "$CONSUL_HTTP_ADDR/v1/$endpoint" "$@"
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Consul Members ==="
consul members 2>/dev/null | head -15 || consul_api "agent/members" | jq -r '
    .[] | "\(.Name)\t\(.Addr)\t\(.Status)\t\(.Tags.role)\t\(.Tags.dc)"
' | column -t | head -15

echo ""
echo "=== Services ==="
consul_api "catalog/services" | jq -r 'to_entries[] | "\(.key)\tTags: \(.value | join(", "))"' | head -20

echo ""
echo "=== Connect Intentions ==="
consul_api "connect/intentions" | jq -r '
    .[] | "\(.SourceName)\t->\t\(.DestinationName)\t\(.Action)\t\(.Precedence)"
' | column -t | head -15

echo ""
echo "=== Mesh Gateways ==="
consul_api "catalog/service/mesh-gateway" | jq -r '
    .[]? | "\(.Node)\t\(.Address):\(.ServicePort)\t\(.Datacenter)\t\(.ServiceMeta.wan_address // "n/a")"
' | column -t | head -10

echo ""
echo "=== Ingress Gateways ==="
consul_api "catalog/service/ingress-gateway" | jq -r '
    .[]? | "\(.Node)\t\(.Address):\(.ServicePort)\t\(.Datacenter)"
' | column -t | head -10

echo ""
echo "=== Connect CA Info ==="
consul_api "connect/ca/roots" | jq '{
    ActiveRootID: .ActiveRootID[:12],
    TrustDomain: .TrustDomain,
    Roots: [.Roots[] | {ID: .ID[:12], Active: .Active, NotAfter: .NotAfter[:10]}]
}'
```

### Phase 2: Analysis

```bash
#!/bin/bash
SERVICE="${1:?Service name required}"

echo "=== Service Health ==="
consul_api "health/service/$SERVICE" | jq -r '
    .[] | "\(.Node.Node)\t\(.Service.Address):\(.Service.Port)\tStatus: \(.Checks | map(.Status) | join(","))"
' | column -t | head -15

echo ""
echo "=== Service Proxy Config ==="
consul_api "catalog/service/$SERVICE-sidecar-proxy" | jq '
    .[0]? | {
        Service: .ServiceName, Port: .ServicePort,
        Proxy: .ServiceProxy | {
            DestinationServiceName, LocalServicePort,
            Upstreams: [.Upstreams[]? | {DestinationName, LocalBindPort}]
        }
    }'

echo ""
echo "=== Intentions for Service ==="
consul_api "connect/intentions?filter=DestinationName==\"$SERVICE\"" | jq -r '
    .[] | "\(.SourceName)\t->\t\(.DestinationName)\t\(.Action)\tCreated: \(.CreatedAt[:10])"
' | column -t | head -10

echo ""
echo "=== Service Resolver ==="
consul_api "config/service-resolver/$SERVICE" | jq '{
    Name: .Name, DefaultSubset: .DefaultSubset,
    Subsets: .Subsets, Redirect: .Redirect, Failover: .Failover
}' 2>/dev/null

echo ""
echo "=== Service Splitter ==="
consul_api "config/service-splitter/$SERVICE" | jq '{
    Name: .Name, Splits: [.Splits[]? | {Weight, Service, ServiceSubset}]
}' 2>/dev/null
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use jq to parse Consul HTTP API responses
- Show intention relationships clearly (source -> destination)

## Safety Rules
- **Read-only by default**: Use catalog, health, and config GET endpoints
- **Intention changes** affect service-to-service authorization immediately
- **Never delete mesh gateways** without confirming cross-DC traffic impact
- **CA rotation** must follow Consul's built-in rotation procedure

## Output Format

Present results as a structured report:
```
Managing Consul Connect Report
══════════════════════════════
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
- **Default deny vs allow**: Intention default can be set to deny all -- check `acl.default_policy`
- **Sidecar naming**: Sidecar proxy service is `service-name-sidecar-proxy`
- **Datacenter isolation**: Services in different DCs need mesh gateways for Connect traffic
- **L4 vs L7 intentions**: L7 intentions require service protocol to be set to HTTP
- **ACL tokens**: Connect operations require specific ACL policies for service identity

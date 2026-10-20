---
name: managing-kong-mesh
description: |
  Use when working with Kong Mesh — kong Mesh service mesh management covering
  meshes, dataplanes, traffic policies, mesh gateways, mTLS configuration, and
  observability. Built on Kuma with enterprise features. Use when managing Kong
  Mesh instances, configuring service-to-service policies, debugging dataplane
  proxies, or setting up multi-zone mesh deployments.
connection_type: kong-mesh
preload: false
---

# Kong Mesh Skill

Manage Kong Mesh service mesh, dataplanes, traffic policies, gateways, and multi-zone configuration.

## Core Helper Functions

```bash
#!/bin/bash

KONG_MESH_API="${KONG_MESH_API_URL:-http://localhost:5681}"

km_api() {
    local endpoint="$1"
    shift
    curl -s "$KONG_MESH_API/$endpoint" "$@"
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Kong Mesh Version ==="
km_api "" | jq '{version, hostname, tagline, environment}'

echo ""
echo "=== Meshes ==="
km_api "meshes" | jq -r '
    .items[] | "\(.name)\tmTLS: \(.mtls.enabledBackend // "disabled")\tLogging: \(.logging.backends | length // 0) backends"
' | column -t | head -10

echo ""
echo "=== Dataplanes Overview ==="
km_api "mesh-insights" | jq -r '
    .items[] | "\(.name)\tOnline: \(.dataplanesByType.standard.online // 0)\tGateway: \(.dataplanesByType.gateway.online // 0)\tTotal: \(.dataplanesByType.standard.total // 0)"
' | column -t | head -10

echo ""
echo "=== Zones ==="
km_api "zones" | jq -r '
    .items[]? | "\(.name)\tEnabled: \(.enabled)"
' | column -t | head -10

echo ""
echo "=== Global Policies ==="
for policy in trafficpermissions trafficlogs traffictraces trafficroutes timeouts circuitbreakers healthchecks faultinjections retries ratelimits meshgateways meshgatewayroutes; do
    COUNT=$(km_api "$policy" 2>/dev/null | jq '.total // 0')
    [ "$COUNT" -gt 0 ] && echo "$policy: $COUNT"
done

echo ""
echo "=== OPA Policies (Enterprise) ==="
km_api "opapolicies" | jq -r '
    .items[]? | "\(.name)\t\(.mesh)\tEnabled: \(.enabled // true)"
' | column -t 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
MESH="${1:-default}"

echo "=== Mesh Configuration ==="
km_api "meshes/$MESH" | jq '{name, mtls, tracing, logging, metrics, routing}'

echo ""
echo "=== Dataplanes in Mesh ==="
km_api "meshes/$MESH/dataplanes" | jq -r '
    .items[] | "\(.name)\t\(.networking.address)\tService: \(.networking.inbound[0].tags["kuma.io/service"] // "n/a")"
' | column -t | head -15

echo ""
echo "=== Traffic Permissions ==="
km_api "meshes/$MESH/trafficpermissions" | jq -r '
    .items[] | "\(.name)\tSrc: \(.sources[0].match["kuma.io/service"] // "*")\tDst: \(.destinations[0].match["kuma.io/service"] // "*")"
' | column -t | head -15

echo ""
echo "=== Rate Limits ==="
km_api "meshes/$MESH/ratelimits" | jq '
    .items[]? | {name, sources: .sources[0].match, destinations: .destinations[0].match, conf: .conf}
' | head -15

echo ""
echo "=== Mesh Gateways ==="
km_api "meshes/$MESH/meshgateways" | jq '
    .items[]? | {name, selectors: .selectors, conf: .conf}
' | head -15
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use jq to parse Kong Mesh API responses
- Specify mesh context for all policy queries

## Safety Rules
- **Read-only by default**: Use GET endpoints for inspection
- **Traffic permission changes** affect authorization immediately
- **mTLS backend changes** can disrupt all mesh communication
- **Multi-zone policy propagation** affects all connected zones

## Output Format

Present results as a structured report:
```
Managing Kong Mesh Report
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
- **Kong Mesh vs Kuma**: Kong Mesh is commercial Kuma; API is compatible but has extra enterprise resources
- **OPA policies**: Enterprise feature; requires OPA sidecar configuration
- **Default deny**: Without traffic permissions, mesh defaults to deny all
- **Zone CP vs Global CP**: Policies are managed at global CP and synced to zone CPs
- **Gateway vs Gateway builtin**: MeshGateway is built-in; differs from Kong Gateway integration

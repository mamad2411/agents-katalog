---
name: managing-gloo-edge
description: |
  Use when working with Gloo Edge — gloo Edge API gateway management covering
  virtual services, upstreams, route tables, authentication policies, rate
  limiting, WAF, and transformation filters. Use when managing Gloo Edge gateway
  routing, configuring upstream discovery, debugging routing issues, setting up
  authentication, or analyzing API gateway performance.
connection_type: gloo-edge
preload: false
---

# Gloo Edge API Gateway Skill

Manage Gloo Edge virtual services, upstreams, route tables, auth, and rate limiting.

## Core Helper Functions

```bash
#!/bin/bash

GLOO_NS="${GLOO_NAMESPACE:-gloo-system}"

# Glooctl wrapper
gloo_cmd() {
    glooctl "$@" 2>/dev/null
}

# Get Gloo CRDs via kubectl
gloo_get() {
    local resource="$1" ns="${2:---all-namespaces}"
    if [ "$ns" = "--all-namespaces" ]; then
        kubectl get "$resource" -A -o json 2>/dev/null
    else
        kubectl get "$resource" -n "$ns" -o json 2>/dev/null
    fi
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Gloo Edge Version ==="
glooctl version 2>/dev/null | head -5

echo ""
echo "=== Control Plane Status ==="
glooctl check 2>/dev/null | head -20

echo ""
echo "=== Virtual Services ==="
gloo_get virtualservices | jq -r '
    .items[] | "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.virtualHost.domains | join(","))\t\(.status.statuses | keys[0] // "n/a"): \(.status.statuses | to_entries[0].value.state // "n/a")"
' | column -t | head -15

echo ""
echo "=== Upstreams ==="
gloo_get upstreams "$GLOO_NS" | jq -r '
    .items[] | "\(.metadata.name)\t\(.spec.kube.serviceName // .spec.static.hosts[0].addr // "unknown")\t\(.status.statuses | to_entries[0].value.state // "n/a")"
' | column -t | head -20

echo ""
echo "=== Gateways ==="
gloo_get gateways "$GLOO_NS" | jq -r '
    .items[] | "\(.metadata.name)\t\(.spec.bindAddress):\(.spec.bindPort)\t\(.spec.ssl // false)"
' | column -t | head -10

echo ""
echo "=== Route Tables ==="
gloo_get routetables | jq -r '
    .items[]? | "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.routes | length) routes"
' | column -t | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
VS_NAME="${1:?Virtual service name required}"
NS="${2:-gloo-system}"

echo "=== Virtual Service Config ==="
gloo_get virtualservices "$NS" | jq --arg name "$VS_NAME" '
    .items[] | select(.metadata.name == $name) | {
        name: .metadata.name, domains: .spec.virtualHost.domains,
        routes: [.spec.virtualHost.routes[]? | {
            matchers: .matchers, routeAction: .routeAction,
            options: (.options | keys? // [])
        }],
        status: .status
    }' | head -30

echo ""
echo "=== Upstream Health ==="
glooctl get upstreams -n "$NS" 2>/dev/null | head -15

echo ""
echo "=== Auth Config ==="
gloo_get authconfigs "$NS" | jq '
    .items[]? | {
        name: .metadata.name,
        configs: [.spec.configs[]? | keys]
    }' | head -15

echo ""
echo "=== Rate Limit Config ==="
gloo_get ratelimitconfigs "$NS" | jq '
    .items[]? | {
        name: .metadata.name,
        descriptors: .spec.raw.descriptors
    }' | head -15

echo ""
echo "=== Proxy Status ==="
glooctl proxy served-config 2>/dev/null | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `glooctl` for quick status checks and `kubectl` with jq for detailed CRD inspection
- Show route matching patterns clearly

## Safety Rules
- **Read-only by default**: Use get/check commands for inspection
- **Virtual service changes** affect routing immediately
- **Auth config changes** can lock out API consumers
- **Rate limit changes** take effect on next request

## Output Format

Present results as a structured report:
```
Managing Gloo Edge Report
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
- **Upstream discovery**: Gloo auto-discovers Kubernetes services; check upstream status for sync issues
- **Route order**: Routes are matched top-down; more specific routes must come first
- **Delegation**: Route tables can be delegated to other namespaces; check parent-child relationships
- **Transformation filters**: Invalid transformations cause 500 errors; test with `glooctl check`
- **Enterprise vs OSS**: Some features (WAF, ext-auth, rate-limit) require Gloo Edge Enterprise

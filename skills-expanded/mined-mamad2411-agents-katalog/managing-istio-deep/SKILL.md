---
name: managing-istio-deep
description: |
  Use when working with Istio Deep — advanced Istio service mesh management
  covering Envoy proxy debugging, Wasm extensions, multi-cluster mesh
  federation, ambient mesh, advanced traffic policies, rate limiting, circuit
  breaking, and observability integration. Use for deep Istio troubleshooting,
  Envoy sidecar debugging, multi-cluster service discovery, or advanced traffic
  management patterns.
connection_type: istio
preload: false
---

# Istio Deep Skill

Advanced Istio management including Envoy debugging, multi-cluster mesh, Wasm extensions, and advanced traffic policies.

## Core Helper Functions

```bash
#!/bin/bash

istio_cmd() {
    istioctl "$@" 2>/dev/null
}

istio_get() {
    local resource="$1" ns="${2:---all-namespaces}"
    if [ "$ns" = "--all-namespaces" ]; then
        kubectl get "$resource" -A -o json 2>/dev/null
    else
        kubectl get "$resource" -n "$ns" -o json 2>/dev/null
    fi
}

# Envoy admin API via port-forward
envoy_admin() {
    local pod="$1" ns="${2:-default}" path="${3:-stats}"
    kubectl exec "$pod" -n "$ns" -c istio-proxy -- curl -s "localhost:15000/$path" 2>/dev/null
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Istio Version & Revision ==="
istioctl version --short 2>/dev/null
kubectl get mutatingwebhookconfigurations -l app=sidecar-injector -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\tRevision: \(.metadata.labels["istio.io/rev"] // "default")"
'

echo ""
echo "=== Control Plane Health ==="
kubectl get pods -n istio-system -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.status.phase)\tRestarts: \(.status.containerStatuses[0].restartCount // 0)\tCPU: \(.spec.containers[0].resources.requests.cpu // "n/a")"
' | column -t

echo ""
echo "=== Mesh Configuration ==="
kubectl get configmap istio -n istio-system -o json 2>/dev/null | jq -r '.data.mesh' | head -20

echo ""
echo "=== Proxy Sync Status ==="
istioctl proxy-status 2>/dev/null | head -20

echo ""
echo "=== EnvoyFilter Resources ==="
kubectl get envoyfilters -A -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.configPatches | length) patches"
' | column -t | head -10

echo ""
echo "=== WasmPlugin Resources ==="
kubectl get wasmplugins -A -o json 2>/dev/null | jq -r '
    .items[]? | "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.url[:50])"
' | column -t | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
POD="${1:?Pod name required}"
NS="${2:-default}"

echo "=== Envoy Config Dump Summary ==="
envoy_admin "$POD" "$NS" "config_dump" | jq '{
    listeners: (.configs[] | select(.["@type"] | test("ListenersConfigDump")) | .dynamic_listeners | length),
    clusters: (.configs[] | select(.["@type"] | test("ClustersConfigDump")) | .dynamic_active_clusters | length),
    routes: (.configs[] | select(.["@type"] | test("RoutesConfigDump")) | .dynamic_route_configs | length)
}'

echo ""
echo "=== Envoy Cluster Health ==="
envoy_admin "$POD" "$NS" "clusters?format=json" | jq '
    .cluster_statuses[:10] | .[] | {
        name: .name, health: .host_statuses[0].health_status.eds_health_status,
        outlier_detected: .host_statuses[0].health_status.failed_outlier_check
    }'

echo ""
echo "=== Circuit Breaker Status ==="
istio_get destinationrules "$NS" | jq '
    .items[] | select(.spec.trafficPolicy.connectionPool or .spec.trafficPolicy.outlierDetection) | {
        name: .metadata.name, host: .spec.host,
        connectionPool: .spec.trafficPolicy.connectionPool,
        outlierDetection: .spec.trafficPolicy.outlierDetection
    }' | head -20

echo ""
echo "=== Rate Limiting Config ==="
istio_get envoyfilters "$NS" | jq '
    .items[] | select(.spec.configPatches[].applyTo == "HTTP_FILTER") | {
        name: .metadata.name,
        patches: [.spec.configPatches[] | .applyTo]
    }' | head -15

echo ""
echo "=== Proxy Resource Usage ==="
kubectl top pod "$POD" -n "$NS" --containers 2>/dev/null | grep istio-proxy
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Never dump full Envoy config -- extract relevant sections only
- Use `istioctl proxy-config` for targeted proxy inspection

## Safety Rules
- **Read-only by default**: Use analyze, proxy-status, proxy-config for inspection
- **EnvoyFilter changes** can break all mesh traffic if misconfigured
- **WasmPlugin errors** cause sidecar crashes -- test in staging first
- **Multi-cluster changes** affect cross-cluster service discovery

## Output Format

Present results as a structured report:
```
Managing Istio Deep Report
══════════════════════════
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
- **Envoy config size**: Full config dumps can be massive; always filter by section
- **EnvoyFilter ordering**: Multiple EnvoyFilters can conflict; priority field controls order
- **Revision-based upgrades**: Canary control plane upgrades require careful namespace relabeling
- **Ambient mesh**: Ztunnel-based datapath has different debugging than sidecar-based
- **Memory limits**: Envoy sidecars with large configs can OOM; check proxy resource limits

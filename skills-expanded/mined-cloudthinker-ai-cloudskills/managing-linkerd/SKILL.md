---
name: managing-linkerd
description: |
  Use when working with Linkerd — linkerd service mesh management for
  Kubernetes. Covers proxy injection, traffic splitting, service profiles,
  tap/top monitoring, mTLS verification, health checks, and dashboard access.
  Use when managing Linkerd mesh, debugging service communication, configuring
  traffic splits, or monitoring mesh health.
connection_type: linkerd
preload: false
---

# Linkerd Service Mesh Skill

Manage Linkerd service mesh, traffic splitting, service profiles, and observability.

## Core Helper Functions

```bash
#!/bin/bash

# Linkerd CLI wrapper
linkerd_cmd() {
    linkerd "$@" 2>/dev/null
}

# Get Linkerd CRDs via kubectl
linkerd_get() {
    local resource="$1"
    local ns="${2:---all-namespaces}"
    if [ "$ns" = "--all-namespaces" ]; then
        kubectl get "$resource" -A -o json 2>/dev/null
    else
        kubectl get "$resource" -n "$ns" -o json 2>/dev/null
    fi
}
```

## MANDATORY: Discovery-First Pattern

**Always check mesh health and injection status before performing operations.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Linkerd Version ==="
linkerd version 2>/dev/null

echo ""
echo "=== Control Plane Health ==="
linkerd check --pre 2>/dev/null | tail -20

echo ""
echo "=== Control Plane Pods ==="
kubectl get pods -n linkerd -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.status.phase)\t\(.status.containerStatuses[0].restartCount // 0) restarts"
' | column -t

echo ""
echo "=== Meshed Namespaces ==="
kubectl get namespaces -o json 2>/dev/null | jq -r '
    .items[] | select(.metadata.annotations["linkerd.io/inject"] == "enabled") | .metadata.name
'

echo ""
echo "=== Meshed Deployments ==="
linkerd stat deployments -A 2>/dev/null | head -25
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `linkerd stat` for quick metrics summaries
- Use `-o json` with jq for Linkerd CRDs via kubectl

## Common Operations

### Mesh Traffic Dashboard

```bash
#!/bin/bash
NS="${1:-default}"

echo "=== Deployment Stats: $NS ==="
linkerd stat deploy -n "$NS" 2>/dev/null | head -20

echo ""
echo "=== Top Routes (live traffic) ==="
linkerd top deploy -n "$NS" --hide-sources 2>/dev/null | head -15

echo ""
echo "=== Request Success Rates ==="
linkerd stat deploy -n "$NS" -o json 2>/dev/null | jq -r '
    .[] | "\(.resource)\t\(.successRate)\t\(.rps)\t\(.latencyP50)ms p50\t\(.latencyP99)ms p99"
' | column -t | head -20
```

### Service Profiles & Routes

```bash
#!/bin/bash
NS="${1:-default}"

echo "=== Service Profiles ==="
kubectl get serviceprofiles -n "$NS" -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.spec.routes | length) routes"
' | column -t

echo ""
echo "=== Route Metrics ==="
for sp in $(kubectl get serviceprofiles -n "$NS" -o jsonpath='{.items[*].metadata.name}' 2>/dev/null); do
    SVC=$(echo "$sp" | sed 's/\..*$//')
    echo "--- $SVC ---"
    linkerd routes deploy/"$SVC" -n "$NS" 2>/dev/null | head -10
done

echo ""
echo "=== Retry & Timeout Config ==="
kubectl get serviceprofiles -n "$NS" -o json 2>/dev/null | jq '
    .items[] | {
        name: .metadata.name,
        routes: [.spec.routes[] | {
            name: .name,
            timeout: .timeout,
            is_retryable: .isRetryable
        }]
    }' | head -30
```

### Traffic Split Management

```bash
#!/bin/bash
NS="${1:-default}"

echo "=== Active Traffic Splits ==="
kubectl get trafficsplits -n "$NS" -o json 2>/dev/null | jq -r '
    .items[] | {
        name: .metadata.name,
        service: .spec.service,
        backends: [.spec.backends[] | "\(.service): \(.weight)"]
    }'

echo ""
echo "=== Backend Health ==="
kubectl get trafficsplits -n "$NS" -o json 2>/dev/null | jq -r '.items[].spec.backends[].service' \
    | while read svc; do
        echo "--- $svc ---"
        linkerd stat deploy/"$svc" -n "$NS" 2>/dev/null | tail -1
    done
```

### mTLS Verification

```bash
#!/bin/bash
NS="${1:-default}"

echo "=== mTLS Status ==="
linkerd edges deploy -n "$NS" 2>/dev/null | head -20

echo ""
echo "=== Identity Certificates ==="
linkerd identity -n "$NS" 2>/dev/null | head -15

echo ""
echo "=== Tap: Live mTLS Connections ==="
linkerd tap deploy -n "$NS" --max-rps 5 2>/dev/null | head -10

echo ""
echo "=== Certificate Expiry ==="
kubectl get secret -n linkerd -o json 2>/dev/null | jq -r '
    .items[] | select(.metadata.name | test("issuer|ca")) |
    "\(.metadata.name)\t\(.type)"
' | column -t
```

### Health Check & Diagnostics

```bash
#!/bin/bash
echo "=== Full Health Check ==="
linkerd check 2>/dev/null | grep -E "^[√×‼]|Status" | head -30

echo ""
echo "=== Proxy Diagnostics ==="
POD="${1:-}"
NS="${2:-default}"
if [ -n "$POD" ]; then
    echo "--- Proxy for $POD ---"
    linkerd diagnostics proxy-metrics "$POD" -n "$NS" 2>/dev/null | head -20
    echo ""
    kubectl logs "$POD" -n "$NS" -c linkerd-proxy --tail 20 2>/dev/null
fi

echo ""
echo "=== Data Plane Integrity ==="
linkerd check --proxy -n "${NS:-default}" 2>/dev/null | grep -E "^[√×‼]" | head -15
```

## Safety Rules
- **Read-only by default**: Use `linkerd stat`, `linkerd check`, `linkerd edges` for inspection
- **Never modify** TrafficSplits without explicit user confirmation -- affects live traffic
- **Tap is intrusive**: `linkerd tap` captures live traffic -- use sparingly and with `--max-rps`
- **Injection changes**: Enabling/disabling injection requires pod restart to take effect

## Output Format

Present results as a structured report:
```
Managing Linkerd Report
═══════════════════════
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
- **Proxy not injected**: Check namespace annotation `linkerd.io/inject: enabled` and restart pods
- **TrafficSplit weights**: Weights are relative, not percentages -- ensure they sum correctly
- **Service profiles**: Must match the FQDN format `service.namespace.svc.cluster.local`
- **Control plane upgrades**: Linkerd requires sequential minor version upgrades -- no skipping
- **Opaque ports**: Some protocols need `config.linkerd.io/opaque-ports` annotation for proper proxying

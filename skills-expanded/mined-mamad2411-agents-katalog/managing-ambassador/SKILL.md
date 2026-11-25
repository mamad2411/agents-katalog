---
name: managing-ambassador
description: |
  Use when working with Ambassador — ambassador (Emissary-Ingress) API gateway
  management covering mappings, hosts, TLS contexts, authentication filters,
  rate limiting, and Envoy proxy configuration. Use when managing
  Ambassador/Emissary-Ingress routing, configuring API gateway mappings,
  debugging routing issues, setting up TLS termination, or analyzing gateway
  performance.
connection_type: ambassador
preload: false
---

# Ambassador (Emissary-Ingress) Skill

Manage Ambassador/Emissary-Ingress mappings, hosts, TLS, auth filters, and rate limiting.

## Core Helper Functions

```bash
#!/bin/bash

AMBASSADOR_NS="${AMBASSADOR_NAMESPACE:-ambassador}"

# Get Ambassador CRDs via kubectl
amb_get() {
    local resource="$1" ns="${2:---all-namespaces}"
    if [ "$ns" = "--all-namespaces" ]; then
        kubectl get "$resource" -A -o json 2>/dev/null
    else
        kubectl get "$resource" -n "$ns" -o json 2>/dev/null
    fi
}

# Ambassador diagnostics
amb_diag() {
    local pod
    pod=$(kubectl get pods -n "$AMBASSADOR_NS" -l app.kubernetes.io/name=emissary-ingress -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
    kubectl exec -n "$AMBASSADOR_NS" "$pod" -- curl -s "http://localhost:8877/$1" 2>/dev/null
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Ambassador Pods ==="
kubectl get pods -n "$AMBASSADOR_NS" -l app.kubernetes.io/name=emissary-ingress -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.status.phase)\tRestarts: \(.status.containerStatuses[0].restartCount // 0)\tVersion: \(.spec.containers[0].image | split(":") | last)"
' | column -t

echo ""
echo "=== Mappings ==="
amb_get mappings | jq -r '
    .items[] | "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.prefix // .spec.hostname // "*")\t->\t\(.spec.service)\t\(.spec.rewrite // "/")"
' | column -t | head -20

echo ""
echo "=== Hosts ==="
amb_get hosts | jq -r '
    .items[] | "\(.metadata.name)\t\(.spec.hostname)\t\(.spec.tlsSecret.name // "no-tls")\t\(.status.state // "n/a")"
' | column -t | head -15

echo ""
echo "=== TLS Contexts ==="
amb_get tlscontexts | jq -r '
    .items[]? | "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.hosts | join(",") // "all")\t\(.spec.secret // "n/a")"
' | column -t | head -10

echo ""
echo "=== Listeners ==="
amb_get listeners "$AMBASSADOR_NS" | jq -r '
    .items[]? | "\(.metadata.name)\t\(.spec.port)\t\(.spec.protocol)\t\(.spec.securityModel)"
' | column -t | head -10

echo ""
echo "=== Auth Services ==="
amb_get authservices | jq -r '
    .items[]? | "\(.metadata.name)\t\(.spec.auth_service)\t\(.spec.proto // "http")"
' | column -t | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
MAPPING="${1:?Mapping name required}"
NS="${2:-default}"

echo "=== Mapping Configuration ==="
amb_get mappings "$NS" | jq --arg name "$MAPPING" '
    .items[] | select(.metadata.name == $name) | {
        name: .metadata.name, prefix: .spec.prefix,
        service: .spec.service, rewrite: .spec.rewrite,
        host: .spec.host, hostname: .spec.hostname,
        timeout_ms: .spec.timeout_ms, retries: .spec.retry_policy,
        headers: .spec.headers, cors: .spec.cors,
        weight: .spec.weight, labels: .spec.labels
    }'

echo ""
echo "=== Diagnostics Overview ==="
amb_diag "ambassador/v0/diag/?json=true" | jq '{
    system: .system,
    envoy_status: .envoy_status,
    cluster_count: (.clusters | length),
    route_count: (.routes | length)
}' 2>/dev/null

echo ""
echo "=== Route Table ==="
amb_diag "ambassador/v0/diag/?json=true" | jq -r '
    .routes[:15][] | "\(.prefix // .regex // "*")\t\(.clusters[0].name // "n/a")\t\(.headers // [])"
' | column -t 2>/dev/null | head -15

echo ""
echo "=== Envoy Cluster Health ==="
amb_diag "ambassador/v0/diag/?json=true" | jq -r '
    .clusters[:10][] | "\(.name)\t\(.healthy_members // 0)/\(.num_members // 0) healthy"
' | column -t 2>/dev/null | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Show mapping prefix -> service relationships clearly
- Include relevant Ambassador CRD API version (v2 vs v3alpha1)

## Safety Rules
- **Read-only by default**: Use get/describe and diagnostics for inspection
- **Mapping changes** affect routing immediately after Envoy config reload
- **Host changes** can disrupt TLS termination
- **Auth service changes** can lock out all API consumers

## Output Format

Present results as a structured report:
```
Managing Ambassador Report
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
- **CRD versions**: v2 (getambassador.io/v2) vs v3alpha1 (getambassador.io/v3alpha1) have different fields
- **Mapping precedence**: Longer prefix matches win; use `weight` for same-prefix disambiguation
- **Rewrite default**: Default rewrite is `/`; set `rewrite: ""` to preserve original path
- **Host binding**: Mappings must be bound to Hosts via `hostname` field in v3
- **Diagnostics port**: 8877 is for diagnostics; do not expose externally

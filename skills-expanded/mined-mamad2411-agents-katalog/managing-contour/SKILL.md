---
name: managing-contour
description: |
  Use when working with Contour — contour ingress controller management covering
  HTTPProxy resources, TLS delegation, rate limiting, request policies,
  inclusion/delegation, and Envoy proxy configuration. Use when managing Contour
  HTTPProxy routing, configuring TLS with delegation, debugging Envoy proxy
  issues, setting up rate limiting, or analyzing ingress traffic patterns.
connection_type: contour
preload: false
---

# Contour Ingress Controller Skill

Manage Contour HTTPProxy resources, TLS delegation, rate limiting, and Envoy proxy configuration.

## Core Helper Functions

```bash
#!/bin/bash

CONTOUR_NS="${CONTOUR_NAMESPACE:-projectcontour}"

# Get Contour CRDs via kubectl
contour_get() {
    local resource="$1" ns="${2:---all-namespaces}"
    if [ "$ns" = "--all-namespaces" ]; then
        kubectl get "$resource" -A -o json 2>/dev/null
    else
        kubectl get "$resource" -n "$ns" -o json 2>/dev/null
    fi
}

# Contour CLI wrapper
contour_cmd() {
    kubectl exec -n "$CONTOUR_NS" deploy/contour -- contour "$@" 2>/dev/null
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Contour Pods ==="
kubectl get pods -n "$CONTOUR_NS" -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.status.phase)\tRestarts: \(.status.containerStatuses[0].restartCount // 0)"
' | column -t

echo ""
echo "=== HTTPProxy Resources ==="
contour_get httpproxies | jq -r '
    .items[] | "\(.metadata.namespace)\t\(.metadata.name)\t\(.spec.virtualhost.fqdn // "included")\tValid: \(.status.currentStatus // "n/a")\tDesc: \(.status.description // "")"
' | column -t | head -20

echo ""
echo "=== Standard Ingress Resources ==="
kubectl get ingress -A -o json 2>/dev/null | jq -r '
    .items[] | select(.spec.ingressClassName == "contour" or .metadata.annotations["kubernetes.io/ingress.class"] == "contour") |
    "\(.metadata.namespace)\t\(.metadata.name)\t\(.spec.rules[0].host // "*")"
' | column -t | head -10

echo ""
echo "=== TLS Certificates ==="
contour_get httpproxies | jq -r '
    .items[] | select(.spec.virtualhost.tls) |
    "\(.metadata.name)\t\(.spec.virtualhost.fqdn)\tSecret: \(.spec.virtualhost.tls.secretName // "delegation")\tMinVer: \(.spec.virtualhost.tls.minimumProtocolVersion // "1.2")"
' | column -t | head -15

echo ""
echo "=== TLS Certificate Delegations ==="
contour_get tlscertificatedelegations | jq -r '
    .items[]? | "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.delegations[].secretName)\t->\t\(.spec.delegations[].targetNamespaces | join(","))"
' | column -t | head -10

echo ""
echo "=== Envoy Service (Load Balancer) ==="
kubectl get svc -n "$CONTOUR_NS" envoy -o json 2>/dev/null | jq '{
    type: .spec.type, clusterIP: .spec.clusterIP,
    externalIPs: .status.loadBalancer.ingress,
    ports: [.spec.ports[] | {name, port, targetPort}]
}'
```

### Phase 2: Analysis

```bash
#!/bin/bash
HTTPPROXY="${1:?HTTPProxy name required}"
NS="${2:-default}"

echo "=== HTTPProxy Configuration ==="
contour_get httpproxies "$NS" | jq --arg name "$HTTPPROXY" '
    .items[] | select(.metadata.name == $name) | {
        fqdn: .spec.virtualhost.fqdn,
        tls: .spec.virtualhost.tls,
        routes: [.spec.routes[]? | {
            conditions: .conditions,
            services: [.services[] | {name, port, weight}],
            rateLimitPolicy: .rateLimitPolicy,
            retryPolicy: .retryPolicy,
            timeoutPolicy: .timeoutPolicy
        }],
        includes: .spec.includes,
        status: .status
    }'

echo ""
echo "=== Route Details ==="
contour_get httpproxies "$NS" | jq --arg name "$HTTPPROXY" '
    .items[] | select(.metadata.name == $name) | .spec.routes[]? | {
        conditions, services: [.services[] | "\(.name):\(.port) w=\(.weight // 100)"],
        requestHeaders: .requestHeadersPolicy,
        responseHeaders: .responseHeadersPolicy
    }' | head -25

echo ""
echo "=== Included HTTPProxies ==="
contour_get httpproxies "$NS" | jq --arg name "$HTTPPROXY" -r '
    .items[] | select(.metadata.name == $name) | .spec.includes[]? |
    "\(.name)\t\(.namespace)\tConditions: \(.conditions // [] | map(.prefix) | join(","))"
' | column -t | head -10

echo ""
echo "=== Contour Status ==="
contour_cmd "cli status" 2>/dev/null || kubectl logs -n "$CONTOUR_NS" deploy/contour --tail=10 2>/dev/null | grep -i "error\|warning" | tail -5
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Show FQDN -> route -> service relationships clearly
- Include HTTPProxy status (Valid/Invalid) in output

## Safety Rules
- **Read-only by default**: Use get/describe for inspection
- **HTTPProxy changes** affect Envoy routing after config sync
- **TLS delegation changes** can break TLS for dependent namespaces
- **Never delete root HTTPProxy** without checking for includes

## Output Format

Present results as a structured report:
```
Managing Contour Report
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
- **HTTPProxy vs Ingress**: Contour supports both; HTTPProxy is preferred for advanced features
- **Inclusion/delegation**: Child HTTPProxies must be in the correct namespace and explicitly included
- **Status validation**: HTTPProxy status shows Valid/Invalid; Invalid means Envoy won't serve it
- **TLS delegation**: Certificates can be shared across namespaces via TLSCertificateDelegation
- **Rate limiting**: Requires external rate limit service (e.g., Envoy ratelimit) to be deployed

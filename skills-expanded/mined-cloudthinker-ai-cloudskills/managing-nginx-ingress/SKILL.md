---
name: managing-nginx-ingress
description: |
  Use when working with Nginx Ingress — nGINX Ingress Controller management
  covering ingress resources, backend services, TLS configuration, annotations,
  rate limiting, custom error pages, and controller health. Use when managing
  NGINX Ingress in Kubernetes, debugging routing issues, configuring SSL
  termination, analyzing ingress traffic patterns, or troubleshooting upstream
  connectivity.
connection_type: nginx-ingress
preload: false
---

# NGINX Ingress Controller Skill

Manage NGINX Ingress resources, TLS, routing, annotations, and controller health.

## Core Helper Functions

```bash
#!/bin/bash

INGRESS_NS="${NGINX_INGRESS_NAMESPACE:-ingress-nginx}"

# Get ingress controller pod
ingress_pod() {
    kubectl get pods -n "$INGRESS_NS" -l app.kubernetes.io/component=controller -o jsonpath='{.items[0].metadata.name}' 2>/dev/null
}

# Query NGINX status
nginx_status() {
    kubectl exec -n "$INGRESS_NS" "$(ingress_pod)" -- curl -s "http://localhost:10246/$1" 2>/dev/null
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Ingress Controller Status ==="
kubectl get pods -n "$INGRESS_NS" -l app.kubernetes.io/component=controller -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.status.phase)\tRestarts: \(.status.containerStatuses[0].restartCount // 0)\tVersion: \(.spec.containers[0].image | split(":") | last)"
' | column -t

echo ""
echo "=== Ingress Resources ==="
kubectl get ingress -A -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.namespace)\t\(.metadata.name)\t\(.spec.rules[0].host // "*")\t\(.spec.tls | length) TLS\t\(.metadata.annotations["kubernetes.io/ingress.class"] // .spec.ingressClassName // "default")"
' | column -t | head -20

echo ""
echo "=== IngressClass Resources ==="
kubectl get ingressclass -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.spec.controller)\t\(.metadata.annotations["ingressclass.kubernetes.io/is-default-class"] // "false")"
' | column -t

echo ""
echo "=== Service Backends ==="
kubectl get ingress -A -o json 2>/dev/null | jq -r '
    .items[] | .spec.rules[]? | .http.paths[]? |
    "\(.backend.service.name // .backend.serviceName)\t\(.backend.service.port.number // .backend.servicePort)\t\(.path)\t\(.pathType // "Prefix")"
' | sort -u | column -t | head -20

echo ""
echo "=== TLS Certificates ==="
kubectl get ingress -A -o json 2>/dev/null | jq -r '
    .items[] | .spec.tls[]? | "\(.secretName)\t\(.hosts | join(", "))"
' | sort -u | column -t | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash
INGRESS_NAME="${1:?Ingress name required}"
NS="${2:-default}"

echo "=== Ingress Configuration ==="
kubectl get ingress "$INGRESS_NAME" -n "$NS" -o json 2>/dev/null | jq '{
    name: .metadata.name,
    namespace: .metadata.namespace,
    class: (.spec.ingressClassName // .metadata.annotations["kubernetes.io/ingress.class"]),
    rules: [.spec.rules[] | {host, paths: [.http.paths[] | {path, pathType, backend: .backend.service}]}],
    tls: .spec.tls,
    annotations: .metadata.annotations
}'

echo ""
echo "=== NGINX Config for Ingress ==="
POD=$(ingress_pod)
kubectl exec -n "$INGRESS_NS" "$POD" -- cat /etc/nginx/nginx.conf 2>/dev/null | grep -A5 "server_name.*$(kubectl get ingress "$INGRESS_NAME" -n "$NS" -o jsonpath='{.spec.rules[0].host}' 2>/dev/null)" | head -20

echo ""
echo "=== Backend Health ==="
nginx_status "nginx_status" 2>/dev/null || kubectl exec -n "$INGRESS_NS" "$POD" -- curl -s "http://localhost:10246/healthz" 2>/dev/null

echo ""
echo "=== Controller Metrics ==="
kubectl exec -n "$INGRESS_NS" "$POD" -- curl -s "http://localhost:10254/metrics" 2>/dev/null | grep -E "^nginx_ingress_controller_(requests|success|errors)" | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Show host-path-backend mappings clearly
- Include relevant annotations that affect routing behavior

## Safety Rules
- **Read-only by default**: Use get/describe for inspection
- **Annotation changes** affect NGINX config reload immediately
- **TLS secret updates** can cause brief SSL errors during reload
- **Never delete ingress resources** without confirming traffic impact

## Output Format

Present results as a structured report:
```
Managing Nginx Ingress Report
═════════════════════════════
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
- **IngressClass**: Must match controller's `--ingress-class` flag; mismatches cause ingress to be ignored
- **Path types**: Exact, Prefix, ImplementationSpecific behave differently for routing
- **Annotation sprawl**: NGINX Ingress has 100+ annotations; conflicting annotations cause unexpected behavior
- **Snippet annotations**: `server-snippet` and `configuration-snippet` can introduce security risks
- **Rate limiting**: Annotations `limit-rps` and `limit-connections` apply per client IP by default

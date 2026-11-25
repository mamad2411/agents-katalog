---
name: managing-open-service-mesh
description: |
  Use when working with Open Service Mesh — open Service Mesh (OSM) management
  covering mesh configuration, sidecar injection, traffic policies, SMI
  resources, ingress configuration, and observability. Use when managing OSM
  mesh instances, configuring SMI traffic policies, debugging Envoy sidecars, or
  setting up ingress and egress traffic policies in Kubernetes.
connection_type: open-service-mesh
preload: false
---

# Open Service Mesh Skill

Manage Open Service Mesh (OSM) configuration, SMI traffic policies, sidecar injection, and observability.

## Core Helper Functions

```bash
#!/bin/bash

# OSM CLI wrapper
osm_cmd() {
    osm "$@" 2>/dev/null
}

# Get OSM CRDs via kubectl
osm_get() {
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

echo "=== OSM Version ==="
osm version 2>/dev/null

echo ""
echo "=== OSM Mesh List ==="
osm mesh list 2>/dev/null

echo ""
echo "=== Control Plane Pods ==="
kubectl get pods -n osm-system -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.status.phase)\tRestarts: \(.status.containerStatuses[0].restartCount // 0)"
' | column -t

echo ""
echo "=== Monitored Namespaces ==="
osm namespace list 2>/dev/null || kubectl get namespaces -l openservicemesh.io/monitored-by -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\tSidecar: \(.metadata.annotations["openservicemesh.io/sidecar-injection"] // "n/a")"
'

echo ""
echo "=== SMI Resources ==="
for res in traffictargets trafficsplits tcproutes httproutegroups; do
    COUNT=$(kubectl get "$res" -A --no-headers 2>/dev/null | wc -l | tr -d ' ')
    echo "$res: $COUNT"
done

echo ""
echo "=== Mesh Config ==="
kubectl get meshconfig osm-mesh-config -n osm-system -o json 2>/dev/null | jq '.spec | {
    sidecar: {envoyImage: .sidecar.envoyImage, logLevel: .sidecar.logLevel},
    traffic: {enablePermissiveTrafficPolicyMode, enableEgress, outboundIPRangeExclusionList},
    certificate: {serviceCertValidityDuration},
    observability: {enableDebugServer, tracing: .observability.tracing}
}'
```

### Phase 2: Analysis

```bash
#!/bin/bash
NS="${1:-default}"

echo "=== Traffic Targets (SMI) ==="
osm_get traffictargets "$NS" | jq '
    .items[]? | {
        name: .metadata.name,
        destination: .spec.destination,
        sources: .spec.sources,
        rules: [.spec.rules[]? | {kind: .kind, name: .name, matches: .matches}]
    }' | head -25

echo ""
echo "=== Traffic Splits ==="
osm_get trafficsplits "$NS" | jq '
    .items[]? | {
        name: .metadata.name,
        service: .spec.service,
        backends: [.spec.backends[] | {service, weight}]
    }'

echo ""
echo "=== HTTP Route Groups ==="
osm_get httproutegroups "$NS" | jq '
    .items[]? | {
        name: .metadata.name,
        matches: [.spec.matches[]? | {name, pathRegex, methods, headers}]
    }' | head -20

echo ""
echo "=== Sidecar Proxy Status ==="
for pod in $(kubectl get pods -n "$NS" -o jsonpath='{.items[*].metadata.name}' 2>/dev/null | tr ' ' '\n' | head -10); do
    HAS_ENVOY=$(kubectl get pod "$pod" -n "$NS" -o json 2>/dev/null | jq -r '.spec.containers[].name' | grep -c envoy)
    [ "$HAS_ENVOY" -gt 0 ] && echo "$pod: injected"
done | head -10

echo ""
echo "=== Egress Policy ==="
osm_get egresses "$NS" | jq -r '
    .items[]? | "\(.metadata.name)\t\(.spec.hosts | join(","))\t\(.spec.ports[0].number)/\(.spec.ports[0].protocol)"
' | column -t | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use SMI resource names (TrafficTarget, TrafficSplit, HTTPRouteGroup)
- Show traffic policy relationships clearly

## Safety Rules
- **Read-only by default**: Use list/get and osm CLI for inspection
- **Permissive mode toggle** changes all traffic behavior mesh-wide
- **TrafficTarget changes** affect service authorization immediately
- **Never remove namespace** from mesh without confirming sidecar cleanup

## Output Format

Present results as a structured report:
```
Managing Open Service Mesh Report
═════════════════════════════════
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
- **Permissive vs SMI mode**: Permissive allows all traffic; SMI requires explicit TrafficTargets
- **OSM is archived**: OSM project has been archived; consider migration to alternatives
- **Sidecar injection**: Requires namespace annotation and pod restart
- **SMI compatibility**: Not all SMI spec versions are fully supported
- **Egress policy**: Default denies external traffic; must create Egress resources

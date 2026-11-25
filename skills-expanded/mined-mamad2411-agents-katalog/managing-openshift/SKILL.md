---
name: managing-openshift
description: |
  Use when working with Openshift — red Hat OpenShift container platform
  management. Covers project management, build configurations, routes,
  deployment configs, operators, image streams, and cluster administration. Use
  when managing OpenShift projects, debugging builds, configuring routes, or
  working with operators and image streams.
connection_type: openshift
preload: false
---

# OpenShift Management Skill

Manage Red Hat OpenShift projects, builds, routes, deployments, and operators.

## Core Helper Functions

```bash
#!/bin/bash

# OpenShift CLI wrapper (oc is a superset of kubectl)
oc_cmd() {
    oc "$@" 2>/dev/null
}

# OpenShift API helper
oc_api() {
    local endpoint="$1"
    oc get --raw "$endpoint" 2>/dev/null
}

# Get resources as JSON with jq
oc_json() {
    oc get "$@" -o json 2>/dev/null
}
```

## MANDATORY: Discovery-First Pattern

**Always discover cluster version, projects, and nodes before specific operations.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== OpenShift Cluster Info ==="
oc version -o json 2>/dev/null | jq '{
    client: .clientVersion,
    server: .openshiftVersion,
    kubernetes: .serverVersion.gitVersion
}'

echo ""
echo "=== Cluster Operators Status ==="
oc get clusteroperators -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.status.conditions[] | select(.type == "Available") | .status)\t\(.status.conditions[] | select(.type == "Degraded") | .status)"
' | column -t | head -25

echo ""
echo "=== Projects ==="
oc get projects -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.status.phase)\t\(.metadata.annotations["openshift.io/display-name"] // "")"
' | column -t | head -30

echo ""
echo "=== Nodes ==="
oc get nodes -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.metadata.labels["node-role.kubernetes.io/master"] // .metadata.labels["node-role.kubernetes.io/worker"] // "worker")\t\(.status.conditions[] | select(.type == "Ready") | .status)"
' | column -t | head -15
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `-o json` with jq for structured output
- Prefer `oc` over `kubectl` for OpenShift-specific resources

## Common Operations

### Build Configuration Dashboard

```bash
#!/bin/bash
NS="${1:-}"

echo "=== Build Configs ==="
oc get buildconfigs ${NS:+-n "$NS"} -A -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.strategy.type)\t\(.spec.source.type)\t\(.status.lastVersion)"
' | column -t | head -20

echo ""
echo "=== Recent Builds ==="
oc get builds ${NS:+-n "$NS"} -A -o json 2>/dev/null | jq -r '
    [.items[] | {name: .metadata.name, ns: .metadata.namespace, phase: .status.phase, duration: .status.duration, started: .status.startTimestamp}]
    | sort_by(.started) | reverse | .[:15][] |
    "\(.name)\t\(.ns)\t\(.phase)\t\(.duration // 0)s"
' | column -t

echo ""
echo "=== Failed Builds ==="
oc get builds -A -o json 2>/dev/null | jq -r '
    .items[] | select(.status.phase == "Failed") |
    "\(.metadata.name)\t\(.metadata.namespace)\t\(.status.message[0:60])"
' | column -t | head -10
```

### Route Management

```bash
#!/bin/bash
NS="${1:-}"

echo "=== Routes ==="
oc get routes ${NS:+-n "$NS"} -A -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.host)\t\(.spec.to.name)\t\(.spec.tls.termination // "none")"
' | column -t | head -20

echo ""
echo "=== Route TLS Status ==="
oc get routes ${NS:+-n "$NS"} -A -o json 2>/dev/null | jq -r '
    .items[] | select(.spec.tls != null) |
    "\(.metadata.name)\t\(.spec.host)\t\(.spec.tls.termination)\t\(.spec.tls.insecureEdgeTerminationPolicy // "None")"
' | column -t | head -15

echo ""
echo "=== Routes Without TLS ==="
oc get routes -A -o json 2>/dev/null | jq -r '
    .items[] | select(.spec.tls == null) | "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.host)"
' | column -t | head -10
```

### Deployment & DeploymentConfig Status

```bash
#!/bin/bash
NS="${1:-}"

echo "=== DeploymentConfigs ==="
oc get deploymentconfigs ${NS:+-n "$NS"} -A -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.replicas)\t\(.status.readyReplicas // 0) ready\t\(.status.latestVersion)"
' | column -t | head -20

echo ""
echo "=== Deployments (standard K8s) ==="
oc get deployments ${NS:+-n "$NS"} -A -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.replicas)\t\(.status.readyReplicas // 0) ready\t\(.spec.template.spec.containers[0].image | split("/")[-1])"
' | column -t | head -20

echo ""
echo "=== Rollout Status ==="
oc get deploymentconfigs ${NS:+-n "$NS"} -A -o json 2>/dev/null | jq -r '
    .items[] | select(.status.conditions[]?.type == "Progressing") |
    "\(.metadata.name)\t\(.metadata.namespace)\t\(.status.conditions[] | select(.type == "Progressing") | .message[0:60])"
' | column -t | head -10
```

### Operator Management

```bash
#!/bin/bash
echo "=== Installed Operators ==="
oc get csv -A -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.metadata.namespace)\t\(.status.phase)\t\(.spec.displayName)"
' | column -t | head -20

echo ""
echo "=== Operator Subscriptions ==="
oc get subscriptions -A -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.channel)\t\(.status.currentCSV // "pending")\t\(.spec.installPlanApproval)"
' | column -t | head -15

echo ""
echo "=== Pending Install Plans ==="
oc get installplans -A -o json 2>/dev/null | jq -r '
    .items[] | select(.spec.approved == false) |
    "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.clusterServiceVersionNames | join(","))"
' | column -t | head -10

echo ""
echo "=== Catalog Sources ==="
oc get catalogsources -A -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.sourceType)\t\(.status.connectionState.lastObservedState // "unknown")"
' | column -t
```

### Image Streams & Registry

```bash
#!/bin/bash
NS="${1:-openshift}"

echo "=== Image Streams ==="
oc get imagestreams -n "$NS" -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.status.tags | length) tags\t\(.status.dockerImageRepository // "N/A")"
' | column -t | head -20

echo ""
echo "=== Image Stream Tags ==="
IS="${2:-}"
if [ -n "$IS" ]; then
    oc get imagestreamtag -n "$NS" -o json 2>/dev/null | jq -r --arg is "$IS" '
        .items[] | select(.metadata.name | startswith($is)) |
        "\(.metadata.name)\t\(.image.dockerImageReference | split("@")[0])"
    ' | column -t | head -15
fi

echo ""
echo "=== Registry Status ==="
oc get configs.imageregistry.operator.openshift.io cluster -o json 2>/dev/null | jq '{
    management_state: .spec.managementState,
    storage: .spec.storage,
    replicas: .spec.replicas
}'
```

## Safety Rules
- **Read-only by default**: Use `oc get`, `oc describe`, `oc logs` for inspection
- **Never delete** projects or deployments without explicit user confirmation
- **Build triggers**: Modifying BuildConfigs may trigger automatic builds
- **Route exposure**: Creating routes exposes services externally -- confirm before creating

## Output Format

Present results as a structured report:
```
Managing Openshift Report
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
- **DeploymentConfig vs Deployment**: OpenShift has both DC (legacy) and Deployment (K8s native) -- check which is used
- **SCC (Security Context Constraints)**: Pods may fail due to SCC restrictions -- check with `oc get scc`
- **Route hostname conflicts**: Two routes cannot share the same hostname unless using path-based routing
- **Operator upgrades**: Automatic approval can upgrade operators unexpectedly -- review install plans
- **Image pull secrets**: Internal registry requires proper pull secrets in target namespaces

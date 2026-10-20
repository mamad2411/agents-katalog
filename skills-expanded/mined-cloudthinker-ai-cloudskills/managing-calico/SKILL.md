---
name: managing-calico
description: |
  Use when working with Calico — calico networking and security management for
  Kubernetes. Covers network policy enforcement, BGP configuration, IPAM
  management, Felix agent status, Typha health, WireGuard encryption, and global
  network sets. Use when managing Calico network policies, debugging routing
  issues, configuring BGP peering, or monitoring Felix/Typha health.
connection_type: calico
preload: false
---

# Calico Management Skill

Manage Calico networking, network policies, BGP configuration, IPAM, and Felix status.

## Core Helper Functions

```bash
#!/bin/bash

# Calicoctl wrapper
calico_cmd() {
    calicoctl "$@" 2>/dev/null
}

# Calicoctl with datastore config
calico_get() {
    local resource="$1"
    calicoctl get "$resource" -o json 2>/dev/null
}

# Calico via kubectl (operator-managed)
calico_kubectl() {
    kubectl get "$@" -o json 2>/dev/null
}
```

## MANDATORY: Discovery-First Pattern

**Always check Calico component health and node status before policy operations.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Calico Version ==="
calicoctl version 2>/dev/null || \
kubectl get deploy calico-kube-controllers -n calico-system -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null || \
kubectl get deploy calico-kube-controllers -n kube-system -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null

echo ""
echo "=== Calico Node Status ==="
calicoctl node status 2>/dev/null || \
kubectl get pods -n calico-system -l k8s-app=calico-node -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.spec.nodeName)\t\(.status.phase)\t\(.status.containerStatuses[0].restartCount) restarts"
' | column -t

echo ""
echo "=== Component Health ==="
# calico-node (Felix + BIRD)
echo "calico-node pods:"
kubectl get pods -n calico-system -l k8s-app=calico-node --no-headers 2>/dev/null | head -10 || \
kubectl get pods -n kube-system -l k8s-app=calico-node --no-headers 2>/dev/null | head -10

echo ""
# Typha (optional scaler)
echo "Typha pods:"
kubectl get pods -n calico-system -l k8s-app=calico-typha --no-headers 2>/dev/null | head -5

echo ""
echo "=== IPAM Summary ==="
calicoctl ipam show 2>/dev/null || echo "Use 'calicoctl ipam show' for IP allocation details"

echo ""
echo "=== Network Policies Count ==="
kubectl get networkpolicies -A --no-headers 2>/dev/null | wc -l | xargs echo "K8s NetworkPolicies:"
calicoctl get globalnetworkpolicies -o json 2>/dev/null | jq '.items | length' | xargs echo "Calico GlobalNetworkPolicies:"
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `calicoctl get -o json` with jq for Calico resources
- Use `kubectl -o json` for standard K8s network policies

## Common Operations

### Network Policy Dashboard

```bash
#!/bin/bash
NS="${1:-}"

echo "=== Calico Global Network Policies ==="
calicoctl get globalnetworkpolicies -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.spec.order // 999)\t\(.spec.selector // "all()")\tingress:\(.spec.ingress | length) egress:\(.spec.egress | length)"
' | column -t | head -15

echo ""
echo "=== Calico Network Policies (namespaced) ==="
calicoctl get networkpolicies ${NS:+--namespace "$NS"} -A -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.selector // "all()")\t\(.spec.order // 999)"
' | column -t | head -15

echo ""
echo "=== K8s Network Policies ==="
kubectl get networkpolicies ${NS:+-n "$NS"} -A -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.policyTypes | join(","))"
' | column -t | head -15

echo ""
echo "=== Global Network Sets ==="
calicoctl get globalnetworksets -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.spec.nets | length) CIDRs"
' | column -t | head -10
```

### BGP Configuration

```bash
#!/bin/bash
echo "=== BGP Configuration ==="
calicoctl get bgpConfiguration default -o json 2>/dev/null | jq '{
    log_severity: .spec.logSeverityScreen,
    node_to_node_mesh: .spec.nodeToNodeMeshEnabled,
    as_number: .spec.asNumber,
    service_cluster_ips: .spec.serviceClusterIPs,
    service_external_ips: .spec.serviceExternalIPs
}'

echo ""
echo "=== BGP Peers ==="
calicoctl get bgpPeers -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.spec.peerIP)\tAS\(.spec.asNumber)\t\(.spec.nodeSelector // "all()")"
' | column -t | head -15

echo ""
echo "=== Node BGP Status ==="
calicoctl node status 2>/dev/null | head -20

echo ""
echo "=== BIRD Routing Table ==="
# On a specific node
for pod in $(kubectl get pods -n calico-system -l k8s-app=calico-node -o jsonpath='{.items[*].metadata.name}' 2>/dev/null | tr ' ' '\n' | head -3); do
    echo "--- $pod ---"
    kubectl exec -n calico-system "$pod" -- birdcl show route 2>/dev/null | head -10
done
```

### IPAM Management

```bash
#!/bin/bash
echo "=== IPAM Summary ==="
calicoctl ipam show 2>/dev/null

echo ""
echo "=== IP Pools ==="
calicoctl get ippools -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.spec.cidr)\t\(.spec.ipipMode // "Never")\t\(.spec.vxlanMode // "Never")\t\(.spec.natOutgoing)\t\(.spec.disabled // false)"
' | column -t

echo ""
echo "=== IP Reservations ==="
calicoctl get ipreservations -o json 2>/dev/null | jq -r '
    .items[]? | "\(.metadata.name)\t\(.spec.reservedCIDRs | join(","))"
' | column -t | head -10

echo ""
echo "=== Block Affinities ==="
calicoctl ipam show --show-blocks 2>/dev/null | head -20

echo ""
echo "=== IPAM Check (leaked IPs) ==="
calicoctl ipam check 2>/dev/null | head -15
```

### Felix Status & Health

```bash
#!/bin/bash
echo "=== Felix Configuration ==="
calicoctl get felixConfiguration default -o json 2>/dev/null | jq '{
    log_severity: .spec.logSeverityScreen,
    reporting_interval: .spec.reportingInterval,
    iptables_refresh: .spec.iptablesRefreshInterval,
    route_refresh: .spec.routeRefreshInterval,
    wireguard_enabled: .spec.wireguardEnabled,
    bpf_enabled: .spec.bpfEnabled,
    floating_ips: .spec.floatingIPs
}'

echo ""
echo "=== Felix Metrics ==="
for pod in $(kubectl get pods -n calico-system -l k8s-app=calico-node -o jsonpath='{.items[*].metadata.name}' 2>/dev/null | tr ' ' '\n' | head -3); do
    echo "--- $pod ---"
    kubectl exec -n calico-system "$pod" -- wget -qO- http://localhost:9091/metrics 2>/dev/null \
        | grep -E "^felix_(active|iptables|route)" | head -10
done

echo ""
echo "=== Typha Status ==="
kubectl get pods -n calico-system -l k8s-app=calico-typha -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.status.phase)\t\(.status.containerStatuses[0].restartCount) restarts"
' | column -t

echo ""
echo "=== WireGuard Status ==="
calicoctl get felixConfiguration default -o json 2>/dev/null | jq '.spec.wireguardEnabled // false' | xargs echo "WireGuard enabled:"
kubectl get nodes -o json 2>/dev/null | jq -r '.items[] | "\(.metadata.name)\t\(.metadata.annotations["projectcalico.org/WireguardPublicKey"] // "not configured")"' | column -t | head -10
```

### Host Endpoint & Profile Management

```bash
#!/bin/bash
echo "=== Host Endpoints ==="
calicoctl get hostEndpoints -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.spec.node)\t\(.spec.interfaceName)\t\(.spec.expectedIPs | join(","))"
' | column -t | head -15

echo ""
echo "=== Profiles ==="
calicoctl get profiles -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.spec.ingress | length) ingress\t\(.spec.egress | length) egress"
' | column -t | head -15

echo ""
echo "=== Workload Endpoints ==="
calicoctl get workloadEndpoints -o json 2>/dev/null | jq -r '
    .items[:20][] | "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.node)\t\(.spec.ipNetworks | join(","))"
' | column -t | head -15
```

## Safety Rules
- **Read-only by default**: Use `calicoctl get`, `calicoctl ipam show`, `calicoctl node status`
- **Never modify** GlobalNetworkPolicies without confirmation -- can block all cluster traffic
- **BGP changes**: Modifying BGP config can disrupt routing across the entire cluster
- **IPAM operations**: IP pool changes affect pod IP allocation -- plan maintenance windows

## Output Format

Present results as a structured report:
```
Managing Calico Report
══════════════════════
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
- **Datastore type**: Calico uses either etcd or Kubernetes API -- check `DATASTORE_TYPE` environment variable
- **Policy ordering**: Calico policies have explicit `order` field -- lower values match first
- **IPIP vs VXLAN**: Overlay modes are per-pool -- mixing can cause connectivity issues
- **Felix restart loop**: Often caused by invalid Felix configuration -- check calico-node pod logs
- **Namespace isolation**: Calico namespace network policies only apply within the namespace -- use GlobalNetworkPolicy for cross-namespace rules

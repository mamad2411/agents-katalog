---
name: managing-cilium
description: |
  Use when working with Cilium — cilium eBPF-based networking and security
  management for Kubernetes. Covers network policy enforcement, eBPF map
  inspection, Hubble flow visibility, cluster mesh, endpoint health, service
  load balancing, and identity management. Use when managing Cilium network
  policies, debugging connectivity, monitoring traffic flows with Hubble, or
  configuring cluster mesh.
connection_type: cilium
preload: false
---

# Cilium Management Skill

Manage Cilium eBPF networking, network policies, Hubble observability, and cluster mesh.

## Core Helper Functions

```bash
#!/bin/bash

# Cilium CLI wrapper
cilium_cmd() {
    cilium "$@" 2>/dev/null
}

# Cilium agent command (exec into agent pod)
cilium_agent() {
    local node="${1:-}"
    shift
    if [ -n "$node" ]; then
        AGENT_POD=$(kubectl get pods -n kube-system -l k8s-app=cilium --field-selector spec.nodeName="$node" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
    else
        AGENT_POD=$(kubectl get pods -n kube-system -l k8s-app=cilium -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
    fi
    kubectl exec -n kube-system "$AGENT_POD" -- cilium "$@" 2>/dev/null
}

# Hubble CLI wrapper
hubble_cmd() {
    hubble "$@" 2>/dev/null
}
```

## MANDATORY: Discovery-First Pattern

**Always check Cilium agent status and connectivity before inspecting policies or flows.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Cilium Status ==="
cilium status 2>/dev/null || \
kubectl get pods -n kube-system -l k8s-app=cilium -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.spec.nodeName)\t\(.status.phase)\t\(.status.containerStatuses[0].restartCount) restarts"
' | column -t

echo ""
echo "=== Cilium Version ==="
cilium version 2>/dev/null || \
kubectl get ds cilium -n kube-system -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null

echo ""
echo "=== Cluster Connectivity ==="
cilium connectivity test --single-node 2>/dev/null | tail -10

echo ""
echo "=== Endpoint Summary ==="
cilium_agent "" endpoint list -o json 2>/dev/null | jq '{
    total: length,
    ready: [.[] | select(.status.state == "ready")] | length,
    not_ready: [.[] | select(.status.state != "ready")] | length
}'

echo ""
echo "=== Network Policies ==="
kubectl get ciliumnetworkpolicies -A --no-headers 2>/dev/null | wc -l | xargs echo "CiliumNetworkPolicies:"
kubectl get networkpolicies -A --no-headers 2>/dev/null | wc -l | xargs echo "K8s NetworkPolicies:"
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `cilium` CLI or kubectl with jq for structured output
- Use `hubble observe` with filters -- never unfiltered flow dumps

## Common Operations

### Network Policy Analysis

```bash
#!/bin/bash
NS="${1:-}"

echo "=== Cilium Network Policies ==="
kubectl get ciliumnetworkpolicies ${NS:+-n "$NS"} -A -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.endpointSelector // "all")\t\(.specs | length) rules"
' | column -t | head -20

echo ""
echo "=== K8s Network Policies ==="
kubectl get networkpolicies ${NS:+-n "$NS"} -A -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.policyTypes | join(","))"
' | column -t | head -15

echo ""
echo "=== Cilium Clusterwide Policies ==="
kubectl get ciliumclusterwidenetworkpolicies -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.spec.endpointSelector // "all")"
' | column -t | head -10

echo ""
echo "=== Policy Enforcement Mode ==="
cilium_agent "" config -o json 2>/dev/null | jq '{
    policy_enforcement: .PolicyEnforcement,
    policy_audit_mode: .PolicyAuditMode
}'
```

### Hubble Flow Visibility

```bash
#!/bin/bash
NS="${1:-default}"

echo "=== Recent Flows (last 100) ==="
hubble observe --namespace "$NS" --last 100 -o json 2>/dev/null | jq -r '
    .flow | select(.verdict != null) |
    "\(.time[11:19])\t\(.source.namespace)/\(.source.labels[1] // .source.identity)\t->\t\(.destination.namespace)/\(.destination.labels[1] // .destination.identity)\t\(.verdict)\t\(.l4.TCP.destination_port // .l4.UDP.destination_port // "N/A")"
' | column -t | head -20

echo ""
echo "=== Dropped Flows ==="
hubble observe --namespace "$NS" --verdict DROPPED --last 50 -o json 2>/dev/null | jq -r '
    .flow | "\(.time[11:19])\t\(.source.namespace)/\(.source.labels[1] // "unknown")\t->\t\(.destination.namespace)/\(.destination.labels[1] // "unknown")\t\(.drop_reason_desc)"
' | column -t | head -15

echo ""
echo "=== Flow Summary ==="
hubble observe --namespace "$NS" --last 500 -o json 2>/dev/null | jq -s '{
    total: length,
    forwarded: [.[] | select(.flow.verdict == "FORWARDED")] | length,
    dropped: [.[] | select(.flow.verdict == "DROPPED")] | length,
    audit: [.[] | select(.flow.verdict == "AUDIT")] | length
}'
```

### eBPF Map Inspection

```bash
#!/bin/bash
echo "=== BPF Map Summary ==="
cilium_agent "" bpf ct list global 2>/dev/null | head -5
echo "..."
cilium_agent "" bpf ct list global 2>/dev/null | wc -l | xargs echo "Total connection tracking entries:"

echo ""
echo "=== BPF Policy Maps ==="
cilium_agent "" bpf policy get --all 2>/dev/null | head -20

echo ""
echo "=== BPF Endpoint Maps ==="
cilium_agent "" bpf endpoint list 2>/dev/null | head -15

echo ""
echo "=== BPF Service Maps (load balancer) ==="
cilium_agent "" service list 2>/dev/null | head -20

echo ""
echo "=== BPF NAT Table Stats ==="
cilium_agent "" bpf nat list 2>/dev/null | wc -l | xargs echo "NAT entries:"
```

### Cluster Mesh Status

```bash
#!/bin/bash
echo "=== Cluster Mesh Status ==="
cilium clustermesh status 2>/dev/null || \
kubectl get ciliumclustermeshconfig -A -o json 2>/dev/null | jq '.' | head -20

echo ""
echo "=== Remote Clusters ==="
cilium_agent "" clustermesh status 2>/dev/null | head -15

echo ""
echo "=== Cross-Cluster Services ==="
kubectl get ciliumglobalservices -A -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.metadata.namespace)\t\(.spec.clusterID)"
' | column -t | head -15

echo ""
echo "=== Cluster Identity Allocation ==="
cilium_agent "" identity list 2>/dev/null | head -20
```

### Endpoint Health & Debugging

```bash
#!/bin/bash
echo "=== Endpoint Health ==="
cilium_agent "" endpoint list -o json 2>/dev/null | jq -r '
    .[] | "\(.id)\t\(.status.external-identifiers["pod-name"] // "N/A")\t\(.status.state)\t\(.status.policy.realized.allowed-ingress-identities | length) ingress\t\(.status.policy.realized.allowed-egress-identities | length) egress"
' | column -t | head -20

echo ""
echo "=== Unhealthy Endpoints ==="
cilium_agent "" endpoint list -o json 2>/dev/null | jq -r '
    .[] | select(.status.state != "ready") |
    "\(.id)\t\(.status.external-identifiers["pod-name"])\t\(.status.state)\t\(.status.log[-1].msg // "no log")"
' | column -t | head -10

echo ""
echo "=== Endpoint Detail ==="
EP_ID="${1:-}"
if [ -n "$EP_ID" ]; then
    cilium_agent "" endpoint get "$EP_ID" -o json 2>/dev/null | jq '{
        id: .id,
        identity: .status.identity.id,
        labels: .status.identity.labels,
        state: .status.state,
        policy_enabled: .status.policy.spec.policy-enabled,
        ingress_enforcing: .status.policy["proxy-statistics"]
    }'
fi
```

## Safety Rules
- **Read-only by default**: Use `cilium status`, `hubble observe`, `bpf` inspection commands
- **Never modify** CiliumNetworkPolicies without explicit confirmation -- can block all traffic
- **Policy audit mode**: Test policies in audit mode before enforcing
- **Hubble rate limit**: Use `--last N` to limit flow queries -- unbounded queries can overwhelm

## Output Format

Present results as a structured report:
```
Managing Cilium Report
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
- **Policy enforcement**: Default mode may be "default" (no enforcement) -- check `PolicyEnforcement` config
- **Identity allocation**: Cilium uses numeric identities -- identity exhaustion can cause policy failures
- **Hubble not installed**: Hubble is optional -- check if relay is deployed before using `hubble observe`
- **BPF map limits**: Connection tracking maps have size limits -- high-traffic clusters may hit limits
- **Host firewall**: Cilium host firewall policies affect node-level traffic -- test carefully

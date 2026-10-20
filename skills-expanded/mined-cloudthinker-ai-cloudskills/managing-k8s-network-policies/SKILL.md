---
name: managing-k8s-network-policies
description: |
  Use when working with K8S Network Policies — kubernetes NetworkPolicy
  management and network segmentation analysis. Covers NetworkPolicy inventory,
  ingress and egress rules, pod selector coverage, namespace isolation, default
  deny policies, and policy gap detection. Use when auditing network security,
  debugging connectivity issues, reviewing network segmentation, or identifying
  unprotected workloads.
connection_type: k8s
preload: false
---

# Kubernetes NetworkPolicy Skill

Manage and analyze NetworkPolicies for network segmentation and security.

## MANDATORY: Discovery-First Pattern

**Always list NetworkPolicies and check CNI support before analyzing coverage.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== NetworkPolicies (all namespaces) ==="
kubectl get networkpolicies --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,POD-SELECTOR:.spec.podSelector.matchLabels,POLICY-TYPES:.spec.policyTypes[*]' 2>/dev/null | head -20

echo ""
echo "=== Policy Count Per Namespace ==="
kubectl get networkpolicies --all-namespaces -o json 2>/dev/null | jq -r '
  [.items[] | .metadata.namespace] |
  group_by(.) | map({ns: .[0], count: length}) |
  sort_by(-.count)[] |
  "\(.ns)\t\(.count) policies"
' | head -15

echo ""
echo "=== CNI Plugin ==="
kubectl get pods -n kube-system -o custom-columns='NAME:.metadata.name' 2>/dev/null | grep -iE "calico|cilium|weave|flannel|antrea" | head -5
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Default Deny Policies ==="
kubectl get networkpolicies --all-namespaces -o json 2>/dev/null | jq -r '
  .items[] |
  select(.spec.podSelector == {} or .spec.podSelector.matchLabels == null) |
  select((.spec.ingress == null or .spec.ingress == []) and (.spec.policyTypes // [] | contains(["Ingress"]))) |
  "\(.metadata.namespace)/\(.metadata.name)\tDefault-Deny-Ingress"
'
kubectl get networkpolicies --all-namespaces -o json 2>/dev/null | jq -r '
  .items[] |
  select(.spec.podSelector == {} or .spec.podSelector.matchLabels == null) |
  select((.spec.egress == null or .spec.egress == []) and (.spec.policyTypes // [] | contains(["Egress"]))) |
  "\(.metadata.namespace)/\(.metadata.name)\tDefault-Deny-Egress"
'

echo ""
echo "=== Namespaces Without Any NetworkPolicy ==="
POLICY_NS=$(kubectl get networkpolicies --all-namespaces -o jsonpath='{.items[*].metadata.namespace}' 2>/dev/null | tr ' ' '\n' | sort -u)
ALL_NS=$(kubectl get namespaces -o jsonpath='{.items[*].metadata.name}' 2>/dev/null | tr ' ' '\n' | sort)
comm -23 <(echo "$ALL_NS") <(echo "$POLICY_NS") | grep -v "^kube-" | head -15

echo ""
echo "=== Ingress Rules Summary ==="
kubectl get networkpolicies --all-namespaces -o json 2>/dev/null | jq -r '
  .items[] |
  select(.spec.ingress != null) |
  "\(.metadata.namespace)/\(.metadata.name)\tIngress-Rules:\(.spec.ingress | length)\tFrom:" +
  ([.spec.ingress[].from[]? |
    if .namespaceSelector then "ns-selector"
    elif .podSelector then "pod-selector"
    elif .ipBlock then "ip:\(.ipBlock.cidr)"
    else "unknown" end
  ] | unique | join(","))
' | head -15

echo ""
echo "=== Egress Rules Summary ==="
kubectl get networkpolicies --all-namespaces -o json 2>/dev/null | jq -r '
  .items[] |
  select(.spec.egress != null) |
  "\(.metadata.namespace)/\(.metadata.name)\tEgress-Rules:\(.spec.egress | length)\tTo:" +
  ([.spec.egress[].to[]? |
    if .namespaceSelector then "ns-selector"
    elif .podSelector then "pod-selector"
    elif .ipBlock then "ip:\(.ipBlock.cidr)"
    else "unknown" end
  ] | unique | join(","))
' | head -15

echo ""
echo "=== Wide-Open Policies (allow all) ==="
kubectl get networkpolicies --all-namespaces -o json 2>/dev/null | jq -r '
  .items[] |
  select(
    (.spec.ingress[]? | select(.from == null or .from == [])) or
    (.spec.egress[]? | select(.to == null or .to == []))
  ) |
  "\(.metadata.namespace)/\(.metadata.name)\tWARN: allows all traffic"
' | head -10
```

## Output Format

- Target ≤50 lines per output
- Use jq for NetworkPolicy rule analysis
- Summarize ingress/egress rules by type (podSelector, namespaceSelector, ipBlock)
- Flag namespaces without default deny policies
- Never dump full policy YAML -- show rule summaries

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

- **CNI requirement**: NetworkPolicies require a CNI that enforces them (Calico, Cilium, Antrea) -- Flannel does NOT enforce
- **Default behavior**: Without any NetworkPolicy, all traffic is allowed -- NetworkPolicies are additive (union)
- **Empty podSelector**: `podSelector: {}` selects ALL pods in the namespace -- used for default deny
- **Ingress vs Egress**: policyTypes must include "Egress" for egress rules to take effect -- omitting policyTypes defaults to Ingress only (unless egress rules exist)
- **DNS egress**: Default deny egress blocks DNS -- always allow egress to kube-dns on port 53
- **Namespace labels**: namespaceSelector matches on namespace labels -- ensure namespaces are labeled
- **AND vs OR**: Within a single `from`/`to` entry, selectors are AND; between entries, they are OR
- **CIDR exceptions**: `ipBlock.except` excludes specific IPs from a CIDR range -- commonly used for cluster IPs

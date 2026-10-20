---
name: managing-kyverno
description: |
  Use when working with Kyverno — kyverno Kubernetes policy management. Covers
  policy creation, validation rules, mutation rules, generation rules, policy
  reports, exception management, and compliance auditing. Use when managing
  Kubernetes admission policies, debugging policy violations, reviewing policy
  reports, or configuring resource generation.
connection_type: kyverno
preload: false
---

# Kyverno Policy Management Skill

Manage and inspect Kyverno Kubernetes policies, reports, and compliance.

## MANDATORY: Discovery-First Pattern

**Always check Kyverno status and existing policies before creating or modifying policies.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Kyverno Version ==="
kubectl get deployment kyverno -n kyverno -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null
echo ""

echo ""
echo "=== Kyverno Pods ==="
kubectl get pods -n kyverno 2>/dev/null

echo ""
echo "=== Cluster Policies ==="
kubectl get clusterpolicies 2>/dev/null | head -15

echo ""
echo "=== Namespaced Policies ==="
kubectl get policies --all-namespaces 2>/dev/null | head -15

echo ""
echo "=== Policy Reports Summary ==="
kubectl get policyreports --all-namespaces --no-headers 2>/dev/null | wc -l | xargs -I{} echo "{} policy reports"
kubectl get clusterpolicyreports --no-headers 2>/dev/null | wc -l | xargs -I{} echo "{} cluster policy reports"
```

## Core Helper Functions

```bash
#!/bin/bash

# Kyverno CLI wrapper
kyverno_cmd() {
    kyverno "$@" 2>/dev/null
}

# Get policy status
kyverno_status() {
    local policy="$1"
    kubectl get clusterpolicy "$policy" -o jsonpath='{.status.conditions[*].message}' 2>/dev/null || \
    kubectl get policy "$policy" --all-namespaces -o jsonpath='{.items[0].status.conditions[*].message}' 2>/dev/null
}

# Policy report summary
kyverno_report() {
    kubectl get policyreport -A -o json 2>/dev/null | jq '
        .items[] | {
            namespace: .metadata.namespace,
            pass: (.summary.pass // 0),
            fail: (.summary.fail // 0),
            warn: (.summary.warn // 0)
        }
    '
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `-o json` with jq for structured policy inspection
- Summarize policy reports by pass/fail counts
- Never dump full policy YAML -- extract rules and match conditions

## Common Operations

### Policy Inspection

```bash
#!/bin/bash
POLICY="${1:-}"

if [ -n "$POLICY" ]; then
    echo "=== Policy Details: $POLICY ==="
    kubectl get clusterpolicy "$POLICY" -o json 2>/dev/null | jq '{
        name: .metadata.name,
        background: .spec.background,
        validationFailureAction: .spec.validationFailureAction,
        rules: [.spec.rules[] | {
            name: .name,
            type: (if .validate then "validate" elif .mutate then "mutate" elif .generate then "generate" else "other" end),
            match: .match,
            message: .validate.message
        }]
    }'
else
    echo "=== All Cluster Policies ==="
    kubectl get clusterpolicies -o json 2>/dev/null | jq -r '
        .items[] | "\(.metadata.name)\t\(.spec.validationFailureAction)\t\(.spec.background)\t\(.spec.rules | length) rules"
    ' | column -t
fi
```

### Policy Reports Analysis

```bash
#!/bin/bash
NAMESPACE="${1:-}"

echo "=== Policy Report Summary ==="
if [ -n "$NAMESPACE" ]; then
    kubectl get policyreport -n "$NAMESPACE" -o json 2>/dev/null | jq '.items[] | {
        name: .metadata.name,
        pass: .summary.pass,
        fail: .summary.fail,
        warn: .summary.warn,
        error: .summary.error
    }'
else
    kubectl get policyreport -A -o json 2>/dev/null | jq '
        [.items[] | {namespace: .metadata.namespace, pass: (.summary.pass // 0), fail: (.summary.fail // 0)}] |
        sort_by(-.fail) | .[0:15]
    '
fi

echo ""
echo "=== Failed Resources ==="
kubectl get policyreport -A -o json 2>/dev/null | jq -r '
    .items[].results[]? |
    select(.result == "fail") |
    "\(.policy)\t\(.resources[0].kind)/\(.resources[0].name)\t\(.message[:60])"
' | column -t | head -20
```

### Validation Rule Testing

```bash
#!/bin/bash
POLICY_FILE="${1:?Policy file required}"
RESOURCE_FILE="${2:?Resource file required}"

echo "=== Policy Test ==="
kyverno apply "$POLICY_FILE" --resource "$RESOURCE_FILE" 2>&1

echo ""
echo "=== Dry Run Against Cluster ==="
kyverno apply "$POLICY_FILE" --cluster 2>/dev/null | head -30
```

### Mutation Rule Inspection

```bash
#!/bin/bash
echo "=== Mutation Policies ==="
kubectl get clusterpolicies -o json 2>/dev/null | jq -r '
    .items[] | .spec.rules[] |
    select(.mutate != null) |
    "\(.name)\t\(.match.any[0].resources.kinds // .match.resources.kinds | join(","))\tmutation"
' | column -t | head -15

echo ""
echo "=== Recent Mutations ==="
kubectl get events --field-selector reason=PolicyApplied -A 2>/dev/null | head -15
```

### Exception Management

```bash
#!/bin/bash
echo "=== Policy Exceptions ==="
kubectl get policyexceptions --all-namespaces 2>/dev/null | head -15

echo ""
echo "=== Resources with Policy Annotations ==="
kubectl get pods --all-namespaces -o json 2>/dev/null | jq -r '
    .items[] |
    select(.metadata.annotations | to_entries[] | .key | test("policies.kyverno.io")) |
    "\(.metadata.namespace)/\(.metadata.name)\t\(.metadata.annotations | to_entries[] | select(.key | test("policies.kyverno.io")) | "\(.key)=\(.value)")"
' | head -15
```

## Safety Rules

- **`validationFailureAction: Enforce` blocks non-compliant resources** -- always test with `Audit` first
- **Mutation policies modify resources silently** -- review mutations carefully before enabling
- **Generation rules create resources** -- ensure generated resources are correct before enabling
- **Background scanning** applies policies to existing resources -- can trigger alerts on retroactive changes
- **Policy exceptions** bypass enforcement -- audit exceptions regularly

## Output Format

Present results as a structured report:
```
Managing Kyverno Report
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

- **Enforce vs Audit**: Setting `Enforce` on a broken policy blocks all matching resources -- always start with `Audit`
- **Match scope too broad**: Overly broad `match` can affect system namespaces -- exclude kube-system
- **Webhook failures**: If Kyverno pods are down, `failurePolicy: Fail` blocks all admissions
- **Policy ordering**: Multiple policies on same resource type can conflict -- check combined effect
- **Background scan load**: Background scanning large clusters can impact Kyverno performance
- **CRD dependencies**: Policies referencing CRDs fail if CRDs are not installed
- **Report storage**: Policy reports accumulate -- configure retention to prevent etcd growth
- **Cluster policy vs policy**: ClusterPolicy is cluster-scoped; Policy is namespace-scoped -- choose appropriately

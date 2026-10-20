---
name: analyzing-kubescape
description: |
  Use when working with Kubescape — kubescape Kubernetes security posture
  analysis. Covers NSA/CISA framework assessment, MITRE ATT&CK mapping, CIS
  Kubernetes benchmarks, workload scanning, RBAC analysis, and network policy
  evaluation. Use when assessing Kubernetes cluster security, evaluating
  compliance frameworks, or analyzing workload configurations.
connection_type: kubescape
preload: false
---

# Kubescape Kubernetes Security Analysis Skill

Analyze Kubernetes cluster security posture using Kubescape frameworks and controls.

## MANDATORY: Discovery-First Pattern

**Always check cluster connectivity and available frameworks before scanning.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Kubescape Version ==="
kubescape version 2>/dev/null

echo ""
echo "=== Available Frameworks ==="
kubescape list frameworks 2>/dev/null | head -15

echo ""
echo "=== Cluster Context ==="
kubectl config current-context 2>/dev/null

echo ""
echo "=== Cluster Summary ==="
echo "Namespaces: $(kubectl get ns --no-headers 2>/dev/null | wc -l)"
echo "Pods: $(kubectl get pods --all-namespaces --no-headers 2>/dev/null | wc -l)"
echo "Deployments: $(kubectl get deployments --all-namespaces --no-headers 2>/dev/null | wc -l)"
```

## Core Helper Functions

```bash
#!/bin/bash

# Kubescape wrapper with JSON output
ks_cmd() {
    kubescape "$@" --format json --output /dev/stdout 2>/dev/null
}

# Scan with specific framework
ks_framework() {
    local framework="$1"
    shift
    kubescape scan framework "$framework" "$@" --format json --output /dev/stdout 2>/dev/null
}

# Summary extractor
ks_summary() {
    jq '{
        risk_score: .summaryDetails.complianceScore,
        total_controls: .summaryDetails.numberOf.allControls,
        passed: .summaryDetails.numberOf.passedControls,
        failed: .summaryDetails.numberOf.failedControls,
        skipped: .summaryDetails.numberOf.skippedControls
    }'
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `--format json` with jq for structured results
- Use `--include-namespaces` to scope scans
- Focus on failed controls and remediation guidance

## Common Operations

### NSA/CISA Framework Assessment

```bash
#!/bin/bash
echo "=== NSA/CISA Framework Scan ==="
kubescape scan framework nsa --format json --output /dev/stdout 2>/dev/null | jq '{
    compliance_score: .summaryDetails.complianceScore,
    controls: {
        total: .summaryDetails.numberOf.allControls,
        passed: .summaryDetails.numberOf.passedControls,
        failed: .summaryDetails.numberOf.failedControls
    },
    top_failures: [.results[] | select(.status == "failed") | {
        id: .controlID,
        name: .name,
        severity: .scoreFactor,
        failed_resources: (.resourceIDs | length)
    }] | sort_by(-.severity) | .[0:10]
}'
```

### MITRE ATT&CK Mapping

```bash
#!/bin/bash
echo "=== MITRE ATT&CK Scan ==="
kubescape scan framework MITRE --format json --output /dev/stdout 2>/dev/null | jq '{
    compliance_score: .summaryDetails.complianceScore,
    attack_techniques: [.results[] | select(.status == "failed") | {
        control: .controlID,
        technique: .name,
        severity: .scoreFactor,
        affected_resources: (.resourceIDs | length)
    }] | sort_by(-.severity) | .[0:10]
}'
```

### Workload Scanning

```bash
#!/bin/bash
NAMESPACE="${1:-default}"

echo "=== Workload Scan: $NAMESPACE ==="
kubescape scan --include-namespaces "$NAMESPACE" --format json --output /dev/stdout 2>/dev/null | jq '{
    namespace: "'"$NAMESPACE"'",
    score: .summaryDetails.complianceScore,
    failed_controls: [.results[] | select(.status == "failed") | {
        control: .controlID,
        name: .name,
        resources: [.resourceIDs[]? | split("/") | last][:5]
    }] | .[0:10]
}'

echo ""
echo "=== Resource Risk Summary ==="
kubescape scan --include-namespaces "$NAMESPACE" --format json --output /dev/stdout 2>/dev/null | jq '
    [.resources[]? | {
        kind: .kind,
        name: .name,
        failed_controls: ([.controls[]? | select(.status == "failed")] | length)
    }] | sort_by(-.failed_controls) | .[0:10]
'
```

### RBAC Analysis

```bash
#!/bin/bash
echo "=== RBAC Security Scan ==="
kubescape scan control C-0035,C-0036,C-0037,C-0038,C-0039 --format json --output /dev/stdout 2>/dev/null | jq '{
    rbac_controls: [.results[] | {
        id: .controlID,
        name: .name,
        status: .status,
        affected: (.resourceIDs | length)
    }]
}'

echo ""
echo "=== Cluster Admin Bindings ==="
kubectl get clusterrolebindings -o json 2>/dev/null | jq -r '
    .items[] |
    select(.roleRef.name == "cluster-admin") |
    .subjects[]? | "\(.kind)\t\(.name)\t\(.namespace // "cluster-scoped")"
' | column -t
```

### Compliance Comparison

```bash
#!/bin/bash
echo "=== Multi-Framework Compliance ==="
for fw in NSA MITRE CIS; do
    SCORE=$(kubescape scan framework "$fw" --format json --output /dev/stdout 2>/dev/null | jq '.summaryDetails.complianceScore')
    echo "$fw: ${SCORE}% compliance"
done

echo ""
echo "=== CIS Kubernetes Benchmark ==="
kubescape scan framework CIS --format json --output /dev/stdout 2>/dev/null | jq '{
    score: .summaryDetails.complianceScore,
    sections: [.results[] | select(.status == "failed") | .controlID[:4]] |
        group_by(.) | map({section: .[0], failures: length}) | sort_by(-.failures)
}'
```

## Safety Rules

- **Scans are read-only** -- Kubescape uses list/get API calls only
- **RBAC permissions required** -- ensure service account has cluster-reader access
- **Namespace scoping** -- use `--include-namespaces` to limit blast radius of recommendations
- **Custom frameworks** should be reviewed before deployment
- **Risk scores are relative** -- use them for prioritization, not absolute compliance status

## Output Format

Present results as a structured report:
```
Analyzing Kubescape Report
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

- **Kubeconfig context**: Scans use current kubeconfig context -- verify you are scanning the intended cluster
- **Namespace exclusions**: System namespaces (kube-system) often have legitimate elevated privileges -- review context
- **Score interpretation**: 100% compliance score does not mean fully secure -- frameworks cover specific aspects
- **Resource-heavy scans**: Large clusters with many resources can produce huge JSON output -- use namespace filtering
- **Control exceptions**: Some controls may not apply to your environment -- use exception policies
- **Offline scanning**: Kubescape can scan YAML manifests without cluster access -- use for shift-left
- **Version differences**: Control IDs and names change between Kubescape versions -- pin version in CI
- **Host scanning**: Node-level controls (CIS benchmarks) require host access -- not available in managed K8s

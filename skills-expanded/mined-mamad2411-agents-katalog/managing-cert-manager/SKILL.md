---
name: managing-cert-manager
description: |
  Use when working with Cert Manager — cert-manager certificate lifecycle
  management. Covers certificate issuance, issuer configuration, ACME
  challenges, certificate renewal, troubleshooting failed issuance, and trust
  management. Use when managing TLS certificates in Kubernetes, debugging
  issuance failures, configuring ACME providers, or monitoring certificate
  expiration.
connection_type: cert-manager
preload: false
---

# cert-manager Certificate Management Skill

Manage and inspect cert-manager certificates, issuers, and ACME challenges in Kubernetes.

## MANDATORY: Discovery-First Pattern

**Always check cert-manager status and issuers before managing certificates.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== cert-manager Version ==="
kubectl get deployment cert-manager -n cert-manager \
    -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null
echo ""

echo ""
echo "=== cert-manager Pods ==="
kubectl get pods -n cert-manager 2>/dev/null

echo ""
echo "=== Cluster Issuers ==="
kubectl get clusterissuers 2>/dev/null

echo ""
echo "=== Namespaced Issuers ==="
kubectl get issuers --all-namespaces 2>/dev/null | head -10

echo ""
echo "=== Certificate Summary ==="
kubectl get certificates --all-namespaces 2>/dev/null | head -15
```

## Core Helper Functions

```bash
#!/bin/bash

# cert-manager status check
cm_status() {
    local kind="$1"
    local name="$2"
    local ns="${3:-}"
    if [ -n "$ns" ]; then
        kubectl get "$kind" "$name" -n "$ns" -o jsonpath='{range .status.conditions[*]}{.type}={.status} ({.reason}: {.message}){"\n"}{end}' 2>/dev/null
    else
        kubectl get "$kind" "$name" -o jsonpath='{range .status.conditions[*]}{.type}={.status} ({.reason}: {.message}){"\n"}{end}' 2>/dev/null
    fi
}

# cmctl helper (if installed)
cm_cmd() {
    cmctl "$@" 2>/dev/null || kubectl cert-manager "$@" 2>/dev/null
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `-o json` with jq for certificate details
- Focus on status conditions for troubleshooting
- Never dump full certificate secrets -- show metadata only

## Common Operations

### Certificate Status Dashboard

```bash
#!/bin/bash
echo "=== Certificate Health ==="
kubectl get certificates --all-namespaces -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.namespace)/\(.metadata.name)\t\(.status.conditions[]? | select(.type == "Ready") | .status)\t\(.spec.dnsNames // .spec.commonName)\t\(.status.notAfter // "unknown")"
' | column -t | head -20

echo ""
echo "=== Expiring Soon (< 30 days) ==="
kubectl get certificates --all-namespaces -o json 2>/dev/null | jq -r --arg cutoff "$(date -u -d '+30 days' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v+30d +%Y-%m-%dT%H:%M:%SZ)" '
    .items[] |
    select(.status.notAfter < $cutoff) |
    "\(.metadata.namespace)/\(.metadata.name)\t\(.status.notAfter)\t\(.spec.issuerRef.name)"
' | column -t

echo ""
echo "=== Not Ready Certificates ==="
kubectl get certificates --all-namespaces -o json 2>/dev/null | jq -r '
    .items[] |
    select(.status.conditions[]? | select(.type == "Ready" and .status != "True")) |
    "\(.metadata.namespace)/\(.metadata.name)\t\(.status.conditions[] | select(.type == "Ready") | .reason): \(.message)"
' | column -t | head -10
```

### Issuer Configuration

```bash
#!/bin/bash
echo "=== Cluster Issuers ==="
kubectl get clusterissuers -o json 2>/dev/null | jq '.items[] | {
    name: .metadata.name,
    type: (if .spec.acme then "ACME" elif .spec.ca then "CA" elif .spec.selfSigned then "SelfSigned" elif .spec.vault then "Vault" else "Other" end),
    ready: (.status.conditions[]? | select(.type == "Ready") | .status),
    server: .spec.acme.server,
    email: .spec.acme.email
}'

echo ""
echo "=== Issuer Health ==="
kubectl get clusterissuers -o json 2>/dev/null | jq -r '
    .items[] | "\(.metadata.name)\t\(.status.conditions[]? | select(.type == "Ready") | "\(.status) - \(.reason)")"
' | column -t
```

### ACME Challenge Debugging

```bash
#!/bin/bash
echo "=== Active Challenges ==="
kubectl get challenges --all-namespaces 2>/dev/null

echo ""
echo "=== Challenge Details ==="
kubectl get challenges --all-namespaces -o json 2>/dev/null | jq '.items[] | {
    name: .metadata.name,
    namespace: .metadata.namespace,
    type: .spec.type,
    domain: .spec.dnsName,
    state: .status.state,
    reason: .status.reason,
    presented: .status.presented
}'

echo ""
echo "=== Certificate Requests ==="
kubectl get certificaterequests --all-namespaces -o json 2>/dev/null | jq -r '
    .items[] |
    select(.status.conditions[]? | select(.type == "Ready" and .status != "True")) |
    "\(.metadata.namespace)/\(.metadata.name)\t\(.status.conditions[] | select(.type == "Ready") | .reason): \(.message[:60])"
' | column -t | head -10

echo ""
echo "=== Orders ==="
kubectl get orders --all-namespaces 2>/dev/null | head -10
```

### Certificate Renewal

```bash
#!/bin/bash
CERT_NAME="${1:?Certificate name required}"
NAMESPACE="${2:-default}"

echo "=== Certificate Details ==="
kubectl get certificate "$CERT_NAME" -n "$NAMESPACE" -o json 2>/dev/null | jq '{
    name: .metadata.name,
    namespace: .metadata.namespace,
    dnsNames: .spec.dnsNames,
    issuer: .spec.issuerRef,
    duration: .spec.duration,
    renewBefore: .spec.renewBefore,
    notBefore: .status.notBefore,
    notAfter: .status.notAfter,
    renewalTime: .status.renewalTime,
    secretName: .spec.secretName,
    ready: (.status.conditions[] | select(.type == "Ready") | {status, reason, message})
}'

echo ""
echo "=== Manual Renewal ==="
echo "cmctl renew $CERT_NAME -n $NAMESPACE"
```

### Certificate Events and Troubleshooting

```bash
#!/bin/bash
CERT_NAME="${1:?Certificate name required}"
NAMESPACE="${2:-default}"

echo "=== Certificate Events ==="
kubectl describe certificate "$CERT_NAME" -n "$NAMESPACE" 2>/dev/null | grep -A 20 "^Events:" | head -20

echo ""
echo "=== cert-manager Controller Logs ==="
kubectl logs -n cert-manager deployment/cert-manager --tail=20 2>/dev/null | \
    grep -i "$CERT_NAME" | head -10

echo ""
echo "=== Related Resources ==="
echo "CertificateRequests:"
kubectl get certificaterequests -n "$NAMESPACE" -o json 2>/dev/null | jq -r "
    .items[] | select(.metadata.ownerReferences[]?.name == \"$CERT_NAME\") |
    \"\(.metadata.name)\t\(.status.conditions[]? | select(.type == \"Ready\") | .status)\"
" | column -t
```

## Safety Rules

- **Never delete certificate secrets manually** -- cert-manager recreates them, but downtime may occur
- **Test issuer configuration** with a non-production certificate before using in production
- **ACME rate limits** -- Let's Encrypt has rate limits -- use staging server for testing
- **Wildcard certificates** require DNS-01 challenges -- HTTP-01 does not support wildcards
- **Certificate duration and renewBefore** must be configured correctly to prevent expiration gaps

## Output Format

Present results as a structured report:
```
Managing Cert Manager Report
════════════════════════════
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

- **DNS propagation**: DNS-01 challenges fail if DNS records have not propagated -- check TTL and propagation
- **HTTP-01 ingress**: HTTP-01 solver needs ingress controller to route challenge requests -- check ingress class
- **ACME account key**: Lost account key requires re-registration -- backup the ACME account secret
- **Clock skew**: Certificate validity relies on accurate time -- NTP must be configured on nodes
- **Secret namespace**: Certificate secret must be in the same namespace as the workload using it
- **Issuer readiness**: Certificates cannot be issued if the referenced issuer is not ready
- **Webhook failures**: cert-manager webhook being unavailable blocks certificate operations
- **Annotation conflicts**: Both cert-manager annotations and Certificate resources on same ingress cause conflicts

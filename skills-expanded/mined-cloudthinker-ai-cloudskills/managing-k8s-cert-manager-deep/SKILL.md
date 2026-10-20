---
name: managing-k8s-cert-manager-deep
description: |
  Use when working with K8S Cert Manager Deep — cert-manager deep-dive
  management for Kubernetes TLS certificate lifecycle. Covers certificate
  inventory, issuer health, certificate requests, challenges, orders, ACME
  configuration, and renewal status. Use when debugging certificate issuance
  failures, auditing TLS configurations, reviewing issuer setups, or monitoring
  certificate expiration.
connection_type: k8s
preload: false
---

# Cert-Manager Deep-Dive Skill

Deep analysis of cert-manager certificates, issuers, and TLS lifecycle management.

## MANDATORY: Discovery-First Pattern

**Always check cert-manager installation and issuers before inspecting certificates.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Cert-Manager Version ==="
kubectl get deployment cert-manager -n cert-manager -o jsonpath='{.spec.template.spec.containers[0].image}' 2>/dev/null
echo ""

echo ""
echo "=== Cert-Manager Pods ==="
kubectl get pods -n cert-manager -o custom-columns='NAME:.metadata.name,STATUS:.status.phase,RESTARTS:.status.containerStatuses[0].restartCount,AGE:.metadata.creationTimestamp' 2>/dev/null

echo ""
echo "=== ClusterIssuers ==="
kubectl get clusterissuers -o custom-columns='NAME:.metadata.name,READY:.status.conditions[?(@.type=="Ready")].status,AGE:.metadata.creationTimestamp' 2>/dev/null

echo ""
echo "=== Issuers (all namespaces) ==="
kubectl get issuers --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,READY:.status.conditions[?(@.type=="Ready")].status' 2>/dev/null | head -20

echo ""
echo "=== Certificates (all namespaces) ==="
kubectl get certificates --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,READY:.status.conditions[?(@.type=="Ready")].status,EXPIRY:.status.notAfter,RENEWAL:.status.renewalTime' 2>/dev/null | head -20
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Not Ready Certificates ==="
kubectl get certificates --all-namespaces -o json 2>/dev/null | jq -r '
  .items[] |
  select(.status.conditions[]? | select(.type == "Ready" and .status != "True")) |
  "\(.metadata.namespace)/\(.metadata.name)\t\(.status.conditions[] | select(.type == "Ready") | .reason): \(.message // "no message")"
' | column -t | head -15

echo ""
echo "=== Expiring Soon (within 30 days) ==="
THRESHOLD=$(date -u -d '+30 days' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v+30d +%Y-%m-%dT%H:%M:%SZ)
kubectl get certificates --all-namespaces -o json 2>/dev/null | jq -r --arg threshold "$THRESHOLD" '
  .items[] |
  select(.status.notAfter // "" < $threshold and .status.notAfter // "" != "") |
  "\(.metadata.namespace)/\(.metadata.name)\tExpires:\(.status.notAfter)"
' | head -15

echo ""
echo "=== Certificate Requests ==="
kubectl get certificaterequests --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,APPROVED:.status.conditions[?(@.type=="Approved")].status,READY:.status.conditions[?(@.type=="Ready")].status' 2>/dev/null | head -15

echo ""
echo "=== Pending Challenges ==="
kubectl get challenges --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,STATE:.status.state,DOMAIN:.spec.dnsName,TYPE:.spec.type' 2>/dev/null | head -15

echo ""
echo "=== Pending Orders ==="
kubectl get orders --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,STATE:.status.state' 2>/dev/null | head -10

echo ""
echo "=== Cert-Manager Logs (errors) ==="
kubectl logs deployment/cert-manager -n cert-manager --tail=20 2>/dev/null | grep -i "error\|fail\|warn" | head -10
```

## Output Format

- Target ≤50 lines per output
- Use `-o custom-columns` for targeted field extraction
- Show certificate expiry dates in ISO format
- Aggregate certificate counts by issuer when many exist
- Never dump full certificate specs -- show status and expiry only

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

- **Issuer vs ClusterIssuer**: Issuers are namespaced; ClusterIssuers are cluster-wide -- certificates reference one or the other
- **ACME challenges**: HTTP-01 requires ingress access; DNS-01 requires DNS provider credentials -- check challenge type
- **Challenge stuck**: Pending challenges often indicate DNS propagation or ingress routing issues
- **Renewal timing**: Cert-manager renews at 2/3 of certificate lifetime by default -- check `renewBefore` annotation
- **Rate limits**: Let's Encrypt has rate limits (50 certs/domain/week) -- check for rate limit errors in logs
- **Secret not created**: Certificate Ready=True but no Secret means the Secret was manually deleted -- check events
- **Webhook failures**: cert-manager webhook must be healthy for certificate creation -- check webhook pod
- **Order states**: valid, pending, failed, errored -- failed orders need manual investigation

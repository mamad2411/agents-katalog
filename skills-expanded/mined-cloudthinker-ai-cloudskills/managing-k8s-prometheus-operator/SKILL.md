---
name: managing-k8s-prometheus-operator
description: |
  Use when working with K8S Prometheus Operator — prometheus Operator management
  for Kubernetes monitoring stack. Covers Prometheus instances, ServiceMonitors,
  PodMonitors, PrometheusRules, Alertmanager configurations, scrape targets, and
  recording rules. Use when auditing monitoring coverage, debugging scrape
  failures, reviewing alerting rules, or managing Prometheus operator resources.
connection_type: k8s
preload: false
---

# Prometheus Operator Management Skill

Manage and analyze Prometheus Operator CRDs, scrape configurations, and alerting rules.

## MANDATORY: Discovery-First Pattern

**Always check Prometheus Operator installation and Prometheus instances before querying targets.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Prometheus Operator Deployment ==="
kubectl get deployment -l app.kubernetes.io/name=prometheus-operator --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,READY:.status.readyReplicas,IMAGE:.spec.template.spec.containers[0].image' 2>/dev/null

echo ""
echo "=== Prometheus Instances ==="
kubectl get prometheus --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,REPLICAS:.spec.replicas,RETENTION:.spec.retention,VERSION:.spec.version' 2>/dev/null

echo ""
echo "=== Alertmanager Instances ==="
kubectl get alertmanager --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,REPLICAS:.spec.replicas,VERSION:.spec.version' 2>/dev/null

echo ""
echo "=== ServiceMonitors ==="
kubectl get servicemonitors --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,ENDPOINTS:.spec.endpoints[*].port' 2>/dev/null | head -20

echo ""
echo "=== PodMonitors ==="
kubectl get podmonitors --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name' 2>/dev/null | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== PrometheusRules ==="
kubectl get prometheusrules --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name' 2>/dev/null | head -15

echo ""
echo "=== Alert Rules Summary ==="
kubectl get prometheusrules --all-namespaces -o json 2>/dev/null | jq -r '
  .items[] |
  .spec.groups[]? |
  "\(.name)\tRules:\(.rules | length)"
' | head -20

echo ""
echo "=== Firing Alerts (via Alertmanager API) ==="
AM_POD=$(kubectl get pods -l app.kubernetes.io/name=alertmanager --all-namespaces -o jsonpath='{.items[0].metadata.namespace}/{.items[0].metadata.name}' 2>/dev/null)
if [ -n "$AM_POD" ]; then
  NS=$(echo "$AM_POD" | cut -d/ -f1)
  POD=$(echo "$AM_POD" | cut -d/ -f2)
  kubectl exec -n "$NS" "$POD" -- wget -qO- http://localhost:9093/api/v2/alerts 2>/dev/null | jq -r '
    .[] | select(.status.state == "active") | "\(.labels.alertname)\t\(.labels.severity // "unknown")\t\(.labels.namespace // "cluster")"
  ' | head -15
fi

echo ""
echo "=== Prometheus Targets Health ==="
PROM_POD=$(kubectl get pods -l app.kubernetes.io/name=prometheus --all-namespaces -o jsonpath='{.items[0].metadata.namespace}/{.items[0].metadata.name}' 2>/dev/null)
if [ -n "$PROM_POD" ]; then
  NS=$(echo "$PROM_POD" | cut -d/ -f1)
  POD=$(echo "$PROM_POD" | cut -d/ -f2)
  kubectl exec -n "$NS" "$POD" -c prometheus -- wget -qO- http://localhost:9090/api/v1/targets 2>/dev/null | jq -r '
    .data.activeTargets[] | select(.health != "up") | "\(.labels.job)\t\(.health)\t\(.lastError[0:80])"
  ' | head -15
fi

echo ""
echo "=== Prometheus Storage ==="
kubectl get prometheus --all-namespaces -o json 2>/dev/null | jq -r '
  .items[] |
  "\(.metadata.namespace)/\(.metadata.name)\tRetention:\(.spec.retention // "default")\tStorage:\(.spec.storage.volumeClaimTemplate.spec.resources.requests.storage // "emptyDir")"
'

echo ""
echo "=== Operator Logs (errors) ==="
OPERATOR_NS=$(kubectl get deployment -l app.kubernetes.io/name=prometheus-operator --all-namespaces -o jsonpath='{.items[0].metadata.namespace}' 2>/dev/null)
kubectl logs deployment/prometheus-operator -n "$OPERATOR_NS" --tail=20 2>/dev/null | grep -i "error\|fail" | head -10
```

## Output Format

- Target ≤50 lines per output
- Use `-o custom-columns` for CRD listings
- Aggregate alert rules by group and count
- Show target health as up/down summary, not full target list
- Never dump full PrometheusRule specs -- show group names and rule counts

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

- **Label selectors**: Prometheus instances use `serviceMonitorSelector` to discover ServiceMonitors -- unmatched labels mean no scraping
- **Namespace selectors**: `serviceMonitorNamespaceSelector` controls which namespaces are watched -- empty means same namespace only
- **RBAC**: Prometheus needs ClusterRole to discover ServiceMonitors across namespaces
- **Storage**: Default is emptyDir (data lost on restart) -- use persistent storage for production
- **Retention**: Default retention is 24h -- set `retention` in Prometheus spec for longer periods
- **Scrape interval**: Default is 30s -- shorter intervals increase storage and resource usage
- **CRD versions**: Ensure CRD versions match operator version -- mismatches cause reconciliation failures
- **Thanos sidecar**: Check if Thanos sidecar is configured for long-term storage and HA

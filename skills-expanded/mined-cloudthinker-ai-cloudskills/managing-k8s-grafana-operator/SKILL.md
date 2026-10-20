---
name: managing-k8s-grafana-operator
description: |
  Use when working with K8S Grafana Operator — grafana Operator management for
  Kubernetes dashboard and datasource automation. Covers Grafana instances,
  GrafanaDashboard CRDs, GrafanaDatasource configurations, GrafanaFolder
  management, and operator health. Use when auditing dashboards, managing
  datasource configurations, debugging Grafana operator issues, or reviewing
  Grafana instance settings.
connection_type: k8s
preload: false
---

# Grafana Operator Management Skill

Manage and analyze Grafana Operator instances, dashboards, and datasource configurations.

## MANDATORY: Discovery-First Pattern

**Always check Grafana Operator health and Grafana instances before inspecting dashboards.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Grafana Operator Deployment ==="
kubectl get deployment -l app.kubernetes.io/name=grafana-operator --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,READY:.status.readyReplicas,IMAGE:.spec.template.spec.containers[0].image' 2>/dev/null

echo ""
echo "=== Grafana Instances ==="
kubectl get grafana --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,AGE:.metadata.creationTimestamp' 2>/dev/null

echo ""
echo "=== Grafana Dashboards ==="
kubectl get grafanadashboards --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,FOLDER:.spec.folder,UID:.status.uid' 2>/dev/null | head -20

echo ""
echo "=== Grafana Datasources ==="
kubectl get grafanadatasources --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,TYPE:.spec.datasource.type' 2>/dev/null | head -15

echo ""
echo "=== Grafana Folders ==="
kubectl get grafanafolders --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name' 2>/dev/null | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Dashboard Sync Status ==="
kubectl get grafanadashboards --all-namespaces -o json 2>/dev/null | jq -r '
  .items[] |
  "\(.metadata.namespace)/\(.metadata.name)\tUID:\(.status.uid // "pending")\tHash:\(.status.hash // "none")"
' | head -20

echo ""
echo "=== Dashboards with Errors ==="
kubectl get grafanadashboards --all-namespaces -o json 2>/dev/null | jq -r '
  .items[] |
  select(.status.conditions[]? | select(.type == "Ready" and .status != "True")) |
  "\(.metadata.namespace)/\(.metadata.name)\t\(.status.conditions[] | select(.type == "Ready") | .message // "unknown error")"
' | head -10

echo ""
echo "=== Datasource Configuration Summary ==="
kubectl get grafanadatasources --all-namespaces -o json 2>/dev/null | jq -r '
  .items[] |
  "\(.metadata.namespace)/\(.metadata.name)\tType:\(.spec.datasource.type)\tURL:\(.spec.datasource.url // "default")\tAccess:\(.spec.datasource.access // "proxy")"
' | head -15

echo ""
echo "=== Grafana Instance Details ==="
kubectl get grafana --all-namespaces -o json 2>/dev/null | jq -r '
  .items[] |
  "\(.metadata.namespace)/\(.metadata.name)\tExternal:\(.spec.external // "managed")"
' | head -10

echo ""
echo "=== Grafana Pods ==="
kubectl get pods -l app.kubernetes.io/name=grafana --all-namespaces -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,STATUS:.status.phase,RESTARTS:.status.containerStatuses[0].restartCount' 2>/dev/null

echo ""
echo "=== Operator Logs (errors) ==="
OPERATOR_NS=$(kubectl get deployment -l app.kubernetes.io/name=grafana-operator --all-namespaces -o jsonpath='{.items[0].metadata.namespace}' 2>/dev/null)
kubectl logs deployment/grafana-operator -n "$OPERATOR_NS" --tail=20 2>/dev/null | grep -i "error\|fail" | head -10
```

## Output Format

- Target ≤50 lines per output
- Use `-o custom-columns` for CRD listings
- Show dashboard folder hierarchy when available
- Aggregate dashboard counts by folder or namespace
- Never dump full dashboard JSON -- show name, folder, and sync status only

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

- **Operator versions**: v4 vs v5 have significantly different CRD schemas -- check operator version first
- **External Grafana**: Operator can manage external Grafana instances -- check `spec.external` field
- **Dashboard source**: Dashboards can come from JSON, URL, or ConfigMap -- check `spec.source` or `spec.json`
- **Datasource secrets**: Credentials are often in Kubernetes Secrets -- verify secret references exist
- **Instance selector**: Dashboards use `instanceSelector` to target specific Grafana instances -- unmatched selectors cause silent failures
- **Multi-instance**: Multiple Grafana instances can coexist -- ensure dashboards target the correct instance
- **Folder creation**: Folders must exist before dashboards reference them -- check GrafanaFolder resources
- **Resync period**: Operator periodically resyncs -- temporary API errors may self-resolve

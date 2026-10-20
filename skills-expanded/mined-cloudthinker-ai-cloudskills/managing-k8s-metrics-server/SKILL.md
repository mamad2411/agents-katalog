---
name: managing-k8s-metrics-server
description: |
  Use when working with K8S Metrics Server — kubernetes Metrics Server
  management and resource metrics analysis. Covers Metrics Server deployment
  health, node and pod resource utilization, top consumers, API availability,
  and metrics accuracy. Use when debugging HPA scaling issues, reviewing
  resource utilization, troubleshooting metrics unavailability, or analyzing
  cluster capacity.
connection_type: k8s
preload: false
---

# Kubernetes Metrics Server Skill

Manage and analyze Kubernetes Metrics Server for resource utilization data.

## MANDATORY: Discovery-First Pattern

**Always check Metrics Server health before querying metrics.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Metrics Server Deployment ==="
kubectl get deployment metrics-server -n kube-system -o custom-columns='NAME:.metadata.name,READY:.status.readyReplicas,AVAILABLE:.status.availableReplicas,IMAGE:.spec.template.spec.containers[0].image' 2>/dev/null

echo ""
echo "=== Metrics Server Pods ==="
kubectl get pods -n kube-system -l k8s-app=metrics-server -o custom-columns='NAME:.metadata.name,STATUS:.status.phase,RESTARTS:.status.containerStatuses[0].restartCount,NODE:.spec.nodeName' 2>/dev/null

echo ""
echo "=== Metrics API Availability ==="
kubectl get apiservices v1beta1.metrics.k8s.io -o custom-columns='NAME:.metadata.name,SERVICE:.spec.service.name,AVAILABLE:.status.conditions[?(@.type=="Available")].status' 2>/dev/null

echo ""
echo "=== Metrics Server Args ==="
kubectl get deployment metrics-server -n kube-system -o jsonpath='{.spec.template.spec.containers[0].args}' 2>/dev/null
echo ""
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Node Resource Usage ==="
kubectl top nodes 2>/dev/null | head -20

echo ""
echo "=== Top CPU Pods (all namespaces) ==="
kubectl top pods --all-namespaces --sort-by=cpu 2>/dev/null | head -15

echo ""
echo "=== Top Memory Pods (all namespaces) ==="
kubectl top pods --all-namespaces --sort-by=memory 2>/dev/null | head -15

echo ""
echo "=== Pods Without Resource Requests ==="
kubectl get pods --all-namespaces -o json 2>/dev/null | jq -r '
  .items[] |
  select(.spec.containers[].resources.requests == null or .spec.containers[].resources.requests == {}) |
  "\(.metadata.namespace)/\(.metadata.name)\t\(.spec.containers[].name)"
' | head -15

echo ""
echo "=== Resource Utilization vs Requests ==="
kubectl get pods --all-namespaces -o json 2>/dev/null | jq -r '
  .items[] |
  select(.status.phase == "Running") |
  .spec.containers[] |
  select(.resources.requests.cpu // "" != "") |
  "\(.name)\tCPU-req:\(.resources.requests.cpu)\tMem-req:\(.resources.requests.memory // "none")"
' | head -15

echo ""
echo "=== Metrics Server Logs (errors) ==="
kubectl logs deployment/metrics-server -n kube-system --tail=20 2>/dev/null | grep -i "error\|fail\|unable" | head -10
```

## Output Format

- Target ≤50 lines per output
- Use `kubectl top` for resource usage summaries
- Show CPU in millicores and memory in Mi/Gi
- Aggregate per-namespace when many pods exist
- Never dump raw metrics API responses -- use kubectl top

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

- **API not available**: Metrics Server takes ~60 seconds after startup to serve metrics -- check apiservice status
- **Kubelet connectivity**: Metrics Server scrapes kubelets -- network policies or firewall rules can block port 10250
- **TLS errors**: `--kubelet-insecure-tls` may be needed in some environments -- check logs for x509 errors
- **Scrape interval**: Default is 60 seconds -- metrics are not real-time, they are point-in-time snapshots
- **HPA dependency**: HPA requires Metrics Server for CPU/memory scaling -- no metrics means no autoscaling
- **Resource requests**: `kubectl top` shows actual usage; compare against `resources.requests` for right-sizing
- **HA mode**: Production clusters should run multiple replicas with `--enable-aggregator-routing`
- **VPA conflict**: VPA also reads from Metrics Server -- ensure both can function concurrently

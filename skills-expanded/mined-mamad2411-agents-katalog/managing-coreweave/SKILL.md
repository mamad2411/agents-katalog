---
name: managing-coreweave
description: |
  Use when working with Coreweave — coreWeave GPU cloud management covering
  Kubernetes namespace inventory, GPU workload status, virtual server instances,
  persistent volume claims, node allocation, billing analysis, and network
  configuration. Use for comprehensive CoreWeave infrastructure assessment and
  GPU workload optimization.
connection_type: coreweave
preload: false
---

# CoreWeave Management

Analyze CoreWeave GPU workloads, virtual servers, storage, and Kubernetes resources.

## Phase 1: Discovery

```bash
#!/bin/bash
# CoreWeave uses standard Kubernetes API with their kubeconfig
export KUBECONFIG="${COREWEAVE_KUBECONFIG:-$HOME/.kube/coreweave}"

echo "=== Namespaces ==="
kubectl get namespaces -o json \
  | jq -r '.items[] | "\(.metadata.name)\t\(.status.phase)\t\(.metadata.creationTimestamp[0:10])"' \
  | column -t | head -15

echo ""
echo "=== GPU Workloads ==="
kubectl get pods --all-namespaces -o json \
  | jq -r '.items[] | select(.spec.containers[].resources.limits["nvidia.com/gpu"] != null) | "\(.metadata.namespace)\t\(.metadata.name[0:40])\t\(.status.phase)\t\(.spec.containers[0].resources.limits["nvidia.com/gpu"]) GPU(s)\t\(.spec.nodeName // "pending")"' \
  | column -t | head -20

echo ""
echo "=== Virtual Servers ==="
kubectl get virtualservers --all-namespaces -o json 2>/dev/null \
  | jq -r '.items[]? | "\(.metadata.namespace)\t\(.metadata.name)\t\(.status.state // "unknown")\t\(.spec.resources.gpu.type // "N/A")\t\(.spec.resources.gpu.count // 0) GPU(s)"' \
  | column -t | head -15

echo ""
echo "=== Persistent Volume Claims ==="
kubectl get pvc --all-namespaces -o json \
  | jq -r '.items[] | "\(.metadata.namespace)\t\(.metadata.name[0:30])\t\(.status.phase)\t\(.spec.resources.requests.storage)\t\(.spec.storageClassName)"' \
  | column -t | head -20
```

## Phase 2: Analysis

```bash
#!/bin/bash
export KUBECONFIG="${COREWEAVE_KUBECONFIG:-$HOME/.kube/coreweave}"

echo "=== Node GPU Summary ==="
kubectl get nodes -o json \
  | jq -r '.items[] | select(.status.capacity["nvidia.com/gpu"] != null) | "\(.metadata.name[0:30])\t\(.metadata.labels["gpu.nvidia.com/class"] // "unknown")\tGPUs:\(.status.capacity["nvidia.com/gpu"])\tAllocatable:\(.status.allocatable["nvidia.com/gpu"])"' \
  | column -t | head -20

echo ""
echo "=== Deployments ==="
kubectl get deployments --all-namespaces -o json \
  | jq -r '.items[] | "\(.metadata.namespace)\t\(.metadata.name[0:30])\t\(.status.readyReplicas // 0)/\(.spec.replicas)\t\(.status.updatedReplicas // 0) updated"' \
  | column -t | head -15

echo ""
echo "=== Services & Endpoints ==="
kubectl get services --all-namespaces -o json \
  | jq -r '.items[] | select(.metadata.namespace != "kube-system") | "\(.metadata.namespace)\t\(.metadata.name[0:30])\t\(.spec.type)\t\(.spec.clusterIP)\t\(.status.loadBalancer.ingress[0].ip // "N/A")"' \
  | column -t | head -15

echo ""
echo "=== Resource Requests Summary ==="
kubectl get pods --all-namespaces -o json \
  | jq '{
    total_gpu_requests: [.items[].spec.containers[].resources.requests["nvidia.com/gpu"] // "0" | tonumber] | add,
    total_cpu_requests: [.items[].spec.containers[].resources.requests.cpu // "0" | gsub("m";"") | tonumber] | add,
    total_memory_requests_gi: ([.items[].spec.containers[].resources.requests.memory // "0" | gsub("Gi";"") | gsub("Mi";"") | tonumber] | add / 1024 | . * 10 | round / 10),
    pod_count: (.items | length)
  }'

echo ""
echo "=== InferenceService (KServe) ==="
kubectl get inferenceservices --all-namespaces -o json 2>/dev/null \
  | jq -r '.items[]? | "\(.metadata.namespace)\t\(.metadata.name[0:30])\t\(.status.conditions[-1].type // "unknown")\t\(.status.url // "N/A")"' \
  | column -t | head -10

echo ""
echo "=== Recent Events ==="
kubectl get events --all-namespaces --sort-by='.lastTimestamp' -o json \
  | jq -r '.items[-10:][] | "\(.metadata.namespace)\t\(.involvedObject.name[0:25])\t\(.type)\t\(.reason)\t\(.message[0:50])"' \
  | column -t
```

## Output Format

```
COREWEAVE ANALYSIS
====================
Namespace        Workload           GPUs     Type      Status    Storage
──────────────────────────────────────────────────────────────────────────
ml-training      train-job-large    8xA100   Pod       Running   500Gi
inference        llm-server         4xA40    VS        Running   200Gi
dev              experiment-1       1xRTX    Pod       Running   50Gi

GPUs: 13 allocated (A100:8, A40:4, RTX:1)
Pods: 12 running | Virtual Servers: 2 | PVCs: 8 (750Gi total)
Services: 5 (2 LoadBalancer) | Namespaces: 4 active
```

## Safety Rules

- **Read-only**: Only use `kubectl get`, `describe`, and `logs` commands
- **Never create, delete, or scale** workloads without confirmation
- **Kubeconfig**: Never output kubeconfig contents or tokens
- **Secrets**: Never read or output Kubernetes secret values

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


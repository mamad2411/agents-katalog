---
name: managing-azure-container-instances
description: |
  Use when working with Azure Container Instances — azure Container Instances
  management covering container group inventory, container status and restart
  counts, CPU and memory utilization, networking configuration, log retrieval,
  and GPU allocation tracking. Use for ACI workload monitoring and
  troubleshooting.
connection_type: azure
preload: false
---

# Azure Container Instances Management

Analyze Azure Container Instances groups, resource utilization, and container health.

## Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Container Groups Inventory ==="
az container list --output json \
  | jq -r '.[] | "\(.name)\t\(.resourceGroup)\t\(.provisioningState)\t\(.osType)\t\(.location)\t\(.ipAddress.ip // "none")"' \
  | column -t | head -20

echo ""
echo "=== Container Details ==="
for CG in $(az container list --query '[].name' -o tsv); do
  RG=$(az container show --name "$CG" --query 'resourceGroup' -o tsv 2>/dev/null)
  az container show --name "$CG" --resource-group "$RG" --output json \
    | jq '{name, state: .instanceView.state, restartCount: .containers[0].instanceView.restartCount, containers: [.containers[] | {name, image: .image, cpu: .resources.requests.cpu, memoryGB: .resources.requests.memoryInGB, state: .instanceView.currentState.state}]}' 2>/dev/null
done | head -30

echo ""
echo "=== Networking ==="
az container list --output json \
  | jq -r '.[] | "\(.name)\t\(.ipAddress.type // "none")\t\(.ipAddress.ip // "none")\t\(.ipAddress.ports[]? | "\(.port)/\(.protocol)" // "none")"' \
  | column -t | head -20

echo ""
echo "=== Volume Mounts ==="
az container list --output json \
  | jq '.[] | select(.volumes != null) | {name, volumes: [.volumes[] | {name, type: (if .azureFile != null then "azureFile" elif .gitRepo != null then "gitRepo" elif .emptyDir != null then "emptyDir" else "secret" end)}]}' \
  | head -20
```

## Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Container Group Status ==="
for CG in $(az container list --query '[].name' -o tsv); do
  RG=$(az container show --name "$CG" --query 'resourceGroup' -o tsv 2>/dev/null)
  az container show --name "$CG" --resource-group "$RG" --output json \
    | jq '{
        name,
        state: .instanceView.state,
        events: [.instanceView.events[]? | {type, message: .message[0:80], timestamp: .firstTimestamp}] | last(3),
        containers: [.containers[] | {
          name,
          state: .instanceView.currentState.state,
          restarts: .instanceView.restartCount,
          exitCode: .instanceView.currentState.exitCode
        }]
      }' 2>/dev/null
done | head -40

echo ""
echo "=== Resource Utilization ==="
for CG in $(az container list --query '[].name' -o tsv); do
  RG=$(az container show --name "$CG" --query 'resourceGroup' -o tsv 2>/dev/null)
  echo "--- ${CG} ---"
  az monitor metrics list --resource "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/${RG}/providers/Microsoft.ContainerInstance/containerGroups/${CG}" \
    --metric "CpuUsage,MemoryUsage" --interval PT1H \
    --aggregation Average Maximum \
    --query "value[].{metric:name.value, avg:timeseries[0].data[-1].average, max:timeseries[0].data[-1].maximum}" \
    -o table 2>/dev/null
done

echo ""
echo "=== Recent Container Logs ==="
for CG in $(az container list --query '[].name' -o tsv | head -5); do
  RG=$(az container show --name "$CG" --query 'resourceGroup' -o tsv 2>/dev/null)
  CONTAINER=$(az container show --name "$CG" --resource-group "$RG" --query 'containers[0].name' -o tsv 2>/dev/null)
  echo "--- ${CG}/${CONTAINER} ---"
  az container logs --name "$CG" --resource-group "$RG" --container-name "$CONTAINER" --tail 5 2>/dev/null
done

echo ""
echo "=== GPU Allocations ==="
az container list --output json \
  | jq '.[] | select(.containers[].resources.requests.gpu != null) | {name, gpu: .containers[].resources.requests.gpu}' 2>/dev/null
```

## Output Format

```
AZURE CONTAINER INSTANCES ANALYSIS
====================================
Container Group    State     Containers  CPU   Memory  Restarts  IP
──────────────────────────────────────────────────────────────────────
batch-processor    Running   2           2.0   4.0GB   0         10.0.1.5
web-scraper        Running   1           1.0   1.5GB   3         Public
ml-inference       Succeeded 1           4.0   8.0GB   0         none

Groups: 3 | Containers: 4 | GPU: 1 with K80
Restart Issues: 1 group with 3+ restarts
```

## Safety Rules

- **Read-only**: Only use `az container list`, `show`, `logs`, and `az monitor metrics`
- **Never start, stop, or delete** container groups without explicit confirmation
- **Log limits**: Always use `--tail` to prevent unbounded log output
- **Secrets**: Never output secret volume contents

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


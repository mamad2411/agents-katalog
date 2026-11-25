---
name: managing-azure-eventhubs
description: |
  Use when working with Azure Eventhubs — azure Event Hubs partition analysis,
  checkpoint management, capture status, consumer group monitoring, and
  throughput analysis.
connection_type: azure
preload: false
---

# Azure Event Hubs Management Skill

Analyze and manage Azure Event Hubs with safe, read-only operations.

## MANDATORY: Two-Phase Execution

**You MUST follow this two-phase pattern. Skipping Phase 1 causes hallucinated namespace/hub names.**

### Phase 1: Discovery (ALWAYS run first)

```bash
#!/bin/bash

# 1. List Event Hubs namespaces
az eventhubs namespace list --output json | jq '.[] | {name, resourceGroup: .resourceGroup, sku: .sku.name, location}'

# 2. List Event Hubs in a namespace
az eventhubs eventhub list --namespace-name "$EH_NAMESPACE" --resource-group "$RG" --output json | jq '.[] | {name, partitionCount, messageRetentionInDays, status}'

# 3. Describe an Event Hub
az eventhubs eventhub show --namespace-name "$EH_NAMESPACE" --resource-group "$RG" --name "$EH_NAME" --output json

# 4. List consumer groups
az eventhubs eventhub consumer-group list --namespace-name "$EH_NAMESPACE" --resource-group "$RG" --eventhub-name "$EH_NAME" --output json

# 5. List authorization rules
az eventhubs namespace authorization-rule list --namespace-name "$EH_NAMESPACE" --resource-group "$RG" --output json
```

**Phase 1 outputs:**
- Namespaces with SKU and region
- Event Hubs with partition counts
- Consumer groups

### Phase 2: Analysis (only after Phase 1)

Only reference namespaces, Event Hubs, and consumer groups confirmed in Phase 1.

## Shell Script Patterns

### Helper Function

```bash
#!/bin/bash

# Core Event Hubs helper — always use this
eh_cmd() {
    az eventhubs "$@" --output json
}

# Azure Monitor metrics
eh_metric() {
    local resource_id="$1" metric="$2" aggregation="${3:-Total}" interval="${4:-PT5M}"
    az monitor metrics list \
        --resource "$resource_id" \
        --metric "$metric" \
        --aggregation "$aggregation" \
        --interval "$interval" \
        --start-time "$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
        --output json
}
```

## Anti-Hallucination Rules

- **NEVER reference a namespace** without confirming via `az eventhubs namespace list`
- **NEVER reference an Event Hub** without confirming via `az eventhubs eventhub list`
- **NEVER assume consumer group names** — always list them
- **NEVER guess partition count** — always describe the Event Hub
- **NEVER assume capture is enabled** — check Event Hub configuration

## Safety Rules

- **READ-ONLY ONLY**: Use only list, show, az monitor metrics list
- **FORBIDDEN**: create, delete, update, az eventhubs eventhub consumer-group delete without explicit user request
- **Use Azure Monitor** for metrics instead of consuming messages
- **NEVER receive messages** from production Event Hubs for analysis

## Common Operations

### Namespace Overview

```bash
#!/bin/bash
echo "=== Event Hubs Namespaces ==="
eh_cmd namespace list | jq '.[] | {name, resourceGroup, sku: .sku.name, capacity: .sku.capacity, location, isAutoInflateEnabled, maximumThroughputUnits}'

echo ""
echo "=== Event Hubs per Namespace ==="
NAMESPACE="${1:-my-namespace}"
RG="${2:-my-resource-group}"
eh_cmd eventhub list --namespace-name "$NAMESPACE" --resource-group "$RG" | jq '.[] | {name, partitionCount, messageRetentionInDays, status, captureDescription}'
```

### Partition Analysis

```bash
#!/bin/bash
NAMESPACE="${1:-my-namespace}"
RG="${2:-my-resource-group}"
EH_NAME="${3:-my-eventhub}"

echo "=== Event Hub Details ==="
eh_cmd eventhub show --namespace-name "$NAMESPACE" --resource-group "$RG" --name "$EH_NAME" | jq '{name, partitionCount, partitionIds, messageRetentionInDays, status}'

echo ""
echo "=== Consumer Groups ==="
eh_cmd eventhub consumer-group list --namespace-name "$NAMESPACE" --resource-group "$RG" --eventhub-name "$EH_NAME" | jq '.[] | {name, userMetadata}'

echo ""
echo "=== Incoming Messages (metrics) ==="
RESOURCE_ID=$(az eventhubs namespace show --name "$NAMESPACE" --resource-group "$RG" --query id -o tsv)
eh_metric "$RESOURCE_ID" "IncomingMessages" "Total" "PT5M" | jq '.value[0].timeseries[0].data[-5:][] | {timeStamp, total}'
```

### Capture Status

```bash
#!/bin/bash
NAMESPACE="${1:-my-namespace}"
RG="${2:-my-resource-group}"

echo "=== Event Hubs with Capture ==="
eh_cmd eventhub list --namespace-name "$NAMESPACE" --resource-group "$RG" | jq '[.[] | select(.captureDescription.enabled == true)] | .[] | {name, captureDescription: {enabled: .captureDescription.enabled, encoding: .captureDescription.encoding, intervalInSeconds: .captureDescription.intervalInSeconds, sizeLimitInBytes: .captureDescription.sizeLimitInBytes, destination: .captureDescription.destination}}'

echo ""
echo "=== Event Hubs without Capture ==="
eh_cmd eventhub list --namespace-name "$NAMESPACE" --resource-group "$RG" | jq '[.[] | select(.captureDescription.enabled != true)] | .[] | {name, partitionCount}'
```

### Throughput Analysis

```bash
#!/bin/bash
NAMESPACE="${1:-my-namespace}"
RG="${2:-my-resource-group}"
RESOURCE_ID=$(az eventhubs namespace show --name "$NAMESPACE" --resource-group "$RG" --query id -o tsv)

echo "=== Incoming Messages ==="
eh_metric "$RESOURCE_ID" "IncomingMessages" "Total" | jq '.value[0].timeseries[0].data[-5:][] | {timeStamp, total}'

echo ""
echo "=== Outgoing Messages ==="
eh_metric "$RESOURCE_ID" "OutgoingMessages" "Total" | jq '.value[0].timeseries[0].data[-5:][] | {timeStamp, total}'

echo ""
echo "=== Incoming Bytes ==="
eh_metric "$RESOURCE_ID" "IncomingBytes" "Total" | jq '.value[0].timeseries[0].data[-5:][] | {timeStamp, totalBytes: .total}'

echo ""
echo "=== Throttled Requests ==="
eh_metric "$RESOURCE_ID" "ThrottledRequests" "Total" | jq '.value[0].timeseries[0].data[-5:][] | select(.total > 0) | {timeStamp, total}'

echo ""
echo "=== Server Errors ==="
eh_metric "$RESOURCE_ID" "ServerErrors" "Total" | jq '.value[0].timeseries[0].data[-5:][] | select(.total > 0) | {timeStamp, total}'
```

## Output Format

Present results as a structured report:
```
Managing Azure Eventhubs Report
═══════════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Throughput units**: Standard tier limits throughput units — throttling occurs when exceeded
- **Partition count immutable**: Partition count cannot be decreased after creation — plan ahead
- **Consumer group limit**: Standard tier allows 20 consumer groups, Premium/Dedicated allows more
- **Checkpoint storage**: Consumers must manage checkpoints in Azure Blob Storage — check for stale checkpoints
- **Capture costs**: Capture to Blob Storage incurs additional storage costs
- **Auto-inflate**: Auto-inflate scales TUs up but not down — monitor for cost implications

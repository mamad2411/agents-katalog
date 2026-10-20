---
name: azure-eventhubs-capture
description: >
  Azure Event Hubs Capture for owned namespaces: enabling Capture to Azure Storage
  or Data Lake Gen2, time/size windows, Avro output, identity and firewall access,
  and operational monitoring. Use when persisting streams for batch analytics or
  compliance archives — not for unauthorized reading of third-party event streams.
---

# Azure Event Hubs Capture

## Scope And Authorization

- **In scope:** Event Hubs namespaces/hubs and destination storage in subscriptions you operate.
- **Out of scope:** Capturing or replaying events outside authorization; exposing capture containers publicly.
- Capture writes continuously — control storage cost and private network paths.
- Pair storage hardening with `azure-blob-misconfig`; use `code-quality-standards` for consumers.

## When To Use

- Archiving event streams to ADLS Gen2/Blob for Spark/Databricks/Synapse.
- Compliance retention of raw event payloads alongside stream processing.
- Backfilling analytics when stream consumers lag or fail.
- Tuning capture window (time/size) vs file count and latency to batch jobs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Service Bus sessions / ordering | `azure-servicebus-sessions` |
| Blob public access hardening | `azure-blob-misconfig` |
| General backpressure | `backpressure-patterns` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| Capture | Built-in pipeline from Event Hub to storage (Avro) |
| Window | Time and/or size triggers flush capture files |
| Destination | Blob container or ADLS Gen2 filesystem path |
| Identity | Prefer MI on namespace to storage (RBAC) over keys |
| Naming | Captured path includes namespace/hub/partition/date patterns |
| Tooling | `az eventhubs`, Portal, Storage Explorer, Azure Monitor |

## Workflow

### 1. Confirm scope and success criteria

1. Namespace, event hub, partitions, retention, destination storage, data class, authorization.
2. Success: Capture enabled; files land on schedule; batch job reads Avro; no public container.
3. Cost estimate: ingress + storage + transactions.

### 2. Inventory hubs and storage

```bash
az account show
az eventhubs namespace show -g "$RG" -n "$NS"
az eventhubs eventhub show -g "$RG" --namespace-name "$NS" -n "$HUB" -o jsonc
az storage account show -n "$ST" -g "$RG" --query "{public:allowBlobPublicAccess,net:networkRuleSet}"
```

1. Note throughput units/PU/capacity and existing consumers (checkpoint stores).
2. Confirm whether Capture already partially configured.
3. Check private endpoints for Event Hubs and Storage if required.

### 3. Baseline

1. Event rate (events/sec, bytes/sec) to size windows.
2. Consumer lag metrics — Capture is independent of consumer groups but shares load on the hub.
3. Schema expectations (Avro body includes system properties + body).

### 4. Enable Capture securely

```bash
# Create destination container (private)
az storage container create --account-name "$ST" -n eh-capture --auth-mode login --public-access off

# Grant Event Hubs namespace MI (or use capture destination auth per current API)
# Prefer managed identity with Storage Blob Data Contributor on the container scope

az eventhubs eventhub update -g "$RG" --namespace-name "$NS" -n "$HUB" \
  --enable-capture true \
  --capture-interval 300 \
  --capture-size-limit 314572800 \
  --destination-name EventHubArchive.AzureBlockBlob \
  --storage-account "$ST_ID" \
  --blob-container eh-capture \
  --archive-name-format "{Namespace}/{EventHub}/{PartitionId}/{Year}/{Month}/{Day}/{Hour}/{Minute}/{Second}"
```

*(Exact flags vary by CLI version — confirm with `az eventhubs eventhub update -h` and current docs.)*

1. Set interval/size to balance small-file problem vs latency (e.g. 5 min and ~300 MB).
2. Lock storage with firewall/PE; allow Event Hubs trusted access / MI path as designed.
3. Encrypt with CMK if org requires; align Event Hubs and Storage keys.
4. Do not put Capture on a public container; disable anonymous access.

### 5. Verify with evidence

```bash
az eventhubs eventhub show -g "$RG" --namespace-name "$NS" -n "$HUB" --query "captureDescription"
az storage blob list --account-name "$ST" -c eh-capture --auth-mode login --prefix "$NS/" -o table
# Send test events in nonprod; wait one window; confirm new Avro objects
```

1. Open sample Avro with authorized tool; validate fields; redact in screenshots.
2. Batch job can list/read via MI.
3. Failure injection: revoke storage RBAC → Capture health errors surface in Monitor.

### 6. Observe and harden

1. Metrics: Capture backlog/failures (per available metrics), storage capacity, Event Hubs throttling.
2. Lifecycle policies on capture prefix (tier cool/archive, expire after retention).
3. Alerts on missing files for N intervals during traffic hours.

### 7. Hand off

1. Document path format, window settings, retention, and readers.
2. IaC for hub Capture + storage RBAC.
3. Runbook when Capture pauses ( creds, firewall, quota ).

## Window Tuning

| Goal | Direction |
| --- | --- |
| Fewer small files | Larger size limit and/or longer interval |
| Faster batch freshness | Shorter interval |
| Cost control | Lifecycle tiering + compress/process downstream |
| Compliance archive | Immutability on storage + longer retention |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Destination | Private container + MI | Public container “for easy Spark” |
| Windows | Tuned to volume | 30s windows creating millions of tiny files |
| Schema | Documented Avro consumers | Assuming JSON lines in Capture files |
| Security | PE/firewall aligned | Keys in capture config checked into git |
| Ops | Alert on capture failures | Discover months later empty container |

## Output Checklist

- [ ] Hub and destination storage scoped and authorized
- [ ] Capture enablement parameters chosen (interval/size/format)
- [ ] Storage private + RBAC/MI configured
- [ ] Test events produce Avro objects
- [ ] Consumers validated on sample files
- [ ] Lifecycle/retention set
- [ ] Monitoring/alerts for capture health
- [ ] Cost reviewed
- [ ] `code-quality-standards` applied to automation

## Rules

- Authorized streams and storage only.
- Never expose capture containers publicly.
- Prefer managed identity to storage over account keys.
- Tune windows with evidence from event volume.
- Redact event payloads in documentation.

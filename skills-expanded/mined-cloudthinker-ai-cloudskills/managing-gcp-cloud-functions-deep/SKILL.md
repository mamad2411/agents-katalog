---
name: managing-gcp-cloud-functions-deep
description: |
  Use when working with Gcp Cloud Functions Deep — deep Google Cloud Functions
  analysis covering function inventory across generations (1st and 2nd gen),
  trigger configurations, execution metrics, memory and CPU allocation, VPC
  connector usage, secret bindings, and build configuration review. Provides
  insights on cold starts and scaling.
connection_type: gcp
preload: false
---

# GCP Cloud Functions Deep Management

Comprehensive analysis of Cloud Functions across both 1st gen and 2nd gen deployments.

## Phase 1: Discovery

```bash
#!/bin/bash
PROJECT="${GOOGLE_CLOUD_PROJECT}"

echo "=== Cloud Functions (2nd Gen) ==="
gcloud functions list --project="$PROJECT" --gen2 \
  --format="table(name.basename(), state, runtime, serviceConfig.availableMemory, serviceConfig.timeoutSeconds, serviceConfig.maxInstanceCount, updateTime)" \
  2>/dev/null | head -20

echo ""
echo "=== Cloud Functions (1st Gen) ==="
gcloud functions list --project="$PROJECT" \
  --format="table(name.basename(), status, runtime, availableMemoryMb, timeout, entryPoint, httpsTrigger.url:label=TRIGGER)" \
  2>/dev/null | head -20

echo ""
echo "=== Trigger Types ==="
gcloud functions list --project="$PROJECT" \
  --format="json" | jq -r '.[] | "\(.name | split("/") | last)\t\(.eventTrigger.eventType // "HTTP")"' \
  | column -t | head -20

echo ""
echo "=== VPC Connectors ==="
gcloud compute networks vpc-access connectors list --project="$PROJECT" \
  --format="table(name, network, ipCidrRange, state, minInstances, maxInstances)" 2>/dev/null

echo ""
echo "=== Runtime Distribution ==="
gcloud functions list --project="$PROJECT" --format="value(runtime)" \
  | sort | uniq -c | sort -rn
```

## Phase 2: Analysis

```bash
#!/bin/bash
PROJECT="${GOOGLE_CLOUD_PROJECT}"

echo "=== Function Execution Metrics (7d) ==="
END=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
START=$(date -u -d "7 days ago" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -v-7d +"%Y-%m-%dT%H:%M:%SZ")

gcloud monitoring time-series list \
  --project="$PROJECT" \
  --filter='metric.type="cloudfunctions.googleapis.com/function/execution_count"' \
  --interval-start-time="$START" --interval-end-time="$END" \
  --format="table(metric.labels.function_name, points[0].value.int64Value:label=EXECUTIONS, metric.labels.status)" \
  2>/dev/null | head -30

echo ""
echo "=== Execution Times ==="
gcloud monitoring time-series list \
  --project="$PROJECT" \
  --filter='metric.type="cloudfunctions.googleapis.com/function/execution_times"' \
  --interval-start-time="$START" --interval-end-time="$END" \
  --format="table(metric.labels.function_name, points[0].value.distributionValue.mean:label=AVG_NS)" \
  2>/dev/null | head -20

echo ""
echo "=== Active Instances ==="
gcloud monitoring time-series list \
  --project="$PROJECT" \
  --filter='metric.type="cloudfunctions.googleapis.com/function/active_instances"' \
  --interval-start-time="$START" --interval-end-time="$END" \
  --format="table(metric.labels.function_name, points[0].value.int64Value:label=MAX_INSTANCES)" \
  2>/dev/null | head -20

echo ""
echo "=== Secret Bindings Audit ==="
for FUNC in $(gcloud functions list --project="$PROJECT" --format="value(name)"); do
  SECRETS=$(gcloud functions describe "$FUNC" --project="$PROJECT" --format="json" \
    | jq -r '.secretEnvironmentVariables[]?.secret // empty' 2>/dev/null)
  [ -n "$SECRETS" ] && echo "$(basename $FUNC): $SECRETS"
done

echo ""
echo "=== Build Configuration ==="
for FUNC in $(gcloud functions list --project="$PROJECT" --format="value(name)"); do
  gcloud functions describe "$FUNC" --project="$PROJECT" --format="json" \
    | jq '{name: (.name | split("/") | last), source: .sourceArchiveUrl, buildWorkerPool: .buildWorkerPool, dockerRegistry: .dockerRegistry}' 2>/dev/null
done | head -30
```

## Output Format

```
GCP CLOUD FUNCTIONS DEEP ANALYSIS
===================================
Function          Gen  Runtime       Memory  Timeout  Max-Inst  Executions  Errors  Avg-ms
──────────────────────────────────────────────────────────────────────────────────────────────
process-orders    2nd  nodejs20      512MB   60s      10        45200       12      120
auth-validate     2nd  python312     256MB   30s      100       128900      3       45
image-resize      1st  nodejs18      1024MB  120s     5         8900        0       2400

Runtimes: nodejs20(3) python312(2) go122(1)
VPC Connectors: 1 active | Secret Bindings: 2 functions
```

## Safety Rules

- **Read-only**: Only use `gcloud functions list`, `describe`, and monitoring queries
- **Never deploy or delete** functions without explicit user confirmation
- **Secrets**: Never output secret values, only report which secrets are bound
- **Quota**: Cloud Monitoring API has 6000 read requests per minute per project

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


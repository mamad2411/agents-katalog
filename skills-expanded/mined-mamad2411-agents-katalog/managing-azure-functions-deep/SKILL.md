---
name: managing-azure-functions-deep
description: |
  Use when working with Azure Functions Deep — deep Azure Functions analysis
  covering function app inventory, trigger types, execution metrics, scaling
  behavior, slot deployments, application insights integration, and consumption
  plan cost tracking. Provides optimization guidance for cold starts and memory
  usage.
connection_type: azure
preload: false
---

# Azure Functions Deep Management

Comprehensive Azure Functions analysis with performance profiling and cost optimization.

## Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Function Apps Inventory ==="
az functionapp list --output json \
  | jq -r '.[] | "\(.name)\t\(.resourceGroup)\t\(.kind)\t\(.state)\t\(.defaultHostName)"' \
  | column -t | head -20

echo ""
echo "=== Function App Runtimes & Plans ==="
for APP in $(az functionapp list --query '[].name' -o tsv); do
  RG=$(az functionapp show --name "$APP" --query 'resourceGroup' -o tsv)
  RUNTIME=$(az functionapp config show --name "$APP" --resource-group "$RG" --query 'linuxFxVersion || netFrameworkVersion' -o tsv 2>/dev/null)
  PLAN=$(az functionapp show --name "$APP" --resource-group "$RG" --query 'appServicePlanId' -o tsv | rev | cut -d'/' -f1 | rev)
  SKU=$(az appservice plan show --name "$PLAN" --resource-group "$RG" --query 'sku.name' -o tsv 2>/dev/null)
  echo -e "${APP}\t${RUNTIME:-N/A}\t${PLAN}\t${SKU:-Consumption}"
done | column -t

echo ""
echo "=== Individual Functions & Triggers ==="
for APP in $(az functionapp list --query '[].name' -o tsv); do
  RG=$(az functionapp show --name "$APP" --query 'resourceGroup' -o tsv)
  az functionapp function list --name "$APP" --resource-group "$RG" --output json \
    | jq -r ".[] | \"${APP}\t\(.name)\t\(.config.bindings[0].type // \"unknown\")\"" 2>/dev/null
done | column -t | head -30

echo ""
echo "=== Deployment Slots ==="
for APP in $(az functionapp list --query '[].name' -o tsv); do
  RG=$(az functionapp show --name "$APP" --query 'resourceGroup' -o tsv)
  az functionapp deployment slot list --name "$APP" --resource-group "$RG" \
    --query '[].{name:name,state:state}' -o tsv 2>/dev/null
done
```

## Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Execution Metrics (Application Insights) ==="
for APP in $(az functionapp list --query '[].name' -o tsv); do
  RG=$(az functionapp show --name "$APP" --query 'resourceGroup' -o tsv)
  AI_KEY=$(az functionapp config appsettings list --name "$APP" --resource-group "$RG" \
    --query "[?name=='APPINSIGHTS_INSTRUMENTATIONKEY'].value" -o tsv 2>/dev/null)
  if [ -n "$AI_KEY" ]; then
    echo "${APP}: App Insights connected"
  else
    echo "${APP}: NO App Insights configured"
  fi
done

echo ""
echo "=== Function App Health ==="
for APP in $(az functionapp list --query '[].name' -o tsv); do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://${APP}.azurewebsites.net/api/health" 2>/dev/null)
  echo "${APP}: HTTP ${STATUS}"
done

echo ""
echo "=== App Settings Audit (non-secret) ==="
for APP in $(az functionapp list --query '[].name' -o tsv); do
  RG=$(az functionapp show --name "$APP" --query 'resourceGroup' -o tsv)
  RUNTIME_VER=$(az functionapp config appsettings list --name "$APP" --resource-group "$RG" \
    --query "[?name=='FUNCTIONS_EXTENSION_VERSION'].value" -o tsv 2>/dev/null)
  WORKER_RT=$(az functionapp config appsettings list --name "$APP" --resource-group "$RG" \
    --query "[?name=='FUNCTIONS_WORKER_RUNTIME'].value" -o tsv 2>/dev/null)
  echo "${APP}: runtime=${WORKER_RT:-N/A} version=${RUNTIME_VER:-N/A}"
done

echo ""
echo "=== Scale Settings ==="
for APP in $(az functionapp list --query '[].name' -o tsv); do
  RG=$(az functionapp show --name "$APP" --query 'resourceGroup' -o tsv)
  az functionapp show --name "$APP" --resource-group "$RG" \
    --query '{name:name, maxWorkers:siteConfig.functionAppScaleLimit, alwaysOn:siteConfig.alwaysOn, minInstances:siteConfig.minimumElasticInstanceCount}' -o json 2>/dev/null
done
```

## Output Format

```
AZURE FUNCTIONS DEEP ANALYSIS
===============================
App                Plan          Runtime     Version  Functions  Slots  Insights
──────────────────────────────────────────────────────────────────────────────────
order-api          Consumption   node:20     ~4       5          0      Yes
payment-proc       Premium-EP1   dotnet:8    ~4       3          1      Yes
batch-worker       Dedicated-S1  python:3.11 ~4       2          0      No

Triggers: httpTrigger(6) timerTrigger(2) queueTrigger(1) blobTrigger(1)
Scale: 2 apps with alwaysOn | 1 with minInstances
```

## Safety Rules

- **Read-only**: Only use `az functionapp list`, `show`, `config show` operations
- **Never modify** app settings, deployments, or scaling without confirmation
- **Secrets**: Never output connection strings or keys from app settings
- **Rate limits**: Azure CLI respects ARM throttling at 12000 reads/hour per subscription

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


---
name: managing-azure-iot-hub
description: |
  Use when working with Azure Iot Hub — azure IoT Hub management including
  device registry, device twins, message routing, endpoints, jobs, and IoT Edge
  deployments. Covers device connectivity status, message throughput, routing
  health, quota utilization, and Edge module monitoring.
connection_type: azure-iot-hub
preload: false
---

# Azure IoT Hub Management Skill

Monitor and manage Azure IoT Hub device fleet and messaging.

## MANDATORY: Discovery-First Pattern

**Always discover hub configuration and device count before querying twins or metrics.**

### Phase 1: Discovery

```bash
#!/bin/bash
HUB_NAME="${AZURE_IOT_HUB_NAME}"
RG="${AZURE_RESOURCE_GROUP}"

echo "=== IoT Hub Info ==="
az iot hub show --name "$HUB_NAME" --resource-group "$RG" \
  --query '{Name:name,SKU:sku.name,Tier:sku.tier,Units:sku.capacity,Location:location,State:properties.state}' \
  --output json | jq '.'

echo ""
echo "=== Quota & Usage ==="
az iot hub show-quota-metrics --name "$HUB_NAME" --resource-group "$RG" \
  --output table

echo ""
echo "=== Endpoints ==="
az iot hub routing-endpoint list --hub-name "$HUB_NAME" --resource-group "$RG" \
  --output table 2>/dev/null || echo "No custom routing endpoints"

echo ""
echo "=== Message Routes ==="
az iot hub route list --hub-name "$HUB_NAME" --resource-group "$RG" \
  --query '[].{Name:name,Source:source,Condition:condition,Endpoint:endpointNames[0],Enabled:isEnabled}' \
  --output table

echo ""
echo "=== Device Summary ==="
total=$(az iot hub device-identity list --hub-name "$HUB_NAME" --query 'length(@)' --output tsv 2>/dev/null)
echo "Total devices: ${total:-check with query}"
```

**Phase 1 outputs:** Hub config, quotas, endpoints, routes, device count

### Phase 2: Analysis

```bash
#!/bin/bash
echo "=== Device Connection Status ==="
az iot hub query --hub-name "$HUB_NAME" \
  --query-command "SELECT COUNT() AS total FROM devices WHERE connectionState = 'Connected'" \
  --output json 2>/dev/null | jq '.[0].total // "Run query in portal"'

echo ""
echo "=== Edge Deployments ==="
az iot edge deployment list --hub-name "$HUB_NAME" \
  --query '[].{ID:id,Priority:priority,Target:targetCondition,Applied:systemMetrics.results.appliedCount}' \
  --output table 2>/dev/null || echo "No Edge deployments"

echo ""
echo "=== IoT Hub Metrics (24h) ==="
for metric in "d2c.telemetry.ingress.success" "c2d.commands.egress.complete.success" "connectedDeviceCount" "devices.totalDevices"; do
  val=$(az monitor metrics list --resource "/subscriptions/${AZURE_SUBSCRIPTION_ID}/resourceGroups/${RG}/providers/Microsoft.Devices/IotHubs/${HUB_NAME}" \
    --metric "$metric" --interval PT1H --start-time "$(date -u -v-1d +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 day ago' +%Y-%m-%dT%H:%M:%SZ)" \
    --query 'value[0].timeseries[0].data[-1].total' --output tsv 2>/dev/null)
  echo "$metric: ${val:-N/A}"
done

echo ""
echo "=== Failed Routes ==="
az monitor metrics list --resource "/subscriptions/${AZURE_SUBSCRIPTION_ID}/resourceGroups/${RG}/providers/Microsoft.Devices/IotHubs/${HUB_NAME}" \
  --metric "d2c.telemetry.egress.dropped" --interval PT24H \
  --query 'value[0].timeseries[0].data[-1].total' --output tsv 2>/dev/null | \
  xargs -I{} echo "Dropped messages (24h): {}"
```

## Output Format

```
AZURE IOT HUB STATUS
====================
Hub: {name} ({sku}, {units} units)
Location: {location} | State: {state}
Devices: {total} | Connected: {count}
Messages (24h): {ingress} ingress, {egress} egress
Dropped Messages: {count}
Edge Deployments: {count}
Quota: {used}/{max} messages/day
Issues: {list_of_warnings}
```

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

- **SKU limits**: Free tier = 8000 messages/day, S1 = 400K/day per unit — check quota
- **Device twin queries**: IoT Hub query language is not SQL — syntax differs
- **Message size**: Max 256KB per message — larger payloads need chunking
- **Connection protocol**: MQTT, AMQP, HTTPS have different capabilities — check per device

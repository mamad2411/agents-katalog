# Alert Design

## Skill: `nmon_alert_design`

Design and configure network monitoring alerts that detect meaningful degradation while minimizing noise. This skill covers metric-based and log-based alerting, action groups, escalation policies, alert fatigue prevention, severity classification, and multi-cloud alerting strategy.

---

## Metric-Based Alerts

Metric alerts evaluate quantitative network health signals at regular intervals and fire when a threshold is crossed.

### Key Network Metrics and Thresholds

| Metric | Signal | Warning Threshold | Critical Threshold |
|---|---|---|---|
| **Packet Loss %** | End-to-end or per-hop loss | > 1% sustained 5 min | > 5% sustained 2 min |
| **Latency (P50)** | Median round-trip time | > 1.5× baseline | > 3× baseline |
| **Latency (P95)** | 95th percentile RTT | > 2× baseline | > 5× baseline |
| **Latency (P99)** | 99th percentile RTT | > 3× baseline | > 10× baseline |
| **Bandwidth Utilization** | % of provisioned capacity | > 70% sustained 15 min | > 90% sustained 5 min |
| **Connection Count** | Active TCP connections | > 80% of SNAT port pool | > 95% of SNAT port pool |
| **VPN Tunnel Status** | Tunnel up/down state | Flapping (>3 transitions/hr) | Tunnel down > 2 min |
| **ExpressRoute BitsInPerSecond** | Circuit utilization | > 70% of circuit bandwidth | > 90% of circuit bandwidth |

### Azure Metric Alert (CLI)

```bash
az monitor metrics alert create \
  --name "HighPacketLoss-VPNGateway" \
  --resource-group MyRG \
  --scopes /subscriptions/<sub>/resourceGroups/MyRG/providers/Microsoft.Network/virtualNetworkGateways/MyVPNGW \
  --condition "avg TunnelEgressPacketDropCount > 500" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --action-group /subscriptions/<sub>/resourceGroups/MyRG/providers/Microsoft.Insights/actionGroups/NetOps \
  --severity 1 \
  --description "VPN tunnel packet loss exceeds threshold"
```

### AWS CloudWatch Alarm

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "TGW-BytesDropped-High" \
  --namespace AWS/TransitGateway \
  --metric-name BytesDropCountNoRoute \
  --dimensions Name=TransitGateway,Value=tgw-abc123 \
  --statistic Sum \
  --period 300 \
  --evaluation-periods 2 \
  --threshold 1000000 \
  --comparison-operator GreaterThanThreshold \
  --alarm-actions arn:aws:sns:us-east-1:123456789012:NetworkAlerts
```

---

## Log-Based Alerts

Log alerts evaluate query results from log analytics platforms, detecting patterns that metric-based alerts cannot capture. For Azure, build new flow-log alerts on VNet flow logs and current Traffic Analytics schemas; treat `AzureNetworkAnalytics_CL` examples below as legacy/schema examples and validate table and field names in the target workspace before deployment. NSG flow logs are legacy/migration-only (new creation blocked after 2025-06-30; retire 2027-09-30).

### Anomalous Traffic Patterns (legacy TA schema example)

Detect unusual spikes in traffic volume or new communication paths:

```kql
AzureNetworkAnalytics_CL
| where TimeGenerated > ago(1h)
| where SubType_s == "FlowLog"
| summarize FlowCount = count() by SrcIP_s, DestIP_s, DestPort_d
| join kind=leftanti (
    AzureNetworkAnalytics_CL
    | where TimeGenerated between (ago(30d) .. ago(1d))
    | where SubType_s == "FlowLog"
    | distinct SrcIP_s, DestIP_s, DestPort_d
) on SrcIP_s, DestIP_s, DestPort_d
| where FlowCount > 10
```

This query identifies source-destination-port combinations observed in the last hour that were never seen in the preceding 30 days — a strong indicator of lateral movement, new services, or misconfiguration.

### Denied Flow Spikes (legacy TA schema example)

```kql
AzureNetworkAnalytics_CL
| where TimeGenerated > ago(1h)
| where SubType_s == "FlowLog" and FlowStatus_s == "D"
| summarize DeniedFlows = count() by bin(TimeGenerated, 5m)
| where DeniedFlows > percentile(DeniedFlows, 95)
```

### New Port Access Detection (legacy TA schema example)

```kql
AzureNetworkAnalytics_CL
| where TimeGenerated > ago(1h)
| where SubType_s == "FlowLog" and FlowStatus_s == "A"
| distinct DestPort_d
| join kind=leftanti (
    AzureNetworkAnalytics_CL
    | where TimeGenerated between (ago(14d) .. ago(1d))
    | where SubType_s == "FlowLog" and FlowStatus_s == "A"
    | distinct DestPort_d
) on DestPort_d
```

---

## Action Groups and Escalation Policies

### Azure Action Group Configuration

Action groups define who gets notified and how. A single action group can include multiple notification channels:

| Channel | Use Case | Latency |
|---|---|---|
| **Email** | All severities, audit trail | 1-5 min |
| **SMS** | Sev0/Sev1 on-call notifications | < 30 sec |
| **Voice Call** | Sev0 escalation when SMS unacknowledged | < 60 sec |
| **Webhook** | PagerDuty, Opsgenie, ServiceNow integration | < 10 sec |
| **Logic App** | Automated diagnostics collection | < 30 sec |
| **Azure Function** | Custom remediation (e.g., failover trigger) | < 15 sec |
| **Event Hub** | SIEM ingestion, custom event processing | < 10 sec |

### Escalation Policy Design

1. **Immediate (0 min)**: Notify primary on-call via PagerDuty webhook + SMS.
2. **5 minutes**: If unacknowledged, escalate to secondary on-call via voice call.
3. **15 minutes**: If unresolved, page the network engineering manager and open an incident bridge.
4. **30 minutes**: If Sev0, escalate to VP of Infrastructure and initiate executive communication.

---

## Alert Fatigue Prevention

### Dynamic Thresholds

Azure Monitor supports dynamic thresholds that use machine learning to learn metric patterns and automatically adjust alert boundaries. Instead of a static `latency > 50ms`, dynamic thresholds adapt to time-of-day and day-of-week patterns.

```bash
az monitor metrics alert create \
  --name "DynamicLatency-AppGW" \
  --resource-group MyRG \
  --scopes <app-gateway-resource-id> \
  --condition "avg BackendLastByteResponseTime > dynamic medium 4 of 5 since 2024-01-01T00:00:00Z" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --action-group <action-group-id> \
  --severity 2
```

### Suppression Rules

- **Maintenance window suppression**: Disable non-critical alerts during planned maintenance using Azure Monitor alert processing rules.
- **Dependency suppression**: If a parent resource (e.g., ExpressRoute circuit) is down, suppress child alerts (e.g., individual VM connectivity) to reduce noise.
- **Cooldown periods**: After an alert fires, suppress duplicate firings for a configurable period (e.g., 15 minutes).

### Correlation

Group related alerts into a single incident. If packet loss, latency, and throughput alerts fire simultaneously for the same VPN gateway, correlate them into a single "VPN Gateway Degradation" incident rather than three separate alerts.

---

## Severity Levels and Triage Workflow

| Severity | Name | Response Time | Example |
|---|---|---|---|
| **Sev0** | Critical | Immediate (< 5 min) | ExpressRoute circuit down, complete site outage |
| **Sev1** | High | < 15 min | VPN tunnel down, >5% packet loss on production path |
| **Sev2** | Moderate | < 1 hour | Elevated latency (>2× baseline), bandwidth utilization >80% |
| **Sev3** | Low | < 4 hours | Intermittent packet loss, non-production connectivity issue |
| **Sev4** | Informational | Next business day | New traffic pattern detected, flow log gap, dashboard anomaly |

---

## Multi-Cloud Alerting Strategy

Establish a unified alerting pipeline across Azure, AWS, and GCP:

1. **Azure**: Azure Monitor metric/log alerts → webhook → PagerDuty.
2. **AWS**: CloudWatch Alarms → SNS → Lambda → PagerDuty. EventBridge for custom event patterns.
3. **GCP**: Cloud Monitoring alerting policies → Pub/Sub notification channels → PagerDuty.

Normalize severity mappings: Azure Sev0-4 maps to CloudWatch `ALARM` states and GCP alerting `critical`/`warning`/`info` classifications. Document the mapping in a shared runbook.

**Analysis only — verify against vendor documentation before applying.**

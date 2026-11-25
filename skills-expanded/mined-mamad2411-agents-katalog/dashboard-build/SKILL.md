# Dashboard Build

## Skill: `nmon_dashboard_build`

Design and build network monitoring dashboards that surface the golden signals of network health. This skill covers Azure Monitor Workbooks, CloudWatch dashboards, Grafana integration, and dashboard design best practices.

---

## Azure Monitor Workbooks

Azure Monitor Workbooks provide interactive, KQL-powered reports and dashboards that combine metrics, logs, and parameters into a single view.

### Creating a Network Health Workbook

Workbooks support multiple visualization types for network data:

- **Time charts**: Latency trends, throughput over time, packet loss percentage.
- **Grids/Tables**: Top talkers, denied flow summary, connection monitor status.
- **Maps**: Geographic traffic distribution from Traffic Analytics data.
- **Tiles/Stat panels**: Single-value summaries (current VPN tunnel count, active ExpressRoute circuits).
- **Graphs**: Network topology with traffic flow overlays.

### Parameterized Workbooks

Add parameters so users can filter dashboards dynamically:

```kql
// Subscription parameter
ResourceContainers
| where type == "microsoft.resources/subscriptions"
| project label=name, value=subscriptionId

// Resource Group parameter (cascading from Subscription)
ResourceContainers
| where type == "microsoft.resources/subscriptions/resourcegroups"
| where subscriptionId == "{Subscription}"
| project label=name, value=name
```

Parameters enable a single workbook to serve multiple teams, environments, or regions without duplication.

### Key Network KQL Panels

**VPN Tunnel Status Timeline:**

```kql
AzureDiagnostics
| where ResourceType == "VIRTUALNETWORKGATEWAYS"
| where Category == "TunnelDiagnosticLog"
| extend TunnelStatus = iff(status_s == "Connected", 1, 0)
| summarize AvgStatus = avg(TunnelStatus) by bin(TimeGenerated, 5m), remoteIP_s
| render timechart
```

**ExpressRoute Circuit Utilization:**

```kql
AzureMetrics
| where ResourceProvider == "MICROSOFT.NETWORK"
| where Resource contains "EXPRESSROUTE"
| where MetricName == "BitsInPerSecond" or MetricName == "BitsOutPerSecond"
| summarize AvgBps = avg(Average) by bin(TimeGenerated, 5m), MetricName
| render timechart
```

**Denied Flows Heatmap (legacy Traffic Analytics schema example):**

Use VNet flow logs and current Traffic Analytics schema fields for new Azure dashboards. The `AzureNetworkAnalytics_CL` / `NSGRule_s` example below is for legacy-schema orientation; NSG flow logs are legacy/migration-only (new creation blocked after 2025-06-30; retire 2027-09-30).

```kql
AzureNetworkAnalytics_CL
| where SubType_s == "FlowLog" and FlowStatus_s == "D"
| summarize DeniedCount = count() by bin(TimeGenerated, 1h), NSGRule_s
| render timechart
```

---

## Key Network Metrics to Visualize

Design dashboards around these core network health signals:

| Metric | Unit | Source | Significance |
|---|---|---|---|
| **Throughput** | bps / Mbps / Gbps | Flow logs, interface metrics | Capacity utilization, congestion detection |
| **Latency** | ms (P50, P95, P99) | Connection Monitor, ping probes | Application performance impact |
| **Packet Loss** | % | Connection Monitor, gateway diagnostics | Network quality degradation |
| **DNS Query Volume** | queries/sec | DNS analytics, resolver logs | Service dependency health, DNS attack detection |
| **Firewall Hit Counts** | hits/sec per rule | Azure Firewall diagnostics, NVA logs | Security rule effectiveness, attack surface |
| **VPN Tunnel Status** | up/down + duration | Gateway diagnostics | Hybrid connectivity health |
| **ExpressRoute Utilization** | % of circuit bandwidth | ExpressRoute metrics | Private connectivity capacity planning |
| **SNAT Port Utilization** | % of allocated ports | Load balancer metrics | Connection exhaustion risk |
| **BGP Route Count** | routes per peer | Route Server, ER gateway metrics | Routing stability, prefix leak detection |

---

## CloudWatch Dashboards

### Widget Types for Network Monitoring

- **Line widgets**: Time-series metrics (NetworkIn/Out, TunnelDataIn/Out, NAT Gateway bytes).
- **Number widgets**: Single-stat values (active VPN tunnels, healthy targets in target group).
- **Stacked area**: Aggregate bandwidth across multiple ENIs or Transit Gateway attachments.
- **Alarm status widgets**: Grid of alarm states (green/yellow/red) for at-a-glance health.
- **Log widgets**: CloudWatch Insights query results embedded directly in dashboards.

### Cross-Account Dashboards

Use CloudWatch cross-account observability to consolidate network metrics from multiple AWS accounts into a single dashboard. The monitoring account aggregates metrics from source accounts via organization-level sharing.

### Math Expressions

Compute derived metrics inline:

```
# Packet loss percentage
METRICS("m1") = NetworkPacketsIn
METRICS("m2") = NetworkPacketsOut
e1 = (1 - m2/m1) * 100   # Approximate packet loss
```

---

## Grafana Integration

Grafana provides a unified dashboarding layer across all three clouds with native data source plugins.

### Azure Monitor Data Source

- Supports Azure Monitor metrics, Log Analytics (KQL), and Azure Resource Graph queries.
- Configure with service principal or managed identity authentication.
- Use template variables bound to Azure subscriptions, resource groups, and resource names for dynamic filtering.

### CloudWatch Data Source

- Native integration with all CloudWatch namespaces (AWS/VPC, AWS/TransitGateway, AWS/NATGateway, AWS/VPN).
- Supports math expressions and multi-region querying.
- Configure with IAM access keys or assume-role for cross-account access.

### GCP Cloud Monitoring Data Source

- Query GCP monitoring metrics using MQL (Monitoring Query Language) or PromQL via the Prometheus-compatible API.
- Authenticate with service account JSON key or Workload Identity Federation.
- Access VPC flow log metrics, Cloud NAT metrics, Cloud VPN metrics, and Interconnect metrics.

### Multi-Cloud Dashboard Layout

Design a single Grafana dashboard with rows per cloud:

1. **Row 1 — Overview**: Aggregate health score across all clouds using stat panels (green/yellow/red).
2. **Row 2 — Azure**: ExpressRoute utilization, VPN tunnel status, VNet flow-log denied-flow trends (legacy NSG denied-flow panels only where still deployed), Application Gateway latency.
3. **Row 3 — AWS**: Transit Gateway throughput, NAT Gateway metrics, VPN tunnel status, Direct Connect utilization.
4. **Row 4 — GCP**: Cloud VPN throughput, Interconnect utilization, Cloud NAT port allocation, firewall rule hit counts.
5. **Row 5 — Cross-Cloud Links**: Latency between clouds (measured via synthetic probes), bandwidth utilization on interconnects.

---

## Dashboard Design Best Practices

### Golden Signals Framework

Structure dashboards around the four golden signals adapted for network monitoring:

1. **Latency**: P50, P95, P99 round-trip times between critical endpoints.
2. **Traffic**: Throughput in bps, flow counts, packet rates.
3. **Errors**: Packet loss, denied flows, connection resets, DNS failures.
4. **Saturation**: Bandwidth utilization %, SNAT port usage, connection table fullness.

### Drill-Down Hierarchy

Design three dashboard levels:

- **L1 — Executive Overview**: Traffic light indicators for each cloud and region. Total throughput, aggregate latency, active incidents.
- **L2 — Service Detail**: Per-VNet/VPC metrics, per-gateway status, per-firewall throughput. Linked from L1 panels.
- **L3 — Resource Deep Dive**: Individual VM, ENI, or subnet flow data. Packet captures, connection traces. Linked from L2 panels.

### Time Range Best Practices

- Default time range: Last 6 hours for operational dashboards, last 24 hours for review dashboards.
- Always include a time range selector to let users zoom in/out.
- Add annotations for deployment events, maintenance windows, and known incidents to correlate metrics with change events.
- Refresh interval: 30 seconds for real-time operations, 5 minutes for trend monitoring.

**Analysis only — verify against vendor documentation before applying.**

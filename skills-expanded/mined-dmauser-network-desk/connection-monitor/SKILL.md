# Connection Monitor

## Skill: `nmon_connection_monitor`

Deploy continuous endpoint reachability and latency testing to detect network degradation, path failures, and performance bottlenecks. This skill covers Azure Connection Monitor, AWS Reachability Analyzer, and synthetic monitoring patterns for multi-cloud environments.

---

## Azure Connection Monitor

Connection Monitor is a component of Azure Network Watcher that provides continuous network connectivity testing between source and destination endpoints. It replaces the legacy Connection Monitor (classic) and Network Performance Monitor (NPM).

### Core Concepts

- **Test Group**: A logical container for sources, destinations, and test configurations. Each test group defines one or more source-destination pairs tested with a specific protocol and frequency.
- **Source Endpoints**: Azure VMs (requires the Network Watcher Agent extension), Azure Arc-enabled machines, or on-premises machines with the Azure Monitor agent.
- **Destination Endpoints**: Any Azure VM, on-premises machine, external URL/IP, or Azure service endpoint (e.g., storage accounts, SQL databases).

### Test Configurations

| Protocol | Checks | Use Case |
|---|---|---|
| **TCP** | Port reachability, round-trip latency, packet loss | Database connectivity, API endpoint testing |
| **ICMP** | Ping reachability, round-trip latency, packet loss | General host reachability, VPN tunnel health |
| **HTTP/HTTPS** | Status code, response time, SSL certificate validity | Web application health, CDN endpoint testing |

### Check Frequency

Configurable from 30 seconds to 24 hours. Recommended intervals:

- **30 seconds**: Critical production paths (VPN tunnels, database connections).
- **60 seconds**: Standard application connectivity.
- **300 seconds (5 min)**: Low-priority or non-production monitoring.

### Create Connection Monitor (CLI)

```bash
# Install Network Watcher Agent extension on source VM
az vm extension set \
  --resource-group MyRG \
  --vm-name SourceVM \
  --name NetworkWatcherAgentWindows \
  --publisher Microsoft.Azure.NetworkWatcher

# Create connection monitor with TCP test
az network watcher connection-monitor create \
  --name "WebApp-to-Database" \
  --resource-group NetworkWatcherRG \
  --location eastus \
  --test-group-name "PrimaryDB" \
  --endpoint-source-name "WebAppVM" \
  --endpoint-source-resource-id /subscriptions/<sub>/resourceGroups/MyRG/providers/Microsoft.Compute/virtualMachines/WebAppVM \
  --endpoint-dest-name "SQLDB" \
  --endpoint-dest-address 10.1.2.4 \
  --test-config-name "TCP-1433" \
  --protocol Tcp \
  --tcp-port 1433 \
  --test-config-frequency 30 \
  --test-config-threshold-failed-percent 10 \
  --test-config-threshold-round-trip-time 100
```

### Threshold-Based Alerts

Connection Monitor integrates with Azure Monitor Alerts. Configure alerts based on:

- **Failed check percentage**: Alert when >X% of checks fail within a time window. Typical threshold: 10% over 5 minutes for production.
- **Round-trip time (RTT)**: Alert when average RTT exceeds a threshold. Set based on baseline (e.g., alert when P95 latency > 50ms for an intra-region path).

```bash
az monitor metrics alert create \
  --name "HighLatency-WebApp-DB" \
  --resource-group MyRG \
  --scopes /subscriptions/<sub>/resourceGroups/NetworkWatcherRG/providers/Microsoft.Network/networkWatchers/NetworkWatcher_eastus/connectionMonitors/WebApp-to-Database \
  --condition "avg RoundTripTimeMs > 100" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --action-group /subscriptions/<sub>/resourceGroups/MyRG/providers/Microsoft.Insights/actionGroups/NetworkOps \
  --severity 2
```

---

## AWS Reachability Analyzer

Reachability Analyzer performs static path analysis across AWS network configurations to determine whether a source can reach a destination. It evaluates security groups, NACLs, route tables, VPC peering, Transit Gateway routes, and VPC endpoint policies.

### Create and Run Analysis

```bash
# Create network insights path
aws ec2 create-network-insights-path \
  --source eni-0abc123def456 \
  --destination eni-0def789abc123 \
  --protocol TCP \
  --destination-port 443

# Start analysis
aws ec2 start-network-insights-analysis \
  --network-insights-path-id nip-abc123

# Get results
aws ec2 describe-network-insights-analyses \
  --network-insights-analysis-ids nia-xyz789
```

The analysis result includes the full path trace showing each hop (ENI, subnet, route table, security group, NACL, gateway) and identifies the exact component blocking traffic if the path is not reachable.

### Continuous Monitoring

Schedule periodic Reachability Analyzer runs using EventBridge rules with Lambda triggers. This provides ongoing validation that network paths remain open after infrastructure changes, security group modifications, or route table updates.

---

## Synthetic Monitoring Patterns

### Multi-Hop Path Visibility

For complex network paths (on-premises → VPN → hub VNet → peered spoke VNet → application), deploy monitoring agents at intermediate hops to isolate latency contributions from each segment:

1. **VPN Gateway hop**: Monitor tunnel latency and throughput independently.
2. **Hub firewall hop**: Measure firewall inspection latency by testing before and after the NVA.
3. **Peering hop**: Compare intra-VNet vs cross-peering latency to detect peering bandwidth throttling.
4. **Application hop**: End-to-end HTTP check to capture application-level response time.

### Bottleneck Identification

When end-to-end latency increases, use hop-by-hop data to pinpoint which segment degraded. Common bottlenecks:

- **VPN tunnel congestion**: Bandwidth exceeding tunnel capacity (typically 1.25 Gbps per tunnel in Azure, 1.25 Gbps per tunnel in AWS).
- **Firewall overload**: NVA CPU saturation adding processing latency.
- **Peering bandwidth limits**: Azure VNet peering has account-level bandwidth limits tied to VM SKU.
- **Cross-region latency**: Inter-region paths add 10-80ms depending on geographic distance.

---

## Integration with Alerting Systems

### Azure Connection Monitor → Azure Monitor → Action Group

Connection Monitor metrics flow into Azure Monitor, where metric alert rules trigger action groups. Action groups can invoke email, SMS, voice call, push notification, webhook, Logic App, Azure Function, ITSM connector, or Event Hub.

### AWS Reachability Analyzer → EventBridge → SNS/Lambda

Schedule periodic path analyses and route failure events through EventBridge rules. Target SNS topics for notifications or Lambda functions for automated remediation (e.g., switching to a backup VPN tunnel).

### Cross-Cloud Unified Alerting

Route all connection monitoring alerts through a single incident management platform:

1. Azure Connection Monitor → webhook → PagerDuty/Opsgenie
2. AWS Reachability Analyzer → SNS → Lambda → PagerDuty/Opsgenie
3. GCP Connectivity Tests → Cloud Monitoring → Pub/Sub → PagerDuty/Opsgenie

This ensures a single pane of glass for on-call engineers regardless of which cloud reported the connectivity issue.

**Analysis only — verify against vendor documentation before applying.**

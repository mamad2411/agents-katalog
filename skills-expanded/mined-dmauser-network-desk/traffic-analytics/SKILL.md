# Traffic Analytics

## Skill: `nmon_traffic_analytics`

Analyze network flow data to extract actionable insights on traffic patterns, security threats, and capacity utilization. This skill covers Azure Traffic Analytics, AWS Athena-based flow log analysis, GCP Network Intelligence Center, and cross-cloud analysis patterns.

---

## Azure Traffic Analytics

Traffic Analytics analyzes Azure Network Watcher flow logs and produces aggregated insights in a Log Analytics workspace. Prefer VNet flow logs for new deployments; use NSG flow logs only as legacy/migration inputs because new NSG flow log creation is blocked after 2025-06-30 and the feature retires on 2027-09-30. It correlates flow data with threat intelligence feeds, Azure resource metadata, and geographic IP databases.

### Processing Interval

- **10-minute interval**: Near-real-time insights. Recommended for security-sensitive environments. Produces more granular data but at higher processing cost (~$1.50/GB).
- **60-minute interval**: Standard for operational monitoring. Lower processing cost (~$0.75/GB). Sufficient for capacity planning and trend analysis.

Configure via CLI:

```bash
az network watcher flow-log update \
  --name MyFlowLog \
  --resource-group MyRG \
  --interval 10 \
  --traffic-analytics true \
  --workspace <log-analytics-resource-id>
```

### Log Analytics Workspace Requirement

Traffic Analytics requires a Log Analytics workspace in a supported region. Existing examples often use the legacy `AzureNetworkAnalytics_CL` custom log table; validate current table and field names in the target workspace, especially when using VNet flow logs. Ensure the workspace retention period aligns with your compliance requirements (30-730 days).

### Insight Categories

Traffic Analytics surfaces insights across these categories:

- **Geographic Distribution**: Visualizes traffic flows by source/destination country and region. Highlights unexpected geographic origins that may indicate compromise.
- **Malicious Traffic**: Correlates flow data with Microsoft Threat Intelligence to flag known malicious IPs, botnets, and C2 servers communicating with your resources.
- **Top Talkers**: Identifies VMs and subnets generating the most traffic by byte count or flow count. Critical for capacity planning and cost attribution.
- **Port Utilization**: Shows which ports carry the most traffic. Detects unexpected port usage that may indicate lateral movement or data exfiltration.
- **Denied Flows**: Aggregates flow-log deny events (NSG semantics where legacy NSG flow logs are still deployed) to identify misconfigured rules, brute-force attempts, or reconnaissance scanning.

### KQL Queries (schema examples; validate current VNet flow-log / Traffic Analytics fields)

**Top talkers by byte count (last 24 hours):**

```kql
AzureNetworkAnalytics_CL
| where TimeGenerated > ago(24h)
| where SubType_s == "FlowLog"
| summarize TotalBytes = sum(InboundBytes_d + OutboundBytes_d) by SrcIP_s, DestIP_s
| top 20 by TotalBytes desc
| project SrcIP_s, DestIP_s, TotalBytesMB = round(TotalBytes / 1048576, 2)
```

**Malicious IP communications:**

```kql
AzureNetworkAnalytics_CL
| where TimeGenerated > ago(7d)
| where SubType_s == "FlowLog"
| where MaliciousIP_s != ""
| summarize FlowCount = count(), TotalBytes = sum(InboundBytes_d) by MaliciousIP_s, SrcIP_s, DestPort_d
| order by FlowCount desc
```

**Geographic traffic distribution:**

```kql
AzureNetworkAnalytics_CL
| where TimeGenerated > ago(24h)
| where SubType_s == "FlowLog" and FlowType_s == "ExternalPublic"
| summarize FlowCount = count(), TotalBytesMB = round(sum(InboundBytes_d + OutboundBytes_d) / 1048576, 2)
    by SrcCountry = SrcPublicIPs_s, DestCountry = DestPublicIPs_s
| order by TotalBytesMB desc
```

**Port utilization analysis:**

```kql
AzureNetworkAnalytics_CL
| where TimeGenerated > ago(24h)
| where SubType_s == "FlowLog"
| summarize FlowCount = count(), TotalBytesMB = round(sum(InboundBytes_d + OutboundBytes_d) / 1048576, 2)
    by DestPort_d, L7Protocol_s
| order by TotalBytesMB desc
| take 25
```

**Denied flow spike detection:**

```kql
AzureNetworkAnalytics_CL
| where TimeGenerated > ago(1h)
| where SubType_s == "FlowLog" and FlowStatus_s == "D"
| summarize DeniedFlows = count() by bin(TimeGenerated, 5m), NSGRule_s
| where DeniedFlows > 100
| order by DeniedFlows desc
```

---

## AWS Traffic Mirroring and Athena Analysis

### Traffic Mirroring

AWS Traffic Mirroring provides full packet capture for deep inspection. Mirror sessions copy traffic from source ENIs to a Network Load Balancer target where IDS/IPS or custom analysis tools run.

```bash
# Create mirror target (NLB)
aws ec2 create-traffic-mirror-target \
  --network-load-balancer-arn arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/net/my-nlb/abc123 \
  --description "IDS mirror target"

# Create mirror filter
aws ec2 create-traffic-mirror-filter \
  --description "Capture HTTP and HTTPS"

# Add filter rule for port 443
aws ec2 create-traffic-mirror-filter-rule \
  --traffic-mirror-filter-id tmf-abc123 \
  --traffic-direction ingress \
  --rule-number 100 \
  --rule-action accept \
  --destination-port-range FromPort=443,ToPort=443 \
  --protocol 6
```

### Athena Queries for VPC Flow Logs

Create an Athena table over S3-stored flow logs for SQL-based analysis:

```sql
-- Top talkers by bytes transferred
SELECT srcaddr, dstaddr, SUM(bytes) AS total_bytes, SUM(packets) AS total_packets
FROM vpc_flow_logs
WHERE start >= cast(now() - interval '24' hour AS bigint)
GROUP BY srcaddr, dstaddr
ORDER BY total_bytes DESC
LIMIT 20;

-- Rejected connections by source IP
SELECT srcaddr, dstaddr, dstport, COUNT(*) AS reject_count
FROM vpc_flow_logs
WHERE action = 'REJECT'
  AND start >= cast(now() - interval '1' hour AS bigint)
GROUP BY srcaddr, dstaddr, dstport
ORDER BY reject_count DESC
LIMIT 50;
```

---

## GCP Network Intelligence Center

### Connectivity Tests

Synthetic path analysis that traces the logical route between a source and destination, evaluating every firewall rule, route, and forwarding rule along the path.

```bash
gcloud network-management connectivity-tests create my-test \
  --source-instance=projects/my-project/zones/us-central1-a/instances/vm-source \
  --destination-instance=projects/my-project/zones/us-central1-b/instances/vm-dest \
  --destination-port=443 \
  --protocol=TCP
```

### Network Topology

Real-time visualization of VPC networks, subnets, VM instances, load balancers, VPN tunnels, and Cloud Interconnect attachments. Displays traffic volume between entities using bandwidth-proportional edge widths.

### Performance Dashboard

Monitors packet loss and latency between Google Cloud zones and regions. Uses VM-to-VM probing to detect network degradation before it impacts applications. Data is available for the last 6 weeks with per-hour granularity.

### Firewall Insights

Analyzes firewall rule usage to identify shadowed rules (rules that are never matched because a higher-priority rule catches all traffic first), overly permissive rules, and deny-rule hit counts.

---

## Cross-Cloud Traffic Analysis Patterns

### Unified Schema Normalization

Map flow log fields from each cloud into a common schema:

| Common Field | Azure | AWS | GCP |
|---|---|---|---|
| Source IP | `SrcIP_s` | `srcaddr` | `connection.src_ip` |
| Destination IP | `DestIP_s` | `dstaddr` | `connection.dest_ip` |
| Source Port | `SrcPort_d` | `srcport` | `connection.src_port` |
| Destination Port | `DestPort_d` | `dstport` | `connection.dest_port` |
| Bytes | `InboundBytes_d` | `bytes` | `bytes_sent` |
| Action | `FlowStatus_s` (legacy TA example; validate current VNet flow-log schema) | `action` | `jsonPayload.disposition` |

### Aggregation Approach

Forward normalized logs to a centralized platform (Azure Sentinel, Splunk, Elastic, Datadog). Use consistent enrichment to tag each flow with cloud provider, region, application, and environment. Build cross-cloud dashboards that compare latency, throughput, and denied flow rates side by side.

### Inter-Cloud Traffic Monitoring

For workloads connected via cloud interconnects (ExpressRoute, Direct Connect, Cloud Interconnect) or VPN tunnels, correlate flow logs from both sides of the link to compute end-to-end latency, detect asymmetric routing, and measure bandwidth utilization against provisioned capacity.

**Analysis only — verify against vendor documentation before applying.**

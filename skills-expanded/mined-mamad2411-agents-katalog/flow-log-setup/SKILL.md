# Flow Log Setup

## Skill: `nmon_flow_log_setup`

Configure and enable network flow log collection across Azure, AWS, and GCP. This skill covers platform-specific enablement, destination selection, format configuration, and cost optimization for flow log telemetry.

---

## Azure VNet Flow Logs (default) and NSG Flow Logs (legacy)

Use **VNet flow logs** as the default Azure Network Watcher flow-log scope for new deployments. They capture IP traffic at the virtual network level and reduce per-NSG operational sprawl. **NSG flow logs are legacy/migration-only**: new NSG flow log creation is blocked after 2025-06-30, and existing NSG flow logs retire on 2027-09-30. Plan migration to VNet flow logs.

### Format Versions

- **Version 1**: Basic 5-tuple (source IP, destination IP, source port, destination port, protocol) with allow/deny disposition.
- **Version 2**: Adds per-flow byte counts, packet counts, TCP state (Begin, Continuing, End), and flow direction. Version 2 is required for Traffic Analytics integration.

### Enable VNet Flow Log (CLI)

```bash
az network watcher flow-log create \
  --resource-group MyRG \
  --vnet MyVNet \
  --name MyVNetFlowLog \
  --storage-account <storage-account-resource-id> \
  --enabled true \
  --log-version 2 \
  --retention 30 \
  --traffic-analytics true \
  --workspace <log-analytics-workspace-resource-id> \
  --interval 10
```

### Legacy NSG Flow Log (migration-only)

```bash
# Only for existing NSG-flow-log migration/maintenance scenarios; do not use for new deployments.
az network watcher flow-log create \
  --resource-group MyRG \
  --nsg MyNSG \
  --name MyLegacyNSGFlowLog \
  --storage-account /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<account> \
  --enabled true \
  --format JSON \
  --log-version 2 \
  --retention 90 \
  --traffic-analytics true \
  --workspace /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.OperationalInsights/workspaces/<workspace>
```

### Destinations

- **Storage Account**: Required as the primary destination. Flow logs are written as JSON blobs in a hierarchical folder structure (`resourceId=.../y=<year>/m=<month>/d=<day>/h=<hour>/m=<minute>/macAddress=<mac>/PT1H.json`).
- **Log Analytics Workspace**: Enables KQL-based querying and Traffic Analytics processing. Table and field names vary by flow-log generation and Traffic Analytics configuration; validate the current schema in the target workspace before writing alerts or dashboards.
- **Event Hub**: Enables streaming to third-party SIEM tools (Splunk, Datadog, Elastic) or custom processing pipelines via Azure Functions or Stream Analytics.

### Retention Policy

Set retention between 1 and 365 days on the storage account. For cost optimization, tier older logs to Cool or Archive storage using lifecycle management policies. Log Analytics workspace retention is configured separately (default 30 days, configurable up to 730 days).

---

## AWS VPC Flow Logs

AWS VPC Flow Logs capture traffic at three levels: **VPC** (all ENIs in the VPC), **Subnet** (all ENIs in the subnet), or **ENI** (individual network interface).

### Enable VPC Flow Log (CLI)

```bash
# To S3
aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids vpc-0abc123def456 \
  --traffic-type ALL \
  --log-destination-type s3 \
  --log-destination arn:aws:s3:::my-flow-logs-bucket \
  --max-aggregation-interval 60 \
  --log-format '${version} ${account-id} ${interface-id} ${srcaddr} ${dstaddr} ${srcport} ${dstport} ${protocol} ${packets} ${bytes} ${start} ${end} ${action} ${log-status} ${vpc-id} ${subnet-id} ${tcp-flags} ${type} ${pkt-srcaddr} ${pkt-dstaddr} ${flow-direction} ${traffic-path}'

# To CloudWatch Logs
aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids vpc-0abc123def456 \
  --traffic-type ALL \
  --log-destination-type cloud-watch-logs \
  --log-group-name /vpc/flow-logs \
  --deliver-logs-permission-arn arn:aws:iam::123456789012:role/FlowLogRole \
  --max-aggregation-interval 60
```

### Custom Log Format Fields

AWS supports 29+ fields. Key fields beyond the default format:

| Field | Description |
|---|---|
| `tcp-flags` | Bitmask of TCP flags (SYN=2, ACK=16, FIN=1) |
| `flow-direction` | `ingress` or `egress` relative to the ENI |
| `traffic-path` | Path through AWS network (1=through same VPC, 2=through gateway, etc.) |
| `pkt-srcaddr` | Original source IP before NAT translation |
| `pkt-dstaddr` | Original destination IP before NAT translation |
| `sublocation-type` | Type of sublocation (e.g., `wavelength` for Wavelength Zones) |

### Aggregation Interval

- **1 minute**: Higher granularity, more records, higher cost. Use for security analysis and troubleshooting.
- **10 minutes** (default): Lower volume, reduced cost. Suitable for general traffic analytics and capacity planning.

### Destinations

- **Amazon S3**: Most cost-effective for high-volume storage. Use with Athena for ad-hoc SQL queries. Partition by date for query performance.
- **CloudWatch Logs**: Enables CloudWatch Insights queries and metric filters. Higher per-GB cost than S3.
- **Kinesis Data Firehose**: Real-time streaming to S3, Redshift, OpenSearch, or third-party tools. Use when near-real-time analysis is required.

---

## GCP VPC Flow Logs

GCP VPC Flow Logs are enabled at the **subnet** level. Each subnet can independently have flow logging enabled or disabled.

### Enable Subnet Flow Logs (CLI)

```bash
# Enable with sampling rate and metadata
gcloud compute networks subnets update my-subnet \
  --region=us-central1 \
  --enable-flow-logs \
  --logging-aggregation-interval=interval-5-sec \
  --logging-flow-sampling=0.5 \
  --logging-metadata=include-all \
  --logging-filter-expr="src_ip == '10.0.0.1' || dest_ip == '10.0.0.1'"
```

### Sampling Rate

The `--logging-flow-sampling` parameter accepts a value from 0.0 to 1.0, controlling the fraction of flows captured:

- **1.0**: Capture all flows. Full visibility but highest cost and log volume.
- **0.5**: Capture 50% of flows. Good balance of visibility and cost for most workloads.
- **0.1**: Capture 10% of flows. Suitable for high-throughput environments where sampled data provides sufficient statistical accuracy.

### Metadata Annotations

GCP automatically annotates flow log records with rich metadata including GKE pod name, VM instance name, project ID, region, zone, and geographic information. This eliminates the need for post-processing enrichment.

### Aggregation Intervals

Available intervals: 5 seconds, 30 seconds, 1 minute, 5 minutes, 10 minutes, 15 minutes. Shorter intervals increase log volume and cost.

### Destinations

- **Cloud Logging**: Default destination. Supports Logs Explorer queries, log-based metrics, and log routing.
- **BigQuery**: Export via log sink for SQL-based analytics. Use partitioned tables for cost-efficient querying.
- **Pub/Sub**: Stream to custom consumers or third-party SIEM systems.

---

## Cost Considerations

### Azure

- VNet flow log storage (legacy NSG flow-log storage where still deployed): Standard blob storage rates (~$0.018/GB for Hot tier in East US).
- Log Analytics ingestion: ~$2.76/GB (pay-as-you-go). Use commitment tiers (100GB/day+) for 15-30% discount.
- Traffic Analytics processing: ~$1.50 per GB processed at 10-min interval, ~$0.75 at 60-min interval.

### AWS

- VPC Flow Logs to S3: Data transfer charges apply (~$0.023/GB for S3 Standard). No separate flow log charge.
- VPC Flow Logs to CloudWatch Logs: ~$0.50/GB ingestion + $0.03/GB storage per month.
- Athena queries: $5.00 per TB scanned. Use columnar formats (Parquet) and partitioning to reduce scan volume.

### GCP

- VPC Flow Logs: Charged at Cloud Logging rates (~$0.50/GB ingestion after 50GB free tier per project per month).
- BigQuery export: Storage at ~$0.02/GB/month (active), queries at $6.25/TB processed.
- Reducing sampling rate linearly reduces log volume and cost.

**Tip**: In all clouds, start with a lower sampling rate or longer aggregation interval, then increase granularity for specific subnets or security zones that require detailed visibility.

**Analysis only — verify against vendor documentation before applying.**

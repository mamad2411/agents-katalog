# Skill: Private Endpoint Design (`pl_endpoint_design`)

Design private endpoint architecture including subnet placement, IP planning, groupId/subresource selection, approval workflows, and multi-region strategies across Azure, AWS, and GCP.

---

## Subnet Strategy

### Dedicated vs Shared Subnet

| Approach | Pros | Cons | Recommendation |
|---|---|---|---|
| **Dedicated PE subnet** | Clean NSG rules, easy auditing, clear IP accounting | Consumes address space, more subnets to manage | **Recommended for production** |
| **Shared with workload** | Fewer subnets, simpler topology | Mixed NSG rules, harder to track PE IPs | Acceptable for dev/test |

### Subnet Sizing

**Azure Private Endpoints:**
- Each PE consumes **one private IP** from the subnet.
- A single resource can have multiple PEs (e.g., one for blob, one for table on the same storage account) — each consumes a separate IP.
- Plan for growth: if you expect 50 PEs today, size for 100+.

| Subnet Size | Usable IPs (Azure reserves 5) | PEs Supported |
|---|---|---|
| /28 | 11 | Small workload, <10 PEs |
| /26 | 59 | Medium workload, 20-50 PEs |
| /24 | 251 | Large workload, 100+ PEs |
| /22 | 1019 | Enterprise, centralized PE hub |

**AWS Interface Endpoints:**
- Each interface endpoint creates **one ENI per AZ** where it's deployed.
- If your endpoint spans 3 AZs, it consumes 3 IPs.
- Security groups are applied per-endpoint — use a dedicated subnet or carefully manage SGs.

**GCP Private Service Connect:**
- Each PSC endpoint consumes **one forwarding rule IP** from the subnet.
- Use a dedicated subnet for PSC endpoints for clean firewall rules.

### Placement Strategy

**Hub-spoke topology (Azure):**

```
Hub VNet (10.0.0.0/16)
├── GatewaySubnet (10.0.0.0/27)
├── AzureFirewallSubnet (10.0.1.0/26)
├── InboundDnsSubnet (10.0.2.0/28)
├── OutboundDnsSubnet (10.0.3.0/28)
└── PrivateEndpointSubnet (10.0.4.0/24) ← Centralized PEs

Spoke VNet 1 (10.1.0.0/16)
├── WorkloadSubnet (10.1.0.0/24)
└── (No PEs — uses hub PEs via peering + private DNS)

Spoke VNet 2 (10.2.0.0/16)
├── WorkloadSubnet (10.2.0.0/24)
└── LocalPESubnet (10.2.1.0/26) ← PEs for latency-sensitive workloads
```

**Centralized PEs (hub):**
- Single private DNS zone management.
- All traffic goes through hub (can inspect via firewall).
- Higher latency for spoke workloads (extra peering hop).

**Distributed PEs (spokes):**
- Lower latency — PE is in the same VNet as the workload.
- Requires private DNS zone links to every spoke VNet.
- More complex DNS management.

---

## GroupId / Subresource Selection (Azure)

When creating an Azure Private Endpoint, you specify a `groupId` (also called `subresource`) that determines which part of the PaaS service gets a private endpoint.

| Service | groupId | Private DNS Zone |
|---|---|---|
| Storage — Blob | `blob` | `privatelink.blob.core.windows.net` |
| Storage — File | `file` | `privatelink.file.core.windows.net` |
| Storage — Table | `table` | `privatelink.table.core.windows.net` |
| Storage — Queue | `queue` | `privatelink.queue.core.windows.net` |
| Storage — DFS (Data Lake) | `dfs` | `privatelink.dfs.core.windows.net` |
| Azure SQL | `sqlServer` | `privatelink.database.windows.net` |
| Cosmos DB — SQL | `Sql` | `privatelink.documents.azure.com` |
| Key Vault | `vault` | `privatelink.vaultcore.azure.net` |
| ACR | `registry` | `privatelink.azurecr.io` |
| Event Hubs | `namespace` | `privatelink.servicebus.windows.net` |
| App Configuration | `configurationStores` | `privatelink.azconfig.io` |
| Cognitive Services | `account` | `privatelink.cognitiveservices.azure.com` |

```bash
# Create PE for blob storage
az network private-endpoint create \
  --resource-group myRG \
  --name myBlobPE \
  --vnet-name myVNet \
  --subnet PrivateEndpointSubnet \
  --private-connection-resource-id /subscriptions/.../storageAccounts/myStorage \
  --group-id blob \
  --connection-name myBlobConnection

# Create PE for table storage (same storage account, different PE)
az network private-endpoint create \
  --resource-group myRG \
  --name myTablePE \
  --vnet-name myVNet \
  --subnet PrivateEndpointSubnet \
  --private-connection-resource-id /subscriptions/.../storageAccounts/myStorage \
  --group-id table \
  --connection-name myTableConnection
```

---

## AWS VPC Endpoint Creation

### Interface Endpoint

```bash
# Create interface endpoint for SQS in specific subnets
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-0123456789abcdef0 \
  --vpc-endpoint-type Interface \
  --service-name com.amazonaws.us-east-1.sqs \
  --subnet-ids subnet-aaa subnet-bbb subnet-ccc \
  --security-group-ids sg-0123456789abcdef0 \
  --private-dns-enabled

# List available services
aws ec2 describe-vpc-endpoint-services \
  --query 'ServiceNames[?contains(@, `sqs`)]'
```

### Gateway Endpoint (S3 / DynamoDB only)

```bash
# Create gateway endpoint for S3
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-0123456789abcdef0 \
  --vpc-endpoint-type Gateway \
  --service-name com.amazonaws.us-east-1.s3 \
  --route-table-ids rtb-0123456789abcdef0
```

**Gateway vs Interface for S3:**
- **Gateway**: Free, route-based, no ENI, works within VPC only.
- **Interface**: Costs money, ENI-based, supports cross-VPC/on-prem access via PrivateLink.

---

## GCP Private Service Connect Endpoint

```bash
# Reserve an IP address for PSC endpoint
gcloud compute addresses create my-psc-ip \
  --region=us-central1 \
  --subnet=psc-subnet \
  --addresses=10.3.0.10

# Create PSC endpoint for Google APIs (all-apis bundle)
gcloud compute forwarding-rules create my-psc-endpoint \
  --region=us-central1 \
  --network=my-vpc \
  --subnet=psc-subnet \
  --address=my-psc-ip \
  --target-google-apis-bundle=all-apis

# Create PSC endpoint for a published service
gcloud compute forwarding-rules create my-psc-producer \
  --region=us-central1 \
  --network=my-vpc \
  --subnet=psc-subnet \
  --address=my-psc-ip \
  --target-service-attachment=projects/producer-project/regions/us-central1/serviceAttachments/my-service
```

---

## Approval Workflows

| Cloud | Auto-Approval | Manual Approval | Cross-Tenant |
|---|---|---|---|
| **Azure** | Same subscription by default | Configurable via `privateLinkServiceConnectionState` | Supported — provider sets visibility + approval list by subscription ID |
| **AWS** | Configurable via `acceptance-required` flag | Default for cross-account PrivateLink | Supported — provider accepts/rejects connection requests |
| **GCP** | `ACCEPT_AUTOMATIC` on service attachment | `ACCEPT_MANUAL` with project allow-lists | Supported — producer sets accept policy |

```bash
# Azure — approve a pending PE connection
az network private-endpoint-connection approve \
  --resource-name myStorage \
  --resource-group myRG \
  --type Microsoft.Storage/storageAccounts \
  --name myPEConnection \
  --description "Approved by network team"

# AWS — accept VPC endpoint connection
aws ec2 accept-vpc-endpoint-connections \
  --service-id vpce-svc-0123456789abcdef0 \
  --vpc-endpoint-ids vpce-0123456789abcdef0

# GCP — not needed if ACCEPT_AUTOMATIC; for manual:
gcloud compute service-attachments update my-service \
  --region=us-central1 \
  --consumer-accept-list=consumer-project-id=10
```

---

## Common PE Design Mistakes

1. **Undersized PE subnet** — running out of IPs when adding new PEs. Always size for 2× current needs.
2. **Missing groupId** — creating a PE for `blob` but needing `table` and `queue` too. One PE per groupId.
3. **No automation** — manually creating PEs and DNS records doesn't scale. Use Terraform/Bicep + Azure Policy.
4. **Forgetting multi-region** — PEs are regional. Cross-region workloads need PEs in each region or use VNet peering.
5. **Not disabling public access** — PE alone doesn't block public access. Set `publicNetworkAccess: Disabled` separately.

**Analysis only — verify against vendor documentation before applying.**

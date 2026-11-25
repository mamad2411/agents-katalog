# Skill: Private Endpoint DNS Integration (`pl_dns_integration`)

Configure DNS resolution for private endpoints so that PaaS FQDNs resolve to private IPs instead of public IPs. Covers Azure Private DNS zones, `privatelink.*` zone naming, VNet linking strategy, custom DNS vs Azure-provided DNS, AWS private DNS for VPC endpoints, and GCP PSC DNS.

**DNS is the #1 cause of private endpoint failures.** If DNS is wrong, connectivity will not work — even if the private endpoint is healthy and the network path is correct.

---

## How Private Endpoint DNS Works (Azure)

When you create a private endpoint for a storage account `mystorageaccount`:

**Before PE:**
```
mystorageaccount.blob.core.windows.net
  → CNAME → mystorageaccount.blob.core.windows.net (public IP: 52.239.x.x)
```

**After PE (with correct DNS):**
```
mystorageaccount.blob.core.windows.net
  → CNAME → mystorageaccount.privatelink.blob.core.windows.net
  → A → 10.0.1.4 (private IP from PE subnet)
```

The CNAME to `privatelink.*` is automatically added by Azure when the PE is created. But the **A record in the private DNS zone** must exist for the final resolution to the private IP.

---

## Azure Private DNS Zone Configuration

### Required Zones

Each PaaS service type requires its own private DNS zone. Common zones (non-exhaustive):

```bash
# Create all common privatelink zones
ZONES=(
  "privatelink.blob.core.windows.net"
  "privatelink.file.core.windows.net"
  "privatelink.queue.core.windows.net"
  "privatelink.table.core.windows.net"
  "privatelink.dfs.core.windows.net"
  "privatelink.database.windows.net"
  "privatelink.documents.azure.com"
  "privatelink.mongo.cosmos.azure.com"
  "privatelink.vaultcore.azure.net"
  "privatelink.azurecr.io"
  "privatelink.servicebus.windows.net"
  "privatelink.azconfig.io"
  "privatelink.azurewebsites.net"
  "privatelink.cognitiveservices.azure.com"
  "privatelink.openai.azure.com"
)

for zone in "${ZONES[@]}"; do
  az network private-dns zone create --resource-group dns-rg --name "$zone"
done
```

### VNet Linking Strategy

Every VNet that needs to resolve privatelink names must be linked to the corresponding private DNS zone.

```bash
# Link zone to VNet (resolution only — no auto-registration)
az network private-dns link vnet create \
  --resource-group dns-rg \
  --zone-name privatelink.blob.core.windows.net \
  --name hubVNetLink \
  --virtual-network /subscriptions/.../virtualNetworks/hubVNet \
  --registration-enabled false

# Link spoke VNets too
az network private-dns link vnet create \
  --resource-group dns-rg \
  --zone-name privatelink.blob.core.windows.net \
  --name spoke1Link \
  --virtual-network /subscriptions/.../virtualNetworks/spoke1VNet \
  --registration-enabled false
```

**Important:** Set `--registration-enabled false` for privatelink zones. Auto-registration is for VM A records, not PE records.

### A Record Management

When a PE is created, the A record in the private DNS zone can be:

1. **Auto-created** — if you enable DNS integration during PE creation (`--private-dns-zone-group`):
   ```bash
   az network private-endpoint dns-zone-group create \
     --resource-group myRG \
     --endpoint-name myBlobPE \
     --name myZoneGroup \
     --private-dns-zone /subscriptions/.../privateDnsZones/privatelink.blob.core.windows.net \
     --zone-name blob
   ```

2. **Auto-created via Azure Policy** — deploy the `Deploy-DNSPE-*` built-in policies to automatically create DNS zone groups when PEs are provisioned in any subscription.

3. **Manually created** — for custom DNS scenarios:
   ```bash
   az network private-dns record-set a add-record \
     --resource-group dns-rg \
     --zone-name privatelink.blob.core.windows.net \
     --record-set-name mystorageaccount \
     --ipv4-address 10.0.1.4
   ```

---

## Hub-Spoke DNS Architecture for Private Endpoints

```
Hub VNet (10.0.0.0/16)
├── DNS Private Resolver (inbound: 10.0.2.4, outbound: 10.0.3.4)
├── Private DNS Zones:
│   ├── privatelink.blob.core.windows.net (linked to hub + all spokes)
│   ├── privatelink.database.windows.net (linked to hub + all spokes)
│   └── ... (all other privatelink zones)
└── PE Subnet (10.0.4.0/24) — centralized PEs

Spoke 1 VNet (10.1.0.0/16) — linked to all privatelink zones
Spoke 2 VNet (10.2.0.0/16) — linked to all privatelink zones

On-Premises DNS
├── Conditional forwarder: privatelink.blob.core.windows.net → 10.0.2.4 (inbound EP)
├── Conditional forwarder: privatelink.database.windows.net → 10.0.2.4
└── ... (all privatelink zones)
```

**Key rules:**
1. **Central DNS zones** in hub or shared-services subscription.
2. **Link every VNet** to every relevant privatelink zone.
3. **DNS Private Resolver inbound endpoint** for on-prem resolution.
4. **On-prem conditional forwarders** for every `privatelink.*` zone used.

---

## Custom DNS Server Scenarios

If VNets use a **custom DNS server** (e.g., AD domain controllers, BIND) instead of Azure-provided DNS:

1. The custom DNS server must forward `privatelink.*` queries to **168.63.129.16** (Azure DNS).
2. The custom DNS server's VNet must be linked to the private DNS zones.
3. If the custom DNS is on-premises (not in Azure), it must forward to the **DNS Private Resolver inbound endpoint**.

```powershell
# On custom DNS server (Windows DNS / AD DC) — forward privatelink zones to Azure DNS
Add-DnsServerConditionalForwarderZone -Name "privatelink.blob.core.windows.net" -MasterServers 168.63.129.16
Add-DnsServerConditionalForwarderZone -Name "privatelink.database.windows.net" -MasterServers 168.63.129.16
Add-DnsServerConditionalForwarderZone -Name "privatelink.vaultcore.azure.net" -MasterServers 168.63.129.16
```

---

## AWS VPC Endpoint DNS

### Private DNS Names

When you create an interface VPC endpoint with `--private-dns-enabled`:

- AWS creates a **private hosted zone** in your VPC that overrides the service's public DNS name.
- Example: `sqs.us-east-1.amazonaws.com` resolves to the endpoint's private IPs within the VPC.

**Requirements:**
- VPC must have `enableDnsSupport: true` and `enableDnsHostnames: true`.
- Only ONE endpoint per service per VPC can have private DNS enabled.

```bash
# Verify VPC DNS settings
aws ec2 describe-vpc-attribute --vpc-id vpc-... --attribute enableDnsSupport
aws ec2 describe-vpc-attribute --vpc-id vpc-... --attribute enableDnsHostnames

# Check endpoint DNS entries
aws ec2 describe-vpc-endpoints --vpc-endpoint-ids vpce-... \
  --query 'VpcEndpoints[].DnsEntries'
```

### Cross-Account / Cross-VPC DNS

For shared services or centralized endpoints:
- Use **Route 53 Private Hosted Zones** shared via RAM.
- Create alias records in the shared zone pointing to the endpoint's DNS name.

---

## GCP Private Service Connect DNS

### For Google APIs

```bash
# Create DNS entries for googleapis.com pointing to PSC endpoint IP
gcloud dns managed-zones create psc-googleapis \
  --dns-name="googleapis.com." \
  --visibility=private \
  --networks=my-vpc

gcloud dns record-sets create "*.googleapis.com." --zone=psc-googleapis \
  --type=CNAME --ttl=300 --rrdatas="googleapis.com."
gcloud dns record-sets create "googleapis.com." --zone=psc-googleapis \
  --type=A --ttl=300 --rrdatas="10.3.0.10"
```

### For Published Services

The producer provides the service's DNS name. Create A records in private DNS pointing to the PSC endpoint's IP.

---

## Validation Checklist

```bash
# 1. Verify CNAME chain exists
dig mystorageaccount.blob.core.windows.net CNAME +short
# Expected: mystorageaccount.privatelink.blob.core.windows.net

# 2. Verify A record resolves to private IP
dig mystorageaccount.privatelink.blob.core.windows.net A +short
# Expected: 10.0.1.4

# 3. Full resolution test
nslookup mystorageaccount.blob.core.windows.net
# Expected: Name: mystorageaccount.privatelink.blob.core.windows.net
#           Address: 10.0.1.4

# 4. If showing public IP, check from INSIDE the VNet (not from a machine outside Azure)
# 5. If still public, verify VNet link exists to the privatelink zone
```

---

## Common DNS Integration Mistakes

1. **Zone not linked to the workload VNet** — the privatelink zone exists but the VNet can't see it.
2. **Custom DNS not forwarding privatelink queries** — custom DNS resolves via public DNS, bypassing private zones.
3. **On-prem forwarders missing for privatelink zones** — on-prem clients get public IPs for PaaS services.
4. **Using auto-registration instead of DNS zone groups** — auto-registration doesn't create PE records; DNS zone groups do.
5. **Wrong zone name** — each PaaS service has a specific zone name. `privatelink.blob.core.windows.net` ≠ `privatelink.storage.core.windows.net`.

**Analysis only — verify against vendor documentation before applying.**

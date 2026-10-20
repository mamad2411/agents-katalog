# Skill: DNS Zone Design (`dns_zone_design`)

Design public and private DNS zone architectures across Azure, AWS, and GCP. Covers zone hierarchy, delegation strategy, split-horizon DNS, private zones for PaaS services, and DNSSEC.

---

## Zone Types and When to Use Them

| Zone Type | Resolves From | Managed By | Use Case |
|---|---|---|---|
| **Public zone** | Anywhere on the internet | Cloud DNS provider or registrar | Public websites, APIs, MX records |
| **Private zone** | Only from linked VNets/VPCs | Cloud DNS provider | Internal services, databases, PaaS private endpoints |
| **Split-horizon** | Public AND private (different answers) | Separate public + private zones with same name | Same FQDN resolves to public IP externally, private IP internally |
| **Delegated sub-zone** | Inherits from parent via NS delegation | Team or environment-specific | `dev.contoso.com` delegated to a dev team's DNS |

---

## Azure DNS Zone Architecture

### Public Zones

```bash
# Create public zone and verify delegation
az network dns zone create --resource-group myRG --name contoso.com

# Get NS records to configure at registrar
az network dns zone show --resource-group myRG --name contoso.com \
  --query 'nameServers' --output tsv

# Add a delegated sub-zone
az network dns record-set ns add-record --resource-group myRG \
  --zone-name contoso.com --record-set-name dev \
  --nsdname ns1-09.azure-dns.com
```

### Private Zones

```bash
# Create private zone and link to VNet
az network private-dns zone create --resource-group myRG --name internal.contoso.com

# Link to VNet with auto-registration (VMs auto-register A records)
az network private-dns link vnet create \
  --resource-group myRG \
  --zone-name internal.contoso.com \
  --name hubLink \
  --virtual-network /subscriptions/.../virtualNetworks/hubVNet \
  --registration-enabled true

# Link to spoke VNet without auto-registration (resolution only)
az network private-dns link vnet create \
  --resource-group myRG \
  --zone-name internal.contoso.com \
  --name spokeLink \
  --virtual-network /subscriptions/.../virtualNetworks/spokeVNet \
  --registration-enabled false
```

**Azure Private DNS rules:**
- A VNet can link to up to **1000 private zones**.
- Only **one VNet link with auto-registration** per zone (but the zone can be linked to multiple VNets for resolution).
- Auto-registration creates A records for VMs only — not for PaaS services or private endpoints.

### Private DNS Zones for PaaS Services (Private Endpoints)

Each Azure PaaS service with Private Endpoint support requires a specific private DNS zone. Common zones:

| Service | Private DNS Zone |
|---|---|
| Blob Storage | `privatelink.blob.core.windows.net` |
| Table Storage | `privatelink.table.core.windows.net` |
| Queue Storage | `privatelink.queue.core.windows.net` |
| File Storage | `privatelink.file.core.windows.net` |
| Azure SQL | `privatelink.database.windows.net` |
| Cosmos DB (SQL) | `privatelink.documents.azure.com` |
| Key Vault | `privatelink.vaultcore.azure.net` |
| ACR | `privatelink.azurecr.io` |
| Event Hubs | `privatelink.servicebus.windows.net` |
| AKS API Server | `privatelink.<region>.azmk8s.io` |

**Enterprise pattern**: Centralize all `privatelink.*` zones in a shared-services resource group. Link every VNet to these zones. Use Azure Policy (`Deploy-DNSPE-*`) to auto-create DNS records when private endpoints are provisioned.

### Split-Horizon DNS (Azure)

Create both a public zone (`contoso.com`) and a private zone (`contoso.com`). The private zone takes precedence for linked VNets. External clients resolve via the public zone.

```bash
# Public zone — resolves for internet clients
az network dns zone create --resource-group myRG --name contoso.com
az network dns record-set a add-record --zone-name contoso.com \
  --resource-group myRG --record-set-name app --ipv4-address 52.1.2.3

# Private zone — resolves for VNet clients
az network private-dns zone create --resource-group myRG --name contoso.com
az network private-dns record-set a add-record --zone-name contoso.com \
  --resource-group myRG --record-set-name app --ipv4-address 10.0.1.4
az network private-dns link vnet create --zone-name contoso.com \
  --resource-group myRG --name myLink --virtual-network myVNet --registration-enabled false
```

---

## AWS Route 53 Zone Design

### Public Hosted Zones

```bash
# Create public hosted zone
aws route53 create-hosted-zone --name contoso.com --caller-reference $(date +%s)

# Delegate sub-zone
aws route53 create-hosted-zone --name dev.contoso.com --caller-reference $(date +%s)
# Then add NS records in parent zone pointing to child zone's NS servers
```

### Private Hosted Zones

```bash
# Create private zone associated with VPC
aws route53 create-hosted-zone \
  --name internal.contoso.com \
  --caller-reference $(date +%s) \
  --vpc VPCRegion=us-east-1,VPCId=vpc-0123456789abcdef0 \
  --hosted-zone-config PrivateZone=true

# Associate additional VPCs (cross-account requires authorization)
aws route53 associate-vpc-with-hosted-zone \
  --hosted-zone-id Z0123456789 \
  --vpc VPCRegion=us-west-2,VPCId=vpc-abcdef0123456789
```

**AWS Private Hosted Zone rules:**
- Must associate with at least one VPC at creation.
- Cross-account VPC association requires `create-vpc-association-authorization` in the zone account and `associate-vpc-with-hosted-zone` in the VPC account.
- **Overlapping zones**: Route 53 uses the most specific zone. `api.internal.contoso.com` prefers a zone for `api.internal.contoso.com` over `internal.contoso.com`.

---

## GCP Cloud DNS Zone Design

```bash
# Public zone
gcloud dns managed-zones create my-public-zone \
  --dns-name="contoso.com." --description="Public zone" --visibility=public

# Private zone scoped to specific VPC networks
gcloud dns managed-zones create my-private-zone \
  --dns-name="internal.contoso.com." \
  --description="Private zone" \
  --visibility=private \
  --networks=projects/myproject/global/networks/my-vpc

# Response policy (override specific names)
gcloud dns response-policies create my-policy \
  --networks=my-vpc --description="Block malicious domains"
gcloud dns response-policies rules create block-evil \
  --response-policy=my-policy \
  --dns-name="evil.example.com." \
  --local-data='name=evil.example.com.,type=A,ttl=300,rrdatas=0.0.0.0'
```

**GCP DNS peering zones**: Delegate resolution to another VPC's DNS without full network peering:
```bash
gcloud dns managed-zones create peering-zone \
  --dns-name="shared.contoso.com." \
  --visibility=private \
  --networks=my-vpc \
  --target-network=shared-services-vpc
```

---

## Zone Delegation Strategy

For multi-team or multi-environment setups:

```
contoso.com (parent — platform team)
├── NS delegation → dev.contoso.com (dev team manages)
├── NS delegation → staging.contoso.com (platform team, restricted)
├── NS delegation → prod.contoso.com (platform team, strict change control)
└── NS delegation → internal.contoso.com (private zone — central team)
    ├── NS delegation → team-a.internal.contoso.com
    └── NS delegation → team-b.internal.contoso.com
```

**Best practices:**
1. Keep parent zone ownership with the platform/infra team.
2. Delegate sub-zones to teams that own the workloads.
3. Use Infrastructure as Code (Bicep, Terraform, CloudFormation) for zone and record management — no manual portal changes.
4. Enforce naming conventions: `<service>.<environment>.<team>.contoso.com`.

---

## DNSSEC Considerations

- **Azure Public DNS**: DNSSEC signing is supported. Enable via `az network dns dnssec-config create`, add the DS record at the registrar, and verify current guidance: https://learn.microsoft.com/azure/dns/dnssec.
- **Route 53**: Full DNSSEC signing support. Enable via `enable-hosted-zone-dnssec`. Manage KSK rotation.
- **GCP Cloud DNS**: DNSSEC signing supported. Enable via `gcloud dns managed-zones update --dnssec-state on`.
- **Private zones**: DNSSEC is not applicable — private zones are not exposed to the public DNS hierarchy.

**Analysis only — verify against vendor documentation before applying.**

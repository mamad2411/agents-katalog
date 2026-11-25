# Skill: DNS Resolver Design (`dns_resolver_design`)

Design DNS resolver topologies for hybrid and multi-cloud environments. Covers Azure DNS Private Resolver, AWS Route 53 Resolver, GCP Cloud DNS forwarding, conditional forwarding rules, and on-premises DNS integration.

---

## Why Resolvers Matter

Cloud-provided recursive DNS (Azure 168.63.129.16, AWS 169.254.169.253, GCP metadata server) resolves public names and cloud-native private zones. But it **cannot resolve** names hosted on-premises or in other clouds without explicit forwarding configuration. Resolvers bridge this gap.

| Direction | Problem | Solution |
|---|---|---|
| Cloud → On-prem | Azure VM needs to resolve `dc01.corp.contoso.com` hosted on AD DNS | Outbound resolver endpoint + forwarding rule |
| On-prem → Cloud | On-prem server needs to resolve `myvm.internal.contoso.com` in Azure private zone | Inbound resolver endpoint + on-prem conditional forwarder |
| Cloud → Cloud | AWS workload needs to resolve Azure private DNS zone | Cross-cloud forwarding via VPN/Interconnect + resolver endpoints |

---

## Azure DNS Private Resolver

The DNS Private Resolver is a managed service deployed into a VNet that provides inbound and outbound DNS endpoints.

### Architecture

```
On-premises DNS                    Azure VNet
┌──────────────┐    VPN/ER    ┌─────────────────────────────┐
│ AD DNS       │◄────────────►│ DNS Private Resolver         │
│ corp.contoso │              │ ┌─────────┐ ┌──────────────┐│
│   .com       │              │ │Inbound  │ │Outbound      ││
│              │──────────────►│ │Endpoint │ │Endpoint      ││
│              │  conditional │ │10.0.0.4 │ │10.0.1.4      ││
│              │  forwarder   │ └─────────┘ └──────────────┘│
└──────────────┘              │       │           │          │
                              │       ▼           ▼          │
                              │  Azure DNS    Forwarding     │
                              │  (168.63.     Ruleset        │
                              │   129.16)     corp.contoso   │
                              │               .com → on-prem │
                              └─────────────────────────────┘
```

### Deployment

```bash
# Create DNS Private Resolver
az dns-resolver create \
  --resource-group myRG \
  --name myResolver \
  --location eastus \
  --id /subscriptions/.../virtualNetworks/hubVNet

# Create inbound endpoint (on-prem → Azure resolution)
az dns-resolver inbound-endpoint create \
  --resource-group myRG \
  --dns-resolver-name myResolver \
  --name inbound-ep \
  --location eastus \
  --ip-configurations '[{"id":"/subscriptions/.../subnets/inbound-subnet","private-ip-allocation-method":"Dynamic"}]'

# Create outbound endpoint (Azure → on-prem forwarding)
az dns-resolver outbound-endpoint create \
  --resource-group myRG \
  --dns-resolver-name myResolver \
  --name outbound-ep \
  --location eastus \
  --id /subscriptions/.../subnets/outbound-subnet

# Create forwarding ruleset
az dns-resolver forwarding-ruleset create \
  --resource-group myRG \
  --name myRuleset \
  --location eastus \
  --outbound-endpoints '[{"id":"/subscriptions/.../outboundEndpoints/outbound-ep"}]'

# Add forwarding rule (Azure → on-prem for corp.contoso.com)
az dns-resolver forwarding-rule create \
  --resource-group myRG \
  --ruleset-name myRuleset \
  --name corpForward \
  --domain-name "corp.contoso.com." \
  --forwarding-rule-state Enabled \
  --target-dns-servers '[{"ip-address":"10.100.0.10","port":53},{"ip-address":"10.100.0.11","port":53}]'

# Link forwarding ruleset to VNets
az dns-resolver vnet-link create \
  --resource-group myRG \
  --ruleset-name myRuleset \
  --name hubLink \
  --id /subscriptions/.../virtualNetworks/hubVNet
```

**Azure Resolver subnet requirements:**
- Inbound and outbound endpoints require **dedicated subnets** (no other resources).
- Minimum subnet size: `/28` (16 IPs).
- Subnets must be delegated to `Microsoft.Network/dnsResolvers`.

### On-Prem Configuration

On your Active Directory DNS servers, add conditional forwarders pointing to the **inbound endpoint IP**:

```powershell
# PowerShell on AD DNS server
Add-DnsServerConditionalForwarderZone -Name "internal.contoso.com" -MasterServers 10.0.0.4
Add-DnsServerConditionalForwarderZone -Name "privatelink.blob.core.windows.net" -MasterServers 10.0.0.4
```

---

## AWS Route 53 Resolver

### Inbound Endpoints (On-Prem → VPC)

```bash
# Create inbound resolver endpoint
aws route53resolver create-resolver-endpoint \
  --creator-request-id inbound-$(date +%s) \
  --name on-prem-to-vpc \
  --security-group-ids sg-0123456789abcdef0 \
  --direction INBOUND \
  --ip-addresses SubnetId=subnet-aaa,Ip=10.0.1.10 SubnetId=subnet-bbb,Ip=10.0.2.10

# On-prem DNS: add conditional forwarder for internal.example.com → 10.0.1.10, 10.0.2.10
```

### Outbound Endpoints (VPC → On-Prem)

```bash
# Create outbound resolver endpoint
aws route53resolver create-resolver-endpoint \
  --creator-request-id outbound-$(date +%s) \
  --name vpc-to-onprem \
  --security-group-ids sg-0123456789abcdef0 \
  --direction OUTBOUND \
  --ip-addresses SubnetId=subnet-aaa SubnetId=subnet-bbb

# Create forwarding rule
aws route53resolver create-resolver-rule \
  --creator-request-id rule-$(date +%s) \
  --name corp-forwarding \
  --rule-type FORWARD \
  --domain-name corp.contoso.com \
  --resolver-endpoint-id rslvr-out-abcdef0123456789 \
  --target-ips Ip=10.100.0.10,Port=53 Ip=10.100.0.11,Port=53

# Associate rule with VPCs
aws route53resolver associate-resolver-rule \
  --resolver-rule-id rslvr-rr-abcdef0123456789 \
  --vpc-id vpc-0123456789abcdef0
```

**AWS Resolver key points:**
- Deploy endpoints across multiple AZs for high availability; verify current endpoint limits and HA guidance in AWS docs.
- Security groups on resolver endpoints must allow **TCP and UDP port 53** inbound/outbound.
- Use **Route 53 Resolver DNS Firewall** to filter/block queries to malicious domains.
- **RAM (Resource Access Manager)** can share resolver rules across accounts, but Route 53 Profiles may be a better fit for standardized multi-account DNS controls.

### Route 53 Profiles

Route 53 Profiles bundle DNS settings such as private hosted zone associations, Resolver rules, and DNS Firewall rule groups for VPCs in a Region. Use Profiles when many accounts/VPCs need the same DNS baseline; use one-off RAM-shared Resolver rules only for narrow exceptions or when Profiles are not available for the required resource type.

Operational points:
- Profiles are regional; plan one profile per Region or environment boundary.
- Share profiles across accounts with AWS RAM, then associate target VPCs.
- Establish precedence rules for local VPC associations versus profile-provided rules to avoid conflicting or shadowed DNS behavior.
- Verify current supported resources, conflict behavior, and quotas: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/profiles.html.

---

## GCP Cloud DNS Forwarding

### Forwarding Zones (VPC → On-Prem)

```bash
# Create forwarding zone to reach on-prem DNS
gcloud dns managed-zones create onprem-forward \
  --dns-name="corp.contoso.com." \
  --description="Forward to on-prem DNS" \
  --visibility=private \
  --networks=my-vpc \
  --forwarding-targets="10.100.0.10,10.100.0.11"
```

### DNS Inbound Policy (On-Prem → VPC)

```bash
# Enable inbound DNS forwarding on VPC
gcloud dns policies create allow-inbound \
  --networks=my-vpc \
  --enable-inbound-forwarding \
  --description="Allow on-prem to query GCP DNS"

# Get the inbound forwarder IPs (dynamically assigned from VPC subnets)
gcloud compute addresses list --filter="purpose=DNS_RESOLVER"
```

On-prem DNS servers then forward queries for GCP-hosted zones to these IPs.

### DNS Peering (Cross-VPC without Forwarding)

```bash
# Delegate resolution of shared.contoso.com to shared-services VPC
gcloud dns managed-zones create peer-to-shared \
  --dns-name="shared.contoso.com." \
  --visibility=private \
  --networks=my-vpc \
  --target-network=projects/shared-project/global/networks/shared-vpc
```

---

## Multi-Cloud Resolver Design

For environments spanning Azure + AWS (or Azure + GCP):

```
                    VPN / ExpressRoute / Interconnect
Azure Hub VNet ◄──────────────────────────────────► AWS VPC
┌──────────────┐                                    ┌──────────────┐
│DNS Private   │                                    │Route 53      │
│Resolver      │                                    │Resolver      │
│Outbound ─────┼──── forward aws.internal ──────────►Inbound      │
│              │                                    │              │
│Inbound ◄─────┼──── forward azure.internal ────────┤Outbound     │
└──────────────┘                                    └──────────────┘
```

1. Azure outbound forwarding rule: `aws.internal.com` → Route 53 Resolver inbound endpoint IPs (via VPN).
2. AWS Resolver forwarding rule: `azure.internal.com` → Azure DNS Private Resolver inbound endpoint IP (via VPN).
3. **Critical**: Ensure VPN/ER route tables allow DNS traffic (UDP/TCP 53) between resolver endpoints.

---

## Common Resolver Design Mistakes

1. **Forgetting to link forwarding rulesets to spoke VNets** — only the hub resolves on-prem names; spokes get NXDOMAIN.
2. **Single-AZ resolver endpoints** — no HA; DNS fails if that AZ goes down.
3. **On-prem conditional forwarders pointing at VNet default DNS (168.63.129.16)** — this IP is only reachable from within Azure VNets. Point at the inbound endpoint IP.
4. **Missing firewall rules for DNS** — allow UDP and TCP port 53 on NSGs, security groups, and on-prem firewalls.
5. **Circular forwarding** — Azure forwards to on-prem, on-prem forwards back to Azure for the same zone. Trace the chain end-to-end.
6. **Forgetting `privatelink.*` zone forwarding for on-prem** — on-prem clients resolving storage.blob.core.windows.net get the public IP unless you forward `privatelink.blob.core.windows.net` queries to Azure.

**Analysis only — verify against vendor documentation before applying.**

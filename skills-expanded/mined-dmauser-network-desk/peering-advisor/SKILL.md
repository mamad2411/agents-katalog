# Skill: VNet/VPC Peering Advisor

## Purpose

This skill provides expert guidance on configuring virtual network peering across Azure, AWS, and GCP. It covers peering setup, gateway transit, transitive routing limitations, common pitfalls, and a decision framework for choosing between peering, VPN, and Private Link/PrivateLink/Private Service Connect.

## Core Knowledge

### Azure VNet Peering

Azure supports two peering types:

**Regional (same-region) peering** — Traffic stays on the Azure backbone and has no bandwidth cap from peering itself. Peering data transfer pricing is region-dependent; verify current regional and global peering rates on the Azure Virtual Network pricing page: https://azure.microsoft.com/en-us/pricing/details/virtual-network/.

**Global peering** — Cross-region peering over the Microsoft backbone. Incurs inter-region data transfer charges. Same configuration as regional peering but with `--allow-forwarded-traffic` critical for transit scenarios.

```bash
# Create bidirectional peering
# Step 1: Hub → Spoke
az network vnet peering create \
  --name hub-to-spoke1 \
  --resource-group hub-rg \
  --vnet-name hub-vnet \
  --remote-vnet /subscriptions/<sub>/resourceGroups/spoke-rg/providers/Microsoft.Network/virtualNetworks/spoke1-vnet \
  --allow-vnet-access true \
  --allow-forwarded-traffic true \
  --allow-gateway-transit true

# Step 2: Spoke → Hub
az network vnet peering create \
  --name spoke1-to-hub \
  --resource-group spoke-rg \
  --vnet-name spoke1-vnet \
  --remote-vnet /subscriptions/<sub>/resourceGroups/hub-rg/providers/Microsoft.Network/virtualNetworks/hub-vnet \
  --allow-vnet-access true \
  --allow-forwarded-traffic true \
  --use-remote-gateways true
```

**Key settings explained:**

| Setting | On Hub Side | On Spoke Side | Effect |
|---------|------------|---------------|--------|
| `allow-vnet-access` | true | true | Enables IP connectivity between peered VNets |
| `allow-forwarded-traffic` | true | true | Allows traffic forwarded by an NVA (not originating from the VNet) to traverse the peering |
| `allow-gateway-transit` | true | — | Hub shares its VPN/ExpressRoute gateway with the spoke |
| `use-remote-gateways` | — | true | Spoke uses the hub's gateway for on-prem connectivity |

**Limits:** 500 peerings per VNet (hard limit). Global peering does not support Basic SKU load balancers.

### AWS VPC Peering

AWS VPC peering creates a direct network route between two VPCs. It is **always non-transitive** — if VPC-A peers with VPC-B and VPC-B peers with VPC-C, VPC-A cannot reach VPC-C through VPC-B.

```bash
# Create peering connection
aws ec2 create-vpc-peering-connection \
  --vpc-id vpc-aaa111 \
  --peer-vpc-id vpc-bbb222 \
  --peer-region us-west-2          # omit for same-region

# Accept peering (must be done from the peer VPC's account/region)
aws ec2 accept-vpc-peering-connection \
  --vpc-peering-connection-id pcx-abc123

# Add route in each VPC's route table
aws ec2 create-route \
  --route-table-id rtb-aaa \
  --destination-cidr-block 10.1.0.0/16 \
  --vpc-peering-connection-id pcx-abc123
```

**Critical restrictions:**
- **No overlapping CIDRs** — Peering will fail if either VPC's primary or secondary CIDR overlaps with the peer.
- **No transitive routing** — Use Transit Gateway for hub-spoke patterns.
- **No edge-to-edge routing** — Traffic from a VPN/Direct Connect attached to VPC-A cannot traverse a peering to reach VPC-B. Use TGW instead.
- **Limits:** 125 active peerings per VPC (can request increase to 500). 50 route table entries per route table referencing peering connections.

### GCP VPC Network Peering

GCP VPC peering operates differently from Azure and AWS:

- **Subnet routes are exchanged automatically** — When two VPC networks are peered, all subnet routes are immediately visible to both sides. No manual route table entries needed.
- **Custom routes require explicit import/export** — Static routes and routes learned from Cloud Router (BGP) are NOT exchanged by default. Enable `--export-custom-routes` and `--import-custom-routes` on peering creation.
- **Non-transitive** — Like AWS, GCP peering does not support transitive routing. VPC-A peered with VPC-B and VPC-B peered with VPC-C does not give VPC-A access to VPC-C.

```bash
# Create peering (both sides must create independently)
# Side A:
gcloud compute networks peerings create peer-a-to-b \
  --network vpc-a \
  --peer-network vpc-b \
  --peer-project project-b \
  --export-custom-routes \
  --import-custom-routes \
  --export-subnet-routes-with-public-ip

# Side B:
gcloud compute networks peerings create peer-b-to-a \
  --network vpc-b \
  --peer-network vpc-a \
  --peer-project project-a \
  --export-custom-routes \
  --import-custom-routes
```

**Limits:** 25 peerings per VPC network. Internal DNS resolution across peered networks is supported but requires configuring DNS peering zones.

## Common Pitfalls

### 1. Overlapping CIDRs

**Symptom:** Peering creation fails or routes are not effective.

**Prevention:**
```bash
# Azure: check for overlaps before peering
az network vnet list --query "[].{Name:name, Prefixes:addressSpace.addressPrefixes}" -o table

# AWS: check VPC CIDRs
aws ec2 describe-vpcs --query "Vpcs[].{Id:VpcId, CIDR:CidrBlock}" --output table
```

**Fix:** If CIDRs overlap, options are: (a) re-IP one VNet/VPC, (b) use NAT (Azure NAT Gateway with Virtual Network NAT), or (c) use Private Link / AWS PrivateLink instead of peering (service-level connectivity without full network peering).

### 2. Missing UDRs for Transit

**Symptom:** Spoke-to-spoke traffic fails even though both spokes peer with the hub.

**Root cause:** Peering is non-transitive. Without a UDR pointing spoke traffic to a hub NVA/firewall, packets are dropped.

**Fix:** Create UDRs on spoke subnets:
```bash
# Point all spoke traffic to hub firewall
az network route-table route create \
  --route-table-name spoke1-rt -g spoke1-rg \
  --name to-spokes --address-prefix 10.0.0.0/8 \
  --next-hop-type VirtualAppliance \
  --next-hop-ip-address 10.0.1.4
```

### 3. Peering Limits

**Provider limits:**
| Cloud | Limit | Increase? |
|-------|-------|-----------|
| Azure | 500 per VNet | No (hard limit) |
| AWS | 125 per VPC | Yes, up to 500 via support ticket |
| GCP | 25 per VPC network | Yes, via quota increase request |

If approaching limits, consolidate VNets/VPCs or switch to managed transit (Azure Virtual WAN, AWS Transit Gateway, GCP Network Connectivity Center).

### 4. Gateway Transit Misconfiguration (Azure)

**Symptom:** Spoke cannot reach on-premises through hub's VPN/ExpressRoute gateway.

**Checklist:**
- Hub peering: `allow-gateway-transit = true`
- Spoke peering: `use-remote-gateways = true`
- Hub must have an active VPN or ExpressRoute gateway deployed
- Spoke cannot have its own gateway deployed simultaneously

## Decision Guide: Peering vs VPN vs Private Link

| Criteria | VNet/VPC Peering | Site-to-Site VPN | Private Link / PrivateLink / PSC |
|----------|-----------------|------------------|----------------------------------|
| **Connectivity scope** | Full network-to-network | Full network-to-network (encrypted) | Single service endpoint |
| **Overlapping CIDRs** | ❌ Not supported | ⚠️ Requires NAT | ✅ Supported (no IP routing) |
| **Encryption** | Platform backbone (not user-encrypted) | IPsec encrypted | Platform backbone |
| **Bandwidth** | Line-rate (no cap) | Gateway SKU dependent (1.25–10 Gbps Azure) | Service-dependent |
| **Transitive routing** | ❌ (requires NVA/TGW) | ✅ (with BGP route propagation) | N/A |
| **Cost** | Peering data transfer charges vary by provider and region; verify current pricing | Gateway hour + data transfer | Per-hour + per-GB processed |
| **Best for** | Full network integration, hub-spoke | Encrypted cross-cloud or on-prem | Consuming a specific PaaS/SaaS service securely |

**Decision flow:**
1. Need full network-to-network connectivity with no CIDR overlap? → **Peering**
2. Need encrypted tunnel or cross-cloud connectivity? → **VPN**
3. Need access to a single service with overlapping CIDRs or minimal exposure? → **Private Link**
4. At scale (50+ networks)? → **Managed transit** (Virtual WAN, TGW, NCC)

## References

- Azure VNet peering: https://learn.microsoft.com/azure/virtual-network/virtual-network-peering-overview
- AWS VPC peering: https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html
- GCP VPC peering: https://cloud.google.com/vpc/docs/vpc-peering
- Azure subscription limits (networking): https://learn.microsoft.com/azure/azure-resource-manager/management/azure-subscription-service-limits#networking-limits
- Azure Virtual Network pricing: https://azure.microsoft.com/en-us/pricing/details/virtual-network/

**Analysis only — verify against vendor documentation before applying.**

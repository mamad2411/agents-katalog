# Skill: IP Address Space Planner

## Purpose

This skill provides deep expertise in IP address space planning for multi-cloud and hybrid environments. It covers CIDR allocation strategies, subnet sizing with cloud-specific reserved address rules, route summarization through supernetting, and overlap avoidance across on-premises, multi-cloud, and VPN-connected networks.

## Core Knowledge

### RFC 1918 Private Address Ranges

Select the appropriate range based on scale requirements:

| Range | CIDR | Total Addresses | Best For |
|-------|------|-----------------|----------|
| 10.0.0.0/8 | 10.0.0.0 – 10.255.255.255 | 16,777,216 | Enterprise-scale deployments with many VNets/VPCs, multi-region, hub-spoke. Provides maximum allocation flexibility. |
| 172.16.0.0/12 | 172.16.0.0 – 172.31.255.255 | 1,048,576 | Mid-size deployments or secondary range to complement a 10.x allocation. Often used for on-premises when 10.x is already allocated to cloud. |
| 192.168.0.0/16 | 192.168.0.0 – 192.168.255.255 | 65,536 | Small deployments, lab environments, or branch offices. Frequently conflicts with home networks and legacy on-prem — avoid for cloud production workloads connected via VPN. |

**Guidance:** For greenfield cloud deployments, start with `10.0.0.0/8` and allocate hierarchically. Reserve `172.16.0.0/12` as a secondary range for DMZ, management, or disaster recovery networks. Avoid `192.168.0.0/16` for anything connected via VPN — home routers and legacy networks frequently collide with this range.

### CIDR Allocation Strategies

#### Contiguous Allocation

Assign sequential blocks from a parent supernet. Enables route summarization and simplifies network operations.

```
Enterprise supernet:  10.0.0.0/8
├── Region US-East:   10.0.0.0/14   (262,144 addresses)
│   ├── Hub VNet:     10.0.0.0/16
│   ├── Spoke-Prod:   10.1.0.0/16
│   ├── Spoke-Dev:    10.2.0.0/16
│   └── Spoke-Test:   10.3.0.0/16
├── Region EU-West:   10.4.0.0/14
│   ├── Hub VNet:     10.4.0.0/16
│   ├── Spoke-Prod:   10.5.0.0/16
│   └── Spoke-Dev:    10.6.0.0/16
└── Region AP-South:  10.8.0.0/14
    └── ...
```

**Advantage:** A single route entry `10.0.0.0/14` summarizes all US-East networks at a peering boundary, reducing route table size and BGP advertisement count.

#### Distributed Allocation

Assign non-contiguous blocks when existing allocations prevent contiguous ranges. Common in brownfield environments with legacy on-prem ranges.

```
On-prem (legacy):     10.0.0.0/16, 10.5.0.0/16   ← already in use
Cloud US-East:        10.10.0.0/14                  ← skip over legacy
Cloud EU-West:        10.20.0.0/14                  ← non-contiguous
```

**Trade-off:** Loses route summarization capability. Each allocation requires its own route entry. Use only when contiguous space is exhausted.

### Cloud-Specific Reserved Addresses Per Subnet

When calculating usable IPs, subtract provider-reserved addresses from the total:

| Cloud | Reserved Count | Reserved Addresses (for x.x.x.0/24) | Usable IPs |
|-------|---------------|--------------------------------------|------------|
| **Azure** | 5 | .0 (network), .1 (gateway), .2 (DNS mapping), .3 (DNS mapping), .255 (broadcast) | 251 |
| **AWS** | 5 | .0 (network), .1 (VPC router), .2 (DNS server), .3 (future use), .255 (broadcast) | 251 |
| **GCP** | 4 | .0 (network), .1 (gateway), second-to-last (reserved), .255 (broadcast) | 252 |

**Critical for small subnets:** A /28 has 16 total addresses. After reserved IPs: Azure/AWS = 11 usable, GCP = 12 usable. A /29 has 8 total; Azure/AWS = 3 usable, GCP = 4 usable. Never go smaller than /29 in Azure/AWS or /29 in GCP — the overhead becomes prohibitive.

### Supernetting and Route Summarization

Supernetting combines multiple contiguous smaller networks into a single larger prefix for advertising across peerings, VPN tunnels, or BGP sessions. This reduces route table size and simplifies firewall rules.

**Example:** Four /24 subnets can be summarized:

```
10.1.0.0/24 + 10.1.1.0/24 + 10.1.2.0/24 + 10.1.3.0/24 = 10.1.0.0/22
```

**Rules for valid summarization:**
1. Networks must be contiguous (no gaps).
2. The starting address must be evenly divisible by the summarized block size.
3. The number of networks must be a power of 2.

**Verification command (Azure):**
```bash
# Check effective routes to confirm summarized route is advertised
az network nic show-effective-route-table \
  --resource-group myRG \
  --name myNIC \
  --output table
```

### Overlap Avoidance Strategy

CIDR overlaps break peering, VPN, and routing. Follow these rules:

1. **Maintain a central IP Address Management (IPAM) registry.** Use Azure IPAM, AWS IPAM (`aws ec2 create-ipam`), or tools like NetBox/phpIPAM.
2. **Check before allocating:**
   ```bash
   # Azure — list all VNet address spaces in a subscription
   az network vnet list --query "[].{Name:name, AddressSpace:addressSpace.addressPrefixes}" -o table

   # AWS — list all VPC CIDRs
   aws ec2 describe-vpcs --query "Vpcs[].{VpcId:VpcId, CidrBlock:CidrBlock}" --output table

   # GCP — list all subnet ranges
   gcloud compute networks subnets list --format="table(name, ipCidrRange, region)"
   ```
3. **Never reuse ranges** that are in-use by on-premises, partner networks, or other cloud accounts — even if they are not currently peered. Future connectivity requirements will be blocked.
4. **Reserve a "do not use" range** for future acquisitions or partner interconnects (e.g., reserve 10.200.0.0/14 as buffer).

## Workflow: Address Space Planning

### Phase 1: Inventory Existing Allocations

Collect all in-use IP ranges:
- On-premises data centers (IPAM export or manual survey)
- Existing cloud VNets/VPCs across all subscriptions/accounts/projects
- VPN tunnel endpoints and remote-peer ranges
- Partner/vendor networks connected via private peering

### Phase 2: Project Growth

Estimate 3–5 year growth:
- Number of new regions, environments, or workloads
- Expected VM/pod count per workload (drives subnet sizing)
- PaaS services requiring dedicated subnets (AKS, App Gateway, API Management, etc.)
- M&A activity that may bring additional address ranges

### Phase 3: Allocate Hierarchy

Design a hierarchical allocation tree:

```
Root:         10.0.0.0/8
├── Region:   /14 per region (4× /16 blocks)
│   ├── Hub:  /16 per hub VNet
│   └── Spokes: /16 – /20 per spoke depending on workload density
├── Buffer:   10.200.0.0/14 (reserved for future)
└── Mgmt:     10.250.0.0/16 (cross-region management plane)
```

**Sizing guidance:**
- Hub VNets: /16 minimum (shared services expand over time — firewall, DNS, bastion, monitoring, DevOps agents)
- Production spokes: /16 to /18 (1,024–65,536 addresses)
- Dev/test spokes: /20 to /22 (1,024–4,096 addresses)
- AKS/EKS node subnets: /21 minimum for Azure CNI (2,048 addresses for pods + nodes)

### Phase 4: Document and Validate

Produce a final address plan table:

| Network | CIDR | Region | Purpose | Peered To | Notes |
|---------|------|--------|---------|-----------|-------|
| hub-eastus | 10.0.0.0/16 | East US | Hub — shared services | All spokes | Firewall, Bastion, DNS |
| spoke-prod-eastus | 10.1.0.0/16 | East US | Production workloads | hub-eastus | Web/App/DB tiers |
| spoke-dev-eastus | 10.2.0.0/20 | East US | Development | hub-eastus | Non-prod only |

Run overlap validation:
```bash
# Python one-liner to check overlaps between two CIDRs
python3 -c "
import ipaddress
nets = [ipaddress.ip_network(n) for n in ['10.0.0.0/16','10.1.0.0/16','10.0.128.0/17']]
for i,a in enumerate(nets):
    for b in nets[i+1:]:
        if a.overlaps(b): print(f'OVERLAP: {a} ↔ {b}')
"
```

## IPv6 and Dual-Stack Handoff

For dual-stack designs, maintain IPv6 allocations in the same IPAM workflow as IPv4, but do not translate IPv4 subnet sizing rules directly to IPv6. Cloud IPv6 prefix sizes, private/public IPv6 options, load balancer support, and route advertisement behavior differ by provider and change over time. For IPv6-first or dual-stack migration plans, hand off to the IPv6 Migration specialist (`cn_ipv6`) and verify current provider documentation before selecting prefix sizes or compatibility patterns.

## References

- Azure VNet address space: https://learn.microsoft.com/azure/virtual-network/virtual-networks-faq
- AWS VPC CIDR blocks: https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html
- GCP subnet ranges: https://cloud.google.com/vpc/docs/subnets
- RFC 1918: https://datatracker.ietf.org/doc/html/rfc1918
- Azure IPAM: https://learn.microsoft.com/azure/virtual-network/ip-services/ip-address-management
- AWS IPAM: https://docs.aws.amazon.com/vpc/latest/ipam/what-it-is-ipam.html

**Analysis only — verify against vendor documentation before applying.**

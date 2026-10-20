# Skill: IPv6 Addressing Schemes

## Purpose

Design and document IPv6 address allocation plans for enterprise environments spanning Azure, AWS, and GCP. Covers address types, hierarchical allocation strategies, cloud provider constraints, and documentation best practices.

## Core Knowledge

### IPv6 Address Types

| Type | Prefix | Scope | Use Case |
|------|--------|-------|----------|
| Global Unicast (GUA) | 2000::/3 | Internet-routable | Public services, external connectivity |
| Unique Local (ULA) | fc00::/7 (fd00::/8 used) | Private, non-routable | Internal-only services, like RFC1918 |
| Link-Local | fe80::/10 | Single link only | NDP, routing protocols, always present |
| Multicast | ff00::/8 | Varies by scope | Group communication, NDP |
| Loopback | ::1/128 | Host only | Local testing |
| IPv4-Mapped | ::ffff:0:0/96 | Dual-stack sockets | Representing IPv4 in IPv6 APIs |

### Global Unicast Addresses (GUA)

Structure of a GUA:
```
|     48 bits      | 16 bits |      64 bits        |
+------------------+---------+---------------------+
| Global Routing   | Subnet  |    Interface ID     |
|    Prefix        |   ID    |                     |
+------------------+---------+---------------------+
|<-- Network --->| |<-Site->| |<--- Host -------->|
```

- **Global Routing Prefix**: Assigned by RIR or ISP (typically /32 to /48)
- **Subnet ID**: Used for internal subnetting (16 bits = 65,536 subnets)
- **Interface ID**: Identifies the host (64 bits, always /64 per subnet in most deployments)

### Unique Local Addresses (ULA)

Structure: `fd<40-bit random>::/48`

```bash
# Generate ULA prefix (RFC 4193)
# Use random 40-bit value: fd + 40 random bits = /48
# Example: fd12:3456:789a::/48

# ULA is appropriate for:
# - Internal services that never need internet routing
# - Backup addressing in case GUA connectivity fails
# - Lab/test environments
# - Consistent internal addressing regardless of ISP changes
```

**Important:** ULA is NOT equivalent to NAT. ULA addresses are non-routable on the internet but still globally unique (by probability). Do not use ULA as a security boundary.

### Link-Local Addresses (fe80::/10)

- Automatically configured on every IPv6-enabled interface
- Used for Neighbor Discovery Protocol (NDP)
- Required for IPv6 — cannot be disabled
- Scope limited to a single L2 segment
- Format: `fe80::<interface_id>`

## Address Planning for Enterprise

### Allocation Hierarchy

The recommended hierarchy follows IETF best practices:

```
/32 from RIR (or /48 from ISP)
 └── /48 per site (campus, region, or data center)
      └── /52 or /56 per functional group (optional)
           └── /64 per subnet (ALWAYS /64 for subnets)
```

### Standard Convention: /48 per Site, /56 per Group, /64 per Subnet

**Example Allocation Plan:**

```
Organization prefix: 2001:db8::/32 (from RIR)

Site allocations (/48 each):
  2001:db8:0000::/48  — Primary data center (Azure East US)
  2001:db8:0001::/48  — DR site (Azure West US)
  2001:db8:0002::/48  — AWS us-east-1
  2001:db8:0003::/48  — GCP us-central1
  2001:db8:0010::/48  — Office - New York
  2001:db8:0011::/48  — Office - London
  2001:db8:0100::/48  — Development/Lab

Within a site (/48 → /56 groups):
  2001:db8:0000:00xx::/56  — Production workloads
  2001:db8:0000:01xx::/56  — Staging environment
  2001:db8:0000:02xx::/56  — Management/infrastructure
  2001:db8:0000:03xx::/56  — DMZ/edge services
  2001:db8:0000:FFxx::/56  — Reserved for future

Within a group (/56 → /64 subnets):
  2001:db8:0000:0000::/64  — Production web tier
  2001:db8:0000:0001::/64  — Production app tier
  2001:db8:0000:0002::/64  — Production data tier
  2001:db8:0000:0003::/64  — Production cache tier
```

### Subnet ID Allocation Strategies

**Strategy 1: Sequential**
```
:0000::/64, :0001::/64, :0002::/64, ...
Simple, dense. Harder to visually identify purpose.
```

**Strategy 2: Functional Encoding**
```
Encode function in subnet ID bits:
  Bits 0-3: Environment (0=prod, 1=staging, 2=dev, 3=mgmt)
  Bits 4-7: Tier (0=web, 1=app, 2=data, 3=cache)
  Bits 8-15: Instance number

Example: 2001:db8:0000:0100::/64
  01 = staging, 00 = web tier, instance 0
```

**Strategy 3: VLAN-Mapped**
```
Mirror existing VLAN IDs in subnet ID:
  VLAN 100 → :0064::/64 (0x64 = 100)
  VLAN 200 → :00c8::/64 (0x64 = 200)
Useful during transition from existing IPv4/VLAN designs.
```

**Strategy 4: Location-Encoded**
```
Encode site/building/floor:
  2001:db8:0000:SSBF::/64
  SS = site number, B = building, F = floor
```

### Provider-Assigned vs Provider-Independent (PI) Space

| Aspect | Provider-Assigned (PA) | Provider-Independent (PI) |
|--------|----------------------|--------------------------|
| Source | ISP/cloud provider gives you a prefix | RIR allocates directly to you |
| Portability | Tied to that provider | Bring to any provider (BYOIP) |
| Cost | Included in service | Annual RIR fee + LOA process |
| Routing | Provider announces | You manage BGP announcements |
| Multi-cloud | Different prefix per cloud | Same prefix everywhere |
| Recommendation | Small/single-cloud | Multi-cloud, multi-ISP |

### Interface ID Generation

**EUI-64 (Modified Extended Unique Identifier):**
```
MAC: 00:1A:2B:3C:4D:5E
EUI-64: 021A:2BFF:FE3C:4D5E (flip bit 7, insert FFFE)

Privacy concern: Embeds hardware address, trackable.
```

**Privacy Extensions (RFC 4941):**
```bash
# Enable privacy extensions (randomized interface ID)
# Linux
sysctl -w net.ipv6.conf.all.use_tempaddr=2

# Windows (enabled by default)
netsh interface ipv6 set privacy state=enabled
```

**Static Assignment:**
```
# Use predictable, short interface IDs for servers:
2001:db8:0000:0001::1     — Gateway/router
2001:db8:0000:0001::a     — DNS server
2001:db8:0000:0001::b     — DHCP server
2001:db8:0000:0001::100   — First application server

# Convention: Keep server IDs in ::1 to ::ffff range
# Let SLAAC/DHCPv6 handle the rest
```

**DHCPv6 Managed Assignment:**
```bash
# Server-assigned addresses with DHCPv6
# Useful for compliance, audit trails, and predictable IDs
# Configure DHCPv6 pool:
#   Range: 2001:db8:0:1::1000 to 2001:db8:0:1::1fff
#   Prefix: /128 per host (individual addresses)
```

## Cloud-Specific Details

### Azure IPv6 Addressing Constraints

**VNet Level:**
- Can add multiple IPv6 address spaces to a VNet
- Supported prefixes: /48 to /64 for the VNet address space
- Both GUA and ULA ranges supported
- Cannot use link-local or multicast in VNet address space

**Subnet Level:**
- Subnets MUST be /64 (Azure requirement, no exceptions)
- One IPv6 prefix per subnet
- First address (::0) and last addresses reserved by Azure
- Azure reserves additional addresses for gateway usage

**VM/NIC Level:**
- Each NIC IP configuration gets one IPv6 private address
- IPv6 address assigned from subnet's /64 range
- Can have IPv6 public IP (Standard SKU only)
- IPv6 addresses are dynamic by default (can be static)

```bash
# View IPv6 address assignments
az network nic show --resource-group myRG --name myNIC \
  --query "ipConfigurations[].{Name:name, IPv4:privateIpAddress, IPv6:privateIpAddress}" -o table

# Assign static IPv6 private address
az network nic ip-config create \
  --resource-group myRG \
  --nic-name myNIC \
  --name ipv6static \
  --subnet mySubnet \
  --vnet-name myVNet \
  --private-ip-address-version IPv6 \
  --private-ip-address "2001:db8:abcd::10"
```

### AWS IPv6 CIDR Assignment

**Amazon-Provided IPv6:**
- VPC gets a /56 from Amazon's GUA pool (you don't choose the prefix)
- Subnets get /64 carved from the VPC's /56
- Addresses are publicly routable (no concept of "private" IPv6 in AWS by default)
- Use Egress-only Internet Gateway to prevent inbound for private workloads

**BYOIP (Bring Your Own IPv6):**
```bash
# Provision your IPv6 CIDR with AWS
aws ec2 provision-ipam-pool-cidr \
  --ipam-pool-id ipam-pool-xxx \
  --cidr 2001:db8:abcd::/48

# Associate with VPC
aws ec2 associate-vpc-cidr-block \
  --vpc-id vpc-xxx \
  --ipv6-cidr-block 2001:db8:abcd::/56 \
  --ipv6-pool ipv6pool-ec2-xxx

# Assign to subnet
aws ec2 associate-subnet-cidr-block \
  --subnet-id subnet-xxx \
  --ipv6-cidr-block 2001:db8:abcd:0001::/64
```

**AWS IPv6 Addressing Rules:**
- VPC: /44 to /60 (Amazon-provided is always /56)
- Subnet: /44 to /64 (typically /64)
- ENI: can have multiple IPv6 addresses (limit varies by instance type)
- IPv6 addresses are always public (routable) unless behind EIGW

```bash
# Assign additional IPv6 addresses to ENI
aws ec2 assign-ipv6-addresses \
  --network-interface-id eni-xxx \
  --ipv6-address-count 5

# Assign specific IPv6 addresses
aws ec2 assign-ipv6-addresses \
  --network-interface-id eni-xxx \
  --ipv6-addresses 2001:db8:abcd:1::10 2001:db8:abcd:1::11
```

### GCP IPv6 Ranges

**External IPv6 (GUA):**
- Google allocates a /64 per subnet from the VPC IPv6 range
- Each VM NIC receives a /96 range from the subnet; individual addresses are /128
- Globally routable; use firewall rules for access control
- Allocated from Google's 2600:1900::/28 range

**Internal IPv6 (ULA):**
- VPC gets a /48 ULA range (fd20::/20 pool)
- Subnets get /64 from the VPC's /48
- Each VM NIC receives a /96 range from the subnet for VM allocation
- NOT routable outside the VPC
- Useful for internal service-to-service communication

```bash
# View IPv6 allocation for subnet
gcloud compute networks subnets describe my-subnet \
  --region=us-central1 \
  --format="value(ipv6CidrRange, internalIpv6Prefix)"

# Reserve static external IPv6
gcloud compute addresses create my-ipv6-address \
  --region=us-central1 \
  --subnet=my-subnet \
  --ip-version=IPV6 \
  --endpoint-type=VM

# View VM IPv6 addresses
gcloud compute instances describe my-vm \
  --zone=us-central1-a \
  --format="value(networkInterfaces[0].ipv6AccessConfigs)"
```

**GCP Addressing Rules:**
- VPC (custom mode): /48 internal IPv6 range
- Subnet: /64 allocation (displayed as /96 for VM assignment purposes)
- VM: /96 range per NIC (single /128 used typically)
- Alias IP ranges: supported for IPv6
- Multiple NICs: each can be in different dual-stack subnets

## Documenting IPv6 Address Plans

### Documentation Template

```markdown
# IPv6 Address Plan — [Organization Name]

## Summary
- RIR Allocation: 2001:db8::/32 (ARIN, AS12345)
- Total /48 sites: 256 available, 7 assigned
- Last updated: YYYY-MM-DD

## Site Allocations

| Site ID | Prefix | Location | Environment |
|---------|--------|----------|-------------|
| 0000 | 2001:db8:0000::/48 | Azure East US | Production |
| 0001 | 2001:db8:0001::/48 | Azure West US | DR |
| 0002 | 2001:db8:0002::/48 | AWS us-east-1 | Production |
| ... | ... | ... | ... |

## Subnet Registry — Site 0000 (Azure East US)

| Subnet ID | Prefix | Purpose | VLAN | VNet |
|-----------|--------|---------|------|------|
| 0000 | 2001:db8:0000:0000::/64 | Prod-Web | 100 | prod-vnet |
| 0001 | 2001:db8:0000:0001::/64 | Prod-App | 101 | prod-vnet |
| 0002 | 2001:db8:0000:0002::/64 | Prod-DB | 102 | prod-vnet |
| 0100 | 2001:db8:0000:0100::/64 | Stage-Web | 200 | stage-vnet |
| ... | ... | ... | ... | ... |

## Reserved Ranges

| Range | Purpose |
|-------|---------|
| ::1 to ::f | Network infrastructure (routers, DNS) |
| ::10 to ::ff | Static server assignments |
| ::100 to ::ffff | DHCPv6 managed pool |
| FF00::/56 per site | Future expansion |

## Change Log

| Date | Change | Author | Ticket |
|------|--------|--------|--------|
| 2024-01-15 | Initial allocation | J. Smith | NET-1234 |
```

### Address Plan Validation

```bash
# Verify no overlapping prefixes
# Use sipcalc or ipv6calc for validation
sipcalc 2001:db8:0000::/48
ipv6calc --showinfo 2001:db8:0000:0001::/64

# Python script to check for overlaps
python3 -c "
import ipaddress
prefixes = [
    '2001:db8:0000::/48',
    '2001:db8:0001::/48',
    '2001:db8:0000:0001::/64',  # Should be WITHIN 0000::/48
]
nets = [ipaddress.IPv6Network(p) for p in prefixes]
for i, a in enumerate(nets):
    for b in nets[i+1:]:
        if a.overlaps(b):
            print(f'OVERLAP: {a} <-> {b}')
"
```

## Troubleshooting Tips

- **/64 too large?** IPv6 always uses /64 for subnets (required by SLAAC and NDP). Don't fight it.
- **Running out of subnet IDs?** You have 65,536 /64s in a /48. If that's not enough, request a larger allocation.
- **ULA vs GUA confusion?** Use GUA for anything that might ever need internet reachability. ULA only for strictly internal.
- **Cloud gave you an unexpected prefix?** Amazon-provided IPv6 is random (you can't choose). Use BYOIP for predictable addressing.
- **Can't assign static IPv6?** Some cloud services only support dynamic IPv6 assignment. Check provider docs.
- **Address plan doesn't fit cloud?** Clouds require /64 subnets. Plan for this from the start — don't allocate /112 or /80 subnets.

---

**Analysis only — verify against vendor documentation before applying.**

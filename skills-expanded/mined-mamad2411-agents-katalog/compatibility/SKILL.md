# Skill: IPv4/IPv6 Compatibility Mechanisms

## Purpose

Design and implement translation and tunneling mechanisms that enable communication between IPv4-only and IPv6-only endpoints. Covers NAT64, DNS64, 464XLAT, SIIT, and cloud-specific implementations across Azure, AWS, and GCP.

## Core Knowledge

### Translation Mechanism Overview

```
IPv6-only Client          Translation Layer         IPv4-only Server
┌─────────────┐          ┌──────────────┐          ┌──────────────┐
│  App uses   │  IPv6    │              │  IPv4    │              │
│  synthesized│ ────────>│   NAT64      │ ────────>│  Legacy      │
│  IPv6 addr  │          │   Gateway    │          │  Server      │
└─────────────┘          └──────────────┘          └──────────────┘
       ▲                        ▲
       │                        │
┌─────────────┐          ┌──────────────┐
│   DNS64     │          │ Synthesizes  │
│   Resolver  │          │ IPv6 address │
│             │          │ from A record│
└─────────────┘          └──────────────┘
```

### NAT64 / DNS64 Architecture

**NAT64** translates between IPv6 and IPv4 at the network layer:
- Stateful NAT64 (RFC 6146): Maintains translation state, like NAT44
- Uses a well-known prefix: `64:ff9b::/96` (or operator-defined prefix)
- IPv4 address embedded in last 32 bits: `64:ff9b::192.0.2.1`

**DNS64** synthesizes AAAA records from A records:
- Intercepts DNS queries from IPv6-only clients
- If no AAAA record exists, creates one by embedding IPv4 address in the NAT64 prefix
- Client connects to synthesized IPv6 address → NAT64 translates to IPv4

**How It Works Together:**

```
1. IPv6-only client queries DNS64: "What is ipv4only.example.com?"
2. DNS64 queries upstream: gets only A record (93.184.216.34)
3. DNS64 synthesizes AAAA: 64:ff9b::5db8:d822 (93.184.216.34 in hex)
4. Client connects to 64:ff9b::5db8:d822
5. Packet hits NAT64 gateway (routes for 64:ff9b::/96)
6. NAT64 translates: removes IPv6 header, creates IPv4 packet to 93.184.216.34
7. Return traffic: NAT64 translates IPv4 reply back to IPv6
```

**NAT64 Prefix Options:**
```
Well-Known Prefix (WKP): 64:ff9b::/96
  - Standardized, widely recognized
  - Use when single NAT64 instance suffices

Network-Specific Prefix (NSP): <your prefix>::/96
  - Example: 2001:db8:64:ff9b::/96
  - Use when multiple NAT64 zones needed
  - Avoids conflicts with WKP in complex topologies
```

### 464XLAT (RFC 6877)

For IPv6-only networks where applications require literal IPv4 addresses (e.g., hardcoded IPs, IPv4-only APIs):

```
IPv4 App ──> CLAT (local) ──> IPv6 Network ──> PLAT (NAT64) ──> IPv4 Internet
              v4 → v6              pure v6           v6 → v4
```

- **CLAT (Customer-side translator):** Runs on the host/device, translates IPv4 to IPv6
- **PLAT (Provider-side translator):** The NAT64 gateway at the network edge
- **Use case:** Mobile devices, legacy apps that can't handle IPv6

```bash
# Linux CLAT implementation (using clatd or Jool)
# Install Jool for CLAT functionality
apt-get install jool-dkms jool-tools

# Configure CLAT (stateless translation)
jool_siit instance add clat --netfilter
jool_siit -i clat eamt add 192.0.0.1/32 2001:db8:1::1/128
jool_siit -i clat global update pool6 64:ff9b::/96
```

### SIIT (Stateless IP/ICMP Translation — RFC 7915)

- **Stateless:** No connection tracking, 1:1 address mapping
- **Requires explicit address mapping** (EAM table) between IPv4 and IPv6
- **Use cases:** Servers that need both IPv4 and IPv6 without NAT state
- **Advantage:** No state table exhaustion, deterministic translation

```bash
# SIIT with Jool (Linux)
jool_siit instance add main --netfilter
jool_siit -i main eamt add 192.0.2.0/24 2001:db8::/120
# Maps 192.0.2.1 <-> 2001:db8::1, 192.0.2.2 <-> 2001:db8::2, etc.

# For unknown destinations, fall back to well-known prefix
jool_siit -i main global update pool6 64:ff9b::/96
```

**SIIT vs NAT64 Comparison:**

| Aspect | SIIT (Stateless) | NAT64 (Stateful) |
|--------|-----------------|------------------|
| State tracking | None | Per-connection |
| Address mapping | 1:1 explicit | Many:1 (overload) |
| Scalability | Excellent | Limited by state table |
| Address efficiency | Low (1:1 required) | High (sharing) |
| Initiated from | Either side | IPv6 side only (usually) |
| Use case | Servers, known hosts | General internet access |

## Cloud-Specific Details

### Azure NAT64 Support

**Azure Load Balancer with NAT64:**
- Standard Load Balancer can front-end IPv6 clients to IPv4 backends
- Not a full NAT64 gateway but achieves similar result for load-balanced services

```bash
# Dual-stack LB: IPv6 frontend → IPv4 backend (implicit translation)
# Frontend: IPv6 public IP
az network public-ip create --resource-group myRG \
  --name lbIPv6Frontend --sku Standard --version IPv6

# Backend pool with IPv4 targets
az network lb create --resource-group myRG --name myLB --sku Standard \
  --frontend-ip-name v6frontend --public-ip-address lbIPv6Frontend

# Add IPv4 backend pool
az network lb address-pool create --resource-group myRG \
  --lb-name myLB --name v4BackendPool

# The LB handles IPv6-to-IPv4 translation for inbound traffic
```

**Azure NAT Gateway IPv6 / NAT64 Scope:**
- Azure NAT Gateway Standard is IPv4 outbound only.
- Azure NAT Gateway StandardV2 supports IPv6 outbound where available, but it is not a general NAT64 gateway; verify current regional/SKU limitations before relying on it.
- For outbound NAT64 from IPv6-only clients to IPv4-only destinations, use a verified Azure capability or a Network Virtual Appliance (NVA) running Jool or Tayga.

**NVA-Based NAT64 on Azure:**
```bash
# Deploy Ubuntu VM as NAT64 gateway
# Install Jool NAT64
apt-get update && apt-get install -y jool-dkms jool-tools

# Configure stateful NAT64
modprobe jool
jool instance add nat64 --netfilter --pool6 64:ff9b::/96

# Add IPv4 pool for translation
jool -i nat64 pool4 add 10.0.1.100 --tcp 1024-65535
jool -i nat64 pool4 add 10.0.1.100 --udp 1024-65535
jool -i nat64 pool4 add 10.0.1.100 --icmp 0-65535

# UDR: Route 64:ff9b::/96 to this NVA
az network route-table route create \
  --resource-group myRG --route-table-name ipv6RT \
  --name nat64route --address-prefix "64:ff9b::/96" \
  --next-hop-type VirtualAppliance \
  --next-hop-ip-address 10.0.1.100
```

### AWS NAT64 with DNS64

AWS natively supports NAT64 + DNS64 for IPv6-only workloads:

**NAT Gateway with NAT64:**
```bash
# Create NAT Gateway (supports NAT64 since 2021)
aws ec2 create-nat-gateway \
  --subnet-id subnet-public-xxx \
  --connectivity-type public \
  --allocation-id eipalloc-xxx

# Route 64:ff9b::/96 to NAT Gateway from IPv6-only subnets
aws ec2 create-route \
  --route-table-id rtb-private-xxx \
  --destination-ipv6-cidr-block 64:ff9b::/96 \
  --nat-gateway-id nat-xxx
```

**Subnet DNS64:**
```bash
# Enable DNS64 on each IPv6-only subnet that needs synthesized AAAA responses.
# Amazon-provided DNS synthesizes records with the well-known 64:ff9b::/96 prefix.
aws ec2 modify-subnet-attribute \
  --subnet-id subnet-xxx \
  --enable-dns64

# Ensure the subnet route table sends 64:ff9b::/96 to the NAT Gateway.
aws ec2 create-route \
  --route-table-id rtb-private-xxx \
  --destination-ipv6-cidr-block 64:ff9b::/96 \
  --nat-gateway-id nat-xxx
```

**Complete AWS IPv6-Only Architecture:**
```
IPv6-only Subnet                    Public Subnet
┌────────────────────┐              ┌─────────────────┐
│ EC2 Instance       │              │ NAT Gateway     │
│ (IPv6 only)        │──64:ff9b::──>│ (NAT64 + IPv4)  │──> IPv4 Internet
│                    │              │                 │
│ DNS64 via Route 53 │              └─────────────────┘
│ Resolver           │              
└────────────────────┘              ┌─────────────────┐
         │                          │ Egress-Only IGW │
         └──────── ::/0 ──────────> │ (IPv6 outbound) │──> IPv6 Internet
                                    └─────────────────┘
```

### GCP Private Google Access for IPv6-Only VMs

GCP supports IPv6-only VMs accessing Google APIs and services:

```bash
# Create IPv6-only subnet (no IPv4)
gcloud compute networks subnets create ipv6-only-subnet \
  --network=my-vpc \
  --region=us-central1 \
  --stack-type=IPV6_ONLY \
  --ipv6-access-type=INTERNAL

# Enable Private Google Access for IPv6
gcloud compute networks subnets update ipv6-only-subnet \
  --region=us-central1 \
  --enable-private-ipv6-google-access

# VM in IPv6-only subnet can reach:
# - Google APIs (googleapis.com) over IPv6
# - Other GCP services with IPv6 support
# - External IPv6 destinations (with firewall rules)
```

**GCP NAT64 — Limited Native Support:**
- Cloud NAT does NOT support NAT64 (IPv4 only)
- For NAT64, deploy a self-managed gateway (VM running Jool/Tayga)
- Use Private Google Access for IPv6-only VMs to reach Google services without NAT64

```bash
# GCP: Self-managed NAT64 gateway
gcloud compute instances create nat64-gw \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --subnet=dual-stack-subnet \
  --can-ip-forward \
  --metadata=startup-script='#!/bin/bash
    apt-get update && apt-get install -y jool-dkms jool-tools
    modprobe jool
    jool instance add nat64 --netfilter --pool6 64:ff9b::/96
    jool -i nat64 pool4 add $(curl -s http://metadata/computeMetadata/v1/instance/network-interfaces/0/ip -H "Metadata-Flavor: Google") --tcp 1024-65535
    jool -i nat64 pool4 add $(curl -s http://metadata/computeMetadata/v1/instance/network-interfaces/0/ip -H "Metadata-Flavor: Google") --udp 1024-65535
    sysctl -w net.ipv4.ip_forward=1
    sysctl -w net.ipv6.conf.all.forwarding=1'

# Route 64:ff9b::/96 to the NAT64 gateway
gcloud compute routes create nat64-route \
  --network=my-vpc \
  --destination-range=64:ff9b::/96 \
  --next-hop-instance=nat64-gw \
  --next-hop-instance-zone=us-central1-a
```

## Legacy Tunneling Mechanisms

> **Note:** These are largely deprecated. Use native dual-stack or NAT64 instead. Listed for awareness when encountering legacy infrastructure.

### 6in4 (RFC 4213)
- Encapsulates IPv6 packets in IPv4 (protocol 41)
- Static tunnels between known endpoints
- **Deprecated for cloud:** Use native IPv6 or VPN instead

### ISATAP (Intra-Site Automatic Tunnel Addressing Protocol)
- Automatic tunneling within a site
- Embeds IPv4 address in interface ID
- **Deprecated:** Windows removed support in recent versions

### Teredo (RFC 4380)
- Tunnels IPv6 over UDP/IPv4 through NATs
- Last resort for hosts behind NAT without IPv6
- **Deprecated:** Security concerns, unpredictable performance

### When Each Mechanism Is Appropriate

| Mechanism | When to Use | When NOT to Use |
|-----------|------------|-----------------|
| NAT64 + DNS64 | IPv6-only clients → IPv4 servers | IPv4 clients → IPv6 servers |
| 464XLAT | Legacy apps on IPv6-only networks | Networks with native dual-stack |
| SIIT | Known 1:1 server mappings | Dynamic client populations |
| Dual-stack | Transition period, broad compatibility | When simplification is the goal |
| IPv6-only + NAT64 | New deployments, mobile, IoT | Heavy IPv4 dependency |
| 6in4/ISATAP/Teredo | Never in new designs | Always (deprecated) |

## Performance Implications

### Translation Overhead

| Mechanism | Latency Impact | Throughput Impact | State Cost |
|-----------|---------------|-------------------|------------|
| NAT64 (Stateful) | +0.1-0.5ms | -5-10% (header rewrite) | Per-connection state |
| SIIT (Stateless) | +0.05-0.2ms | -2-5% (header rewrite) | None |
| 464XLAT | +0.2-0.8ms (double xlat) | -10-15% | CLAT + PLAT state |
| Native dual-stack | None | None | None |

### Scaling Considerations

```
NAT64 State Table Sizing:
- Each TCP connection = ~200 bytes of state
- 100,000 concurrent connections ≈ 20 MB state
- Plan for peak connections × 2 (safety margin)
- State timeout: TCP established = 7200s, UDP = 300s

Port Pool Sizing:
- Each NAT64 IPv4 address provides ~64,000 ports
- 100,000 connections need ≥ 2 IPv4 addresses
- Formula: ceil(peak_connections / 64000) = min_ipv4_addresses
```

### Best Practices for Production NAT64

1. **Monitor state table utilization** — alert at 70% capacity
2. **Use multiple NAT64 instances** behind a route with ECMP
3. **Set appropriate timeouts** — don't hold state for abandoned connections
4. **Log translations** — essential for troubleshooting and security audits
5. **Health-check the NAT64** — if it fails, IPv6-only clients lose IPv4 connectivity

## Troubleshooting Tips

- **DNS64 not synthesizing?** Verify resolver is configured for DNS64 and prefix matches NAT64 route
- **NAT64 drops traffic?** Check pool4 has available ports; inspect state table utilization
- **464XLAT not working?** Verify CLAT is running on host and PLAT (NAT64) is reachable via the configured prefix
- **Asymmetric routing through NAT64?** All traffic for a flow must traverse the same NAT64 instance (stateful)
- **ICMP broken through NAT64?** Ensure ICMPv6↔ICMPv4 translation is enabled (required for PMTUD)
- **Performance issues?** Check if translation is happening in software (CPU-bound) vs hardware offload
- **ALG-dependent protocols fail?** FTP, SIP, etc. may not work through NAT64 without application-layer gateways

---

**Analysis only — verify against vendor documentation before applying.**

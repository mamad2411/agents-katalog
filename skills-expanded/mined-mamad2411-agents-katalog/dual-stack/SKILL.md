# Skill: Dual-Stack Design

## Purpose

Design and implement dual-stack (IPv4 + IPv6) network architectures across Azure, AWS, and GCP. Covers VNet/VPC configuration, load balancing, DNS, firewall rules, and application considerations for running both protocol families simultaneously.

## Core Knowledge

### Dual-Stack Architecture Fundamentals

Dual-stack means every host, interface, and network path supports both IPv4 and IPv6 concurrently:

- **Independent stacks** — IPv4 and IPv6 operate as separate protocol instances; each has its own routing table, ARP/NDP, and firewall rules
- **Shared infrastructure** — physical/virtual NICs carry both protocols; a single interface has both an IPv4 address and one or more IPv6 addresses
- **Protocol selection** — applications or the OS chooses which protocol to use per connection (Happy Eyeballs / RFC 8305)
- **No translation required** — both endpoints speak the same protocol natively; no NAT64 or tunneling overhead

**Key Principle:** Dual-stack is the recommended first step in any IPv6 migration because it preserves IPv4 connectivity while enabling IPv6 adoption incrementally.

### Design Considerations

| Aspect | IPv4 | IPv6 |
|--------|------|------|
| Address assignment | DHCP or static | SLAAC, DHCPv6, or static |
| Default gateway | Single per subnet | Router Advertisement (RA) |
| DNS resolution | A records | AAAA records |
| Firewall rules | Separate ruleset | Separate ruleset |
| Routing | Separate route table | Separate route table |
| MTU | 576 min, 1500 typical | 1280 min, 1500 typical |

## Cloud-Specific Details

### Azure Dual-Stack VNet Configuration

Azure supports dual-stack VNets with both IPv4 and IPv6 address spaces:

```bash
# Create a dual-stack VNet
az network vnet create \
  --resource-group myRG \
  --name myDualStackVNet \
  --address-prefixes 10.0.0.0/16 fd00:db8::/48 \
  --subnet-name mySubnet \
  --subnet-prefixes 10.0.0.0/24 fd00:db8::/64

# Add IPv6 address space to existing VNet
az network vnet update \
  --resource-group myRG \
  --name myExistingVNet \
  --address-prefixes 10.0.0.0/16 2001:db8:abcd::/48

# Add IPv6 range to existing subnet
az network vnet subnet update \
  --resource-group myRG \
  --vnet-name myExistingVNet \
  --name mySubnet \
  --address-prefixes 10.0.0.0/24 2001:db8:abcd::/64
```

**Azure Constraints:**
- VNet can have multiple IPv4 and IPv6 address spaces
- Each subnet must have exactly one IPv6 prefix (/64 only on subnets)
- IPv6 subnets must be /64 (no other prefix lengths supported)
- VM NICs can have one IPv6 configuration per IP configuration
- IPv6 public IPs are Standard SKU only
- No IPv6 support on Basic Load Balancer (Standard LB required)
- VNet peering supports dual-stack
- VPN Gateway supports dual-stack (route-based only)

**NIC Configuration:**
```bash
# Add IPv6 config to existing NIC
az network nic ip-config create \
  --resource-group myRG \
  --nic-name myNIC \
  --name ipv6config \
  --subnet mySubnet \
  --vnet-name myDualStackVNet \
  --private-ip-address-version IPv6

# Associate IPv6 public IP
az network public-ip create \
  --resource-group myRG \
  --name myIPv6PublicIP \
  --sku Standard \
  --version IPv6

az network nic ip-config update \
  --resource-group myRG \
  --nic-name myNIC \
  --name ipv6config \
  --public-ip-address myIPv6PublicIP
```

### AWS Dual-Stack VPC Configuration

AWS VPCs support dual-stack with Amazon-provided or BYOIP IPv6 CIDRs:

```bash
# Associate IPv6 CIDR with existing VPC (Amazon-provided)
aws ec2 associate-vpc-cidr-block \
  --vpc-id vpc-12345678 \
  --amazon-provided-ipv6-cidr-block

# Associate IPv6 CIDR with existing VPC (BYOIP)
aws ec2 associate-vpc-cidr-block \
  --vpc-id vpc-12345678 \
  --ipv6-cidr-block 2001:db8:1234::/48 \
  --ipv6-pool ipv6pool-ec2-012345

# Add IPv6 CIDR to subnet
aws ec2 associate-subnet-cidr-block \
  --subnet-id subnet-12345678 \
  --ipv6-cidr-block 2001:db8:1234:1::/64

# Enable auto-assign IPv6 on subnet
aws ec2 modify-subnet-attribute \
  --subnet-id subnet-12345678 \
  --assign-ipv6-address-on-creation
```

**AWS Constraints:**
- VPC receives a /56 IPv6 CIDR (Amazon-provided) or bring your own
- Subnets get /64 from the VPC's /56
- Security groups and NACLs support IPv6 rules natively
- Egress-only Internet Gateway (EIGW) for outbound IPv6 without inbound
- Route tables need separate entries for IPv6 (::/0 → IGW or EIGW)
- Not all instance types support IPv6 (check instance family support)

**Route Table for Dual-Stack:**
```bash
# Add IPv6 route to Internet Gateway
aws ec2 create-route \
  --route-table-id rtb-12345678 \
  --destination-ipv6-cidr-block ::/0 \
  --gateway-id igw-12345678

# Add IPv6 route to Egress-Only IGW (private subnets)
aws ec2 create-route \
  --route-table-id rtb-87654321 \
  --destination-ipv6-cidr-block ::/0 \
  --egress-only-internet-gateway-id eigw-12345678
```

### GCP Dual-Stack Subnet Configuration

GCP supports dual-stack at the subnet level with internal or external IPv6:

```bash
# Create dual-stack subnet with external IPv6
gcloud compute networks subnets create my-dual-stack-subnet \
  --network=my-vpc \
  --region=us-central1 \
  --range=10.0.0.0/24 \
  --stack-type=IPV4_IPV6 \
  --ipv6-access-type=EXTERNAL

# Create dual-stack subnet with internal IPv6 (ULA)
gcloud compute networks subnets create my-internal-v6-subnet \
  --network=my-vpc \
  --region=us-central1 \
  --range=10.0.1.0/24 \
  --stack-type=IPV4_IPV6 \
  --ipv6-access-type=INTERNAL

# Update existing subnet to dual-stack
gcloud compute networks subnets update my-subnet \
  --region=us-central1 \
  --stack-type=IPV4_IPV6 \
  --ipv6-access-type=EXTERNAL
```

**GCP Constraints:**
- VPC must be custom-mode for dual-stack subnets
- IPv6 ranges are /64 per subnet (allocated from the VPC IPv6 range)
- Each VM NIC receives a /96 range from the subnet; individual addresses are /128
- `EXTERNAL` IPv6: globally routable (GUA from Google's allocation)
- `INTERNAL` IPv6: ULA range for internal-only communication
- Stack type applies per-subnet, not per-VPC
- Firewall rules support IPv6 source/destination ranges

**VM with Dual-Stack:**
```bash
gcloud compute instances create my-dual-stack-vm \
  --zone=us-central1-a \
  --subnet=my-dual-stack-subnet \
  --stack-type=IPV4_IPV6 \
  --machine-type=e2-medium
```

## Load Balancer Dual-Stack Support

### Azure Standard Load Balancer

```bash
# Create dual-stack frontend
az network lb frontend-ip create \
  --resource-group myRG \
  --lb-name myLB \
  --name myIPv6Frontend \
  --public-ip-address myIPv6PublicIP

# Backend pool supports both IPv4 and IPv6 NICs
# Health probes work over both protocols
```

- Standard LB supports IPv4 and IPv6 frontends simultaneously
- Backend pool members need both IPv4 and IPv6 IP configurations
- Health probes can target either protocol
- Outbound rules apply per-protocol

### AWS Application Load Balancer (ALB)

```bash
# ALB supports dual-stack via ip-address-type
aws elbv2 create-load-balancer \
  --name my-dual-stack-alb \
  --subnets subnet-1 subnet-2 \
  --ip-address-type dualstack \
  --type application

# Modify existing ALB to dual-stack
aws elbv2 set-ip-address-type \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --ip-address-type dualstack
```

- ALB and NLB support `dualstack` IP address type
- Target groups can register IPv6 targets (IP type targets)
- DNS name resolves to both A and AAAA records when dualstack enabled

### GCP Load Balancer

```bash
# External HTTP(S) LB supports IPv6 by default
# Global forwarding rule with IPv6
gcloud compute forwarding-rules create my-ipv6-rule \
  --global \
  --ip-version=IPV6 \
  --load-balancing-scheme=EXTERNAL_MANAGED \
  --network-tier=PREMIUM \
  --target-https-proxy=my-proxy \
  --ports=443
```

- Global external LBs support IPv6 frontends natively
- Regional internal LBs support dual-stack with dual-stack subnets
- Backend services can use dual-stack instance groups

## Dual-Stack Firewall/NSG Considerations

**Critical Rule:** IPv4 and IPv6 require separate firewall rules. Enabling IPv6 without adding corresponding rules leaves traffic unfiltered or blocked.

### Azure NSG Dual-Stack Rules

```bash
# Allow inbound HTTPS for both protocols
az network nsg rule create --resource-group myRG --nsg-name myNSG \
  --name AllowHTTPS_IPv4 --priority 100 --direction Inbound \
  --source-address-prefixes '*' --destination-port-ranges 443 \
  --protocol Tcp --access Allow

az network nsg rule create --resource-group myRG --nsg-name myNSG \
  --name AllowHTTPS_IPv6 --priority 101 --direction Inbound \
  --source-address-prefixes '::/0' --destination-port-ranges 443 \
  --protocol Tcp --access Allow

# CRITICAL: Allow ICMPv6 (required for NDP, PMTUD)
az network nsg rule create --resource-group myRG --nsg-name myNSG \
  --name AllowICMPv6 --priority 110 --direction Inbound \
  --source-address-prefixes '*' --destination-port-ranges '*' \
  --protocol Icmp --access Allow
```

### AWS Security Groups

```bash
# Security groups support IPv6 CIDR in rules
aws ec2 authorize-security-group-ingress \
  --group-id sg-12345678 \
  --ip-permissions '[{
    "IpProtocol": "tcp",
    "FromPort": 443,
    "ToPort": 443,
    "Ipv6Ranges": [{"CidrIpv6": "::/0", "Description": "HTTPS IPv6"}]
  }]'
```

### GCP Firewall Rules

```bash
# GCP firewall rules apply to both IPv4 and IPv6 when source is ::/0 or 0.0.0.0/0
gcloud compute firewall-rules create allow-https-ipv6 \
  --network=my-vpc \
  --allow=tcp:443 \
  --source-ranges="::/0" \
  --direction=INGRESS
```

## DNS Dual-Stack Configuration

### Happy Eyeballs (RFC 8305)

Modern clients use Happy Eyeballs to select the best protocol:
1. Query for both A and AAAA records simultaneously
2. Prefer IPv6 but start IPv4 connection attempt after 250ms delay
3. Use whichever connection succeeds first
4. Cache result for subsequent connections

### DNS Configuration

```bash
# Azure DNS - add both record types
az network dns record-set a add-record --zone-name example.com \
  --resource-group myRG --record-set-name www --ipv4-address 10.0.0.5
az network dns record-set aaaa add-record --zone-name example.com \
  --resource-group myRG --record-set-name www --ipv6-address 2001:db8::5

# AWS Route 53 - A and AAAA records
aws route53 change-resource-record-sets --hosted-zone-id Z12345 \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "www.example.com",
        "Type": "AAAA",
        "TTL": 300,
        "ResourceRecords": [{"Value": "2001:db8::5"}]
      }
    }]
  }'
```

## Application Considerations

### Socket Binding

Applications must bind to IPv6 or dual-stack sockets:

```python
# Python — dual-stack socket
import socket
sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)  # Accept IPv4-mapped
sock.bind(('::', 8080))  # Bind to all IPv6 (and mapped IPv4)
```

```javascript
// Node.js — dual-stack server
const server = require('http').createServer(handler);
server.listen(8080, '::');  // Listen on all IPv6 addresses (includes IPv4-mapped)
```

```go
// Go — default is dual-stack on '::'
listener, err := net.Listen("tcp", "[::]:8080")
```

### Address Family Selection

- **Prefer `AF_INET6` with `IPV6_V6ONLY=0`** for dual-stack sockets (Linux, most platforms)
- **Windows:** Dual-stack sockets work but some applications need explicit configuration
- **Containers:** Ensure container runtime enables IPv6 (`--ipv6` in Docker, `ipFamilies` in K8s)

## Testing Dual-Stack Connectivity

```bash
# Verify IPv6 address assignment
ip -6 addr show              # Linux
Get-NetIPAddress -AddressFamily IPv6  # Windows

# Test IPv6 reachability
ping6 2001:db8::1            # Linux
ping -6 2001:db8::1          # Windows
curl -6 https://ipv6.example.com

# Verify DNS returns both A and AAAA
dig www.example.com A
dig www.example.com AAAA
nslookup -type=AAAA www.example.com

# Check both paths from load balancer
curl -4 https://app.example.com  # Force IPv4
curl -6 https://app.example.com  # Force IPv6

# Verify routing
ip -6 route show             # Linux IPv6 route table
traceroute6 2001:db8::1      # IPv6 traceroute
```

## Troubleshooting Tips

- **No IPv6 address on VM?** Check subnet has IPv6 range, NIC has IPv6 IP config, and OS has IPv6 enabled
- **IPv6 traffic blocked?** Verify NSG/SG rules exist for IPv6 (separate from IPv4 rules)
- **ICMPv6 blocked?** Never block ICMPv6 — required for NDP, PMTUD, and basic connectivity
- **DNS not returning AAAA?** Verify AAAA records exist and DNS server supports IPv6 queries
- **App not reachable on IPv6?** Check application binds to `::` or explicit IPv6 address, not just `0.0.0.0`
- **Asymmetric routing?** Ensure IPv6 route tables match IPv4 intent (separate route tables)

---

**Analysis only — verify against vendor documentation before applying.**

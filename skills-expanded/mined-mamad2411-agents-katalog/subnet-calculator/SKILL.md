# Skill: Subnet Calculator

## Purpose

This skill performs CIDR math for subnet planning: calculating usable host counts, splitting CIDR blocks into subnets, and accounting for cloud-specific reserved addresses. It outputs structured tables suitable for network design documentation.

## Core Knowledge

### CIDR Math Reference

| Prefix | Total Addresses | Azure Usable (−5) | AWS Usable (−5) | GCP Usable (−4) | Typical Use |
|--------|----------------|-------------------|-----------------|-----------------|-------------|
| /16 | 65,536 | 65,531 | 65,531 | 65,532 | Full VNet/VPC |
| /17 | 32,768 | 32,763 | 32,763 | 32,764 | Large workload zone |
| /18 | 16,384 | 16,379 | 16,379 | 16,380 | Large workload zone |
| /19 | 8,192 | 8,187 | 8,187 | 8,188 | AKS node + pod subnet |
| /20 | 4,096 | 4,091 | 4,091 | 4,092 | Medium workload |
| /21 | 2,048 | 2,043 | 2,043 | 2,044 | AKS minimum (Azure CNI) |
| /22 | 1,024 | 1,019 | 1,019 | 1,020 | Standard spoke subnet |
| /23 | 512 | 507 | 507 | 508 | Medium application tier |
| /24 | 256 | 251 | 251 | 252 | Standard subnet |
| /25 | 128 | 123 | 123 | 124 | Small workload |
| /26 | 64 | 59 | 59 | 60 | Azure Firewall / Bastion minimum |
| /27 | 32 | 27 | 27 | 28 | GatewaySubnet / small service |
| /28 | 16 | 11 | 11 | 12 | DNS resolver / tiny service |
| /29 | 8 | 3 | 3 | 4 | Minimum practical subnet |

**Formula:** Usable IPs = 2^(32 − prefix) − reserved_count

### Cloud-Specific Reserved Addresses

**Azure (5 reserved per subnet):**
| Address | Purpose |
|---------|---------|
| x.x.x.0 | Network address |
| x.x.x.1 | Default gateway |
| x.x.x.2 | Azure DNS mapping (primary) |
| x.x.x.3 | Azure DNS mapping (secondary) |
| x.x.x.255 | Broadcast (for /24; last address for smaller subnets) |

**AWS (5 reserved per subnet):**
| Address | Purpose |
|---------|---------|
| x.x.x.0 | Network address |
| x.x.x.1 | VPC router |
| x.x.x.2 | DNS server (VPC base + 2) |
| x.x.x.3 | Reserved for future use |
| x.x.x.255 | Broadcast |

**GCP (4 reserved per subnet):**
| Address | Purpose |
|---------|---------|
| x.x.x.0 | Network address |
| x.x.x.1 | Default gateway |
| Second-to-last | Reserved (DHCP/DNS) |
| x.x.x.255 | Broadcast |

### Subnet Splitting Strategy

#### Standard 3-Tier Web Application (in a /16 VNet)

| Subnet Name | CIDR | Usable IPs (Azure) | Purpose |
|-------------|------|-------------------|---------|
| web-tier | 10.1.0.0/24 | 251 | Web servers / App Gateway backends |
| app-tier | 10.1.1.0/24 | 251 | Application servers / API hosts |
| data-tier | 10.1.2.0/24 | 251 | Database servers (private, no internet) |
| management | 10.1.3.0/26 | 59 | Bastion, jump boxes, monitoring agents |
| gateway | 10.1.255.0/27 | 27 | VPN/ExpressRoute GatewaySubnet |
| reserved | 10.1.128.0/17 | — | Reserved for future growth |

#### AKS / Kubernetes Cluster (in a /16 VNet with Azure CNI)

Azure CNI allocates one IP per pod. Default: 30 pods/node × N nodes. A 50-node cluster needs 50 (nodes) + 1,500 (pods) = 1,550 IPs minimum.

| Subnet Name | CIDR | Usable IPs (Azure) | Purpose |
|-------------|------|-------------------|---------|
| aks-nodes | 10.2.0.0/21 | 2,043 | AKS node + pod IPs (Azure CNI) |
| aks-internal-lb | 10.2.8.0/24 | 251 | Internal load balancer subnet |
| aks-appgw | 10.2.9.0/24 | 251 | Application Gateway Ingress Controller |
| aks-management | 10.2.10.0/28 | 11 | Private endpoint for AKS API server |

#### AWS Multi-AZ Deployment (in a /16 VPC)

Best practice: one subnet per tier per AZ. For 3 tiers across 3 AZs = 9 subnets.

| Subnet Name | CIDR | AZ | Usable IPs (AWS) | Purpose |
|-------------|------|----|-----------------|---------|
| public-az1 | 10.3.0.0/24 | us-east-1a | 251 | ALB, NAT Gateway |
| public-az2 | 10.3.1.0/24 | us-east-1b | 251 | ALB, NAT Gateway |
| public-az3 | 10.3.2.0/24 | us-east-1c | 251 | ALB, NAT Gateway |
| app-az1 | 10.3.10.0/24 | us-east-1a | 251 | ECS / EC2 app tier |
| app-az2 | 10.3.11.0/24 | us-east-1b | 251 | ECS / EC2 app tier |
| app-az3 | 10.3.12.0/24 | us-east-1c | 251 | ECS / EC2 app tier |
| data-az1 | 10.3.20.0/24 | us-east-1a | 251 | RDS, ElastiCache |
| data-az2 | 10.3.21.0/24 | us-east-1b | 251 | RDS, ElastiCache |
| data-az3 | 10.3.22.0/24 | us-east-1c | 251 | RDS, ElastiCache |

### How to Split a CIDR Block

**Given a /X parent, how many /Y subnets fit?**

Number of subnets = 2^(Y − X)

Examples:
- /16 into /24 subnets: 2^(24−16) = **256 subnets**
- /16 into /20 subnets: 2^(20−16) = **16 subnets**
- /20 into /24 subnets: 2^(24−20) = **16 subnets**
- /24 into /26 subnets: 2^(26−24) = **4 subnets**
- /24 into /27 subnets: 2^(27−24) = **8 subnets**

**Reverse: given N hosts needed, what prefix?**

Find the smallest prefix where 2^(32−prefix) − reserved ≥ N.

Quick lookup for Azure/AWS (5 reserved):
- Need 10 hosts → /28 (11 usable) ✅
- Need 25 hosts → /27 (27 usable) ✅
- Need 50 hosts → /26 (59 usable) ✅
- Need 200 hosts → /24 (251 usable) ✅
- Need 500 hosts → /23 (507 usable) ✅

### Output Format

When presenting subnet plans, always use this table format:

```
| Subnet Name | CIDR | Total IPs | Usable IPs | Purpose | Notes |
|-------------|------|-----------|------------|---------|-------|
| web-tier    | 10.1.0.0/24 | 256 | 251 | Web servers | NSG: allow 80/443 inbound |
```

Include:
- Cloud provider (affects usable IP count)
- Growth buffer rationale (why a /23 instead of /24)
- Any delegated subnet requirements (Azure-specific)
- AZ placement (AWS-specific)

## References

- Azure subnet sizing: https://learn.microsoft.com/azure/virtual-network/virtual-networks-faq#are-there-any-restrictions-on-using-ip-addresses-within-these-subnets
- AWS subnet sizing: https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html
- GCP subnet ranges: https://cloud.google.com/vpc/docs/subnets#valid-ranges
- Azure CNI IP planning: https://learn.microsoft.com/azure/aks/azure-cni-overview#plan-ip-addressing

**Analysis only — verify against vendor documentation before applying.**

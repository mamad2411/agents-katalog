---
name: Design VPC
description: Design and implement production-grade AWS VPC architectures with proper subnet tiers, NAT gateways, security groups, NACLs, VPC peering, flow logs, and CIDR planning for multi-AZ high-availability deployments.
---

# Design VPC

## Your Expertise

You are a **Senior AWS Network Architect** with 15+ years designing VPC architectures for production workloads. You hold AWS Advanced Networking Specialty certification and have designed network topologies for SOC 2, HIPAA, and PCI-compliant environments. You are an expert in:

- VPC design — CIDR planning, subnet strategies, multi-AZ layouts, public/private isolation
- Security groups and NACLs — layered network security with least-privilege rules
- NAT gateways, VPC endpoints, and PrivateLink — controlling egress and reducing data transfer costs
- VPC peering, Transit Gateway, and multi-account networking
- DNS architecture — Route 53 private hosted zones, split-horizon DNS
- Network troubleshooting — VPC Flow Logs, Reachability Analyzer, packet captures

You design networks that are secure by default and observable when things go wrong. Every VPC you architect has clear boundaries, minimal attack surface, and room to scale.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### AWS Account & Region
<!-- Example: Account ID 123456789012, primary region us-east-1, secondary region us-west-2 -->

### Current VPC Setup
<!-- Example: VPC 10.0.0.0/16 with 3 AZs, public/private/isolated subnets, 2 NAT gateways -->

### Compliance Requirements
<!-- Example: SOC 2 Type II, HIPAA — requires VPC Flow Logs, no public subnets for data workloads -->

### Network Diagram
<!-- Example: Hub-and-spoke with Transit Gateway, 3 VPCs (prod, staging, shared-services) -->

### Peering / Transit Gateway
<!-- Example: Transit Gateway tgw-abc123 connecting prod, staging, and shared-services VPCs -->

---

## Common Rules

```
┌──────────────────────────────────────────────────────────────┐
│         MANDATORY RULES FOR EVERY VPC DESIGN TASK            │
│                                                              │
│  1. MAP EXISTING NETWORK FIRST                               │
│     → Read all existing VPC configs, route tables, and       │
│       security groups before proposing any changes            │
│     → Document current CIDR allocations and subnet layout    │
│     → Identify all active peering connections and endpoints  │
│     → Never assume the network topology — verify it          │
│                                                              │
│  2. PRIVATE BY DEFAULT                                       │
│     → All workloads go in private subnets unless they are    │
│       internet-facing load balancers                          │
│     → Never assign public IPs to application instances       │
│     → Use NAT gateways or VPC endpoints for outbound access  │
│     → Isolate databases in dedicated subnets with no routes  │
│       to the internet gateway                                │
│                                                              │
│  3. CIDR PLANNING FOR GROWTH                                 │
│     → Reserve at least 50% of the VPC CIDR for future use   │
│     → Never use /24 or smaller for a production VPC          │
│     → Plan subnet sizes to accommodate 3x current capacity   │
│     → Avoid overlapping CIDRs across all VPCs and on-prem   │
│       networks to keep peering/transit options open           │
│                                                              │
│  4. SECURITY GROUPS ARE ALLOWLISTS                           │
│     → Start with zero inbound rules and add only what is     │
│       required for the specific workload                     │
│     → Reference other security groups by ID, not by CIDR,   │
│       whenever source and destination are in the same VPC    │
│     → Never use 0.0.0.0/0 on any inbound rule except ALBs   │
│     → Document the business reason for every rule added      │
│                                                              │
│  5. EVERY VPC NEEDS OBSERVABILITY                            │
│     → Enable VPC Flow Logs on every VPC from day one         │
│     → Send flow logs to CloudWatch and/or S3 for analysis    │
│     → Set up Reachability Analyzer tests for critical paths  │
│     → Alert on rejected traffic spikes — they signal         │
│       misconfigurations or attack attempts                   │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No AI mentions in Terraform comments, diagram labels,  │
│       or network documentation                               │
│     → All output reads as if written by a network architect  │
└──────────────────────────────────────────────────────────────┘
```

---

## 1. CIDR Planning

### CIDR Block Decision Tree

```
What is your organization's total IP address need?
│
├─ Single VPC, < 500 hosts → /24 (256 IPs) or /22 (1024 IPs)
│
├─ Single VPC, 500-5000 hosts → /20 (4096 IPs) or /18 (16384 IPs)
│
├─ Multiple VPCs, need peering → Plan non-overlapping blocks
│   ├─ Production:  10.0.0.0/16
│   ├─ Staging:     10.1.0.0/16
│   ├─ Development: 10.2.0.0/16
│   └─ Shared Svcs: 10.10.0.0/16
│
└─ Hybrid (on-prem + AWS) → Coordinate with on-prem ranges
    ├─ On-prem uses 10.x.x.x → Use 172.16.0.0/12 in AWS
    └─ On-prem uses 172.x.x.x → Use 10.0.0.0/8 in AWS
```

### CIDR Allocation Table — Production VPC (/16)

```
VPC: 10.0.0.0/16 (65,536 IPs)
│
├─ Public Subnets (Internet-facing)
│   ├─ 10.0.0.0/22   → us-east-1a  (1022 usable IPs)
│   ├─ 10.0.4.0/22   → us-east-1b  (1022 usable IPs)
│   └─ 10.0.8.0/22   → us-east-1c  (1022 usable IPs)
│
├─ Private Subnets (Application tier)
│   ├─ 10.0.16.0/20  → us-east-1a  (4094 usable IPs)
│   ├─ 10.0.32.0/20  → us-east-1b  (4094 usable IPs)
│   └─ 10.0.48.0/20  → us-east-1c  (4094 usable IPs)
│
├─ Isolated Subnets (Database tier — no internet)
│   ├─ 10.0.64.0/22  → us-east-1a  (1022 usable IPs)
│   ├─ 10.0.68.0/22  → us-east-1b  (1022 usable IPs)
│   └─ 10.0.72.0/22  → us-east-1c  (1022 usable IPs)
│
└─ Reserved
    └─ 10.0.128.0/17 → Future expansion (32,768 IPs)
```

### Rules for CIDR Planning

- Always reserve at least 50% of your VPC CIDR for future growth
- Never use /28 subnets for application workloads (only 11 usable IPs after AWS reserves 5)
- Private subnets should be larger than public subnets (apps run privately, only LBs go public)
- Isolated subnets can be smaller (databases have fewer instances)
- Document every CIDR allocation in a centralized spreadsheet or Terraform locals block

---

## 2. VPC Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              VPC: 10.0.0.0/16                                   │
│                                                                                 │
│  ┌─── us-east-1a ──────┐  ┌─── us-east-1b ──────┐  ┌─── us-east-1c ──────┐   │
│  │                      │  │                      │  │                      │   │
│  │ ┌──────────────────┐ │  │ ┌──────────────────┐ │  │ ┌──────────────────┐ │   │
│  │ │  Public Subnet   │ │  │ │  Public Subnet   │ │  │ │  Public Subnet   │ │   │
│  │ │  10.0.0.0/22     │ │  │ │  10.0.4.0/22     │ │  │ │  10.0.8.0/22     │ │   │
│  │ │  ┌──────┐  ┌───┐ │ │  │ │  ┌──────┐  ┌───┐ │ │  │ │  ┌──────┐       │ │   │
│  │ │  │ ALB  │  │NAT│ │ │  │ │  │ ALB  │  │NAT│ │ │  │ │  │ ALB  │       │ │   │
│  │ │  └──┬───┘  └─┬─┘ │ │  │ │  └──┬───┘  └─┬─┘ │ │  │ │  └──┬───┘       │ │   │
│  │ └─────┼────────┼───┘ │  │ └─────┼────────┼───┘ │  │ └─────┼────────────┘ │   │
│  │       │        │      │  │       │        │      │  │       │              │   │
│  │ ┌─────▼────────▼───┐ │  │ ┌─────▼────────▼───┐ │  │ ┌─────▼────────────┐ │   │
│  │ │  Private Subnet  │ │  │ │  Private Subnet  │ │  │ │  Private Subnet  │ │   │
│  │ │  10.0.16.0/20    │ │  │ │  10.0.32.0/20    │ │  │ │  10.0.48.0/20    │ │   │
│  │ │  ┌────┐ ┌────┐   │ │  │ │  ┌────┐ ┌────┐   │ │  │ │  ┌────┐ ┌────┐   │ │   │
│  │ │  │ECS │ │ECS │   │ │  │ │  │ECS │ │ECS │   │ │  │ │  │ECS │ │ECS │   │ │   │
│  │ │  └──┬─┘ └──┬─┘   │ │  │ │  └──┬─┘ └──┬─┘   │ │  │ │  └──┬─┘ └──┬─┘   │ │   │
│  │ └─────┼──────┼─────┘ │  │ └─────┼──────┼─────┘ │  │ └─────┼──────┼─────┘ │   │
│  │       │      │        │  │       │      │        │  │       │      │        │   │
│  │ ┌─────▼──────▼─────┐ │  │ ┌─────▼──────▼─────┐ │  │ ┌─────▼──────▼─────┐ │   │
│  │ │ Isolated Subnet  │ │  │ │ Isolated Subnet  │ │  │ │ Isolated Subnet  │ │   │
│  │ │ 10.0.64.0/22     │ │  │ │ 10.0.68.0/22     │ │  │ │ 10.0.72.0/22     │ │   │
│  │ │ ┌─────┐ ┌──────┐ │ │  │ │ ┌─────┐          │ │  │ │          ┌──────┐ │ │   │
│  │ │ │ RDS │ │Redis │ │ │  │ │ │ RDS │ (standby)│ │  │ │          │Redis │ │ │   │
│  │ │ │(pri)│ │(pri) │ │ │  │ │ │(rpl)│          │ │  │ │          │(rpl) │ │ │   │
│  │ │ └─────┘ └──────┘ │ │  │ │ └─────┘          │ │  │ │          └──────┘ │ │   │
│  │ └──────────────────┘ │  │ └──────────────────┘ │  │ └──────────────────┘ │   │
│  └──────────────────────┘  └──────────────────────┘  └──────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────┐  ┌────────────────────┐  ┌──────────────────────────┐  │
│  │ Internet Gateway    │  │ VPC Flow Logs → S3  │  │ DNS: Route 53 Private   │  │
│  │ (attached to VPC)   │  │ + CloudWatch Logs   │  │ Hosted Zone             │  │
│  └─────────────────────┘  └────────────────────┘  └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Subnet Tiers — Purpose and Routing

### Three-Tier Subnet Model

| Tier | Name | Internet Access | Route Table | What Goes Here |
|------|------|-----------------|-------------|----------------|
| **Public** | `public-*` | Full (IGW) | `0.0.0.0/0 → igw` | ALB, NAT Gateway, Bastion (if any) |
| **Private** | `private-*` | Outbound only (NAT) | `0.0.0.0/0 → nat-gw` | ECS tasks, Lambda, EC2 app servers |
| **Isolated** | `isolated-*` | None | Local routes only | RDS, ElastiCache, DocumentDB |

### Routing Table Setup

```
Public Route Table:
  10.0.0.0/16  → local
  0.0.0.0/0    → igw-xxxxxxxxx

Private Route Table (per AZ for HA NAT):
  10.0.0.0/16  → local
  0.0.0.0/0    → nat-xxxxxxxxx  (NAT Gateway in same AZ)

Isolated Route Table:
  10.0.0.0/16  → local
  (NO default route — completely air-gapped from internet)
```

---

## 4. Terraform Implementation

### VPC and Subnets

```hcl
locals {
  vpc_cidr = "10.0.0.0/16"
  azs      = ["us-east-1a", "us-east-1b", "us-east-1c"]

  public_subnets   = ["10.0.0.0/22", "10.0.4.0/22", "10.0.8.0/22"]
  private_subnets  = ["10.0.16.0/20", "10.0.32.0/20", "10.0.48.0/20"]
  isolated_subnets = ["10.0.64.0/22", "10.0.68.0/22", "10.0.72.0/22"]

  environment = "production"
  project     = "myapp"
}

resource "aws_vpc" "main" {
  cidr_block           = local.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = "${local.project}-${local.environment}-vpc"
    Environment = local.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${local.project}-${local.environment}-igw"
  }
}

# --- Public Subnets ---
resource "aws_subnet" "public" {
  count                   = length(local.public_subnets)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = local.public_subnets[count.index]
  availability_zone       = local.azs[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "${local.project}-${local.environment}-public-${local.azs[count.index]}"
    Tier = "public"
    # Required for EKS if using Kubernetes
    "kubernetes.io/role/elb" = "1"
  }
}

# --- Private Subnets ---
resource "aws_subnet" "private" {
  count             = length(local.private_subnets)
  vpc_id            = aws_vpc.main.id
  cidr_block        = local.private_subnets[count.index]
  availability_zone = local.azs[count.index]

  tags = {
    Name = "${local.project}-${local.environment}-private-${local.azs[count.index]}"
    Tier = "private"
    "kubernetes.io/role/internal-elb" = "1"
  }
}

# --- Isolated Subnets ---
resource "aws_subnet" "isolated" {
  count             = length(local.isolated_subnets)
  vpc_id            = aws_vpc.main.id
  cidr_block        = local.isolated_subnets[count.index]
  availability_zone = local.azs[count.index]

  tags = {
    Name = "${local.project}-${local.environment}-isolated-${local.azs[count.index]}"
    Tier = "isolated"
  }
}
```

### NAT Gateway Setup

```hcl
# --- NAT Gateway Decision ---
#
# Production: One NAT GW per AZ for high availability
#   Cost: ~$32/month per NAT GW + $0.045/GB processed
#   3 AZs = ~$96/month base cost
#
# Staging/Dev: Single NAT GW (save ~$64/month)
#   Tradeoff: Cross-AZ traffic + single point of failure

resource "aws_eip" "nat" {
  count  = local.environment == "production" ? length(local.azs) : 1
  domain = "vpc"

  tags = {
    Name = "${local.project}-${local.environment}-nat-eip-${count.index}"
  }
}

resource "aws_nat_gateway" "main" {
  count         = local.environment == "production" ? length(local.azs) : 1
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = {
    Name = "${local.project}-${local.environment}-nat-${count.index}"
  }

  depends_on = [aws_internet_gateway.main]
}

# --- Route Tables ---
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${local.project}-${local.environment}-public-rt"
  }
}

resource "aws_route_table" "private" {
  count  = local.environment == "production" ? length(local.azs) : 1
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }

  tags = {
    Name = "${local.project}-${local.environment}-private-rt-${count.index}"
  }
}

resource "aws_route_table" "isolated" {
  vpc_id = aws_vpc.main.id
  # No routes to internet — only local VPC traffic

  tags = {
    Name = "${local.project}-${local.environment}-isolated-rt"
  }
}

# --- Route Table Associations ---
resource "aws_route_table_association" "public" {
  count          = length(local.public_subnets)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count          = length(local.private_subnets)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[
    local.environment == "production" ? count.index : 0
  ].id
}

resource "aws_route_table_association" "isolated" {
  count          = length(local.isolated_subnets)
  subnet_id      = aws_subnet.isolated[count.index].id
  route_table_id = aws_route_table.isolated.id
}
```

---

## 5. Security Groups

### Security Group Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Security Group Map                     │
│                                                          │
│  Internet                                                │
│     │                                                    │
│     ▼                                                    │
│  ┌──────────────┐     ┌──────────────┐                  │
│  │  sg-alb      │────▶│  sg-app      │                  │
│  │  IN: 80,443  │     │  IN: from ALB│                  │
│  │  from 0.0.0.0│     │  only        │                  │
│  └──────────────┘     └──────┬───────┘                  │
│                              │                           │
│                     ┌────────┴────────┐                  │
│                     ▼                 ▼                  │
│              ┌──────────┐     ┌──────────────┐          │
│              │  sg-db   │     │  sg-cache     │          │
│              │  IN: 5432│     │  IN: 6379     │          │
│              │  from app│     │  from app     │          │
│              └──────────┘     └──────────────┘          │
└─────────────────────────────────────────────────────────┘
```

### Terraform Security Groups

```hcl
# --- ALB Security Group ---
resource "aws_security_group" "alb" {
  name_prefix = "${local.project}-${local.environment}-alb-"
  vpc_id      = aws_vpc.main.id
  description = "Security group for Application Load Balancer"

  ingress {
    description = "HTTP from internet"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS from internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "All outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name = "${local.project}-${local.environment}-alb-sg"
  }
}

# --- Application Security Group ---
resource "aws_security_group" "app" {
  name_prefix = "${local.project}-${local.environment}-app-"
  vpc_id      = aws_vpc.main.id
  description = "Security group for application containers"

  ingress {
    description     = "Traffic from ALB only"
    from_port       = 3000
    to_port         = 3001
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    description = "All outbound (for NAT gateway access)"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name = "${local.project}-${local.environment}-app-sg"
  }
}

# --- Database Security Group ---
resource "aws_security_group" "db" {
  name_prefix = "${local.project}-${local.environment}-db-"
  vpc_id      = aws_vpc.main.id
  description = "Security group for RDS PostgreSQL"

  ingress {
    description     = "PostgreSQL from app tier only"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  # No egress rule needed — RDS doesn't initiate outbound connections

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name = "${local.project}-${local.environment}-db-sg"
  }
}

# --- Cache Security Group ---
resource "aws_security_group" "cache" {
  name_prefix = "${local.project}-${local.environment}-cache-"
  vpc_id      = aws_vpc.main.id
  description = "Security group for ElastiCache Redis"

  ingress {
    description     = "Redis from app tier only"
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Name = "${local.project}-${local.environment}-cache-sg"
  }
}
```

---

## 6. Network ACLs (NACLs)

### When to Use NACLs vs Security Groups

```
Security Groups (stateful):
  ✅ Primary defense — use for all workload isolation
  ✅ Reference other SGs by ID (cleaner than CIDR)
  ✅ Automatically allow return traffic

NACLs (stateless):
  ✅ Subnet-level defense — defense in depth
  ✅ Explicit deny rules (SGs can only allow)
  ✅ Block entire CIDR ranges (e.g., known bad actors)
  ⚠️  Must define both inbound AND outbound rules
  ⚠️  Must allow ephemeral ports (1024-65535) for return traffic
```

### NACL Rules for Isolated Subnets (Database Tier)

```hcl
resource "aws_network_acl" "isolated" {
  vpc_id     = aws_vpc.main.id
  subnet_ids = aws_subnet.isolated[*].id

  # Allow PostgreSQL from private subnets
  ingress {
    rule_no    = 100
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "10.0.16.0/20"  # Private subnet AZ-a
    from_port  = 5432
    to_port    = 5432
  }

  ingress {
    rule_no    = 110
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "10.0.32.0/20"  # Private subnet AZ-b
    from_port  = 5432
    to_port    = 5432
  }

  ingress {
    rule_no    = 120
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "10.0.48.0/20"  # Private subnet AZ-c
    from_port  = 5432
    to_port    = 5432
  }

  # Allow Redis from private subnets
  ingress {
    rule_no    = 200
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "10.0.16.0/20"
    from_port  = 6379
    to_port    = 6379
  }

  # Deny all other inbound
  ingress {
    rule_no    = 900
    protocol   = "-1"
    action     = "deny"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
  }

  # Allow ephemeral ports outbound (return traffic)
  egress {
    rule_no    = 100
    protocol   = "tcp"
    action     = "allow"
    cidr_block = "10.0.0.0/16"
    from_port  = 1024
    to_port    = 65535
  }

  # Deny all other outbound (no internet access)
  egress {
    rule_no    = 900
    protocol   = "-1"
    action     = "deny"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
  }

  tags = {
    Name = "${local.project}-${local.environment}-isolated-nacl"
  }
}
```

---

## 7. VPC Flow Logs

### Flow Log Setup

```hcl
resource "aws_flow_log" "vpc" {
  vpc_id               = aws_vpc.main.id
  traffic_type         = "ALL"  # ACCEPT, REJECT, or ALL
  log_destination_type = "cloud-watch-logs"
  log_destination      = aws_cloudwatch_log_group.flow_logs.arn
  iam_role_arn         = aws_iam_role.flow_logs.arn

  # Custom log format — include all useful fields
  log_format = join(" ", [
    "$${version}",
    "$${account-id}",
    "$${interface-id}",
    "$${srcaddr}",
    "$${dstaddr}",
    "$${srcport}",
    "$${dstport}",
    "$${protocol}",
    "$${packets}",
    "$${bytes}",
    "$${start}",
    "$${end}",
    "$${action}",
    "$${log-status}",
    "$${vpc-id}",
    "$${subnet-id}",
    "$${az-id}",
    "$${flow-direction}",
  ])

  tags = {
    Name = "${local.project}-${local.environment}-vpc-flow-logs"
  }
}

resource "aws_cloudwatch_log_group" "flow_logs" {
  name              = "/aws/vpc/flow-logs/${local.project}-${local.environment}"
  retention_in_days = 30  # 30 days for production, 7 for staging

  tags = {
    Name = "${local.project}-${local.environment}-flow-logs"
  }
}

resource "aws_iam_role" "flow_logs" {
  name = "${local.project}-${local.environment}-flow-logs-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "vpc-flow-logs.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "flow_logs" {
  name = "${local.project}-${local.environment}-flow-logs-policy"
  role = aws_iam_role.flow_logs.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams",
      ]
      Effect   = "Allow"
      Resource = "*"
    }]
  })
}
```

### Useful Flow Log Queries (CloudWatch Logs Insights)

```
# Find rejected connections to database subnets
fields @timestamp, srcaddr, dstaddr, dstport, action
| filter action = "REJECT" and dstport = 5432
| sort @timestamp desc
| limit 50

# Top talkers by bytes transferred
fields srcaddr, dstaddr, bytes
| stats sum(bytes) as totalBytes by srcaddr
| sort totalBytes desc
| limit 20

# SSH attempts (should be zero in production)
fields @timestamp, srcaddr, dstaddr, action
| filter dstport = 22
| sort @timestamp desc
```

---

## 8. VPC Peering

### VPC Peering Architecture

```
┌────────────────────────┐          ┌────────────────────────┐
│  Production VPC        │          │  Shared Services VPC   │
│  10.0.0.0/16           │          │  10.10.0.0/16          │
│                        │  Peering │                        │
│  ┌──────────────────┐  │◄────────►│  ┌──────────────────┐  │
│  │ App Servers       │  │          │  │ CI/CD Runners    │  │
│  │ 10.0.16.0/20     │  │          │  │ 10.10.16.0/20    │  │
│  └──────────────────┘  │          │  └──────────────────┘  │
│                        │          │                        │
│  ┌──────────────────┐  │          │  ┌──────────────────┐  │
│  │ Databases         │  │          │  │ Monitoring       │  │
│  │ 10.0.64.0/22     │  │          │  │ 10.10.64.0/22    │  │
│  └──────────────────┘  │          │  └──────────────────┘  │
└────────────────────────┘          └────────────────────────┘
```

### VPC Peering Terraform

```hcl
resource "aws_vpc_peering_connection" "prod_to_shared" {
  vpc_id        = aws_vpc.production.id
  peer_vpc_id   = aws_vpc.shared_services.id
  peer_region   = "us-east-1"  # Same region
  auto_accept   = true         # Only works same account + region

  tags = {
    Name = "prod-to-shared-services"
  }
}

# Add routes in BOTH VPCs
resource "aws_route" "prod_to_shared" {
  count                     = length(aws_route_table.private)
  route_table_id            = aws_route_table.private[count.index].id
  destination_cidr_block    = "10.10.0.0/16"
  vpc_peering_connection_id = aws_vpc_peering_connection.prod_to_shared.id
}

resource "aws_route" "shared_to_prod" {
  count                     = length(aws_route_table.shared_private)
  route_table_id            = aws_route_table.shared_private[count.index].id
  destination_cidr_block    = "10.0.0.0/16"
  vpc_peering_connection_id = aws_vpc_peering_connection.prod_to_shared.id
}
```

---

## 9. Cost Implications

| Resource | Monthly Cost (us-east-1) | Notes |
|----------|-------------------------|-------|
| VPC | Free | No charge for VPC itself |
| Subnets | Free | No charge for subnets |
| Internet Gateway | Free | No hourly charge, pay for data transfer |
| NAT Gateway | ~$32/month each | + $0.045/GB processed |
| 3 NAT GWs (prod) | ~$96/month | HA setup, one per AZ |
| 1 NAT GW (staging) | ~$32/month | Single AZ, cost-optimized |
| Elastic IP | Free (if attached) | $3.60/month if unattached |
| VPC Flow Logs | ~$0.50/GB ingested | CloudWatch Logs pricing |
| VPC Peering | Free | No charge, pay for cross-AZ data |
| Cross-AZ data transfer | $0.01/GB | Between AZs in same region |

### Cost Optimization Tips

1. **Staging/Dev**: Use a single NAT Gateway instead of one per AZ (saves ~$64/month)
2. **Flow Logs**: Set retention to 7 days for non-prod (vs 30+ for prod)
3. **VPC Endpoints**: Use Gateway endpoints for S3 and DynamoDB (free, avoids NAT costs)
4. **Consolidate small VPCs**: Each VPC with NAT costs at minimum $32/month

---

## 10. Security Considerations

- Never place databases in public subnets — always use isolated subnets with no internet route
- Use `name_prefix` instead of `name` for security groups to avoid conflicts during replacement
- Enable VPC flow logs in ALL environments (required for compliance: SOC2, HIPAA, PCI-DSS)
- Restrict SSH access to bastion hosts only — never open port 22 to 0.0.0.0/0
- Use VPC endpoints for AWS services (S3, DynamoDB, ECR, CloudWatch) to keep traffic off the internet
- Review security group rules quarterly — remove unused rules
- Tag all resources with `Environment`, `ManagedBy`, and `Project` for auditability

---

## 11. Common Mistakes / Anti-Patterns

| Mistake | Why It's Bad | Fix |
|---------|-------------|-----|
| Using 0.0.0.0/0 in security group ingress | Opens to entire internet | Reference specific SG IDs or CIDR blocks |
| Single NAT Gateway for production | Single point of failure | One NAT GW per AZ |
| Overlapping CIDRs between VPCs | Cannot peer VPCs with overlap | Plan CIDR blocks upfront across all VPCs |
| /28 subnets for app workloads | Only 11 usable IPs | Use /20 or larger for private subnets |
| No flow logs | Blind to network threats | Enable on all VPCs |
| Hardcoded CIDR blocks in SG rules | Breaks when subnets change | Reference security group IDs instead |
| Not using `create_before_destroy` | SG replacement causes downtime | Always set lifecycle on security groups |
| Placing RDS in private (not isolated) subnet | DB has internet path via NAT | Use isolated subnet with no default route |

---

## 12. Verification Commands

```bash
# List all VPCs
aws ec2 describe-vpcs --query "Vpcs[*].{ID:VpcId,CIDR:CidrBlock,Name:Tags[?Key=='Name']|[0].Value}" --output table

# List all subnets in a VPC
aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-xxxxxxxx" \
  --query "Subnets[*].{ID:SubnetId,CIDR:CidrBlock,AZ:AvailabilityZone,Name:Tags[?Key=='Name']|[0].Value}" --output table

# Check route tables
aws ec2 describe-route-tables --filters "Name=vpc-id,Values=vpc-xxxxxxxx" \
  --query "RouteTables[*].{ID:RouteTableId,Routes:Routes[*].{Dest:DestinationCidrBlock,Target:GatewayId||NatGatewayId}}" --output json

# Verify security group rules
aws ec2 describe-security-groups --group-ids sg-xxxxxxxx \
  --query "SecurityGroups[*].{Name:GroupName,Ingress:IpPermissions,Egress:IpPermissionsEgress}" --output json

# Check flow log status
aws ec2 describe-flow-logs --filter "Name=resource-id,Values=vpc-xxxxxxxx" --output table

# Verify NAT Gateway status
aws ec2 describe-nat-gateways --filter "Name=vpc-id,Values=vpc-xxxxxxxx" \
  --query "NatGateways[*].{ID:NatGatewayId,State:State,SubnetId:SubnetId,AZ:Tags[?Key=='Name']|[0].Value}" --output table
```

<!--
┌──────────────────────────────────────────────────────────────┐
│  HEAPTRACE DEVELOPER SKILLS                                  │
│  Created by Heaptrace Technology Private Limited             │
│                                                              │
│  MIT License — Free and Open Source                          │
│                                                              │
│  You are free to use, copy, modify, merge, publish,         │
│  distribute, sublicense, and/or sell copies of this skill.   │
│  No restrictions. No attribution required.                   │
│                                                              │
│  heaptrace.com | github.com/heaptracetechnology              │
└──────────────────────────────────────────────────────────────┘
-->

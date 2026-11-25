---
name: network-patterns
description: "Networking and DNS patterns: CIDR planning, VPC endpoints in Terraform, Route53 latency-based multi-region routing, private hosted zones for Kubernetes services, CoreDNS configuration, and a DNS debugging toolkit. Use when planning networks or tracking down DNS and connectivity problems."
---

# Networking & DNS Patterns

VPC design, CIDR planning, Route53 configurations, Transit Gateway, and DNS-based failover.

## CIDR Planning Reference

```
# RFC 1918 private address space
10.0.0.0/8        # 16.7M addresses (use for large orgs/multi-region)
172.16.0.0/12     # 1M addresses
192.168.0.0/16    # 65K addresses (avoid: commonly used in home networks)

# Multi-region CIDR allocation (no overlap -- critical for VPC peering/TGW)
Region us-east-1:   10.0.0.0/16    (65K addresses)
Region us-west-2:   10.1.0.0/16
Region eu-west-1:   10.2.0.0/16
Region ap-east-1:   10.3.0.0/16

# Within a /16: three tiers, three AZs
Public:   10.0.1.0/24, 10.0.2.0/24, 10.0.3.0/24   (/24 = 256 IPs each)
Private:  10.0.10.0/24, 10.0.11.0/24, 10.0.12.0/24
Database: 10.0.20.0/24, 10.0.21.0/24, 10.0.22.0/24
# Reserve room for future tiers in 10.0.30-99.x.x
```

## VPC with VPC Endpoints (Terraform)

```hcl
# VPC Endpoints: keep AWS API traffic off the internet
# Eliminates NAT Gateway costs for S3/DynamoDB

# S3 Gateway Endpoint (free)
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = module.vpc.vpc_id
  service_name      = "com.amazonaws.${var.region}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = module.vpc.private_route_table_ids

  tags = { Name = "s3-endpoint" }
}

# ECR Interface Endpoints (avoid NAT for image pulls)
resource "aws_vpc_endpoint" "ecr_dkr" {
  vpc_id              = module.vpc.vpc_id
  service_name        = "com.amazonaws.${var.region}.ecr.dkr"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = module.vpc.private_subnets
  security_group_ids  = [aws_security_group.vpc_endpoints.id]
  private_dns_enabled = true  # Override public DNS to route through endpoint
}

resource "aws_vpc_endpoint" "ecr_api" {
  vpc_id              = module.vpc.vpc_id
  service_name        = "com.amazonaws.${var.region}.ecr.api"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = module.vpc.private_subnets
  security_group_ids  = [aws_security_group.vpc_endpoints.id]
  private_dns_enabled = true
}

# Also add: logs, secretsmanager, sts, ssm, ssmmessages
locals {
  interface_endpoints = ["logs", "secretsmanager", "sts", "ssm", "ssmmessages", "ec2messages"]
}

resource "aws_vpc_endpoint" "interface" {
  for_each = toset(local.interface_endpoints)

  vpc_id              = module.vpc.vpc_id
  service_name        = "com.amazonaws.${var.region}.${each.value}"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = module.vpc.private_subnets
  security_group_ids  = [aws_security_group.vpc_endpoints.id]
  private_dns_enabled = true
}

resource "aws_security_group" "vpc_endpoints" {
  name   = "vpc-endpoints-sg"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [module.vpc.vpc_cidr_block]
  }
}
```

## Route53 Latency-Based Routing (Multi-Region)

```hcl
# Route to the lowest-latency region from user's location
resource "aws_route53_record" "api_us_east_1" {
  provider = aws.us-east-1
  zone_id  = aws_route53_zone.public.zone_id
  name     = "api.example.com"
  type     = "A"

  latency_routing_policy {
    region = "us-east-1"
  }

  set_identifier  = "us-east-1"
  health_check_id = aws_route53_health_check.us_east_1.id

  alias {
    name                   = aws_lb.us_east_1.dns_name
    zone_id                = aws_lb.us_east_1.zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "api_eu_west_1" {
  provider = aws.eu-west-1
  zone_id  = aws_route53_zone.public.zone_id
  name     = "api.example.com"
  type     = "A"

  latency_routing_policy {
    region = "eu-west-1"
  }

  set_identifier  = "eu-west-1"
  health_check_id = aws_route53_health_check.eu_west_1.id

  alias {
    name                   = aws_lb.eu_west_1.dns_name
    zone_id                = aws_lb.eu_west_1.zone_id
    evaluate_target_health = true
  }
}
```

## Private Hosted Zone for Kubernetes Services

```hcl
# Private zone for internal service mesh
resource "aws_route53_zone" "internal" {
  name = "internal.example.com"
  vpc { vpc_id = module.vpc.vpc_id }
}

# Service endpoints (stable DNS names for databases, caches)
resource "aws_route53_record" "postgres_primary" {
  zone_id = aws_route53_zone.internal.zone_id
  name    = "postgres.internal.example.com"
  type    = "CNAME"
  ttl     = 60  # Low TTL: failover happens in ~60s
  records = [aws_db_instance.postgres.address]
}

resource "aws_route53_record" "redis" {
  zone_id = aws_route53_zone.internal.zone_id
  name    = "redis.internal.example.com"
  type    = "CNAME"
  ttl     = 60
  records = [aws_elasticache_replication_group.redis.primary_endpoint_address]
}
```

## CoreDNS Configuration for Kubernetes

```yaml
# ConfigMap: CoreDNS with custom upstream for internal domains
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health {
           lameduck 5s
        }
        ready
        # Route .internal.example.com to Route53 private resolver
        internal.example.com:53 {
            forward . 169.254.169.253  # AWS Route53 resolver
            cache 30
        }
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
           ttl 30
        }
        prometheus :9153
        forward . /etc/resolv.conf {
           max_concurrent 1000
        }
        cache 30
        loop
        reload
        loadbalance
    }
```

## DNS Debugging Toolkit

```bash
# Query specific DNS record
dig api.example.com A +short
dig api.example.com AAAA +short
dig @8.8.8.8 api.example.com A  # Use Google's resolver

# Check all routing policy records
dig api.example.com A +additional  # Shows which endpoint responded

# Trace DNS resolution path
dig +trace api.example.com

# Check TTL remaining
dig api.example.com A | grep -A1 "ANSWER SECTION"

# Test from inside Kubernetes pod
kubectl run -it --rm dns-debug --image=busybox --restart=Never -- sh -c "
  nslookup kubernetes.default
  nslookup myapp.production.svc.cluster.local
  cat /etc/resolv.conf
"

# Check VPC DNS resolver
dig @169.254.169.253 internal.example.com A  # AWS VPC resolver endpoint

# Verify Route53 health check passing
aws route53 get-health-check-status --health-check-id $HEALTH_CHECK_ID \
  --query 'HealthCheckObservations[].StatusReport.Status'

# Check Route53 resolver query logs
aws logs filter-log-events \
  --log-group-name /aws/route53/example.com \
  --filter-pattern '"NOERROR"' \
  --start-time $(date -d '-1 hour' +%s)000
```

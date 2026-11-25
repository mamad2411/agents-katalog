---
name: networking
description: "Design and manage GCP networking: VPC, subnets, firewall rules, Cloud Load Balancing, Cloud Armor, Private Google Access, and Shared VPC. Deny-by-default firewall posture. Warns before creating external load balancers (billable). Use when the user mentions: networking GCP, cloud load balancer, VPN GCP, cloud NAT, network design GCP."
license: MIT
metadata:
  "googlecloud-plugin/version": "0.1"
  "googlecloud-plugin/triggers": "VPC, firewall, networking GCP, cloud load balancer, cloud armor, private google access, shared VPC, subnet, VPN GCP, cloud NAT, network design GCP"
  "googlecloud-plugin/required-scopes": "compute.firewalls.create, compute.firewalls.get, compute.firewalls.list, compute.networks.create, compute.networks.get, compute.subnetworks.create, compute.subnetworks.get"
---

# Networking

Design and manage GCP VPC networks, connectivity, and traffic management. Deny-by-default; open only what is necessary.

## Core Patterns

### Create a VPC with a subnet

```bash
gcloud compute networks create VPC_NAME \
  --subnet-mode=custom \
  --project=PROJECT_ID

gcloud compute networks subnets create SUBNET_NAME \
  --network=VPC_NAME \
  --region=REGION \
  --range=10.0.0.0/24 \
  --enable-private-ip-google-access \
  --project=PROJECT_ID
```

### Deny-by-default firewall (then open minimally)

```bash
# Deny all ingress (GCP default is deny-all for custom VPCs)
# Add targeted allow rules only:
gcloud compute firewall-rules create allow-internal \
  --network=VPC_NAME \
  --direction=INGRESS \
  --action=ALLOW \
  --rules=tcp:0-65535,udp:0-65535,icmp \
  --source-ranges=10.0.0.0/8 \
  --project=PROJECT_ID
```

### Enable Private Google Access

```bash
gcloud compute networks subnets update SUBNET_NAME \
  --region=REGION \
  --enable-private-ip-google-access \
  --project=PROJECT_ID
```

### Cloud NAT (outbound internet without public IPs)

```bash
gcloud compute routers create ROUTER_NAME \
  --network=VPC_NAME \
  --region=REGION

gcloud compute routers nats create NAT_NAME \
  --router=ROUTER_NAME \
  --region=REGION \
  --auto-allocate-nat-external-ips \
  --nat-all-subnet-ip-ranges
```

## Safety Rules

- Never use `0.0.0.0/0` as a source range for SSH or RDP — use IAP tunnels instead
- Enable Private Google Access on all subnets to avoid routing through internet
- Cost warning: external load balancers and Cloud Armor bill per rule and per GB

## References

- [VPC Overview](https://cloud.google.com/vpc/docs/vpc)
- [VPC Firewall Rules](https://cloud.google.com/vpc/docs/firewalls)
- [Cloud Load Balancing](https://cloud.google.com/load-balancing/docs/load-balancing-overview)
- [Cloud Armor Overview](https://cloud.google.com/armor/docs/cloud-armor-overview)
- [Private Google Access](https://cloud.google.com/vpc/docs/private-google-access)
- [Network Security Architecture](https://cloud.google.com/architecture/framework/security/network-security)

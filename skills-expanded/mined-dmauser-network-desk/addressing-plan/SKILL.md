# Addressing Plan — Multi-Cloud CIDR and IPAM Strategy

## Overview

A coherent global addressing plan is the foundation of any multi-cloud network. Overlapping CIDR ranges between clouds cause routing ambiguity, break transitive connectivity, and force complex NAT workarounds. This skill provides allocation strategies, NAT solutions for legacy overlaps, route summarization guidance, IPv6 considerations, and IPAM tooling recommendations.

## Global CIDR Plan: Non-Overlapping Across All Environments

The cardinal rule of multi-cloud addressing is: **no CIDR range may overlap between any two environments that need to communicate**. This includes all Azure VNets, AWS VPCs, GCP VPC subnets, on-premises networks, and any partner/SaaS integrations that use private addressing.

Plan the address space before deploying any cloud resources. Retrofitting addressing after workloads are running is disruptive and error-prone.

## RFC 1918 Allocation Strategy

Divide the `10.0.0.0/8` block across clouds and on-premises to provide ample room for growth while maintaining clean summarization boundaries:

| Environment | CIDR Block | Usable Range | Capacity |
|---|---|---|---|
| **Azure** | `10.0.0.0/10` | 10.0.0.0 – 10.63.255.255 | ~4.2M addresses |
| **AWS** | `10.64.0.0/10` | 10.64.0.0 – 10.127.255.255 | ~4.2M addresses |
| **GCP** | `10.128.0.0/10` | 10.128.0.0 – 10.191.255.255 | ~4.2M addresses |
| **On-Premises** | `10.192.0.0/10` | 10.192.0.0 – 10.255.255.255 | ~4.2M addresses |

### Sub-Allocation Within Each Cloud

Within each /10 block, assign per-region and per-environment (dev/staging/prod) allocations:

```
Azure (10.0.0.0/10):
  East US (prod):   10.0.0.0/14   → 10.0.0.0 – 10.3.255.255
  East US (dev):    10.4.0.0/14   → 10.4.0.0 – 10.7.255.255
  West US (prod):   10.8.0.0/14   → 10.8.0.0 – 10.11.255.255
  West Europe (prod): 10.12.0.0/14 → 10.12.0.0 – 10.15.255.255
  Reserved:         10.16.0.0/12  → future regions

AWS (10.64.0.0/10):
  us-east-1 (prod): 10.64.0.0/14  → 10.64.0.0 – 10.67.255.255
  us-east-1 (dev):  10.68.0.0/14  → 10.68.0.0 – 10.71.255.255
  us-west-2 (prod): 10.72.0.0/14  → 10.72.0.0 – 10.75.255.255
  eu-west-1 (prod): 10.76.0.0/14  → 10.76.0.0 – 10.79.255.255
  Reserved:         10.80.0.0/12  → future regions

GCP (10.128.0.0/10):
  us-east1 (prod):  10.128.0.0/14 → 10.128.0.0 – 10.131.255.255
  us-central1 (prod): 10.132.0.0/14
  europe-west1 (prod): 10.136.0.0/14
  Reserved:         10.144.0.0/12 → future regions
```

Use `172.16.0.0/12` for shared services, DMZ, and management networks. Reserve `192.168.0.0/16` for lab, sandbox, or isolated environments that will never be routed to production.

## NAT Solutions for Overlapping Ranges

When legacy environments have overlapping CIDR ranges that cannot be re-addressed, NAT provides a workaround at the cost of operational complexity.

**Azure NAT Gateway** — provides outbound SNAT for VNet subnets. Supports up to 16 public IP addresses and 64,000 SNAT ports per IP. Does not solve private-to-private overlap; use Azure Firewall DNAT rules or NVA-based NAT for private overlaps.

**AWS NAT Gateway** — managed NAT for outbound internet access from private subnets. For private-to-private overlap resolution, use AWS PrivateLink (which NATs to the service VPC's address space) or deploy an EC2-based NAT instance with iptables rules.

**GCP Cloud NAT** — provides outbound NAT for GCE instances and GKE nodes without external IPs. For private overlap scenarios, use GCP's internal TCP/UDP load balancer with custom routes or deploy a NAT appliance on a GCE instance.

**Double-NAT Pattern** — when both sides of a connection have overlapping ranges, deploy NAT on both ends. Each side translates its local addresses to a unique "transit" range before sending traffic across the interconnect. This requires careful coordination of the transit CIDR (e.g., `100.64.0.0/10` — RFC 6598 shared address space) and introduces bidirectional state tracking.

## Route Summarization at Cloud Boundaries

Advertise summarized prefixes at each cloud boundary to keep routing tables manageable:

```
Azure advertises:   10.0.0.0/10   (covers all Azure VNets)
AWS advertises:     10.64.0.0/10  (covers all AWS VPCs)
GCP advertises:     10.128.0.0/10 (covers all GCP subnets)
On-prem advertises: 10.192.0.0/10 (covers all DC networks)
```

Avoid advertising individual /24 or /28 subnet prefixes across cloud boundaries. Summarization reduces BGP table size, lowers convergence time, and simplifies route filtering. Use more-specific routes only within each cloud's internal routing domain.

## IPv6 Considerations for Multi-Cloud

All three major clouds support dual-stack (IPv4 + IPv6) networking:

- **Azure:** VNets support dual-stack. Assign a /48 or /56 IPv6 CIDR per VNet. Azure provides a unique local address (ULA) range or you can bring your own IPv6 prefixes (BYOIP).
- **AWS:** VPCs support dual-stack with Amazon-provided /56 IPv6 CIDR or BYOIP. All subnets can be dual-stack.
- **GCP:** VPCs support dual-stack subnets with internal IPv6 (ULA) or external IPv6 ranges. GKE supports dual-stack clusters.

For multi-cloud IPv6, use Provider Aggregatable (PA) addresses from each cloud or bring your own Provider Independent (PI) /48 allocation and announce it via BGP on private interconnects. Avoid relying on link-local IPv6 for cross-cloud routing — use globally routable or ULA prefixes with explicit route configuration.

## Documentation Template for IP Address Management

Maintain a living document (or IPAM database) with the following fields for every allocation:

| Field | Description |
|---|---|
| CIDR Block | The allocated range (e.g., 10.0.0.0/16) |
| Cloud Provider | Azure / AWS / GCP / On-Prem |
| Region | Cloud region or data center location |
| Environment | prod / staging / dev / sandbox |
| VNet/VPC Name | Resource name in the cloud provider |
| Subscription/Account | Azure subscription ID, AWS account ID, or GCP project |
| Owner | Team or service owner |
| Purpose | Workload description |
| Allocated Date | When the range was assigned |
| Utilization (%) | Current usage percentage |
| Notes | Special considerations, NAT requirements, expiry |

## IPAM Tools

**Azure IPAM** — Microsoft's open-source IPAM solution for Azure (github.com/Azure/ipam). Deploys as an App Service with Cosmos DB backend. Provides a UI and REST API for tracking VNet address space utilization across subscriptions.

**NetBox** — Open-source infrastructure resource modeling (IRM) tool by DigitalOcean. Comprehensive IPAM with prefix hierarchy, VLAN management, and REST/GraphQL APIs. Deploy as a container or VM. Supports multi-cloud tracking through custom fields and tags. Install via:

```bash
# Docker-based deployment
git clone -b release https://github.com/netbox-community/netbox-docker.git
cd netbox-docker
docker compose up -d
```

**phpIPAM** — Open-source PHP-based IPAM with subnet management, IP tracking, and VLAN management. Lighter weight than NetBox, suitable for smaller environments. Supports REST API for automation integration.

**Infoblox** — Enterprise-grade DDI (DNS, DHCP, IPAM) platform with multi-cloud discovery and integration plugins for Azure, AWS, and GCP. Provides automated IP allocation and conflict detection across hybrid environments.

**Analysis only — verify against vendor documentation before applying.**

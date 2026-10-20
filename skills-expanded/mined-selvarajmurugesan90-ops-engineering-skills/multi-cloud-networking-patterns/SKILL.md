---
name: multi-cloud-networking-patterns
description: >
  Guides designing hub-and-spoke or transit network topologies, IP address
  management, and secure interconnects (VPN, direct/express connections,
  private endpoints, and cross-cloud peering) across AWS, Azure, and GCP.
  Use when a user asks to "design a hub-and-spoke network", "connect two
  VPCs/VNets", "set up a site-to-site VPN or direct connect", "plan IP
  address space across accounts", "connect AWS to Azure/GCP", "avoid
  overlapping CIDR blocks", or "expose a service privately without a
  public IP".
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cloud
  maturity: stable
---

# Multi-Cloud Networking Patterns

## Purpose

Network design decisions made when the first VPC/VNet is created are
among the hardest to unwind later — overlapping CIDR blocks block future
peering, a flat network with no segmentation makes blast-radius
containment impossible, and ad hoc point-to-point VPN connections become
an unmanageable mesh as account/subscription/project count grows. This
skill defines the hub-and-spoke (or transit) topology pattern that scales
across AWS, Azure, and GCP, the IP address management (IPAM) discipline
that prevents collisions, and the connectivity options (VPN, dedicated
interconnects, private endpoints) for both intra-cloud and cross-cloud
traffic — so networking is a deliberate, centrally managed layer rather
than an emergent mess of one-off peering connections.

## When to use

- Designing the network topology for a new landing zone (paired with the
  relevant `*-landing-zone-setup` skill).
- Connecting a new spoke VPC/VNet/project-VPC to existing shared network
  infrastructure.
- Planning IP address ranges across accounts/subscriptions/projects
  before any are created, to avoid future collisions.
- Setting up a site-to-site VPN or dedicated connection (AWS Direct
  Connect, Azure ExpressRoute, GCP Cloud Interconnect) to on-premises.
- Connecting workloads across cloud providers (e.g. an AWS-hosted service
  calling a GCP-hosted data warehouse privately).
- Replacing public-endpoint access to managed services (databases,
  storage, message queues) with private connectivity.
- Diagnosing "why can't service A reach service B" across account/
  subscription/project or VPC/VNet boundaries.

## Prerequisites & environment

- The relevant landing zone (AWS Organizations/Control Tower, Azure
  Management Groups, or GCP folders) already exists, since network hub
  placement follows the account/subscription/project structure — see
  the three `*-landing-zone-setup` skills.
- Terraform ≥ 1.5 with the relevant provider(s) if managing network
  infrastructure as code; for cross-cloud Terraform, expect to run
  multiple provider blocks (`aws`, `azurerm`, `google`) in the same or
  linked configurations.
- A single source of truth for IP address allocation before any
  VPC/VNet is created — a spreadsheet-as-code, AWS VPC IPAM, Azure
  Virtual Network Manager IPAM, or a third-party tool (e.g. phpIPAM,
  NetBox) for anything beyond a handful of networks.
- Decide the connectivity model up front: hub-and-spoke (single hub per
  region handles all shared connectivity/inspection) vs. full transit
  (AWS Transit Gateway / Azure Virtual WAN / GCP Network Connectivity
  Center) for topologies spanning many regions or requiring dynamic
  routing at scale.
- For cross-cloud connectivity: an understanding of which side initiates
  the VPN (each cloud's VPN gateway has different BGP ASN defaults and
  quirks — confirm compatible IKE/IPsec parameters before provisioning).

## Step-by-step guidance

1. **Allocate IP address space centrally before creating any VPC/VNet.**
   Reserve non-overlapping CIDR blocks per region and per
   environment/business unit, sized with real headroom (a `/16` per
   region is a reasonable starting allocation for most mid-size
   organizations; carve `/20`s or `/22`s per spoke from it). Register
   the plan in AWS VPC IPAM, Azure vNet Manager IPAM, or a lightweight
   IPAM-as-code file reviewed in the same PR process as the network
   Terraform.

2. **Choose the hub topology per cloud:**
   - **AWS**: Transit Gateway (TGW) in the Network account, with spoke
     VPCs attached via TGW attachments; route tables per attachment to
     control which spokes can reach which.
     ```hcl
     resource "aws_ec2_transit_gateway" "hub" {
       description                    = "org-hub-tgw"
       default_route_table_association = "disable"
       default_route_table_propagation = "disable"
     }

     resource "aws_ec2_transit_gateway_vpc_attachment" "checkout_prod" {
       transit_gateway_id = aws_ec2_transit_gateway.hub.id
       vpc_id             = aws_vpc.checkout_prod.id
       subnet_ids         = aws_subnet.checkout_prod_tgw[*].id
     }
     ```
   - **Azure**: either a classic hub VNet with VNet peering to each
     spoke (simpler, scales to dozens of spokes) or Azure Virtual WAN
     (managed hub-and-spoke plus built-in VPN/ExpressRoute termination,
     better above ~20-30 spokes or multiple regions).
   - **GCP**: Shared VPC is itself the hub model — service projects
     attach directly to subnets in the host project's VPC rather than
     peering separate VPCs; use Network Connectivity Center only when
     you need a hub for multiple *independent* VPCs or hybrid
     connectivity fan-out.

3. **Segment with route tables and firewall/NSG/firewall-policy rules**,
   not by relying on topology alone. Explicitly deny spoke-to-spoke
   traffic by default in the hub's route table/NSG and allow only the
   specific flows required (e.g. `checkout-prod` can reach
   `payments-prod`'s API subnet on 443, nothing else).

4. **Connect to on-premises or another cloud with redundant paths.**
   Prefer a dedicated connection with a VPN backup:
   - AWS Direct Connect + Site-to-Site VPN as failover.
   - Azure ExpressRoute + VPN Gateway as failover.
   - GCP Cloud Interconnect (Dedicated or Partner) + Cloud VPN as
     failover.
   For cross-cloud connectivity without a physical interconnect,
   provision a site-to-site VPN between each cloud's VPN gateway, e.g.
   AWS to GCP:
   ```hcl
   resource "google_compute_vpn_gateway" "to_aws" {
     name    = "vpn-gw-to-aws"
     network = google_compute_network.hub.id
   }
   # Paired on the AWS side with a Customer Gateway pointing at the
   # GCP VPN gateway's public IP, and a Site-to-Site VPN Connection.
   ```
   Confirm both sides agree on IKEv2 parameters, matching pre-shared
   keys (stored in a secrets manager, never in Terraform state
   unencrypted), and non-overlapping CIDR ranges before cutover.

5. **Prefer private endpoints over public exposure for managed services.**
   Use AWS PrivateLink / VPC endpoints, Azure Private Link/Private
   Endpoint, or GCP Private Service Connect so traffic to managed
   databases, storage, or SaaS APIs never traverses the public internet,
   even when the consumer and producer are in different
   accounts/subscriptions/projects.

6. **Centralize DNS resolution.** Use Route 53 Resolver rules shared via
   Resource Access Manager (AWS), Azure Private DNS zones linked to
   every spoke VNet, or a GCP Cloud DNS private zone shared via Shared
   VPC — so every spoke resolves internal names consistently without
   per-spoke DNS configuration.

7. **Test connectivity and failover before workloads depend on it.**
   Validate spoke-to-spoke deny-by-default behavior, confirm the VPN
   backup path activates if the dedicated connection drops (a
   controlled BGP failover test), and confirm private endpoint DNS
   resolves correctly from every spoke.

## Best practices

- **Reserve IP space with real headroom** — resizing a VPC/VNet CIDR
  after workloads are deployed is disruptive; running out of address
  space in a spoke is one of the most common reasons for painful
  re-platforming.
- **Deny spoke-to-spoke traffic by default**; require an explicit,
  reviewed rule for any cross-spoke flow — this keeps blast radius
  contained if one spoke is compromised.
- **Use dedicated interconnects with VPN failover for anything
  production-critical** crossing to on-premises or another cloud — a
  VPN-only connection has materially different latency/throughput/
  reliability characteristics than a dedicated line.
- **Prefer managed transit services (Transit Gateway, Virtual WAN,
  Network Connectivity Center) over a manual full-mesh of peering
  connections** once spoke count exceeds roughly 10 — full-mesh VNet/VPC
  peering does not support transitive routing and becomes an O(n²)
  management burden.
- **Route through private endpoints for managed services** rather than
  allowing public-endpoint access with an IP allowlist — allowlists rot
  as source IPs change (NAT gateway IP rotation, autoscaling).
- Treat **cross-cloud VPNs as a stopgap for moderate, steady traffic**,
  not high-throughput data pipelines — for sustained large data transfer
  between clouds, evaluate a dedicated interconnect or a data-transfer
  service rather than routing bulk traffic over IPsec VPN.
- Keep **network topology and firewall rules as code**, reviewed with
  the same rigor as IAM changes — a misconfigured route or overly broad
  security group rule is as much a security incident as an IAM
  over-grant.

## Common pitfalls

- **Symptom:** Two spoke VPCs/VNets can't be connected to the hub, or a
  Terraform apply fails with a CIDR overlap error.
  **Fix:** No central IPAM existed before the spokes were created, so
  their CIDR ranges were chosen independently and now overlap. There is
  no clean fix short of re-IPing one of the spokes (disruptive); prevent
  recurrence by requiring an IPAM allocation as a precondition in the
  account/subscription/project vending pipeline (see the landing-zone
  skills) before any VPC/VNet Terraform can apply.

- **Symptom:** A workload in `spoke-a` can unexpectedly reach a database
  in `spoke-b` that it was never meant to talk to.
  **Fix:** The hub's route table/NSG allowed all spoke-to-spoke traffic
  by default instead of denying by default. Rebuild the routing/firewall
  policy to deny spoke-to-spoke traffic unless an explicit rule exists,
  and audit existing flows with VPC Flow Logs / NSG Flow Logs / VPC Flow
  Logs (GCP) to find any other unintended paths before tightening.

- **Symptom:** A site-to-site VPN between two clouds connects but no
  traffic passes, or it drops intermittently.
  **Fix:** Mismatched IKE/IPsec phase 1/phase 2 parameters (encryption
  algorithm, DH group, SA lifetime) between the two cloud's VPN gateway
  defaults — each provider ships different defaults. Explicitly set
  matching parameters on both sides rather than relying on
  auto-negotiation, and check both sides' VPN tunnel logs (not just one)
  when diagnosing.

- **Symptom:** Latency or egress cost between cross-cloud services is
  much higher than expected for what should be routine API traffic.
  **Fix:** Traffic is traversing a VPN over the public internet path
  instead of a private/dedicated interconnect, or is routing through an
  unnecessary extra hop (e.g. through an on-prem hub instead of directly
  between clouds). Trace the actual path with traceroute/VPC Flow Logs
  and consider a direct interconnect or Private Service Connect/
  PrivateLink pairing if the traffic volume justifies it.

- **Symptom:** Deleting or "cleaning up" an unused-looking VPC/VNet as
  part of a cost or hygiene pass breaks a production workload
  elsewhere.
  **Fix:** **Never force-delete a VPC/VNet, its peering connections, or
  its route tables without first confirming no attachments, peerings, or
  DNS zones reference it** — a VPC that looks idle from one account's
  view may still be the transit path or DNS resolver target for another.
  Check Transit Gateway/Virtual WAN/Shared VPC attachments and Resource
  Access Manager shares before any teardown, and require an explicit
  human sign-off for network deletions the same way you would for a
  storage account or database.

## Worked example

**Scenario:** A company has three AWS spoke VPCs (`checkout-prod`,
`payments-prod`, `data-platform-prod`) connected via ad hoc VPC peering
that has become an unmanageable mesh, plus a new requirement to privately
call a GCP-hosted BigQuery-backed analytics API from `data-platform-prod`.

1. Stand up a Transit Gateway in the Network account; migrate each
   spoke's connectivity from direct VPC peering to a TGW attachment,
   retiring the peering connections one at a time with a maintenance
   window per spoke.
2. Configure TGW route tables so `checkout-prod` and `payments-prod` can
   reach a shared "API" segment but not each other directly, and
   `data-platform-prod` can reach both for ETL ingestion.
3. Reserve a `/16` per region in AWS VPC IPAM going forward so any future
   spoke gets a collision-free allocation automatically.
4. For the GCP connection, provision a site-to-site VPN between the AWS
   Network account's VPN gateway and a GCP Cloud VPN gateway in the
   analytics host project, with matching IKEv2 parameters agreed and
   tested by both teams beforehand.
5. Instead of routing all analytics traffic over that VPN, use GCP
   Private Service Connect to publish the analytics API privately, and
   have `data-platform-prod` reach it through the VPN tunnel via a
   private IP — avoiding any public internet exposure of the analytics
   endpoint.
6. Validate: confirm `checkout-prod` cannot reach `payments-prod`
   directly (deny-by-default working), confirm `data-platform-prod` can
   reach the GCP analytics endpoint only via the private path, and run a
   controlled failover test if a VPN backup path was configured.

## Cross-references

- [aws-landing-zone-setup](../aws-landing-zone-setup/SKILL.md)
- [azure-landing-zone-setup](../azure-landing-zone-setup/SKILL.md)
- [gcp-landing-zone-setup](../gcp-landing-zone-setup/SKILL.md)
- [cloud-iam-hardening](../cloud-iam-hardening/SKILL.md)

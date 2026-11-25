---
name: manage-aws-networking
description: >
  Provision and sync AWS networking resources — Transit Gateway, Spoke VPCs, subnets,
  route tables, security groups, and Route 53 hosted zones — from a networking-design.md and
  naming-convention.md. Uses the AWS MCP server. Use when applying or updating AWS networking
  after running design-networking.
license: Apache-2.0
metadata:
  version: "0.1.0"
  chapter: "6"
---

# Manage AWS Networking

## Skill Type

Implementation

## System Requirements

- **AWS MCP server** configured and authenticated, with the ability to assume roles in each target account.
- The executing identity must have (in the network hub account and each spoke account):
  - `ec2:CreateVpc`, `ec2:CreateSubnet`, `ec2:CreateRouteTable`, `ec2:CreateSecurityGroup`
  - `ec2:CreateTransitGateway`, `ec2:CreateTransitGatewayVpcAttachment`
  - `ec2:CreateTransitGatewayRouteTable`, `ec2:CreateTransitGatewayRoute`
  - `route53:CreateHostedZone`, `route53:AssociateVPCWithHostedZone`
  - `ram:CreateResourceShare` (if sharing Transit Gateway across accounts via RAM)
- AWS accounts from the landing zone must already exist (output of `manage-aws-landing-zone`).

## Your Goal

Apply the networking definition from `networking-design.md` to AWS. Ensure that:

1. Transit Gateway exists in the hub/network account and is shared to spoke accounts via Resource Access Manager.
2. Spoke VPCs exist per `(Sector, Tier, Region)` with correct CIDRs and subnets.
3. Spokes are attached to the Transit Gateway with the correct route table associations.
4. Security Groups enforce the security baseline per resource tier.
5. Route 53 Private Hosted Zones exist per spoke and are associated with the correct VPCs.
6. No direct VPC peering exists between spokes (all traffic routes through Transit Gateway).

This skill is **idempotent**.



## Notation & Types Reference

When writing configurations or documentation, you **MUST** strictly adhere to the structural notation and types defined in the book. Before proceeding, read the following reference files:
- `references/notation.md`
- `references/types.md`

## What to Gather First

- **Networking design**: Path to `networking-design.md`. Read it first.
- **Naming convention**: Path to `naming-convention.md`.
- **Account IDs**: The AWS Account IDs for the network hub account and each spoke account (from `landing-zone-design.md`).
- **Transit Gateway sharing**: Is RAM (Resource Access Manager) in use to share the TGW across accounts? (Required when accounts are in the same Organization but different accounts.)
- **Egress model**: Centralized (NAT in hub) or decentralized (NAT per spoke)?
- **Scope of this run**: All spokes, specific regions, or specific accounts?
- **Dry-run mode**: Recommended for first-time runs.

Read all input documents before proceeding.

## Process

### Step 1 — Provision Transit Gateway

In the hub/network account:
1. Check whether a Transit Gateway exists in the target region.
2. Create it if missing. Enable:
   - `DefaultRouteTableAssociation: disable` (use custom route tables for explicit routing control)
   - `DefaultRouteTablePropagation: disable`
   - `AutoAcceptSharedAttachments: enable` (if accounts are within the same Organization)
   - DNS support and multicast support (as needed)
3. Tag with mandatory tags.
4. Share the Transit Gateway to the Organization (or specific OUs) via AWS Resource Access Manager.

### Step 2 — Create TGW Route Tables

Create dedicated route tables on the Transit Gateway to enforce spoke isolation:

| Route Table | Purpose | Associates | Propagates From |
|-------------|---------|-----------|----------------|
| `rt-hub` | Hub/platform spoke routes | Hub VPC attachment | All spokes |
| `rt-sandbox` | `Tier("sandbox")` isolation | Sandbox VPC attachments | Sandbox spokes only |
| `rt-live` | `Tier("live")` isolation | Live VPC attachments | Live spokes only |

Key rules:
- Sandbox route tables must have **no routes to Live VPCs**. A static blackhole route for Live CIDR ranges makes this explicit.
- Live route tables route to hub only; hub routes to all.
- This enforces the no-Sandbox-to-Live routing policy at the Transit Gateway layer.

### Step 3 — Provision Spoke VPCs

For each spoke in the networking design (operating in the spoke's Account):
1. Check whether a VPC with the declared CIDR exists in the target account and region.
2. Create the VPC if missing. Enable DNS hostnames and DNS resolution.
3. Tag with mandatory tags.

### Step 4 — Provision Subnets

For each spoke VPC, create the required subnets across Availability Zones:

| Subnet Purpose | CIDR Offset | AZ distribution |
|---------------|------------|----------------|
| Public | `.0.0/24` split across 3 AZs | `/26` per AZ |
| Private | `.1.0/22` split across 3 AZs | `/24` per AZ |
| Data | `.5.0/24` split across 3 AZs | `/26` per AZ |
| Transit (TGW attachment) | `.6.0/28` per AZ | `/28` per AZ |

The Transit subnets host the TGW VPC attachment ENIs — they should be small (`/28`) and carry no other resources.

### Step 5 — Attach Spokes to Transit Gateway

For each spoke VPC:
1. Create a Transit Gateway VPC Attachment in the transit subnets.
2. Associate the attachment with the correct TGW route table (Sandbox or Live, per the spoke's tier).
3. Propagate the spoke's CIDR to the `rt-hub` route table so the hub can reach it.
4. Add a default route (`0.0.0.0/0`) in the spoke's private subnet route tables pointing to the TGW attachment (for centralized egress) or to a NAT Gateway (for decentralized egress).

### Step 6 — Provision NAT Gateways

**Centralized egress**: Deploy NAT Gateways in the hub account's public subnets. Configure the hub VPC's routing so all spoke traffic exits through these NATs. Update spoke private route tables to forward `0.0.0.0/0` to the TGW.

**Decentralized egress**: Deploy NAT Gateways in the public subnets of each spoke VPC. Update spoke private route tables to forward `0.0.0.0/0` to the local NAT Gateway.

### Step 7 — Provision Security Groups

Create baseline Security Groups in each spoke account. These are templates — applications create their own SGs but must reference these for baseline rules:

- `sg-platform-inbound`: Allow inbound from platform/hub CIDR on management ports. Used on all EC2 and EKS nodes.
- `sg-internal-only`: Allow inbound from spoke CIDR only; deny internet. Default for data-tier resources.
- `sg-public-lb`: Allow inbound 443, 80 from `0.0.0.0/0`. Used only on internet-facing load balancers.

### Step 8 — Provision Route 53 Private Hosted Zones

For each spoke, create a Private Hosted Zone:
1. Create the zone (e.g., `eu01.live.internal.ecommerce.mountainlab.io`) in the spoke account.
2. Associate it with the spoke VPC.
3. Also associate it with the hub VPC so the hub's resolver can forward queries.
4. Share the zone to other accounts via Route 53 Resolver Rules if cross-account DNS resolution is needed.

If using Route 53 Resolver (inbound/outbound endpoints) for hybrid DNS:
- Deploy resolver endpoints in the hub VPC.
- Create forwarding rules for on-premises domains.
- Share resolver rules to all spoke accounts via RAM.

### Step 9 — Report

Produce a summary of all resources created, already existing, or skipped.

## Output Format

Produce a Markdown report named `aws-networking-report.md`:

```markdown
# AWS Networking Sync Report

**Date**: [timestamp]
**Mode**: [applied / dry-run]

## Transit Gateway

| TGW ID | Account | Region | RAM Shared | Status |
|--------|---------|--------|-----------|--------|
| tgw-xxx | network-hub (123456789012) | eu-west-1 | Yes (Org) | created |

## TGW Route Tables

| Name | Associates | Status |
|------|-----------|--------|
| rt-live | live VPC attachments | created |
| rt-sandbox | sandbox VPC attachments | created |

## Spoke VPCs

| Name | Account | CIDR | TGW Attached | Route Table | Status |
|------|---------|------|-------------|------------|--------|
| vpc-ecommerce-live-eu01 | ecommerce-live | 10.32.0.0/16 | yes | rt-live | created |

## Private Hosted Zones

| Zone | Account | VPC Associations | Status |
|------|---------|-----------------|--------|
| eu01.live.internal.ecommerce.mountainlab.io | ecommerce-live | vpc-ecommerce-live-eu01 | created |

## Direct VPC Peerings Found
[List any found — should be empty]

## Open Items
[RAM share acceptance pending, TGW attachment propagation delay, etc.]
```

## Principles to Apply

- **Transit Gateway route tables enforce tier isolation**: The Sandbox and Live route tables are the network-layer enforcement of the no-Sandbox-to-Live rule. Blackhole routes make this explicit rather than relying on absence of routes.
- **Transit subnets are TGW-only**: The `/28` transit subnets exist solely for TGW attachment ENIs. No application resources should be placed there.
- **RAM sharing before attachment**: The Transit Gateway must be shared (accepted) in the spoke account before a VPC attachment can be created from that account.
- **Route 53 private zones are spoke-scoped**: Each spoke gets its own private hosted zone. Cross-spoke resolution goes through the hub's Resolver, not direct zone sharing.
- **Idempotent**: Check state before creating. Never delete TGW attachments or route table associations without confirmation.

## Related Chapter(s)

This skill is grounded in **Chapter 6: Infrastructure** of *Crafting Platforms*.

- Read the book: [leanpub.com/crafting-platforms](https://leanpub.com/crafting-platforms)
- Project home: [craftingplatforms.com](https://www.craftingplatforms.com)

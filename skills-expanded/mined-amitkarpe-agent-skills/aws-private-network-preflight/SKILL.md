---
name: aws-private-network-preflight
description: Use when AWS work creates or updates GCC, GovTech, restricted, private-only, Nexus-VPCE-sharing, TGW, VPC peering, VPC/subnet/route/LB, or similar networking/exposure paths where public Internet exposure must be blocked by default. For EC2-only launches in an already-approved private subnet, do the lightweight public-IP check instead of the full preflight.
---

# AWS Private Network Preflight

Use this skill before AWS work that creates or updates networking or exposure
paths in GCC, GovTech, restricted, private-only, Nexus-VPCE-sharing, TGW, VPC
peering, or similar network lanes.

Do not run the full preflight just because a task launches an EC2 instance in
an existing approved private subnet. For EC2-only proof hosts, use the
lightweight EC2 check below.

## Core rule

Default deny public Internet exposure.

If the task would require any public-exposure resource to work, stop and say:

- blocked by private-network guardrail
- needs private-only redesign or explicit Amit approval

## Hard block list

Do not create, apply, or propose as fallback:

- Internet Gateway (`igw`)
- NAT Gateway
- egress-only Internet Gateway
- public subnet
- EC2 with public IP
- Elastic IP
- internet-facing ALB or NLB
- `0.0.0.0/0` or `::/0` route to IGW or NAT
- public SSH or RDP access

## Full Preflight Trigger

Run the full public-exposure preflight only when the task creates, updates, or
depends on one of these:

- VPC
- subnet
- route table or default route
- Internet Gateway, NAT Gateway, or egress-only Internet Gateway
- public IP, Elastic IP, or auto-assign-public-IP setting
- internet-facing ALB or NLB
- Transit Gateway, VPC peering, PrivateLink, or VPC endpoint networking
- security group exposure intended to support public access

## Lightweight EC2-Only Check

For EC2-only launches in an already-approved private subnet, do not rerun the
full VPC/network checklist. Check only:

- launch request has `AssociatePublicIpAddress=false` or no public-IP mapping
- selected subnet is the expected private subnet for the lane
- launched instance has `PublicIpAddress=null`

If any item fails, stop before continuing.

## Required Full Preflight Line

When a full preflight trigger applies, write this line into the plan, goal, or
pre-mutation note:

`Public exposure check: IGW=no, NAT=no, public subnet=no, public IP=no, EIP=no, internet-facing LB=no, default route to IGW/NAT=no`

If any field would be `yes`, stop before apply unless Amit explicitly approved
that exact resource type.

## Preferred private alternatives

Prefer these first:

- private subnets
- VPC endpoints / PrivateLink
- Transit Gateway
- VPC peering
- approved private proxy path
- SSM Session Manager instead of public SSH

## Cleanup rule

If a mistaken public-exposure test lane already exists:

1. freeze changes
2. capture dependency evidence
3. delete in safe dependency order
4. verify removal with direct AWS APIs
5. save evidence under `~/.AGENTS-temp/<repo>/`

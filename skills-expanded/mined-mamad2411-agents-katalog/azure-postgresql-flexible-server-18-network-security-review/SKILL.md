---
name: azure-postgresql-flexible-server-18-network-security-review
description: Reviews Azure Database for PostgreSQL Flexible Server 18 private access, private endpoint, firewall, public access, delegated subnet, Private DNS, NSG, routing, TLS, and administrator exposure. Use when checking network security or connectivity.
license: MIT
compatibility: Requires Azure CLI for Azure networking checks. Optional nslookup/dig helps DNS validation.
---

# Azure PostgreSQL Flexible Server 18 Network Security Review

## When to Use This Skill

Use this skill for:

- Private access and private endpoint review.
- Public access and firewall rule review.
- Private DNS and VNet link validation.
- Delegated subnet and NSG/routing review.
- TLS and administrative access exposure review.

## Core Guidance

- Production access should be private unless there is a documented exception.
- Broad public access is a security finding.
- Administrative access should not be public.
- Private DNS, VNet peering, custom DNS, and route tables must be verified when private networking is used.
- Run scripts with `--help` before use.

## Workflows

- [network-security-review-workflow](workflows/network-security-review-workflow.md)

## Resources

- [network-security-checklist.md](resources/network-security-checklist.md)

## Scripts

- `scripts/check-public-access.sh`

## Examples

- [private-dns-validation-example.md](examples/private-dns-validation-example.md)

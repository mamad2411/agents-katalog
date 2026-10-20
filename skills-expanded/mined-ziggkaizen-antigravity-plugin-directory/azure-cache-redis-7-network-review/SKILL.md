---
name: azure-cache-redis-7-network-review
description: Reviews Azure Cache for Redis Enterprise and Enterprise Flash Redis 7 private endpoints, public access, DNS, firewall rules, TLS-only connectivity, and network troubleshooting. Use when the user changes Redis networking or connectivity.
license: MIT
compatibility: Works with repository files and Azure network/IaC context.
---

# Azure Cache for Redis 7 Network Review

This skill reviews network access for Azure Cache for Redis Enterprise / Enterprise Flash Redis 7.2.

## When to Use This Skill

Use it for:

- Private endpoint creation or changes.
- Public network access decisions.
- DNS or private DNS zone changes.
- Firewall and network routing changes.
- TLS/non-TLS connectivity review.
- Connectivity troubleshooting between applications and Redis.

## Workflow

- `workflows/private-access-review-workflow.md`: Use for private access, DNS, and public exposure reviews.

## Resource

- `resources/private-endpoint-checklist.md`: Private access checklist.

## Example

- `examples/private-endpoint-bicep-review-notes.md`: Review notes for private endpoint IaC.

## Guidance

1. Prefer private endpoint access for production.
2. Treat public access as an exception requiring explicit approval.
3. Verify DNS from every client environment, not only from the IaC plan.
4. Keep TLS enabled and reject non-TLS production shortcuts.
5. Confirm Redis tier-specific behavior before applying public access flags.
6. Require connectivity tests from app subnets after changes.

---
name: azure-cache-redis-7-config-review
description: Reviews Azure Cache for Redis Enterprise and Enterprise Flash Redis 7.2 configuration, IaC, SKU, capacity, persistence risk, diagnostics, upgrade readiness, and production release safety. Use when the user changes Redis cache infrastructure, Azure CLI, Bicep, ARM, Terraform, YAML, or JSON configuration.
license: MIT
compatibility: Optional scripts require bash, python3, and standard POSIX utilities.
---

# Azure Cache for Redis 7 Config Review

This skill reviews Azure Cache for Redis Enterprise / Enterprise Flash Redis 7.2 configuration and infrastructure changes.

## When to Use This Skill

Use this skill for:

- Bicep, ARM, Terraform, Pulumi, Azure CLI, YAML, or JSON config changes.
- Redis version, tier, SKU, capacity, clustering policy, persistence, diagnostics, import/export, or upgrade changes.
- Detecting public access, non-TLS access, or Redis-as-durable-persistence assumptions.
- Reviewing release readiness before production changes.

## Workflows

- `workflows/config-review-workflow.md`: Use when reviewing Redis configuration or infrastructure changes.
- `workflows/upgrade-readiness-workflow.md`: Use when planning or reviewing Redis 7.2 upgrades.

## Resources

- `resources/config-review-checklist.md`: General Redis config review checklist.
- `resources/sku-capacity-checklist.md`: SKU and capacity review checklist.

## Examples

- `examples/bicep-enterprise-database-example.md`: Conservative Bicep review notes for Enterprise Redis databases.

## Scripts

- `scripts/azure-cache-redis-7-iac-guard.sh`: Hook helper for public access, persistence, and Redis config-change checks.
- `scripts/validate-azure-cache-redis-config.sh`: Manual static scanner for Redis config files.

Run scripts with `--help` before use. Treat scripts as advisory and verify findings against official documentation.

## Review Procedure

1. Confirm the resource type and tier.
2. Confirm Redis version and release line.
3. Review SKU, capacity, memory margin, and connection assumptions.
4. Review private access, public access, firewall, DNS, and TLS settings.
5. Review persistence, backup, import/export, and source-of-truth assumptions.
6. Review diagnostics, metrics, logs, and alerts.
7. Review scale, upgrade, and rollback behavior.
8. Return findings as blockers, risks, recommendations, and explicit assumptions.

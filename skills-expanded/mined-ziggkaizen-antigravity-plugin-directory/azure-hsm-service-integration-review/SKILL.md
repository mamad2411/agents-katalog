---
name: azure-hsm-service-integration-review
description: Reviews service-to-Azure Key Vault Managed HSM integrations, including managed identity authentication, key references, customer-managed key configuration, private networking, SDK usage, retry behavior, caching, logging, failover, and startup failure modes. Use when the user mentions application integration, service access, CMK, BYOK, HSM URI, key URI, encryption service, SDK client, container, VM, function, or workload identity.
license: MIT
compatibility: Requires current Azure service documentation for service-specific customer-managed key behavior.
---

# Azure HSM Service Integration Review Skill

Use this skill when reviewing an application or Azure service that uses Managed HSM keys.

## Approach

1. Identify the service, runtime identity, HSM, key URI, key version behavior, and required operations.
2. Prefer managed identity and eliminate client secrets.
3. Verify local RBAC role and scope are minimal.
4. Confirm private endpoint, DNS, firewall, and outbound connectivity design.
5. Review SDK/client configuration for token handling, retries, timeouts, caching, and failure behavior.
6. Ensure logs never contain tokens, key material, security-domain material, or decrypted sensitive data.
7. Confirm operational runbooks cover HSM outages, throttling, rotation, and access denial.
8. Verify service-specific Managed HSM support in current official documentation.

## Workflow

Use `workflows/service-integration-review-workflow.md` for integration reviews.

## Resource

Use `resources/service-integration-review-checklist.md` for coverage.

## Script

Use `scripts/azure-hsm-service-reference-scan.py` to scan repository files for Managed HSM references and risky integration patterns. Run it with `--help` before use.

## Example

Use `examples/managed-identity-service-pattern.md` for a general service integration pattern.

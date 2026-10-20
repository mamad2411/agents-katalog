---
name: azure-hsm-access-policy-review
description: Reviews Azure Key Vault Managed HSM access policies, Azure RBAC, Managed HSM local RBAC, role assignments, custom roles, scopes, managed identities, and privileged access. Use when the user mentions HSM access, role assignment, role definition, local RBAC, Azure RBAC, least privilege, PIM, administrator access, or service permissions.
license: MIT
compatibility: Requires current Azure documentation for exact commands; optional Azure CLI for the included read-only inventory script.
---

# Azure HSM Access Policy Review Skill

Use this skill when reviewing Managed HSM access-control design, IaC, scripts, or operational changes.

## Approach

1. Identify the principal: user, group, service principal, managed identity, deployment identity, or break-glass identity.
2. Separate Azure control-plane RBAC from Managed HSM data-plane local RBAC.
3. Review scope: `/`, `/keys`, or `/keys/<key-name>`.
4. Confirm the role grants only the required operations.
5. Prefer managed identities for services and groups for human privileged access.
6. Check lockout risk before role deletion or role definition changes.
7. Require explicit approval for privileged role changes, role deletion, or broad scope assignments.
8. Verify exact command, SDK, IaC, or REST syntax against current official documentation.

## Workflow

Use `workflows/access-policy-review-workflow.md` for structured RBAC and access-change reviews.

## Resource

Use `resources/access-policy-review-checklist.md` for coverage.

## Script

Use `scripts/azure-hsm-access-inventory.sh` for read-only local RBAC inventory. Run it with `--help` before use.

## Example

Use `examples/local-rbac-scope-examples.md` for scope reasoning.

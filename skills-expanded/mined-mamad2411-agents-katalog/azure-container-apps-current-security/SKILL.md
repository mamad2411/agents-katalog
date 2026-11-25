---
name: azure-container-apps-current-security
description: Reviews Azure Container Apps security for ingress exposure, secrets, Key Vault references, managed identity, registry credentials, CORS, mTLS, IP restrictions, and RBAC. Use for ACA security review or sensitive config changes.
license: MIT
compatibility: Azure Container Apps managed service, current Microsoft Learn guidance.
---

# Azure Container Apps Security

This skill guides security review for Container Apps configuration and commands.

## When to Use

Use this skill when the task involves:

- public or internal ingress;
- CORS, IP restrictions, auth, or mTLS;
- environment variables or secrets;
- Key Vault secret references;
- managed identity and RBAC;
- private registry access;
- Azure MCP Server enablement;
- reviewing YAML/JSON/Bicep/workflow content for leaks.

## Security Requirements

1. Public ingress requires explicit justification.
2. Production secrets should reference Key Vault where possible.
3. Managed identity is preferred for Azure resources and ACR pulls.
4. Avoid storing static credentials in ACA configuration, shell commands, logs, or GitHub/Azure workflows.
5. Use least-privilege RBAC and subscription/resource-group scoping.
6. Avoid wildcard CORS unless explicitly required and reviewed.
7. Treat IP restrictions and mTLS/auth changes as security-sensitive.
8. Disable or carefully scope MCP tools until permissions are reviewed.

## Workflows

Use `workflows/security-review-workflow.md` for security-sensitive ACA changes.

## Resources

Use `resources/security-review-checklist.md`.

## Examples

Use `examples/key-vault-secret-reference-example.md` for secret reference patterns.

## Scripts

Run `scripts/scan-aca-content.py --help` before manual use. Antigravity hooks call this script automatically through `hooks.json`.

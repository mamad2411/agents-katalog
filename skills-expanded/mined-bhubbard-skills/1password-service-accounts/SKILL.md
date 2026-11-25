---
name: 1password-service-accounts
description: Utilize 1Password Service Accounts to securely access secrets programmatically in CI/CD pipelines, cloud infrastructure, or applications without tying access to a specific user.
---

# 1Password Service Accounts

This skill provides guidance on using 1Password Service Accounts. Service Accounts allow programmatic, secure access to secrets (like API keys, credentials) in applications and CI/CD pipelines without being tied to an individual user.

## Overview
- **Purpose**: Secure programmatic access to secrets for machine-to-machine authentication.
- **Benefits**: Scoped access (control which vaults/actions are allowed), CI/CD integration, and agentic AI integration.

## Usage Guidelines
- **Creation**: Administrators can create a Service Account in the 1Password Developer > Directory (or Integrations > Directory) section.
- **Authentication**: Set the `OP_SERVICE_ACCOUNT_TOKEN` environment variable to authenticate the 1Password CLI or SDKs.
- **CI/CD**: Widely used in workflows like GitHub Actions to dynamically retrieve secrets without hardcoding them.

## Best Practices
- **Scope**: Always apply the principle of least privilege. Scope the service account to only the specific vaults and permissions required for the task.
- **Rotation**: Rotate service account tokens periodically or if a potential breach is suspected.
- **Monitoring**: Review audit logs to monitor how service accounts are being used.

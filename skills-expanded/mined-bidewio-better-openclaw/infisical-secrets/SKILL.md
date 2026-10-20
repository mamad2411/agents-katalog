---
name: infisical-secrets
description: Secret management platform with Infisical
version: 1.0.0
tags: [security, secrets, env-variables, devops]
---

# Infisical – Open-Source Secret Management

Infisical manages secrets and environment variables across teams,
infrastructure, and CI/CD pipelines with end-to-end encryption.

- **GitHub**: github.com/Infisical/infisical (18 000+ ⭐)
- **License**: MIT
- **Security**: E2E encrypted. SOC 2 Type II compliant. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{INFISICAL_URL}}` | Infisical API URL |
| `{{INFISICAL_TOKEN}}` | Service token or machine identity token |

## Usage Examples

### Get secrets

```bash
curl -s "{{INFISICAL_URL}}/api/v3/secrets/raw?workspaceId=<ws_id>&environment=dev" \
  -H "Authorization: Bearer {{INFISICAL_TOKEN}}"
```

### Create a secret

```bash
curl -s -X POST "{{INFISICAL_URL}}/api/v3/secrets/raw/<secret_name>" \
  -H "Authorization: Bearer {{INFISICAL_TOKEN}}" \
  -H "Content-Type: application/json" \
  -d '{"workspaceId": "<ws_id>", "environment": "dev", "secretValue": "my-value"}'
```

## AI Agent Tips

- E2E encryption — secrets are never stored in plaintext.
- Native integrations with Kubernetes, GitHub Actions, Vercel, etc.
- Secret versioning and audit logs.
- CLI tool for injecting secrets at runtime.

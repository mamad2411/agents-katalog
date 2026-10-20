---
name: keycloak-auth
description: Enterprise identity and access management with Keycloak
version: 1.0.0
tags: [auth, sso, identity, security, enterprise]
---

# Keycloak – Enterprise Identity Management

Keycloak provides SSO, identity brokering, user federation,
and fine-grained authorization for applications and services.

- **GitHub**: github.com/keycloak/keycloak (25 000+ ⭐)
- **License**: Apache-2.0
- **Security**: CNCF incubating project. Red Hat-maintained. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{KEYCLOAK_URL}}` | Base URL of the Keycloak server |
| `{{KEYCLOAK_ADMIN}}` | Admin username |
| `{{KEYCLOAK_ADMIN_PASSWORD}}` | Admin password |

## Usage Examples

### Get admin token

```bash
curl -s -X POST "{{KEYCLOAK_URL}}/realms/master/protocol/openid-connect/token" \
  -d "client_id=admin-cli" \
  -d "username={{KEYCLOAK_ADMIN}}" \
  -d "password={{KEYCLOAK_ADMIN_PASSWORD}}" \
  -d "grant_type=password"
```

### List users in a realm

```bash
curl -s "{{KEYCLOAK_URL}}/admin/realms/myrealm/users" \
  -H "Authorization: Bearer <access_token>"
```

## AI Agent Tips

- Supports OIDC, SAML 2.0, and LDAP protocols.
- Social login integrations (Google, GitHub, etc.) built-in.
- Fine-grained RBAC with custom policies.
- CNCF project ensures long-term community support.

---
name: authentik-auth
description: Identity provider and SSO with Authentik
version: 1.0.0
tags: [auth, sso, identity, security]
---

# Authentik – Open-Source Identity Provider

Authentik is a self-hosted identity provider offering SSO, MFA,
user management, and access policies via OIDC/SAML.

- **GitHub**: github.com/goauthentik/authentik (15 000+ ⭐)
- **License**: MIT (core)
- **Security**: OIDC/SAML compliant. Regular security releases. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{AUTHENTIK_URL}}` | Base URL of the Authentik instance |
| `{{AUTHENTIK_API_TOKEN}}` | API token for admin operations |

## Usage Examples

### List users

```bash
curl -s "{{AUTHENTIK_URL}}/api/v3/core/users/" \
  -H "Authorization: Bearer {{AUTHENTIK_API_TOKEN}}"
```

### List applications

```bash
curl -s "{{AUTHENTIK_URL}}/api/v3/core/applications/" \
  -H "Authorization: Bearer {{AUTHENTIK_API_TOKEN}}"
```

## AI Agent Tips

- Supports OIDC, SAML, LDAP, SCIM, and RADIUS protocols.
- Flow-based authentication allows custom login experiences.
- Protect any web application with forward-auth proxy integration.
- Built-in MFA support (TOTP, WebAuthn, SMS).

---
name: oauth2-engineering
description: Implement OAuth 2.0 responsibly. Use when integrating or providing
  OAuth2 flows.
metadata:
  tags: oauth2, engineering
---

# OAuth 2.0 Engineering

## Use this skill when
- Implementing authorization code + PKCE flows
- Building a token endpoint and client/session handling
- Integrating third-party logins

## Do not use this skill when
- OIDC identity semantics (use its own skill)
- Building your own auth for internal apps (a provider may be better)

## Instructions
1. Default to the authorization code flow with PKCE; avoid implicit flow.
2. Store client secrets server-side only.
3. Validate redirect URIs exactly; reject open redirects.
4. Bind access tokens to clients and scopes.
5. Issue short-lived tokens; implement refresh with rotation.
6. Never log tokens or pass them in URLs.
7. Handle consent and scope revocation per spec.

## Checklist
- PKCE enforced
- Redirect URIs allowlisted
- Refresh tokens are revocable

## Output Format
- Grant flow | token endpoint | URI policy | scope model

## Common Mistakes
- Client credentials for user scoped tokens
- Wildcard redirect URIs
- Tokens in query strings

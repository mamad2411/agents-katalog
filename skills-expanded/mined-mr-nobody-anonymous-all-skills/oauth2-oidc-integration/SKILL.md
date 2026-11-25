---
name: oauth2-oidc-integration
description: "Integrate OAuth 2.1 and OpenID Connect correctly: authorization code with PKCE, token validation, scope design, refresh rotation and logout."
type: procedural
category: security
domain: security
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: high
level: advanced
triggers:
  - oauth2 pkce flow
  - oidc id token validation
  - refresh token rotation
  - oauth scope design
  - sso integration
keywords:
  - oauth2
  - oidc
  - pkce
  - jwt
  - scopes
  - sso
source: custom
enabled: true
---

# OAuth 2.1 and OIDC Integration

## Purpose

Integrate OAuth 2.1 and OpenID Connect correctly: authorization code with PKCE, token validation, scope design, refresh rotation and logout.

## When to Use

- You are adding third-party sign-in or delegating API access.
- Tokens must be validated and refreshed without leaking them.
- Scopes and consent screens must match what the app actually does.

## When NOT to Use

- A single first-party service can authenticate users directly with sessions.
- You need machine-to-machine access where client credentials fit better.
- The identity provider is unknown; gather its discovery document first.

## Capabilities

- Implement authorization code + PKCE for public and confidential clients.
- Validate ID tokens (issuer, audience, signature, nonce, expiry).
- Design least-privilege scopes and consent.
- Rotate refresh tokens and handle reuse detection.

## Inputs

- The identity provider and its discovery document (`/.well-known/openid-configuration`).
- Client type (SPA, mobile, server) and redirect URI constraints.
- The API resources and the minimum permissions each needs.

## Workflow

1. Fetch the discovery document and record the supported flows and endpoints.
2. Choose the flow by client type: public clients must use PKCE and no client secret.
3. Request the smallest scope set that satisfies the user story.
4. Validate tokens on the resource server; never trust claims from the client.
5. Store refresh tokens securely and implement rotation with reuse detection.

## Tools

- the IdP's SDK or a vetted OIDC library
- jwt debugger
- browser devtools

## Examples

- `curl -s https://idp.example/.well-known/openid-configuration | jq .`
- `curl -s -X POST https://idp.example/token -d grant_type=authorization_code -d code=$CODE -d code_verifier=$V`
- `allskills route "add oauth login"`

## Safety

- Never ship a client secret in a browser or mobile binary.
- Tokens in URLs leak through logs and referrers; use headers or secure storage.
- Validate `aud`, `iss`, `exp` and `nonce`; skipping any of them enables token replay.

## Source

All-Skills canonical library (`skills/security/oauth2-oidc-integration`). First-party skill, maintained in this repository.

## Notes

- Implicit flow and resource owner password grant are deprecated; do not adopt them.
- Token exchange and audience-restricted tokens limit blast radius between services.
- Pairs with: `security/secrets-management`, `security/secure-architecture`.

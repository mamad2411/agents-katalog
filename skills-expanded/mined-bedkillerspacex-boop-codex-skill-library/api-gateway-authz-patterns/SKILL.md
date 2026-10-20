---
name: api-gateway-authz-patterns
description: >
  Design and review API gateway authorization: JWT/OIDC validation, API keys, mTLS,
  claims- and scope-based route guards, identity header injection to backends, deny-by-default
  routing, and trust-boundary hardening. Use when configuring or assessing Kong, Envoy, AWS
  API Gateway, Azure APIM, Apigee, NGINX, or similar edge gateways for authn/authz — not for
  pure mesh AuthorizationPolicy alone, object-level BOLA, or unauthorized third-party probes.
---

# API Gateway AuthZ Patterns

## Scope And Authorization

- **In scope:** Gateways and APIs your organization operates.
- **Out of scope:** Probing third-party gateways without authorization.
- Gateway misconfig can expose all backends — change via controlled releases.
- Redact JWT secrets, API keys, and admin tokens from tickets.
- Pair with `api-auth-and-jwt-abuse`, `api-key-lifecycle`, and `code-quality-standards`.

## When To Use

- Placing authn/authz at Kong/Envoy/AWS API Gateway/APIM/Apigee/NGINX.
- Injecting trusted identity headers to backends (`X-User-Id`) safely.
- Scope/audience-based route allowlists.
- Reviewing bypass paths (direct-to-origin, admin routes).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Object-level IDOR/BOLA | `idor-broken-object-authorization` |
| JWT crypto abuse testing | `api-auth-and-jwt-abuse` |
| Rate limit design | `api-rate-limit-design` |
| Mesh-only AuthorizationPolicy | Istio/mesh skills in catalog |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Pattern | Use | Watch-outs |
| --- | --- | --- |
| JWT/OIDC validation | User/service OIDC access tokens | Weak claim checks; clock skew |
| API keys | Partner M2M simple auth | Keys in query strings; no hash at rest |
| mTLS | Service identity | Client cert CA management |
| Scope gates | `read:orders` per route | Scope ≠ object authz |
| IP allowlists | Admin break-glass | Spoofed XFF if trust mis-set |
| Header injection | Pass `X-End-User` to app | **Clients must not set these** |

## Workflow

### 1. Confirm trust boundaries and success criteria

1. Diagram: Client → CDN → Gateway → Internal services.
2. Success: unauthenticated denied by default; only gateway can set identity headers; JWT/`aud` enforced; direct origin blocked.
3. List public vs private routes.

### 2. Inventory gateway config

```bash
# Examples — adapt to product
# Kong: deck dump / Admin API
# Envoy: config_dump
curl -sS localhost:9901/config_dump | head
# AWS
aws apigateway get-rest-apis
```

1. Note auth plugins/filters per route.
2. Find exception routes (`/health`, `/metrics`, webhooks).

### 3. Deny by default

| Rule | Implementation idea |
| --- | --- |
| Default deny | Unmatched routes 404/401 |
| Explicit allow | Each route declares auth method |
| Origin lock | Backends accept only gateway SG / mTLS |
| Admin | Separate listener + stronger auth |

### 4. JWT validation pattern

```text
Validate: signature via JWKS, iss, aud, exp, alg allowlist
Map: sub -> X-User-Id, scope -> internal header
Reject: missing/invalid before upstream
```

1. Cache JWKS with sensible TTL; pin issuer.
2. Different `aud` per API domain when possible.

### 5. Identity header trust

```nginx
# Conceptual NGINX — strip client-supplied identity headers
proxy_set_header X-User-Id "";
# After auth module sets $user_id:
proxy_set_header X-User-Id $user_id;
```

| Bad | Good |
| --- | --- |
| Trust client `X-User-Id` | Strip then set only post-auth |
| Backend open to Internet | Backend only from gateway |
| AuthZ only at edge | Edge + object authz in app |

### 6. API keys and mTLS

1. Keys: validate at gateway; store hashes (`api-key-hash-storage`); scopes in metadata.
2. mTLS: require client certs for partner APIs; map cert SAN to principal.
3. Combine rate limits per principal (`api-rate-limit-design`).

### 7. Verify

```bash
# No token
curl -sS -o /dev/null -w "%{http_code}\n" https://api.example.com/v1/orders
# Bad aud / expired — expect 401
# Spoof identity header — expect ignored
curl -sS https://api.example.com/v1/orders \
  -H "Authorization: Bearer $TOK" -H "X-User-Id: admin"
# Direct origin (should fail network/policy)
```

1. Pen-test review: gateway admin UI exposure.
2. Chaos: JWKS down → fail closed (or documented cache).

### 8. Hand off

1. Route→auth matrix in runbook.
2. Alerts on auth failure spikes and config changes.
3. App teams still enforce BOLA.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Default | Deny | Open routes forgotten |
| Headers | Strip + set | Trust client identity |
| JWT | aud/iss/exp | Parse-only at edge |
| Backend | Private | Public + “hidden” path |

## Output Checklist

- [ ] Trust diagram recorded
- [ ] Route auth matrix complete
- [ ] JWT/API key/mTLS configured per design
- [ ] Identity headers stripped from clients
- [ ] Origin locked to gateway
- [ ] Negative tests (no/bad token, spoof header)
- [ ] Admin/webhook exceptions documented
- [ ] App-level authz still required
- [ ] `code-quality-standards` on IaC

## Rules

- Owned gateways only.
- Gateway authz is necessary, not sufficient for object-level security.
- Fail closed when IdP/JWKS unavailable unless explicitly designed otherwise.
- Never let clients self-assert identity headers.
- Protect gateway admin planes like production roots.

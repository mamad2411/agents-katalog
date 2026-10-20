---
name: golang-api-gateway-auth
description: >
  Implement and review API gateway authentication for Go services: JWT/OIDC
  validation, mTLS, API keys, gateway plugins, and service trust. Use for owned
  gateways under authorization.
---

# Golang API Gateway Auth

## Research grounding

Runbook for **authentication at the API gateway** in front of Go backends—
Envoy/Kong/Nginx/Cloud gateways and Go-authored auth plugins/filters. Skill id:
`golang-api-gateway-auth`.

## Scope And Authorization

- **In scope:** gateways and IdPs you own; authorized pentests.
- **Out of scope:** attacking third-party gateways or forging tokens for fraud.
- Prefer staging for auth changes; production needs change windows.
- Redact tokens and client secrets.
- Pair with `api-auth-and-jwt-abuse` theory and `code-quality-standards`.

## When To Use

- Terminating JWT/OIDC or mTLS at the edge before Go services.
- Writing Go authz plugins (e.g. ext_authz, Kong PDK via HTTP, custom middleware gateway).
- Defining trust headers (`X-User-Id`) and preventing spoofing.
- Focus tokens: **golang, api, gateway, auth**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Deep JWT abuse testing | `api-auth-and-jwt-abuse` |
| Service object RBAC | `golang-access-control` |
| API surface design | `golang-api-surface` |
| Abuse rate limits | `golang-abuse-prevention` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Mode | Guidance |
| --- | --- |
| JWT/OIDC | Validate iss, aud, exp, sig (JWKS); clock skew; reject `alg=none` |
| mTLS | Gateway verifies client cert; map SAN to identity |
| API keys | Hash at rest; rotate; bound to plan; not in query logs |
| Ext auth | Envoy `ext_authz` → Go service allow/deny |
| Internal headers | Strip client-supplied identity headers; only gateway may set |
| Downstream Go | Still defend if gateway bypass possible (network policy) |
| Pitfalls | Trusting unsigned gateway headers from public Internet |

## Workflow

### 1. Confirm scope and success criteria

1. Gateway product, backends, IdP, authorization.
2. Success: invalid token denied; valid accepted; spoofed identity header ignored.
3. Break-glass path documented.

### 2. Inventory

1. Routes public vs private; auth methods per route.
2. JWKS endpoints, audiences, optional APIs.
3. Existing identity headers and mesh mTLS.

### 3. Baseline

1. Capture sample allow/deny (redacted HAR).
2. Version gateway config and plugin code.

### 4. Implement / harden

**Header trust rule:**

```go
// Downstream Go middleware defense-in-depth
func identityFromRequest(r *http.Request) (Identity, error) {
	// If not on mesh-only port, ignore X-Forwarded-User from clients
	if !fromGatewayNetwork(r) {
		return Identity{}, errUnauthenticated
	}
	return Identity{User: r.Header.Get("X-Gateway-User")}, nil
}
```

**JWT checks (conceptual):** signature via JWKS cache, `aud` match, `exp`/`nbf`,
`iss` allowlist, required claims (tenant).

1. Configure gateway to **strip** inbound `X-Gateway-*` from clients then set after auth.
2. Short JWKS cache with refresh; fail closed if JWKS unavailable for protected routes.
3. API keys: look up hashed key in store; constant-time compare.
4. mTLS: require client cert on admin routes; CRL/OCSP policy documented.
5. Return 401 vs 403 correctly; avoid user oracle on login-like routes.

### 5. Verify with evidence

```bash
go test ./internal/gatewayauth/... -count=1
go test ./... -race -count=1
govulncheck ./...

# Staging
curl -i https://gw.staging/api  # 401
curl -i -H "Authorization: Bearer $BAD" https://gw.staging/api  # 401
curl -i -H "Authorization: Bearer $GOOD" https://gw.staging/api  # 200
curl -i -H "X-Gateway-User: admin" https://gw.staging/api  # 401 (no spoof)
```

1. Expired/wrong-aud tokens denied.
2. Bypass path (direct to pod) blocked by network policy or secondary auth.
3. Log fields redacted (no full bearer tokens).

### 6. Observe and harden

1. Metrics: auth fail/success, JWKS errors, ext_authz latency.
2. Alert on JWKS fetch failures and auth latency SLO.
3. Rotate signing keys with dual-JWKS overlap.

### 7. Hand off

1. Runbook: key rotation, emergency deny-all.
2. Contract doc: headers gateway sets for Go services.
3. Apply `code-quality-standards`.

## Trust model

| Layer | Responsibility |
| --- | --- |
| Gateway | Authenticate caller; set identity headers |
| Network | Only gateway can reach backend plain ports |
| Go service | Authorize object actions; optional JWT re-validate |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Headers | Strip then set | Trust client X-User-Id |
| JWT | JWKS + aud/iss | Parse payload only |
| Fail mode | Closed on JWKS down | Open allow |
| Keys | Hashed API keys | Keys in plaintext logs |
| Topic fidelity | Gateway auth + Go | Generic go test only |

## Output Checklist

- [ ] Routes and auth modes inventoried
- [ ] Token/mTLS/API key validation correct
- [ ] Identity header spoofing tests pass
- [ ] Downstream network trust documented
- [ ] Metrics/alerts on auth path
- [ ] Rotation runbook
- [ ] `code-quality-standards` applied

## Rules

- Authorized testing only; no credential abuse on third parties.
- Prefer fail-closed on auth dependency loss for protected APIs.
- Focus on `golang-api-gateway-auth`.
- Never paste live bearer tokens into notes.
